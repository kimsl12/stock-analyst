# 사용자 측 셋업·검증 가이드

> 이 문서는 **사용자(사이트 소유자)가 직접 수행해야 하는 작업**만 정리합니다.
> 코드 작업은 `web/PLAN.md`를 따르며, 본 문서는 운영 측면 — Vercel/Supabase 대시보드 설정,
> 배포 후 시각 검증, 트러블슈팅 — 을 다룹니다.

작성: 2026-05-05 (Phase 2 완료 시점)

---

## 0. 사전 준비

| 자원 | 값 |
|---|---|
| 운영 도메인 | https://stock-analyst-jungwon1.vercel.app |
| Vercel 프로젝트 | jungwon1/stock-analyst |
| Supabase 프로젝트 | (대시보드에서 확인) |
| Git repo | https://github.com/kimsl12/stock-analyst |
| 화이트리스트 이메일 | jungwon9402@gmail.com |

---

## 1. 첫 비밀번호 설정 (1회만 필요, 2026-05-05 비번 방식 전환)

**목적:** 매직링크 방식 폐기 후 일반 비밀번호 로그인 사용. 첫 1회만 메일 받기.

**단계:**
1. https://stock-analyst-jungwon1.vercel.app/login 접속
2. 이메일 칸에 `jungwon9402@gmail.com` 입력 (비번 칸은 비워둔 채)
3. **"비밀번호를 잊으셨나요? / 처음 사용 시 비밀번호 설정"** 링크 클릭
4. 확인 다이얼로그 → 확인 → 메일 발송 안내
5. 메일함(스팸함 포함, 1-2분 내) → "Reset password" 링크 클릭
6. `/auth/callback?mode=recovery` 페이지로 이동 → 새 비밀번호 8자 이상 입력 (2회)
7. "비밀번호 저장" 클릭 → `/` 자동 이동 + 로그인 완료
8. **이후로는 메일 받을 필요 없음** — `/login`에서 이메일 + 비번으로 바로 로그인

**실패 시:**
- 메일이 안 옴 → Supabase 대시보드 → Auth → Logs → "Recovery" 항목 확인
- 콜백 페이지에서 "인증 토큰이 만료되었거나 잘못되었습니다" → 메일이 1시간 이상 지났을 수 있음. 다시 reset 요청
- "허용되지 않은 이메일입니다" → §2.1 `PUBLIC_ALLOWED_EMAIL` 환경변수 확인 + 재배포

**비밀번호 잊었을 때:** 동일 절차. `/login` → "비밀번호를 잊으셨나요?" → 메일 → 새 비번 설정.

**비밀번호 변경하고 싶을 때 (보안 정책):** 동일 절차로 재설정.

---

## 2. Day 6 사용자 측 작업 — 인증·환경변수 셋업

### 2.1 Vercel 환경변수 4종 등록

Vercel 대시보드 → `stock-analyst` 프로젝트 → **Settings → Environment Variables**:

| 키 | 값 | 환경 |
|---|---|---|
| `PUBLIC_SUPABASE_URL` | https://xxx.supabase.co | Production / Preview |
| `PUBLIC_SUPABASE_ANON_KEY` | eyJ... (anon key) | Production / Preview |
| `SUPABASE_SERVICE_KEY` | eyJ... (service role) | Production만 |
| `PUBLIC_ALLOWED_EMAIL` | jungwon9402@gmail.com | Production / Preview |

저장 후 **재배포 필수** (env 변경은 자동 트리거 안 됨):
```bash
cd "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"
vercel --prod --yes
```

### 2.2 Supabase Auth → URL Configuration

Supabase 대시보드 → Authentication → **URL Configuration**:

| 항목 | 값 |
|---|---|
| Site URL | `https://stock-analyst-jungwon1.vercel.app` |
| Redirect URLs (추가) | `https://stock-analyst-jungwon1.vercel.app/auth/callback` |
| Redirect URLs (개발용 추가) | `http://localhost:4321/auth/callback` |

