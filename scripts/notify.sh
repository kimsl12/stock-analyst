#!/usr/bin/env bash
# notify.sh — 공용 알림 헬퍼 (자동화 실패·손절/목표가·드리프트·브리핑 발행 공통)
#
# 사용:
#   bash scripts/notify.sh "제목" "본문" [priority]
#     priority: default | high  (생략 시 default)
#
# 채널:
#   1. macOS 알림센터 (osascript) — 항상 시도
#   2. ntfy.sh 폰 푸시 — .env.local 에 NTFY_TOPIC 설정 시에만
#      (폰에 ntfy 앱 설치 → 같은 토픽 구독. 토픽명은 추측 불가능한 문자열 권장)
#
# 원칙: 알림 실패가 호출자(watchdog/deploy 스크립트)를 죽이지 않는다 — 항상 exit 0.

TITLE="${1:-종목분석 에이전트}"
BODY="${2:-}"
PRIORITY="${3:-default}"

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# .env.local 자체 로드 (NTFY_TOPIC) — Read 도구 금지 정책에 따라 스크립트가 직접 source
if [ -f "$PROJECT_ROOT/.env.local" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$PROJECT_ROOT/.env.local" 2>/dev/null || true
  set +a
fi

# 1. macOS 알림센터
osascript -e "display notification \"${BODY//\"/\\\"}\" with title \"${TITLE//\"/\\\"}\"" >/dev/null 2>&1 || true

# 2. ntfy.sh (설정 시)
if [ -n "${NTFY_TOPIC:-}" ]; then
  NTFY_PRIO="3"
  [ "$PRIORITY" = "high" ] && NTFY_PRIO="5"
  curl -fsS -m 10 \
    -H "Title: $TITLE" \
    -H "Priority: $NTFY_PRIO" \
    -H "Tags: chart_with_upwards_trend" \
    -d "$BODY" \
    "https://ntfy.sh/$NTFY_TOPIC" >/dev/null 2>&1 || true
fi

exit 0
