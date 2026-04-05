# 종목분석 AI 에이전트 v2.1

## 프로젝트 경로
```
C:\Users\kimsl\Documents\Claude\Projects\종목분석 에이전트
```

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v2.1 | 2026-04-05 | 프롬프트 개선 + ATR 손절 + 가중 스코어카드 + 슬래시 명령어 |
| v2.0 | 2026-04-05 | 9개 에이전트 (Opus) + DART API |
| v1.0 | 2026-04-05 | 초기 6개 에이전트 |

---

## 설치

1. 전체 파일을 프로젝트 폴더에 복사
2. `install.bat` 더블클릭
3. Claude Code 실행: `claude` → `/help`로 명령어 확인

---

## 설치 후 구조

```
.claude/
├── settings.json                ← DART API 키
├── agents/                      ← 9개 분석 에이전트 + SSOT
│   ├── stock-analyst-lead.md
│   ├── data-collector.md
│   ├── company-overview.md
│   ├── financial-analyst.md
│   ├── business-analyst.md
│   ├── momentum-analyst.md
│   ├── risk-analyst.md
│   ├── scorecard-strategist.md
│   ├── report-generator.md
│   └── stop-loss-rules.md
└── commands/                    ← 5개 슬래시 명령어
    ├── 종목분석.md   → /종목분석
    ├── 비교분석.md   → /비교분석
    ├── 빠른분석.md   → /빠른분석
    ├── 손절계산.md   → /손절계산
    └── 리포트.md     → /리포트
```

---

## 사용법

### 슬래시 명령어 (추천)

| 명령어 | 사용 예시 | 설명 |
|--------|----------|------|
| `/종목분석` | `/종목분석 삼성전자` | 전체 분석 리포트 (9개 에이전트 동원) |
| `/비교분석` | `/비교분석 삼성전자 SK하이닉스` | 두 종목 비교 |
| `/빠른분석` | `/빠른분석 네이버` | 핵심 지표 요약 (5분 이내) |
| `/손절계산` | `/손절계산 삼성전자 180000` | ATR 손절가/목표가 계산 |
| `/리포트` | `/리포트 삼성전자` | 분석 결과 → HTML 리포트 생성 |

### 자연어 (자동 위임)

```
삼성전자 분석해줘
SK하이닉스 투자 의견 알려줘
네이버 vs 카카오 비교해줘
현대차 목표주가 산정해줘
```

에이전트를 확실하게 지정하려면:
```
@stock-analyst-lead 삼성전자 분석해줘
```

### agent 고정 모드 (선택)

이 폴더를 종목분석 전용으로 쓰고 싶으면 settings.json에 추가:
```json
{
  "agent": "stock-analyst-lead",
  "env": {
    "DART_API_KEY": "..."
  }
}
```
단, 이 경우 다른 작업은 다른 폴더에서 해야 함.

---

## 오케스트레이션 구조

```
/종목분석 삼성전자
    ↓
Phase 0: data-collector (DART + 웹검색 + ATR)
    ↓
Phase 1: company-overview + financial-analyst + momentum-analyst (병렬)
    ↓
Phase 2: business-analyst + risk-analyst (순차)
    ↓
Phase 3: scorecard-strategist (가중 스코어카드 + ATR 전략)
    ↓
Phase 4: report-generator (HTML/PDF)
```

---

## 핵심 기능

### ATR 손절/목표가 시스템
- 고정비율(8%) + ATR(14일x2) 중 타이트한 쪽 채택
- +10% 수익 시 트레일링 전환, 래칫 구조 (하향 금지)
- SSOT: stop-loss-rules.md

### 업종별 가중 스코어카드
- 자동 판별: 성장주/가치주/배당주/턴어라운드/복합형
- 유형별 10개 항목 가중치 차등 적용

### 품질 강제 규칙
- 자체 밸류에이션 산출 필수 (증권사 나열만으로 불가)
- Moat 정량 지표 2개+ 필수
- 리스크 확률 근거 기준표 적용
- 리드 교차검증 (수치·논리·시간축)