저장 후 즉시 반영됨 (재배포 불필요).

### 2.3 Supabase Auth → Sessions → JWT Expiry

Authentication → Sessions → **JWT expiry limit**:
- 기본값 3600 (1시간) → **2592000** (30일)으로 변경
- 세션 자동 갱신 보장 (브라우저 닫아도 30일 유지)

### 2.4 Supabase Auth → Providers → Email

Authentication → Providers → **Email**:
- "Enable Email Provider" 토글 ON
- "Confirm Email" 토글 OFF (Magic Link만 사용, 회원가입 단계 불필요)

### 2.5 Vercel Deployment Protection (선택)

Vercel 대시보드 → Project Settings → **Deployment Protection**:
- 기본값(Vercel Authentication) → **Disabled** 또는 **Standard Protection** 선택
- Magic Link 콜백이 Vercel 인증 화면을 통과해야 작동하므로, **Disabled 권장**
- (Pro tier 사용자는 Password Protection으로도 가능)

---

## 3. Day 7 검증 — UI·성능 시각 확인

### 3.1 다크/라이트 토글

1. https://stock-analyst-jungwon1.vercel.app/ 접속
2. 우측 상단 ☀/☾ 버튼 클릭
3. 다음 페이지 모두 토글 시 색상 정합 확인:
   - `/` (대시보드)
   - `/all` (전체 인덱스)
   - `/portfolio`
   - `/timemachine`
   - `/compare?a=AAPL&b=MSFT`
   - `/stocks/MRVL` (iframe 안의 분석 리포트도 다크/라이트 호환되는지)
4. 새로고침 시 마지막 선택 유지 (LocalStorage `theme`)
5. 시크릿 창에서 첫 진입 시 시스템 prefers-color-scheme 따름

### 3.2 Lighthouse 측정 (Chrome DevTools)

1. Chrome → F12 → Lighthouse 탭
2. Mode: Navigation, Device: **Mobile + Desktop 둘 다**
3. Categories: Performance + Accessibility + Best Practices
4. "Analyze page load" 클릭
5. 목표 점수:
   - Performance: ≥ 90
   - Accessibility: ≥ 95
   - Best Practices: ≥ 95

**미달 시:**
- LCP > 2.5s → 이미지 lazy load 확인
- CLS > 0.1 → fixed height 강제
- TBT > 300ms → JS lazy load (FlexSearch 등)
→ 리포트 결과를 PLAN.md §17 또는 GitHub Issue로 남기고 Phase 3 백로그에 추가

### 3.3 모바일 대응 검증

Chrome DevTools → Device Toolbar (Cmd+Shift+M) → iPhone 14 Pro / Galaxy S22 / iPad Pro 시뮬레이션:

| 라우트 | 확인 사항 |
|---|---|
| `/` | 위젯 1열 변환 (`@media max-width:600px`) |
| `/all` | 카드 1열 + FilterBar 접힘 |
| `/timemachine` | 라디오 세로 배치 + 표 가로 스크롤 |
| `/compare` | iframe 상하 분할 (`max-width:800px`) |
| `/stocks/MRVL` | iframe 가로 스크롤 |

### 3.4 60+ 리포트 모두 접근

`/all` 페이지에서:
- 검색 박스에 "MRVL" 입력 → 결과 ≥ 1건
- 필터 "morning" 선택 → 모닝 브리핑만 카드 노출
- 무작위 카드 5개 클릭 → 모두 정상 임베드

---

## 4. Day 14 검증 — Phase 2 신규 라우트

### 4.1 `/api/price/[ticker]` 동작

브라우저로 직접:
- https://stock-analyst-jungwon1.vercel.app/api/price/AAPL → JSON 200
- https://stock-analyst-jungwon1.vercel.app/api/price/005930 → 한국 .KS 폴백 OK
- https://stock-analyst-jungwon1.vercel.app/api/price/AAPL?at=2026-04-28 → `at_price`, `return_since_at_pct` 필드

