# -*- coding: utf-8 -*-
"""
score_ledger.py — 종목분석 점수 원장(append-only) + 점수 예측력 평가

배경: analysis/_history/*_timeline.json 은 종목당 최근 3건만 보존한다. 과거 점수가 계속
      잘려 "점수가 실제로 맞았는가"를 검증할 원자료가 사라지므로, 모든 (ticker, v) 를
      knowledge-db/performance/score_ledger.jsonl 에 영구 누적한다.

서브커맨드:
  backfill  timeline 파일의 git 이력 전체를 (ticker, v) 합집합으로 복원해 원장에 기록.
            읽기 전용 git 명령(log / cat-file)만 사용. 원장에 이미 있는 키는 건드리지 않음.
  append    현재 timeline 을 읽어 원장에 없는 (ticker, v) 만 추가. 멱등.
            이미 있는 키라도 원장의 빈 칸(null)이 timeline 에서 나중에 채워졌으면 보충 행을 덧붙인다.
  evaluate  원장 각 행의 5·20·60 거래일 선행 수익률과 벤치마크 초과수익을 계산해
            knowledge-db/performance/score_predictiveness.json 생성.

원장 규칙: 덧붙이기만 한다. 기존 행은 수정·삭제하지 않는다. 같은 (ticker, v) 의 뒤 행은 보충 행으로,
          읽을 때 앞 행의 빈 칸만 채운다 (이미 기록된 값은 덮지 않음 — merged_ledger).
행 필드: ticker, name, v, date, score, grade, target_price(원문), source, first_seen_commit

사용:
    python3 scripts/score_ledger.py backfill
    python3 scripts/score_ledger.py append
    python3 scripts/score_ledger.py evaluate            # 당일 가격 캐시 재사용
    python3 scripts/score_ledger.py evaluate --refresh  # 가격 캐시 무시하고 재수집

소비처: /성과리뷰 Step 0-L — append → evaluate 후 score_predictiveness.json 인용.
"""

import argparse
import json
import math
import re
import subprocess
import sys
from bisect import bisect_left, bisect_right
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from statistics import mean, median, stdev

ROOT = Path(__file__).resolve().parent.parent
HIST_REL = "analysis/_history"
HIST_DIR = ROOT / HIST_REL
LEDGER = ROOT / "knowledge-db/performance/score_ledger.jsonl"
OUT_JSON = ROOT / "knowledge-db/performance/score_predictiveness.json"
PRICE_CACHE = ROOT / "scripts/launchd/.score_ledger_price_cache.json"  # git 제외 대상

KST = timezone(timedelta(hours=9))
FIELDS = ("ticker", "name", "v", "date", "score", "grade", "target_price", "source", "first_seen_commit")

# ── evaluate 설정 ─────────────────────────────────────
HORIZONS = (5, 20, 60)  # 거래일
MIN_N = 30  # 미만이면 insufficient_sample
# 재분석 자동화 가동일. 그 이전 timeline 날짜는 git checkout 으로 오염된 파일 mtime 유래
# (analysis/_audit/perf_audit.md §1.1) → 평가에서 제외. 원장에는 그대로 남긴다.
DATE_FLOOR = "2026-05-08"
ENTRY_GAP_MAX_DAYS = 5
COHORT_MIN = {"analysis_date": 8, "iso_week": 15}
UNLISTED = {"ANTHROPIC"}  # 비상장 — 가격 없음
SYMBOL_OVERRIDE = {"BRKB": "BRK-B", "BRK.B": "BRK-B"}
BENCH_US, BENCH_KR = "SPY", "^KS11"
GRADES = ("강력매수", "매수", "중립", "매도", "강력매도")
BUCKETS = (
    (None, 50, "<50"),
    (50, 60, "50-60"),
    (60, 65, "60-65"),
    (65, 70, "65-70"),
    (70, 75, "70-75"),
    (75, 80, "75-80"),
    (80, None, "80+"),
)


# ── 원장 I/O ─────────────────────────────────────────
def load_ledger():
    rows = []
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


FILL_FIELDS = ("date", "score", "grade", "target_price")


