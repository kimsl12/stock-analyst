# 종목분석 AI 에이전트 v2.1

## 프로젝트 경로
```
C:\Users\kimsl\Documents\Claude\Projects\종목분석 에이전트
```

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v2.1 | 2026-04-05 | 프롬프트 전면 개선 + ATR 손절/목표가 시스템 + 업종별 가중 스코어카드 |
| v2.0 | 2026-04-05 | 9개 에이전트 체계 (Opus 통일) + DART API 연동 |
| v1.0 | 2026-04-05 | 초기 6개 에이전트 |

---

## 설치 방법

1. 다운로드한 파일 전체를 프로젝트 폴더에 복사
2. `install.bat` 더블클릭
3. Claude Code에서 확인:
```bash
cd "C:\Users\kimsl\Documents\Claude\Projects\종목분석 에이전트"
claude
/agents
```

---

## 설치 후 폴더 구조

```
종목분석 에이전트\
├── .claude\
│   ├── settings.json                ← DART API 키
│   └── agents\
│       ├── stock-analyst-lead.md    ← 오케스트레이터 (검증 로직 포함)
│       ├── data-collector.md        ← 데이터 수집 + 교차검증 + ATR
│       ├── company-overview.md      ← 기업개요 + Moat 정량분석
│       ├── financial-analyst.md     ← 재무 + 자체 밸류에이션 필수
│       ├── business-analyst.md      ← 산업 트렌드 + 경쟁구도
│       ├── momentum-analyst.md      ← 모멘텀 + 컨센서스 심화
│       ├── risk-analyst.md          ← 리스크 (확률 근거 필수)
│       ├── scorecard-strategist.md  ← 가중 스코어카드 + ATR 전략
│       ├── report-generator.md      ← HTML/PDF 리포트
│       └── stop-loss-rules.md       ← 손절/목표가 계산 SSOT
├── install.bat                      ← 설치 (더블클릭)
├── install.ps1                      ← 설치 로직
└── README.md                        ← 이 파일
```

---

## 오케스트레이션 구조

```
Phase 0 (데이터) → Phase 1 (병렬 3개) → Phase 2 (순차 2개) → Phase 3 (평가) → Phase 4 (리포트)
```

| Phase | 에이전트 | 역할 | 모델 |
|-------|---------|------|------|
| 0 | data-collector | DART API + 웹검색 + ATR(14) 수집 + 교차검증 | Opus |
| 1 (병렬) | company-overview | 기업개요 + Moat 5대 요인 (정량 지표 필수) | Opus |
| 1 (병렬) | financial-analyst | 실적추이 + 수익성 + 자체 밸류에이션 + 민감도 분석 | Opus |
| 1 (병렬) | momentum-analyst | 모멘텀 + 컨센서스 5개+ + EPS 리비전 + Bull/Bear 논쟁 | Opus |
| 2 (순차) | business-analyst | 산업 트렌드 + 메가트렌드 + 경쟁구도 | Opus |
| 2 (순차) | risk-analyst | 리스크 매트릭스 + 확률 근거 기준표 + Devil's Advocate | Opus |
| 3 | scorecard-strategist | 업종별 가중 스코어카드 + ATR 손절/목표가 + 매수/매도 전략 | Opus |
| 4 | report-generator | HTML/PDF 리포트 자동 생성 (모바일 퍼스트, 접이식) | Opus |

---

## v2.1 주요 개선사항

### 1. 리드 검증 로직 (삼성전자 리포트 평가 기반)
- 수치 정합성 교차검증 (시총=주가x주식수, PER 역산 등)
- 논리 모순 검출 (Moat Wide인데 점유율 하락 등)
- 시간축 일관성 검증 (52주 범위 시점 등)

### 2. ATR 손절/목표가 시스템
- 고정비율(8%) + ATR(14일x2배) 중 타이트한 쪽 채택
- 수익 +10% 도달 시 트레일링 모드 전환
- 래칫 구조: 손절가는 올라가기만 하고 절대 내려가지 않음
- 손익비(R:R) 기반 목표가 자동 산정
- SSOT: stop-loss-rules.md

### 3. 업종별 가중 스코어카드
- 종목 유형 자동 판별 (성장주/가치주/배당주/턴어라운드/복합형)
- 유형별 10개 항목 가중치 차등 적용
- 예: 성장주 → 성장성 20%, 산업트렌드 15% 강조
- 예: 가치주 → 밸류에이션 18%, 재무건전성 15% 강조

### 4. 분석 품질 강제 규칙
- Moat: 요인별 정량 지표 2개 이상 필수
- 밸류에이션: 자체 산출 필수 (증권사 나열만으로 대체 불가)
- 컨센서스: 최소 5개 증권사 + EPS 리비전 + Bull/Bear 논쟁
- 리스크: 발생가능성 판단 기준표 (근거 없는 "중" 금지)

---

## 사용법 예시

```
삼성전자 종목 분석해줘
SK하이닉스 투자 의견 알려줘
네이버 vs 카카오 비교 분석해줘
현대차 목표주가 산정해줘
셀트리온 리스크 분석해줘
```

---

## DART API 정보

- 인증키: .claude/settings.json에 등록됨
- 일일 한도: 10,000건
- 관리 페이지: https://opendart.fss.or.kr/mng/userApiKeyListView.do

---

## 손절/목표가 설정값 (기본값)

| 항목 | 기본값 | 범위 |
|------|--------|------|
| 고정 손절률 | 8% | 5~15% |
| ATR 배수 | 2배 | 1.5~3.0배 |
| 트레일링 전환 수익률 | 10% | 5~20% |
| 목표 손익비 | 2:1 | 1.5~5.0 |