같은 ticker 두 번째 호출 → 응답에 `"cached": true` 포함 (5분 in-memory 캐시).

### 4.2 `/timemachine`

1. 1주 / 1개월 / 3개월 라디오 변경 → 자동 fetch + 표 갱신
2. 수익률 컬럼 +값(녹색) / -값(빨강) 색상 코딩
3. 자동 정렬 (수익률 내림차순)
4. "↻ 다시 가져오기" 버튼 → 캐시 무시 재 fetch

### 4.3 `/compare?a=AAPL&b=MSFT`

1. 자동 비교 시작 (URL에 a, b 있으면)
2. 핵심 지표 표 10행 (현재가/전일비/52주/시총/ATR/손절·목표)
3. 좌우 iframe — 분석 리포트 정상 렌더
4. 셀렉터로 다른 종목 선택 → URL 자동 갱신 (`history.replaceState`)
5. 모바일 너비 ≤ 800px → 상하 분할

### 4.4 PerformanceDonut

1. 대시보드 우하단 "적중률" 위젯
2. 도넛 4-slice (적중·오류·진행중·보류) + 중앙 % + 누적 N건
3. 다크/라이트 토글 시 색상 정합
4. 다음 `/성과리뷰` 실행 시 자동 갱신

---

## 5. 트러블슈팅

| 증상 | 원인 후보 | 조치 |
|---|---|---|
| 매직 링크 클릭 후 redirect_to 오류 | URL Configuration 미등록 | §2.2 Site URL + Redirect URLs 추가 |
| `/` 무한 리다이렉트 | LocalStorage 손상 | DevTools → Application → LocalStorage → `sb-stock-analyst-auth` 키 삭제 후 재로그인 |
| 다른 이메일로 로그인 성공 | `PUBLIC_ALLOWED_EMAIL` 미설정 | §2.1 Vercel env 등록 + 재배포 |
| 빌드 시 `python: command not found` | 구버전 prebuild 잔존 | 현재 모든 빌드 스크립트 Node `.mjs` (포팅 완료) |
| FlexSearch 검색 무응답 | search-data.json 미생성 | `npm run build` 또는 `node web/scripts/build_search_index.mjs` |
| `/api/price/AAPL` 504 timeout | yfinance cold start 30s 초과 | `vercel.json` `maxDuration: 60` 상향 (Pro tier 필요) |
| `/timemachine`에 가격 "불가" 다수 | rate limit 60/min 초과 | 1분 대기 또는 클라이언트 동시성 4 → 2로 하향 (web/src/pages/timemachine.astro) |
| 도넛 "준비 중" placeholder 유지 | `performance_history.md` 누적 0건 | `/성과리뷰` 명령 1회 실행 후 재배포 |
| 배포 후 새 라우트 404 | git push만 했고 vercel deploy 안 됨 | `cd /Volumes/.../종목분석 에이전트 && vercel --prod --yes` (수동) |

---

## 6. 자주 쓰는 명령

```bash
# 작업 폴더로
cd "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트"

# 로컬 빌드 검증
cd web && npm run build && cd ..

# 배포 (수동, 반드시 monorepo root에서)
vercel --prod --yes

# 빌드 로그 확인
vercel inspect <deployment-url> --logs

# 라이브 헬스체크
curl -sS -o /dev/null -w "%{http_code}\n" https://stock-analyst-jungwon1.vercel.app/api/price/AAPL
```

---

## 7. 다음 단계 (Phase 3 P0)

본 가이드 검증 완료 후 가장 마찰이 큰 항목:
1. **GitHub 자동 배포 webhook 활성화** — 매번 수동 `vercel --prod` 제거
   - Vercel 대시보드 → Project Settings → Git → "Connect Git Repository" → kimsl12/stock-analyst
   - 활성화 후 `git push origin main` 만으로 자동 배포
2. main↔gh-pages 자동 사이클 14회 원인 조사 (PLAN §12.2 P0)
3. 본 문서 자체 갱신 — 검증 결과 누적