def _empty(x):
    return x in (None, "")


def merged_ledger():
    """(ticker, v) 당 1행으로 접는다 — 뒤에 덧붙은 보충 행은 앞 행의 빈 칸만 채운다 (기록된 값 불변)."""
    merged = {}
    for r in load_ledger():
        key = (r["ticker"], r["v"])
        m = merged.get(key)
        if m is None:
            merged[key] = dict(r)
            continue
        for k in ("name",) + FILL_FIELDS:
            if _empty(m.get(k)) and not _empty(r.get(k)):
                m[k] = r[k]
    return list(merged.values())


def append_rows(rows):
    """원장 끝에 덧붙이기만 한다 (기존 행 불변)."""
    if not rows:
        return
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps({k: r.get(k) for k in FIELDS}, ensure_ascii=False) + "\n")


def ledger_summary(rows):
    dates = sorted(r["date"][:10] for r in rows if r.get("date"))
    return {
        "rows": len(rows),
        "tickers": len({r["ticker"] for r in rows}),
        "date_min": dates[0] if dates else None,
        "date_max": dates[-1] if dates else None,
    }


# ── backfill ─────────────────────────────────────────
def git(*args, inp=None):
    p = subprocess.run(
        ["git", "-c", "core.quotepath=false", "-C", str(ROOT)] + list(args), input=inp, capture_output=True
    )
    if p.returncode != 0:
        sys.exit("[ledger] git 실패: " + p.stderr.decode("utf-8", "replace")[:300])
    return p.stdout


def cmd_backfill():
    # (commit, path) 쌍 — 경로는 바이트 그대로 유지 (한글·NFD 파일명 안전)
    log = git("log", "--no-renames", "--format=@@%H", "--name-status", "--", HIST_REL)
    pairs, cur = [], None
    for line in log.split(b"\n"):
        if line.startswith(b"@@"):
            cur = line[2:]
        elif line.strip():
            st, _, path = line.partition(b"\t")
            if not st.startswith(b"D") and path.endswith(b"_timeline.json"):
                pairs.append((cur, path))
    pairs.reverse()  # 과거 → 최신
    buf = git("cat-file", "--batch", inp=b"".join(h + b":" + p + b"\n" for h, p in pairs))

    obs, pos, bad = {}, 0, 0
    for h, _ in pairs:
        nl = buf.index(b"\n", pos)
        header = buf[pos:nl]
        pos = nl + 1
        if header.endswith(b"missing"):
            bad += 1
            continue
        size = int(header.split()[-1])
        blob = buf[pos : pos + size]
        pos += size + 1
        try:
            j = json.loads(blob.decode("utf-8"))
        except Exception:
            bad += 1
            continue
        tk = j.get("ticker")
        if not tk:
            continue
        for e in j.get("history") or []:
            key = (tk, e.get("v"))
            o = obs.get(key)
            if o is None:
                o = obs[key] = dict.fromkeys(FIELDS)
                o.update(ticker=tk, v=e.get("v"), source="timeline_git", first_seen_commit=h.decode("ascii"))
            # 병합 규칙 (감사와 동일): 날짜 = 관측 최댓값 (UTC 롤백 버그로 하루 이른 값이 섞임,
            # 늦은 쪽이 최초 기록값과 일치) / 나머지 = 가장 최근 커밋의 non-null 값
            if j.get("name"):
                o["name"] = j["name"]
            d = e.get("date")
            if d and (o["date"] is None or d > o["date"]):
                o["date"] = d
            for k in ("score", "grade", "target_price"):
                if e.get(k) not in (None, ""):
                    o[k] = e[k]

    have = {(r["ticker"], r["v"]) for r in load_ledger()}
    new = [o for key, o in obs.items() if key not in have]
    new.sort(key=lambda o: (o["date"] or "", o["ticker"], -1 if o["v"] is None else o["v"]))
    append_rows(new)
    s = ledger_summary(load_ledger())
    print(
        f"[ledger] backfill: 커밋-파일 {len(pairs)}쌍 (파싱 실패 {bad}) → 고유 (ticker, v) {len(obs)}건, "
        f"신규 기록 {len(new)}건"
    )
    print(f"[ledger] 원장: {s['rows']}행 / {s['tickers']}종목 / 분석일 {s['date_min']} ~ {s['date_max']}")


