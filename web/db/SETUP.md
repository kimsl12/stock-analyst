# Day 1 — Supabase 셋업 가이드

> **사용자(jungwon9402@gmail.com) 직접 작업 가이드.**
> Claude는 SQL/환경 파일을 미리 준비했고, 사용자는 Supabase 대시보드에서 아래 순서대로 클릭/실행만 하면 됩니다.

---

## 0. 사전 준비

- Supabase 프로젝트 생성 완료 ✅ (사용자 확인됨)
- 프로젝트 대시보드 URL: `https://supabase.com/dashboard/project/<프로젝트ID>`

---

## 1. 환경변수 발급 (5분)

### 1-1. Project URL + Anon Key

1. 대시보드 좌측 사이드바 → **Project Settings**
2. **API** 탭
3. **Project URL** 복사 → 메모장에 임시 보관 (예: `https://abcd1234.supabase.co`)
4. **Project API keys** 섹션:
   - **anon public** 키 복사 → 메모장 (`eyJ...`로 시작, 비교적 짧음)
   - **service_role secret** 키 복사 → ★별도 안전한 곳에 보관 (절대 노출 금지)

### 1-2. `.env.local` 작성

프로젝트 루트의 `web/` 폴더에서:

```bash
cd "/Volumes/외장SSD/클로드 AI 폴더/작업폴더/종목분석 에이전트/web"
cp .env.example .env.local
```

`web/.env.local`을 텍스트 에디터로 열어 4개 값 모두 채우기:
- `PUBLIC_SUPABASE_URL` ← Project URL
- `PUBLIC_SUPABASE_ANON_KEY` ← anon public 키
- `SUPABASE_SERVICE_KEY` ← service_role secret 키
- `ALLOWED_EMAIL` ← `jungwon9402@gmail.com` (이미 기본값)

**`.env.local`은 `.gitignore`에 등록되어 있어 절대 commit되지 않습니다.**

---

## 2. DB 스키마 + RLS 적용 (5분)

### 2-1. SQL Editor 열기

대시보드 좌측 사이드바 → **SQL Editor** → **New query**

### 2-2. 3개 SQL 순서대로 실행

**① schema.sql**
1. `web/db/schema.sql` 전체 복사
2. SQL Editor에 붙여넣기
3. 우측 상단 **RUN** (또는 Cmd+Enter)
4. "Success. No rows returned" 메시지 확인

**② rls.sql** (새 query 탭에서)
1. `web/db/rls.sql` 전체 복사 → 붙여넣기 → **RUN**
2. "Success. No rows returned" 확인

**③ verify.sql** (새 query 탭에서)
1. `web/db/verify.sql` 전체 복사 → 붙여넣기 → **RUN**
2. 단일 결과셋 8행이 표시됨. **status 컬럼이 모두 `OK`이면 통과.**

| check_name | expected | 의미 |
|---|---|---|
| `tables_exist` | 4 | public 스키마에 4개 테이블 존재 |
| `rls_enabled` | 4 | 4개 테이블 모두 RLS 활성화 |
| `policies_count` | 5 | RLS 정책 5개 (`own_portfolio_read/write`, `own_holdings_read`, `auth_reports_read`, `auth_models_read`) |
| `indexes_count` | 2 | `idx_reports_type_date`, `idx_reports_ticker` |
| `rows_portfolios` | 0 | 빈 테이블 |
| `rows_holdings` | 0 | 빈 테이블 |
| `rows_model_portfolios` | 0 | 빈 테이블 |
| `rows_reports` | 0 | 빈 테이블 |

`FAIL` 행이 하나라도 있으면 → verify.sql 하단 주석의 항목별 복구 방법 참조 또는 사용자에게 알림.

> **참고:** Supabase SQL Editor는 여러 SELECT를 한 번에 실행하면 **마지막 결과만 UI에 표시**합니다. verify.sql은 단일 결과셋으로 통합되어 있어 이 동작과 무관하게 모든 검증이 한 화면에 보입니다.

---

## 3. Auth 설정 (10분)

### 3-1. 이메일 회원가입 차단 (화이트리스트 1단계)

대시보드 좌측 → **Authentication** → **Sign In / Providers** → **Email**

- **Enable Email provider**: ON
- **Confirm email**: OFF (Magic Link만 사용하므로 불필요)
- **Allow new users to sign up**: **OFF** ★
  - 이렇게 하면 등록되지 않은 이메일은 매직 링크 자체를 받을 수 없음
- **Save** 클릭

> Supabase UI 라벨은 버전마다 약간 다를 수 있습니다. "Disable signup" 또는 "Allow signups" 항목을 찾아 막으면 됩니다.

### 3-2. 사용자 1명 직접 추가

대시보드 좌측 → **Authentication** → **Users** → **Add user** → **Send invitation** (또는 **Create new user**)

