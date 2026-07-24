#!/usr/bin/env bash
# notify.sh — 공용 알림 헬퍼 (자동화 실패·손절/목표가·드리프트·브리핑 발행 공통)
#
# 사용:
#   bash scripts/notify.sh "제목" "본문" [priority]
#     priority: default | high  (생략 시 default — 채널이 macOS 단일이라 현재는 표기용,
#     호출부 시그니처 호환을 위해 유지)
#
# 채널: macOS 알림센터 (osascript) 단일.
#   (ntfy.sh 폰 푸시는 2026-07-24 사용자 지시로 완전 제거 — 6/11 도입 후 미사용)
#
# 원칙: 알림 실패가 호출자(watchdog/deploy 스크립트)를 죽이지 않는다 — 항상 exit 0.

TITLE="${1:-종목분석 에이전트}"
BODY="${2:-}"
PRIORITY="${3:-default}"

osascript -e "display notification \"${BODY//\"/\\\"}\" with title \"${TITLE//\"/\\\"}\"" >/dev/null 2>&1 || true

exit 0