# ── append ───────────────────────────────────────────
def cmd_append():
    led = {(r["ticker"], r["v"]): r for r in merged_ledger()}
    new, filled = [], 0
    for f in sorted(HIST_DIR.glob("*_timeline.json")):
        if f.name.startswith("._"):  # 외장 SSD AppleDouble
            continue
        try:
            j = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[ledger] WARN: {f.name} 읽기 실패 — {e}")
            continue
        tk = j.get("ticker")
        if not tk:
            continue
        for e in j.get("history") or []:
            key = (tk, e.get("v"))
            cur = led.get(key)
            if cur is not None:
                # 보충 행: 최초 기록 때 파서 오류 등으로 비어 있던 칸이 timeline 에서 나중에 채워진 경우만
                if not any(_empty(cur.get(k)) and not _empty(e.get(k)) for k in FILL_FIELDS):
                    continue
                filled += 1
            row = {
                "ticker": tk,
                "name": j.get("name"),
                "v": e.get("v"),
                "date": e.get("date"),
                "score": e.get("score"),
                "grade": e.get("grade"),
                "target_price": e.get("target_price"),
                "source": "timeline_live" if cur is None else "timeline_live_fill",
                "first_seen_commit": None,
            }
            new.append(row)
            led[key] = row if cur is None else {k: (row[k] if _empty(cur.get(k)) else cur[k]) for k in FIELDS}
    append_rows(new)
    s = ledger_summary(load_ledger())
    print(f"[ledger] append: 신규 {len(new) - filled}건 추가, 빈 칸 보충 {filled}건")
    print(f"[ledger] 원장: {s['rows']}행 / {s['tickers']}종목 / 분석일 {s['date_min']} ~ {s['date_max']}")


# ── evaluate: 가격 ───────────────────────────────────
def is_kr(ticker):
    return bool(re.fullmatch(r"\d{6}", ticker))


def _closes(df, sym):
    """배치 결과에서 한 심볼의 종가 {날짜: 값}. NaN 행 제거 (.KS 마지막 행 NaN 함정)."""
    try:
        s = df[sym]["Close"]
    except Exception:
        try:
            s = df["Close"]
            if hasattr(s, "columns"):
                s = s[sym] if sym in s.columns else s.iloc[:, 0]
        except Exception:
            return {}
    s = s.dropna()
    return {d.strftime("%Y-%m-%d"): round(float(v), 4) for d, v in s.items()}


def download(symbols, start, retry=True):
    """배치 다운로드 (40개 단위). 빈 응답 심볼은 1회 재시도."""
    import yfinance as yf

    out = {}
    for i in range(0, len(symbols), 40):
        chunk = symbols[i : i + 40]
        df = yf.download(chunk, start=start, auto_adjust=True, progress=False, group_by="ticker", threads=True)
        for s in chunk:
            out[s] = _closes(df, s)
    miss = [s for s in symbols if not out.get(s)]
    if miss and retry:
        out.update({s: c for s, c in download(miss, start, retry=False).items() if c})
    return out


