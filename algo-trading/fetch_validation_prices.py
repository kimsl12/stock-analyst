#!/usr/bin/env python3
"""
fetch_validation_prices.py — 스코어 검증용 현재가 수집 + 수익률 산출
score_validation.json 을 읽어서 진입가 있는 종목의 현재가를 yfinance로 가져오고
return_pct, direction_correct 를 산출하여 덮어씀.

실행: python3 algo-trading/fetch_validation_prices.py
"""

import json, os, sys
from datetime import datetime, timezone, timedelta

KST = timezone(timedelta(hours=9))

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    val_path = os.path.join(root, 'algo-trading', 'data', 'score_validation.json')

    if not os.path.exists(val_path):
        print('ERROR: score_validation.json 미존재. build_score_validation.mjs 먼저 실행.')
        sys.exit(1)

    with open(val_path) as f:
        data = json.load(f)

    # 진입가 있는 종목만 수집 대상
    targets = [s for s in data['stocks'] if s.get('entry_price') and s.get('score')]
    if not targets:
        print('진입가 있는 종목 0건 — 수집 불필요')
        return

    # yfinance import
    try:
        import yfinance as yf
    except ImportError:
        print('ERROR: yfinance 미설치. pip install yfinance')
        sys.exit(1)

    # 티커 변환 (KRX: 6자리 숫자 → .KS)
    ticker_map = {}
    for s in targets:
        t = s['ticker']
        if s['market'] == 'KRX':
            yf_ticker = f"{t}.KS"
        else:
            yf_ticker = t
        ticker_map[t] = yf_ticker

    yf_tickers = list(set(ticker_map.values()))
    print(f'yfinance 수집: {len(yf_tickers)}개 종목')

    # 가격 수집 (5d로 최신 종가)
    try:
        df = yf.download(yf_tickers, period='5d', progress=False)
        closes = df['Close']
    except Exception as e:
        print(f'ERROR: yfinance 수집 실패: {e}')
        sys.exit(1)

    # 수익률 산출
    updated = 0
    for s in data['stocks']:
        if not s.get('entry_price') or not s.get('score'):
            continue

        yf_t = ticker_map.get(s['ticker'])
        if not yf_t or yf_t not in closes.columns:
            continue

        # 최신 종가
        col = closes[yf_t].dropna()
        if col.empty:
            continue

        current = float(col.iloc[-1])
        entry = s['entry_price']

        if entry > 0:
            ret = round((current - entry) / entry * 100, 2)
            grade = s.get('grade')

            # 방향 정합성: A/B는 양수면 correct, D/F는 음수면 correct
            if grade in ('A', 'B'):
                direction = ret > 0
            elif grade in ('D', 'F'):
                direction = ret < 0
            else:
                direction = None  # C등급은 중립이라 판정 불가

            s['current_price'] = round(current, 2)
            s['return_pct'] = ret
            s['direction_correct'] = direction
            s['price_date'] = str(col.index[-1].date())
            updated += 1

    # 등급별 통계 재계산
    grade_stats = {}
    for g in ['A', 'B', 'C', 'D', 'F']:
        items = [s for s in data['stocks'] if s.get('grade') == g and s.get('return_pct') is not None]
        returns = [s['return_pct'] for s in items]
        correct = sum(1 for s in items if s.get('direction_correct') is True)
        wrong = sum(1 for s in items if s.get('direction_correct') is False)
        total = correct + wrong

        grade_stats[g] = {
            'count': sum(1 for s in data['stocks'] if s.get('grade') == g),
            'with_returns': len(returns),
            'avg_return_pct': round(sum(returns) / len(returns), 2) if returns else None,
            'median_return_pct': round(sorted(returns)[len(returns)//2], 2) if returns else None,
            'min_return_pct': round(min(returns), 2) if returns else None,
            'max_return_pct': round(max(returns), 2) if returns else None,
            'hit_rate': round(correct / total * 100, 1) if total > 0 else None,
            'correct': correct,
            'wrong': wrong,
        }

    data['grade_distribution'] = grade_stats
    data['with_returns'] = sum(1 for s in data['stocks'] if s.get('return_pct') is not None)
    data['generated_at'] = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S KST')
    data['note'] = f'yfinance 연동 완료. {updated}건 현재가 + 수익률 산출.'

    # 검증 결과 판정
    gd = grade_stats
    checks = []
    # 1. 단조 감소
    avgs = [(g, gd[g]['avg_return_pct']) for g in ['A','B','C','D','F'] if gd[g]['avg_return_pct'] is not None]
    if len(avgs) >= 2:
        monotonic = all(avgs[i][1] >= avgs[i+1][1] for i in range(len(avgs)-1))
        checks.append({'test': 'monotonic_decrease', 'pass': monotonic, 'detail': {g: r for g, r in avgs}})

    # 2. A등급 적중률 >= 70%
    a_hit = gd['A']['hit_rate']
    if a_hit is not None:
        checks.append({'test': 'A_hit_rate_70', 'pass': a_hit >= 70, 'value': a_hit})

    # 3. A+B 적중률 >= 60%
    ab_correct = gd['A']['correct'] + gd['B']['correct']
    ab_wrong = gd['A']['wrong'] + gd['B']['wrong']
    ab_total = ab_correct + ab_wrong
    ab_hit = round(ab_correct / ab_total * 100, 1) if ab_total > 0 else None
    if ab_hit is not None:
        checks.append({'test': 'AB_hit_rate_60', 'pass': ab_hit >= 60, 'value': ab_hit})

    # 4. D+F 적중률 >= 50%
    df_correct = gd['D']['correct'] + gd['F']['correct']
    df_wrong = gd['D']['wrong'] + gd['F']['wrong']
    df_total = df_correct + df_wrong
    df_hit = round(df_correct / df_total * 100, 1) if df_total > 0 else None
    if df_hit is not None:
        checks.append({'test': 'DF_hit_rate_50', 'pass': df_hit >= 50, 'value': df_hit})

    all_pass = all(c['pass'] for c in checks) if checks else None
    data['validation_result'] = {
        'overall': 'PASS' if all_pass else ('FAIL' if all_pass is False else 'INSUFFICIENT_DATA'),
        'checks': checks,
        'ab_combined_hit_rate': ab_hit,
        'df_combined_hit_rate': df_hit,
    }

    with open(val_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f'OK: {updated}건 현재가 업데이트')
    print(f'등급별 평균 수익률:')
    for g in ['A','B','C','D','F']:
        s = grade_stats[g]
        avg = f"{s['avg_return_pct']:+.2f}%" if s['avg_return_pct'] is not None else 'N/A'
        hit = f"{s['hit_rate']}%" if s['hit_rate'] is not None else 'N/A'
        print(f"  {g}: avg={avg}, hit={hit}, n={s['with_returns']}")

    print(f"\n검증 결과: {data['validation_result']['overall']}")
    for c in checks:
        status = 'PASS' if c['pass'] else 'FAIL'
        print(f"  [{status}] {c['test']}: {c.get('value', c.get('detail', ''))}")

if __name__ == '__main__':
    main()
