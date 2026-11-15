# BLIND 재분석 SPEC — 2026-11-16 (스케줄 stock_update-2, 7일 런)

- **명령:** `/재분석실행 7 20` → 임계 7일 / 상한 cap10
- **검출 소스:** `analysis/_history/*_timeline.json` max-v date (단일 진실 소스). 7일+ 경과 60종 중 최고령 11-06 코호트(10일) 티커 알파벳순 상위 10.
- **대상 10종:** QQQ · RSP · SCHD · SGOV · SMR · SOXL · SOXS · STX · VST · XOM
  - 동일 11-06 코호트 앞선 10종(GLD·HD·HSBC·IBM·INTC·IONQ·ORCL·PM·QCOM·QLD)은 같은 날 10일 런(staock_update, b42806f1)이 처리 → 본 런은 cap10 잔여분 승계(정상 dual-schedule).
  - standing 제외: ANTHROPIC(비상장), 크립토(QuantTrader 별도).

## 파이프라인 (중앙 집중 BLIND — maxTurns·drift·WebSearch 구조적 회피)

1. **중앙 수집:** 메인이 `scripts/collect_data_20261116_7day.py`(yfinance 단일계열)로 10종 data.json 일괄 수집. ETF 비용률 bps 아티팩트 중앙교정(QQQ/RSP 0.20·SCHD 0.06·SGOV 0.09·SOXL 0.90·SOXS 1.01%), 배당수익률 스케일·52주 아티팩트 가드 적용.
2. **BLIND 분석:** general-purpose 10병렬. 각 에이전트는 자기 종목 data.json + KB만 참조, 이전 v·과거 HTML 미참조. scorecard.md + _report_data.json 2파일만 Write (render/commit 금지).
3. **중앙 렌더:** 메인이 `scripts/render_reports_20261116_7day.py`(normalize 가드)로 10 HTML 생성.
4. **변화추적/cleanup/bootstrap/커밋/배포:** 메인 중앙 처리.

## 매크로 레짐 (공통 배경)

10Y 5.1%(1주전 4.84%→급등 bear flattening)·2Y 4.86%·Fed Funds 3.88% 동결 매파 · AI 디레이팅 지배(11/14~15 저점 반등) · NVDA 11/17 단일 바이너리 · 희토류 유예 2027-01 연장 · F&G CNN 38.6(공포)/크립토 10(극단 공포).

## 결과

성공 10 / 스킵 0 / maxTurns 0 / drift 0. 등급변경 4종(🟢 SMR·STX·VST / 🔻 SOXL). 상세 → `20261116_7day_run.md`.