def load_prices(tickers, start, refresh):
    """수정종가 수집. 당일(KST) 캐시가 필요한 티커·기간을 모두 덮으면 재사용."""
    today = datetime.now(KST).strftime("%Y-%m-%d")
    if not refresh and PRICE_CACHE.exists():
        try:
            c = json.loads(PRICE_CACHE.read_text(encoding="utf-8"))
            known = set(c.get("symbol_of", {})) | set(c.get("skipped", {}))
            if c.get("fetched_on") == today and c.get("start", "9") <= start and set(tickers) <= known:
                print(f"[ledger] 가격 캐시 재사용 ({PRICE_CACHE.relative_to(ROOT)})")
                return c
        except Exception:
            pass

    symbol_of, skipped = {}, {}
    for t in tickers:
        if t in UNLISTED:
            skipped[t] = "비상장"
        elif is_kr(t):
            symbol_of[t] = t + ".KS"
        else:
            symbol_of[t] = SYMBOL_OVERRIDE.get(t, t)
    closes = download(sorted(set(symbol_of.values()) | {BENCH_US, BENCH_KR}), start)
    for b in (BENCH_US, BENCH_KR):
        if not closes.get(b):
            sys.exit(f"[ledger] 벤치마크 {b} 가격 조회 실패 — 평가 중단")
    # 한국 6자리: .KS 빈 응답이면 .KQ 재시도 (KOSDAQ, 예: 466100)
    kq_retry = [t for t in symbol_of if is_kr(t) and not closes.get(symbol_of[t])]
    if kq_retry:
        kq = download([t + ".KQ" for t in kq_retry], start)
        for t in kq_retry:
            if kq.get(t + ".KQ"):
                closes.pop(symbol_of[t], None)
                symbol_of[t] = t + ".KQ"
                closes[symbol_of[t]] = kq[symbol_of[t]]
    for t in list(symbol_of):
        if not closes.get(symbol_of[t]):
            skipped[t] = f"가격 조회 실패 ({symbol_of[t]})"
            closes.pop(symbol_of[t], None)
            del symbol_of[t]

    cache = {"fetched_on": today, "start": start, "symbol_of": symbol_of, "skipped": skipped, "closes": closes}
    PRICE_CACHE.parent.mkdir(parents=True, exist_ok=True)
    PRICE_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    return cache


def forward(series, bench, d, h):
    """(status, 수익률, 벤치마크 수익률). 진입 = 분석일 이후 첫 거래일 종가(분석일 포함),
    청산 = 그 종목 자체 거래일 기준 h 번째 뒤 종가. 벤치마크는 같은 달력 구간(asof)."""
    dates, vals = series
    i = bisect_left(dates, d)
    if i >= len(dates):
        return ("no_entry_bar", None, None)
    if (date.fromisoformat(dates[i]) - date.fromisoformat(d)).days > ENTRY_GAP_MAX_DAYS:
        return ("entry_gap", None, None)
    if i + h >= len(dates):
        return ("not_matured", None, None)
    bd, bv = bench
    j0 = bisect_right(bd, dates[i]) - 1
    j1 = bisect_right(bd, dates[i + h]) - 1
    if j0 < 0 or j1 < 0:
        return ("no_bench", None, None)
    return ("ok", vals[i + h] / vals[i] - 1, bv[j1] / bv[j0] - 1)


# ── evaluate: 통계 (표준 라이브러리) ──────────────────
def norm_grade(s):
    if not s:
        return None
    t = re.sub(r"[\*\s`]", "", str(s))
    tl = t.lower()
    if "강력매도" in t or "strongsell" in tl:
        return "강력매도"
    if "강력매수" in t or "strongbuy" in tl or "강력추천" in t:
        return "강력매수"
    if "매도" in t or tl == "sell" or "비중축소" in t:
        return "매도"
    if "매수" in t or tl == "buy" or t.startswith("추천"):
        return "매수"
    if "중립" in t or "보유" in t or tl == "hold":
        return "중립"
    return None