- **Email**: `jungwon9402@gmail.com`
- **Auto Confirm User**: ON (즉시 활성화)
- **Send** / **Create user**

→ Users 목록에 jungwon9402@gmail.com이 보이면 OK.

### 3-3. 한국어 매직 링크 이메일 템플릿

대시보드 좌측 → **Authentication** → **Email Templates** → **Magic Link** 탭

**Subject** (제목):
```
[종목분석 에이전트] 로그인 링크
```

**Message** (본문 — HTML 영역):
```html
<h2>종목분석 에이전트 로그인</h2>

<p>안녕하세요,</p>

<p>아래 링크를 클릭하시면 종목분석 에이전트 웹 플랫폼에 로그인됩니다.</p>

<p>
  <a href="{{ .ConfirmationURL }}"
     style="display:inline-block;padding:12px 24px;background:#3b82f6;
            color:#fff;text-decoration:none;border-radius:6px;
            font-weight:600;">
    로그인하기
  </a>
</p>

<p style="color:#666;font-size:14px;">
  버튼이 작동하지 않으면 아래 URL을 브라우저에 직접 붙여 넣으세요:<br>
  <code style="word-break:break-all;">{{ .ConfirmationURL }}</code>
</p>

<hr style="border:none;border-top:1px solid #eee;margin:24px 0;">

<p style="color:#999;font-size:12px;">
  본인이 요청하지 않은 메일이라면 무시하셔도 됩니다.<br>
  링크는 1시간 동안 유효합니다.
</p>
```

**Save** 클릭.

### 3-4. Site URL 설정 (Vercel 배포 후 갱신 — Day 3)

지금은 placeholder만 설정하고, Day 3에서 Vercel 배포 URL이 확정되면 갱신합니다.

대시보드 좌측 → **Authentication** → **URL Configuration**:
- **Site URL**: `http://localhost:4321` (Astro 개발 서버 기본 포트 — Day 3에서 `https://stock-analyst-jungwon1.vercel.app`으로 갱신)
- **Redirect URLs**: 비워둠 (Day 6에서 추가)

---

## 4. Magic Link 동작 테스트 (3분)

### 4-1. 발송 테스트

대시보드 좌측 → **Authentication** → **Users**
1. `jungwon9402@gmail.com` 행 클릭
2. **...** 메뉴 → **Send magic link**
3. 받은편지함 확인 → 한국어 본문 메일 도착 확인
4. 링크 클릭 시 `localhost:4321`로 이동(연결 실패 정상 — Day 3까지 서버 없음)

> 메일이 안 오면: Spam 폴더 확인. 그래도 없으면 Authentication → Logs에서 발송 로그 확인.

### 4-2. 비허용 이메일 차단 확인 (선택)

다른 이메일로 매직 링크 요청 시도 → "Email signup not allowed" 류 에러 확인.
(Day 6에서 `web/login` 페이지로 다시 검증할 예정이므로 지금은 스킵 가능)

---

## 5. Day 1 완료 체크리스트

다음 모두 ✅이면 Day 1 완료, Day 2로 진행:

- [ ] `web/.env.local` 4개 값 모두 입력됨 (그리고 `.env.local`은 git 추적 안 됨)
- [ ] verify.sql 결과 5개 섹션 모두 기대값 일치
- [ ] Authentication → Users 목록에 `jungwon9402@gmail.com` 존재
- [ ] "Allow new users to sign up" OFF 상태
- [ ] 한국어 Magic Link 이메일 본문 적용됨
- [ ] 매직 링크 메일 1회 수신 성공

---

## 6. 트러블슈팅

| 증상 | 해결 |
|---|---|
| `gen_random_uuid()` not exist | `create extension if not exists pgcrypto;` 먼저 실행 (Supabase 기본 활성화이지만 만약을 위해) |
| `auth.users` 참조 실패 | Supabase가 자동 생성하는 schema. 새 프로젝트라면 정상 존재. |
| RLS 정책 충돌 | rls.sql은 `drop policy if exists` 우선이라 재실행 안전 |
| 매직 링크 메일 안 옴 | Authentication → Logs 확인. SMTP rate limit (시간당 3통) 가능성. |
| Spam으로 분류 | Free tier 메일은 Supabase 기본 SMTP 사용 — Pro 업그레이드나 Custom SMTP 설정 필요 (이번 작업 외) |

---

## 7. 다음 단계 (Day 2)

Day 1 완료 후 알려주세요. Day 2는 다음을 작업합니다:

- `scripts/sync_portfolio_to_supabase.py` 작성 (로컬 md → Supabase upsert)
- `requirements.txt`에 `supabase-py` 추가
- `.claude/agents/briefing-lead.md` `/내포트폴리오` Phase 4-후에 sync 호출 한 줄 추가
- 1회 수동 sync 실행 → Supabase 데이터 확인

Day 2는 Claude가 직접 코드 작성을 수행합니다. 사용자의 추가 대시보드 작업은 없습니다.