def ranks(a):
    order = sorted(range(len(a)), key=lambda i: a[i])
    r = [0.0] * len(a)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and a[order[j + 1]] == a[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2 + 1  # 동점 평균 순위
        i = j + 1
    return r


def spearman(x, y):
    if len(x) < 3:
        return None
    rx, ry = ranks(x), ranks(y)
    mx, my = mean(rx), mean(ry)
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    if sxx == 0 or syy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / math.sqrt(sxx * syy)


def pct(x):
    return round(100 * x, 2)


def cell(rows):
    """한 칸(등급·점수 구간)의 평균/중앙값/n."""
    n = len(rows)
    if n == 0:
        return {"n": 0, "insufficient_sample": True}
    ex = [r["ex"] for r in rows]
    raw = [r["raw"] for r in rows]
    return {
        "n": n,
        "tickers": len({r["ticker"] for r in rows}),
        "mean_excess_pct": pct(mean(ex)),
        "median_excess_pct": pct(median(ex)),
        "mean_return_pct": pct(mean(raw)),
        "median_return_pct": pct(median(raw)),
        "beat_benchmark_pct": round(100 * sum(1 for e in ex if e > 0) / n, 1),
        "insufficient_sample": n < MIN_N,
    }


def rho(x, y, n_key="n"):
    r = spearman(x, y)
    return {"spearman": None if r is None else round(r, 4), n_key: len(x), "insufficient_sample": len(x) < MIN_N}


def cohort_ic(rows, keyfn, min_n):
    """코호트(같은 분석일/같은 주)별 Spearman(점수, 초과수익) 의 평균."""
    groups = defaultdict(list)
    for r in rows:
        groups[keyfn(r)].append(r)
    ics = []
    for g in groups.values():
        if len(g) >= min_n:
            ic = spearman([r["score"] for r in g], [r["ex"] for r in g])
            if ic is not None:
                ics.append(ic)
    n = len(ics)
    out = {"min_cohort_size": min_n, "n_cohorts": n, "insufficient_sample": n < MIN_N}
    if n:
        out["mean_ic"] = round(mean(ics), 4)
        out["positive_pct"] = round(100 * sum(1 for v in ics if v > 0) / n, 1)
    if n >= 2 and stdev(ics) > 0:
        out["t_stat"] = round(mean(ics) / (stdev(ics) / math.sqrt(n)), 2)
    return out


def iso_week(r):
    y, w, _ = date.fromisoformat(r["date"]).isocalendar()
    return f"{y}-W{w:02d}"


def horizon_block(recs, h):
    status = Counter(r["fwd"][h][0] for r in recs)
    ok = [
        {"ticker": r["ticker"], "date": r["date"], "score": r["score"], "grade": r["grade"],
         "raw": r["fwd"][h][1], "ex": r["fwd"][h][1] - r["fwd"][h][2]}
        for r in recs
        if r["fwd"][h][0] == "ok"
    ]  # fmt: skip
    scored = [r for r in ok if r["score"] is not None]
    by_grade = {g: cell([r for r in ok if r["grade"] == g]) for g in GRADES}
    by_grade["등급없음"] = cell([r for r in ok if r["grade"] is None])
    by_bucket = {
        label: cell([r for r in scored if (lo is None or r["score"] >= lo) and (hi is None or r["score"] < hi)])
        for lo, hi, label in BUCKETS
    }
    # 종목 간(평균 점수 vs 평균 초과수익) / 종목 내(종목 평균 차감)
    by_t = defaultdict(list)
    for r in scored:
        by_t[r["ticker"]].append(r)
    t_mean = {t: (mean(r["score"] for r in g), mean(r["ex"] for r in g)) for t, g in by_t.items()}
    within = [(r["score"] - t_mean[t][0], r["ex"] - t_mean[t][1]) for t, g in by_t.items() if len(g) >= 2 for r in g]
    dates = sorted(r["date"] for r in ok)
    return {
        "status_counts": dict(status),
        "matured_analysis_dates": [dates[0], dates[-1]] if dates else None,
        "overall": cell(ok),
        "by_grade": by_grade,
        "buy_family": cell([r for r in ok if r["grade"] in ("강력매수", "매수")]),
        "non_buy": cell([r for r in ok if r["grade"] in ("중립", "매도", "강력매도")]),
        "by_score_bucket": by_bucket,
        "ic": {
            "pooled": rho([r["score"] for r in scored], [r["ex"] for r in scored]),
            "cohort_by_analysis_date": cohort_ic(scored, lambda r: r["date"], COHORT_MIN["analysis_date"]),
            "cohort_by_iso_week": cohort_ic(scored, iso_week, COHORT_MIN["iso_week"]),
            "between_ticker": rho([v[0] for v in t_mean.values()], [v[1] for v in t_mean.values()], "n_tickers"),
            "within_ticker": rho([w[0] for w in within], [w[1] for w in within]),
        },
    }


def cmd_evaluate(refresh):
    ledger = merged_ledger()
    if not ledger:
        sys.exit("[ledger] 원장이 비어 있음 — backfill / append 먼저 실행")
    excl, recs = Counter(), []
    for r in ledger:
        d = (r.get("date") or "")[:10]
        s = r.get("score")
        score = s if isinstance(s, (int, float)) and not isinstance(s, bool) else None
        grade = norm_grade(r.get("grade"))
        if r["ticker"] in UNLISTED:
            excl["비상장"] += 1
        elif r.get("v") is None:
            excl["v 없음 (버전 없는 원본 폴더)"] += 1
        elif not d:
            excl["날짜 없음"] += 1
        elif d < DATE_FLOOR:
            excl[f"분석일 < {DATE_FLOOR} (mtime 오염 구간)"] += 1
        elif score is None and grade is None:
            excl["점수·등급 모두 없음"] += 1
        else:
            recs.append({"ticker": r["ticker"], "date": d, "score": score, "grade": grade})
    if not recs:
        sys.exit("[ledger] 평가 가능한 행 없음")

    start = (date.fromisoformat(min(r["date"] for r in recs)) - timedelta(days=10)).isoformat()
    cache = load_prices(sorted({r["ticker"] for r in ledger}), start, refresh)
    series = {s: (sorted(c), [c[k] for k in sorted(c)]) for s, c in cache["closes"].items()}

    kept = []
    for r in recs:
        sym = cache["symbol_of"].get(r["ticker"])
        if sym is None:
            excl["가격 조회 실패 종목"] += 1
            continue
        bench = series[BENCH_KR if is_kr(r["ticker"]) else BENCH_US]
        r["fwd"] = {h: forward(series[sym], bench, r["date"], h) for h in HORIZONS}
        kept.append(r)
    if not kept:
        sys.exit("[ledger] 가격이 있는 평가 대상 없음")

    d0, d1 = min(r["date"] for r in kept), max(r["date"] for r in kept)
    last_bar = series[BENCH_US][0][-1]

    def bench_ret(sym):
        ds, vs = series[sym]
        i = min(bisect_left(ds, d0), len(ds) - 1)
        return pct(vs[-1] / vs[i] - 1)

    horizons = {str(h): horizon_block(kept, h) for h in HORIZONS}
    months = (date.fromisoformat(last_bar) - date.fromisoformat(d0)).days / 30.4
    null_score = sum(1 for r in kept if r["score"] is None)
    null_grade = sum(1 for r in kept if r["grade"] is None)
    s = ledger_summary(ledger)
    payload = {
        "generated_at": datetime.now(KST).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "doc": "종목분석 점수(0~100)·등급의 선행 수익률 예측력 — scripts/score_ledger.py evaluate 결정적 산출. "
        "해석은 /성과리뷰 책임. insufficient_sample=true 칸은 판단 근거로 쓰지 말 것.",
        "ledger": {
            "path": str(LEDGER.relative_to(ROOT)),
            "rows": s["rows"],
            "tickers": s["tickers"],
            "analysis_date_range": [s["date_min"], s["date_max"]],
        },
        "evaluated": {
            "rows": len(kept),
            "tickers": len({r["ticker"] for r in kept}),
            "analysis_date_range": [d0, d1],
            "excluded_rows": dict(excl),
            "price_last_bar": last_bar,
        },
        "limitations": [
            f"단일 국면 표본 — 분석일 {d0} 이후 약 {months:.1f}개월, 같은 기간 SPY {bench_ret(BENCH_US):+.2f}% / "
            f"KOSPI {bench_ret(BENCH_KR):+.2f}%. 다른 시장 국면에서는 부호가 달라질 수 있다.",
            "수익률 구간이 서로 겹친다 (종목당 재분석 간격이 보유 기간보다 짧음). 독립 표본 수는 n 보다 작고 "
            "코호트 IC 의 t 값은 과대평가돼 있다.",
            "벤치마크는 SPY / KOSPI 단일이다. 채권·금·레버리지·인버스 ETF 에는 부적합한 비교다.",
            f"평가 대상 중 timeline 점수가 null 인 {null_score}행은 점수 구간·IC 에서, 등급이 null 이거나 비표준인 "
            f"{null_grade}행은 등급 표에서 빠진다. 점수·등급이 모두 null 인 행은 excluded_rows 참조 "
            "(대부분 4~6월 분석분, run.md 변화표 보완 미적용).",
            f"n < {MIN_N} 인 칸과 코호트 수 < {MIN_N} 인 IC 는 insufficient_sample=true.",
            "원장 값은 최초 기록 이후 수정하지 않으므로 timeline 파서 오류(목표가·등급 오추출)가 그대로 남을 수 있다.",
        ],
        "method": {
            "entry": "분석일(KST) 이후 첫 거래일 수정종가 (분석일 포함, "
            f"{ENTRY_GAP_MAX_DAYS}일 넘게 떨어지면 제외)",
            "forward_return": "해당 종목 자체 거래일 기준 close[i+h]/close[i]-1, h = 5·20·60",
            "excess": f"수익률 - 벤치마크 동일 달력 구간 수익률 (한국 6자리 = {BENCH_KR}, 그 외 = {BENCH_US})",
            "ic": "Spearman 순위상관(점수, 초과수익). cohort_by_analysis_date = 같은 분석일 코호트 "
            f"(≥{COHORT_MIN['analysis_date']}건), cohort_by_iso_week = 같은 ISO 주 코호트 (≥{COHORT_MIN['iso_week']}건), "
            "between_ticker = 종목 평균끼리, within_ticker = 종목 평균 차감 후",
            "price_source": "yfinance auto_adjust=True",
        },
        "skipped_tickers": cache["skipped"],
        "horizons": horizons,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"[ledger] 원장 {s['rows']}행 / {s['tickers']}종목 / 분석일 {s['date_min']} ~ {s['date_max']}")
    print(f"[ledger] 평가 대상 {len(kept)}행 / 제외 {dict(excl)}")
    print(f"[ledger] 건너뛴 종목: {cache['skipped'] or '없음'}")
    for h in HORIZONS:
        b = horizons[str(h)]
        ic = b["ic"]
        print(f"[ledger] {h}거래일 — 성숙 {b['overall']['n']}건, 상태 {b['status_counts']}")
        for g in GRADES + ("등급없음",):
            c = b["by_grade"][g]
            if c["n"]:
                flag = " (표본 부족)" if c["insufficient_sample"] else ""
                print(f"    {g}: n={c['n']} 평균초과 {c['mean_excess_pct']:+.2f}% 중앙 {c['median_excess_pct']:+.2f}%{flag}")
        c = b["buy_family"]
        if c["n"]:
            print(f"    매수 계열(강력매수+매수): n={c['n']} 평균초과 {c['mean_excess_pct']:+.2f}%")
        print(
            f"    IC 풀링 {ic['pooled']['spearman']} (n={ic['pooled']['n']}) / "
            f"분석일 코호트 {ic['cohort_by_analysis_date'].get('mean_ic')} ({ic['cohort_by_analysis_date']['n_cohorts']}개) / "
            f"주간 코호트 {ic['cohort_by_iso_week'].get('mean_ic')} ({ic['cohort_by_iso_week']['n_cohorts']}개) / "
            f"종목 간 {ic['between_ticker']['spearman']} / 종목 내 {ic['within_ticker']['spearman']}"
        )
    print(f"[ledger] 저장: {OUT_JSON.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser(description="점수 원장 + 예측력 평가")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("backfill", help="timeline git 이력 → 원장")
    sub.add_parser("append", help="현재 timeline 의 신규 (ticker, v) → 원장")
    ev = sub.add_parser("evaluate", help="선행 수익률·IC → score_predictiveness.json")
    ev.add_argument("--refresh", action="store_true", help="가격 캐시 무시")
    args = ap.parse_args()
    if args.cmd == "backfill":
        cmd_backfill()
    elif args.cmd == "append":
        cmd_append()
    else:
        cmd_evaluate(args.refresh)


if __name__ == "__main__":
    main()
