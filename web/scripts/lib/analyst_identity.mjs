/**
 * analyst_identity.mjs — 애널리스트 순위 집계 기준 (v1, 2026-11-12)
 *
 * 문제: meta.analyst 표기가 수집 경로마다 제각각("Tom Lee" / "Tom Lee (Fundstrat Global Advisors 공동창업자…)"
 *       / "Mike Wilson, 최고투자책임자… (Morgan Stanley)" / "N/A" / "Bloomberg TV 진행진" / 6인 패널 문자열)
 *       → 같은 사람이 여러 행으로 쪼개지고 매체·패널·팀이 개인 순위에 섞임.
 *
 * 집계 기준:
 *  1. 개인 = 실명 1인. 괄호 속 소속·직함, 쉼표 뒤 직함은 이름에서 제거하고 대소문자·별칭을 통일.
 *  2. 진행자·앵커·기자는 예측 주체가 아니므로 참가자에서 제외.
 *  3. 진행자 제외 후 실명이 1인인 항목만 그 개인에게 산입.
 *     2인 이상(공동 저자·패널)은 개인 순위에서 제외하고, 전원이 같은 기관일 때만 기관에 산입.
 *  4. 기관 = 개인 항목(그 사람의 대표 소속) + 팀·기관 명의 리포트. 기관명은 별칭 사전으로 통일하고
 *     계열사(자산운용·WM·리서치 부문)는 모그룹으로 합침. 한 사람은 항상 하나의 대표 소속(최빈값)으로 집계.
 *  5. 매체 진행진·편집부·컨센서스 종합·익명·출처 미상 → 순위 제외(건수만 표기).
 *  6. 점수: 적중(0.5)·오차(0.3)·논리(0.2). 판정이 없는 지표는 0점/만점 처리하지 않고 가중치에서 빼서 재정규화.
 */

// ── 기관 별칭 사전 (위에서부터 첫 매치) ─────────────────────────────────────────
const FIRM_ALIASES = [
  ['Goldman Sachs', /goldman|골드만|\bGSAM\b|^GS$/i],
  ['Morgan Stanley', /morgan\s*stanley|모건\s*스탠리|^MS$/i],
  ['JPMorgan', /j\.?\s*p\.?\s*morgan|jpmorgan|\bJPM\b|JP\s*모[건간]|제이피\s*모[건간]/i],
  ['Bank of America', /bank\s*of\s*america|\bbofa\b|\bboa\b|뱅크\s*오브\s*아메리카|merrill|메릴/i],
  ['Citi', /\bciti(group|bank)?\b|씨티/i],
  ['UBS', /\bUBS\b/],
  ['HSBC', /HSBC/i],
  ['Barclays', /barclays|바클레이[즈스]/i],
  ['Deutsche Bank', /deutsche|도이[치체]/i],
  ['Wells Fargo', /wells\s*fargo|웰스\s*파고/i],
  ['BlackRock', /blackrock|블랙록/i],
  ['Fundstrat', /fundstrat|펀드스트랫/i],
  ['Wedbush', /wedbush|웨드부시/i],
  ['Bernstein', /bernstein|번스타인/i],
  ['Evercore ISI', /evercore|에버코어/i],
  ['Jefferies', /jefferies|제[프퍼]리스/i],
  ['Nomura', /nomura|노무라/i],
  ['Macquarie', /macquarie|맥쿼리/i],
  ['CLSA', /\bCLSA\b/i],
  ['Mizuho', /mizuho|미즈호/i],
  ['RBC Capital Markets', /\bRBC\b/i],
  ['BMO Capital Markets', /\bBMO\b/i],
  ['Truist', /truist/i],
  ['KeyBanc', /keybanc|키\s*뱅크/i],
  ['Raymond James', /raymond\s*james|레이먼드\s*제임스/i],
  ['Piper Sandler', /piper\s*sandler|파이퍼\s*샌들러/i],
  ['Cantor Fitzgerald', /cantor|캔터/i],
  ['TD Cowen', /\bTD\s*cowen|^cowen|코웬|카우언/i],
  ['Stifel', /stifel|스티펠/i],
  ['Needham', /needham|니덤/i],
  ['Rosenblatt', /rosenblatt|로젠블랫/i],
  ['DA Davidson', /\bD\.?\s*A\.?\s*davidson|데이비드?슨/i],
  ['Freedom Broker', /freedom\s*broker|프리덤\s*브로커/i],
  ['Wolfe Research', /wolfe/i],
  ['Yardeni Research', /yardeni|야데니/i],
  ['Allianz', /allianz|알리안츠|앨리안츠/i],
  ['PIMCO', /pimco|핌코/i],
  ['Strategas', /strategas/i],
  ['Ritholtz Wealth Management', /ritholtz/i],
  ['Charles Schwab', /schwab|슈왑/i],
  ['Guggenheim', /guggenheim|구겐하임/i],
  ['Robert W. Baird', /robert\s*w\.?\s*baird|^baird|베어드/i],
  ['CFRA', /\bcfra\b/i],
  ['Rothschild & Co Redburn', /redburn|rothschild|로스차일드|레드번/i],
  ['BNP Paribas', /BNP|exane|엑산/i],
  ['Keefe, Bruyette & Woods', /keefe|\bKBW\b/i],
  ['Oppenheimer', /^oppenheimer|oppenheimer\s*(&|and|co|medtech|team)|오펜하이머/i],
  ['Susquehanna', /susquehanna|서스쿼해나/i],
  ['Berenberg', /berenberg|베렌베르크|베렌버그/i],
  ['Loop Capital', /loop\s*capital|루프\s*캐피[털탈]/i],
  ['H.C. Wainwright', /h\.?\s*c\.?\s*wainwright|웨인라이트/i],
  ['DZ Bank', /DZ\s*(bank|방크|은행)/i],
  ['B. Riley', /b\.?\s*riley|b\.\s*라일리/i],
  ['Seaport', /seaport/i],
  ['Northland', /northland|노스랜드/i],
  ['GLJ Research', /\bGLJ/i],
  ['Oaktree', /oaktree/i],
  ['Arete', /arete|아레테/i],
  ['Daiwa', /daiwa|다이와/i],
  ['FBN Securities', /\bFBN\b/i],
  ['Freedom Capital Markets', /freedom\s*capital|프리덤\s*캐피[털탈]/i],
  ['Phillip Securities', /phillip\s*(securities|capital)|필립\s*증권/i],
  ['China Renaissance', /china\s*renaissance|중국\s*르네상스/i],
  ['Erste Group', /erste|에르스테/i],
  ['William Blair', /william\s*blair|윌리엄\s*블레어/i],
  ['Argus Research', /argus/i],
  ['Roth Capital', /roth\s*capital|로스\s*캐피[털탈]/i],
  ['BNY', /\bBNY\b/],
  ['Citizens', /^citizens|citizens\s*(jmp|financial|capital)|시티즌스/i],
  ['Stephens', /^stephens(\s*(&|inc|co))?|스티븐스/i],
  ['StoneX', /stonex|스톤엑스/i],
  ['Canaccord', /canaccord|캐나코드/i],
  ['Longbow Research', /longbow|롱보우/i],
  ['Itaú BBA', /ita[uú]\s*bba|이타우/i],
  ['상상인증권', /상상인/],
  ['Federal Reserve', /federal\s*reserve|연방\s*준비|연준|연은|\bFed\b/i],
  // 한국 증권사
  ['삼성증권', /삼성\s*증권|samsung\s*securities/i],
  ['미래에셋증권', /미래에셋|mirae/i],
  ['KB증권', /KB\s*증권|kb\s*securities|^KB$/i],
  ['하나증권', /하나\s*(증권|금융투자)|hana\s*securities|^하나$/i],
  ['신한투자증권', /신한/],
  ['SK증권', /SK\s*증권/i],
  ['대신증권', /대신|daishin/i],
  ['키움증권', /키움|kiwoom/i],
  ['NH투자증권', /NH\s*(투자)?\s*증권/i],
  ['한국투자증권', /한국투자증권/],
  ['메리츠증권', /메리츠|meritz/i],
  ['유안타증권', /유안타|yuanta/i],
  ['교보증권', /교보/],
  ['iM증권', /iM\s*증권|하이투자/i],
  ['DS투자증권', /DS\s*투자/i],
  ['LS증권', /LS\s*증권|이베스트/i],
  ['다올투자증권', /다올/],
  ['현대차증권', /현대차\s*증권/],
  ['유진투자증권', /유진\s*투자/],
  ['IBK투자증권', /IBK/i],
  ['한화투자증권', /한화\s*투자/],
  ['DB증권', /DB\s*(증권|금융투자)/i],
  ['한국IR협의회', /한국\s*IR\s*협의회/i],
];

// 매체 — 기관(예측 주체)으로 집계하지 않음. 단 Bloomberg Intelligence/Economics 는 리서치 부문이라 기관 취급.
const RESEARCH_ARM = [['Bloomberg Intelligence', /bloomberg\s*(intelligence|economics)/i]];
const MEDIA_RE =
  /bloomberg|블룸버그|cnbc|reuters|로이터|investing\.com|24\/7|247\s*wall|benzinga|yahoo|marketbeat|daily trade alert|seeking alpha|motley fool|youtube|유튜브|cbs|forbes|investor'?s business daily|whatfinger|coindesk|daily\s*hodl|the fly|markets weekly|fast money|mad money|halftime|squawk|surveillance|asia trade|opening trade|the close|open interest|closing bell|morningstar/i;

// 진행자·앵커·기자 (예측 주체 아님)
const HOSTS = new Set(
  [
    'Jonathan Ferro', 'Lisa Abramowicz', 'Annmarie Hordern', 'Tom Keene', 'Paul Sweeney', 'Katie Greifeld',
    'Romaine Bostick', 'Dani Burger', 'Shery Ahn', 'Haidi Stroud-Watts', 'Paul Allen', 'Anna Edwards',
    'Guy Johnson', 'Tom Mackenzie', 'Francine Lacqua', 'David Gura', 'Scarlet Fu', 'Matt Miller',
    'Kailey Leinz', 'Carol Massar', 'Tim Stenovec', 'Jan-Patrick Barnert', 'Anthony Stephens', 'Alix Steel',
    'Vonnie Quinn', 'Caroline Hyde', 'Ed Ludlow', 'Emily Chang', 'Scott Wapner', 'Sara Eisen',
    'Carl Quintanilla', 'David Faber', 'Melissa Lee', 'Becky Quick', 'Joe Kernen', 'Andrew Ross Sorkin',
    'Kelly Evans', 'Jon Fortt', 'Morgan Brennan', 'Courtney Reagan', 'Frank Holland', 'Dominic Chu',
    'Christina Partsinevelos', 'Brian Sullivan', 'Leslie Picker', 'Brandon Gomez', 'Mike McKee',
    'Michael McKee', 'Kristina Partsinevelos', '조나단 페로', '리사 아브라모비츠', '데이비드 구라', '애나 에드워즈',
    '모건 브레넌',
  ].map((n) => n.toLowerCase()),
);
const HOST_ROLE_RE = /진행|앵커|anchor|host|기자|reporter/i;
// 진행자이면서 본인 의견·종목 추천을 내는 인물 → 예측 주체로 집계
const OPINION_HOSTS = new Set(['jim cramer']);

// 동일인 별칭 (정규화 키 → 정규화 키)
const PERSON_ALIASES = new Map([
  ['bankim chadha', 'binky chadha'],
  ['헬리마 크로프트', 'helima croft'],
  ['벤 스나이더', 'ben snider'],
  ['짐 크레이머', 'jim cramer'],
  ['이사벨 리', 'isabelle lee'],
  ['마이클 하트넷', 'michael hartnett'],
  ['마이크 윌슨', 'mike wilson'],
  ['릭 리더', 'rick rieder'],
  ['스테이시 라스곤', 'stacy rasgon'],
  ['에드 야드니', 'ed yardeni'],
  ['로버트 카플란', 'robert kaplan'],
  ['로리 캘바시나', 'lori calvasina'],
  ['다이앤 스원크', 'diane swonk'],
  ['제프리 로젠버그', 'jeffrey rosenberg'],
]);

// 영문 애칭 통일 (키 전용 — 표시명은 최빈 표기)
const NICK = {
  michael: 'mike', daniel: 'dan', thomas: 'tom', robert: 'bob', william: 'bill', james: 'jim',
  christopher: 'chris', joseph: 'joe', stephen: 'steve', steven: 'steve', edward: 'ed', matthew: 'matt',
  richard: 'rick', benjamin: 'ben', anthony: 'tony', samuel: 'sam', jonathan: 'jon', andrew: 'andy',
  nicholas: 'nick', kenneth: 'ken', jeffrey: 'jeff', gregory: 'greg', timothy: 'tim', alexander: 'alex',
};

// 참가자가 아닌 표기 (예측 주체 불명)
const ANON_RE =
  /^(n\/?a|none|unknown|미상|미확인|없음|익명|-|—)$|복수|다수|컨센서스|consensus|설문|종합|구체\s*출연진|확인\s*불가|미표기|미기재|미공개|인사이더|insider|패널|panel/i;

const ORG_WORD_RE =
  /(팀|증권|센터|진행진|앵커|데스크|편집|담당|리서치|채널|게스트|애널리스트|전략가|이코노미스트|트레이더|분석|협의회|운용|은행|그룹|연구소|투자|캐피[털탈]|파트너스|자산|위원)|\b(Research|Securities|Capital|Management|Institute|Economics|Bank|Group|Team|Desk|Markets?|Television|TV|News|Fool|Club|Money|Partners|Advisors|Advisory|Global|Asset|Investment|Intelligence|Analytics|Funds?|Wealth|Strategy|Strategists?|Panel|Anchors?|Editors?|Channel|Update|Weekly|Brief|Daily|Equity|Economists?|Traders?|Inc|LLC|Corp|Financial|Partners|Brokerage|Genuity)\b/i;

// 섹터·지역·직무어 — 한글 이름처럼 생겨도 이름 아님 ("미국 주식", "인터넷")
const KOREAN_TOPIC_RE =
  /미국|한국|중국|일본|유럽|주식|채권|시장|전략|경제|글로벌|섹터|산업|기술|반도체|자동차|금융|에너지|유틸리티|소비|헬스|바이오|부동산|원자재|원자력|소재|건설|항공|우주|방산|조선|화학|철강|인터넷|미디어|게임|통신|운송|물류|계량|매크로|정책|선진국|신흥국|리스크|인디케이터/;
const LATIN_NAME_RE =
  /^[A-Z][A-Za-z.'’-]+(?:\s+(?:[A-Z][A-Za-z.'’-]*|de|van|von|der|la|du|da|di|le)){1,3}$/;
const KOREAN_NAME_RE = /^[가-힣]{2,4}$|^[가-힣]{1,5}\s[가-힣]{1,6}$/;

// ── 문자열 유틸 ────────────────────────────────────────────────────────────────
const norm = (s) =>
  String(s ?? '')
    .replace(/[（]/g, '(')
    .replace(/[）]/g, ')')
    .replace(/[’`]/g, "'")
    .replace(/\s+/g, ' ')
    .trim();

/** 괄호 밖 구분자로만 분할 */
function splitTop(s, seps) {
  const out = [];
  let depth = 0;
  let buf = '';
  for (let i = 0; i < s.length; i++) {
    const ch = s[i];
    if (ch === '(') depth++;
    else if (ch === ')') depth = Math.max(0, depth - 1);
    if (depth === 0) {
      const sep = seps.find((p) => s.startsWith(p, i));
      if (sep) {
        out.push(buf);
        buf = '';
        i += sep.length - 1;
        continue;
      }
    }
    buf += ch;
  }
  out.push(buf);
  return out.map((t) => t.trim()).filter(Boolean);
}

/** "Name (paren1) (paren2)" → { bare, parens[] } */
function peel(token) {
  const parens = [];
  const bare = token
    .replace(/\(([^()]*(?:\([^()]*\)[^()]*)*)\)/g, (_, c) => {
      parens.push(c.trim());
      return ' ';
    })
    .replace(/\s+/g, ' ')
    .trim();
  return { bare, parens };
}

/** 기관명 정규화. 매체면 null, 사전에 없으면 정리된 원문. 前/전 직함은 무시. */
export function canonFirm(text) {
  let s = norm(text);
  if (!s) return null;
  // "前 브리지워터…, CFR 선임연구원" → 전직 구간 제거
  s = s
    .split(/[,，]/)
    .filter((seg) => !/^\s*(前|전\s)/.test(seg))
    .join(',')
    .trim();
  if (!s) return null;
  for (const [name, re] of RESEARCH_ARM) if (re.test(s)) return name;
  for (const [name, re] of FIRM_ALIASES) if (re.test(s)) return name;
  if (MEDIA_RE.test(s)) return null;
  if (/^(n\/?a|none|unknown|미상|-)$/i.test(s)) return null;
  // 사전 밖: 직함·부문 꼬리 제거한 원문 (예: "Lazard 수석 시장 전략가" → "Lazard")
  const cleaned = s
    .split(/[,，]/)[0]
    .replace(/\s*(수석|선임|최고|공동|창업자|대표|총괄|애널리스트|분석가|투자분석가|전략가|이코노미스트|매니저|CIO|CEO|CFO|MD|팀장|교수|연구원|회장|위원장|겸).*$/i, '')
    .replace(/\s*(리서치센터|리서치|주식전략팀|전략팀|[가-힣·]*팀)$/, '')
    .trim();
  if (!cleaned || cleaned.length < 2 || cleaned.length > 40 || /[\/·]/.test(cleaned)) return null;
  if (/^(co\.?|inc\.?|llc|ltd\.?)$/i.test(cleaned)) return null;
  if (/^(chief|head|senior|managing|founder|co-founder|portfolio|director|president|vice|앵커)\b|(strategist|economist|analyst|officer)$/i.test(cleaned)) return null;
  if (ANON_RE.test(cleaned) || /인용|기반|미확인|출연진|진행|앵커|게스트|트레이더|인터뷰|채널|투자위원회|investment committee|fedwatch/i.test(cleaned)) return null;
  const bareName = cleaned.replace(/\s+(외|등)$/, '');
  if (HOSTS.has(bareName.toLowerCase())) return null;
  // 사람 이름처럼 생긴 문자열(괄호 속 진행자 등)은 기관 아님
  if (HOSTS.has(cleaned.toLowerCase())) return null;
  if ((LATIN_NAME_RE.test(cleaned) || KOREAN_NAME_RE.test(cleaned)) && !ORG_WORD_RE.test(cleaned)) return null;
  return cleaned;
}

/** 사전 매치만 (사전 밖 원문 폴백 없음) */
export function dictFirm(text) {
  const s = norm(text)
    .split(/[,，]/)
    .filter((seg) => !/^\s*(前|전\s)/.test(seg))
    .join(',');
  if (!s) return null;
  for (const [name, re] of RESEARCH_ARM) if (re.test(s)) return name;
  for (const [name, re] of FIRM_ALIASES) if (re.test(s)) return name;
  return null;
}

function isMediaText(s) {
  return MEDIA_RE.test(s) && !RESEARCH_ARM.some(([, re]) => re.test(s));
}

/** 이름 토큰 → 정규화 키(소문자). 사람 이름이 아니면 null */
function personKey(bare) {
  let n = norm(bare)
    .replace(/^(게스트|출연|진행|guest|host)\s*[:：]\s*/i, '')
    .replace(/\s+(등|외)$/, '')
    .replace(/\s+(연구원|애널리스트|팀장|수석|위원|이사)$/, '')
    .replace(/"[^"]*"/g, ' ') // Bankim "Binky" Chadha
    .replace(/\s+/g, ' ')
    .trim();
  if (!n || ANON_RE.test(n) || ORG_WORD_RE.test(n)) return null;
  // 기관명이 토큰 맨 앞에서 시작할 때만 기관 ("Ed Yardeni"·"Peter Oppenheimer" 는 사람)
  if (FIRM_ALIASES.some(([, re]) => re.exec(n)?.index === 0) || MEDIA_RE.test(n)) return null;
  if (!LATIN_NAME_RE.test(n) && !KOREAN_NAME_RE.test(n)) return null;
  if (KOREAN_NAME_RE.test(n) && KOREAN_TOPIC_RE.test(n)) return null;
  let key = n.toLowerCase();
  key = PERSON_ALIASES.get(key) ?? key;
  const [first, ...rest] = key.split(' ');
  if (NICK[first] && rest.length) key = [NICK[first], ...rest].join(' ');
  return { key, display: n };
}

/**
 * 항목 1건 해석 → { persons:[{key,display,firm}], firmHints:[], hostOnly, anon }
 */
export function parseAnalystField(raw) {
  let s = norm(raw);
  const persons = [];
  const firmHints = [];
  let sawHost = false;
  let anon = !s || ANON_RE.test(s.replace(/\(.*?\)/g, '').trim());
  // "인터넷·미디어팀" · "건설/엔지니어링 담당" 같은 섹터 복합어는 분할 전에 '팀'으로 접음 (섹터명이 이름으로 오인되는 것 방지)
  s = s.replace(/[가-힣A-Za-z]+(?:\s*[·\/]\s*[가-힣A-Za-z]+)+\s*(리서치팀|리서치|팀|담당)/g, '팀');

  for (const seg of splitTop(s, [' / ', '/', ';', ' | '])) {
    // 구간 전체가 진행자 묶음: "진행: A, B" 또는 "... (진행)"
    const segHost = /^(진행|앵커|host|anchor)\s*[:：]/i.test(seg) || /\((진행|앵커|host)\)\s*$/i.test(seg);
    let segFirm = null; // "iM증권 전유진·장호" → 앞 기관이 구간 내 뒤 저자에게도 적용
    for (const tok of splitTop(seg, [',', '，', ' · ', '·', '、', ' and ', ' 외 ', '; '])) {
      const peeled = peel(tok);
      const parens = peeled.parens;
      let bare = peeled.bare;
      // "다이앤 스원크 — KPMG US" → 이름 / 소속
      const dash = bare.split(/\s+[—–]\s+/);
      if (dash.length > 1) {
        const right = dash.slice(1).join(' ');
        if (!personKey(dash[0]) && personKey(right)) {
          parens.push(dash[0]); // "CNBC Mad Money — Jim Cramer"
          bare = right;
        } else {
          bare = dash[0];
          parens.push(right);
        }
      }
      // "상상인증권 송지연" · "ADP Nela Richardson" · "CFRA Sam Zino" → 앞 기관 + 이름
      if (!personKey(bare)) {
        const words = bare.split(' ');
        for (let k = Math.min(3, words.length - 1); k >= 1; k--) {
          const head = words.slice(0, k).join(' ');
          const isFirm = FIRM_ALIASES.some(([, re]) => re.test(head)) || (k === 1 && /^[A-Z]{2,6}$/.test(head));
          if (!isFirm) continue;
          const tail = words.slice(k).join(' ');
          if (personKey(tail)) {
            parens.push(head);
            bare = tail;
            segFirm = dictFirm(head) ?? segFirm;
          }
          break; // 가장 긴 기관 접두만 시도
        }
      }
      const roleHost = parens.some((p) => HOST_ROLE_RE.test(p) && !/[:：]/.test(p));
      for (const p of parens) {
        if (/[:：]/.test(p)) {
          // "(Wedbush, 진행: Scott Wapner)" → 진행 앞부분만 기관 힌트
          const head = p.split(/[,，]?\s*(진행|host)\s*[:：]/i)[0];
          if (head) firmHints.push(head);
        } else if (!HOST_ROLE_RE.test(p) && !bare.toLowerCase().includes(p.toLowerCase())) firmHints.push(p); // 애칭 괄호 제외
      }
      const pk = personKey(bare);
      if (!pk) {
        if (bare && !ANON_RE.test(bare)) firmHints.push(bare); // 팀·기관 명의 토큰
        continue;
      }
      const opinionHost = OPINION_HOSTS.has(pk.key);
      if (!opinionHost && (segHost || roleHost || HOSTS.has(pk.key) || HOSTS.has(pk.display.toLowerCase()))) {
        sawHost = true;
        continue;
      }
      // "Tomohiko (Tomo) Sano" 처럼 괄호가 애칭이면 소속 아님
      const ps = parens.filter((p) => !pk.key.includes(p.toLowerCase()));
      const own = ps.map(dictFirm).find(Boolean) ?? ps.map(canonFirm).find(Boolean) ?? null;
      if (!persons.some((p) => p.key === pk.key)) persons.push({ ...pk, firm: own ?? segFirm });
    }
  }
  return { persons, firmHints, hostOnly: sawHost && persons.length === 0, anon };
}

/** 항목 수준 기관 후보 (비매체) */
function itemFirm(item, parsed) {
  // 사전 매치 우선 — 사전 기관이 하나면 그것, 여럿이면 단일 귀속 불가
  const dict = [...new Set(parsed.firmHints.map(dictFirm).filter(Boolean))];
  if (dict.length === 1) return dict[0];
  if (dict.length > 1) return null;
  const uniqHints = [...new Set(parsed.firmHints.map(canonFirm).filter(Boolean))];
  if (uniqHints.length === 1) return uniqHints[0];
  if (uniqHints.length > 1) return null;
  const metaFirm = item.analyst_firm && !/[\/]/.test(item.analyst_firm) ? canonFirm(item.analyst_firm) : null;
  if (metaFirm) return metaFirm;
  const src = norm(item.source);
  const quoted = src.match(/\(([^()]*?)\s*(리서치|콜)?\s*인용\)/);
  if (quoted) {
    const f = canonFirm(quoted[1]);
    if (f) return f;
  }
  if (['ib_official', 'korea_brokerage', 'user_upload'].includes(item.source_type) && !isMediaText(src)) {
    return canonFirm(src.split(/[\/—–(]/)[0]);
  }
  return null;
}

/**
 * 항목 1건의 귀속 결정.
 * @returns {{kind:'individual'|'firm'|'excluded', reason?:string, person?:{key,display,firm}, firm?:string|null}}
 */
export function resolveItem(item) {
  const parsed = parseAnalystField(item.analyst_name);
  const firm = itemFirm(item, parsed);
  if (parsed.persons.length === 1) {
    const p = parsed.persons[0];
    return { kind: 'individual', person: p, firm: p.firm ?? firm };
  }
  if (parsed.persons.length >= 2) {
    // 공동 저자 판정: 이름 문자열에 등장하는 기관이 하나뿐이고 개인 소속과 충돌하지 않을 때만 그 기관에 산입.
    // 문자열에 기관이 없으면 IB·증권사 공식 리포트일 때만 발행 기관으로 귀속 (방송 패널은 제외).
    const own = new Set(parsed.persons.map((p) => p.firm).filter(Boolean));
    const strFirms = new Set(parsed.firmHints.map(dictFirm).filter(Boolean));
    const all = new Set([...own, ...strFirms]);
    // 일부만 소속 표기가 있으면 "A, B, C (BofA)" 처럼 맨 끝 공유 괄호일 때만 공동 저자로 인정
    const partial = own.size > 0 && parsed.persons.some((p) => !p.firm);
    const trailingShared = !parsed.persons.at(-1).firm ? false : parsed.persons.slice(0, -1).every((p) => !p.firm);
    let common = null;
    if (all.size === 1 && (!partial || trailingShared)) common = [...all][0];
    else if (all.size === 0 && ['ib_official', 'korea_brokerage', 'user_upload'].includes(item.source_type)) common = firm;
    return common ? { kind: 'firm', firm: common, reason: 'coauthor' } : { kind: 'excluded', reason: 'panel' };
  }
  const strFirms = new Set(parsed.firmHints.map(dictFirm).filter(Boolean));
  if (strFirms.size > 1) return { kind: 'excluded', reason: 'panel' }; // "GS 팀 · Evercore 팀" 등 복수 기관
  if (parsed.anon && !firm) return { kind: 'excluded', reason: 'anonymous' };
  if (/복수|다수|컨센서스|consensus|설문|종합/i.test(norm(item.analyst_name))) {
    return { kind: 'excluded', reason: 'consensus' };
  }
  if (firm) return { kind: 'firm', firm, reason: 'team' };
  return { kind: 'excluded', reason: 'media' };
}

// ── 점수 ─────────────────────────────────────────────────────────────────────
export function hitScore(o) {
  if (!o) return null;
  if (o.hit === true) return 1;
  if (o.hit === false) return 0;
  if (o.hit === 'partial') return 0.5;
  return null;
}
export function thesisScore(o) {
  const tv = o?.thesis_validity;
  if (tv === 'logic_chain_correct' || tv === 'correct') return 1;
  if (tv === 'logic_chain_partial' || tv === 'partial') return 0.5;
  if (tv === 'logic_chain_incorrect' || tv === 'incorrect') return 0;
  return null;
}
const mean = (xs) => (xs.length ? xs.reduce((a, b) => a + b, 0) / xs.length : null);

export const WEIGHTS = { hit: 0.5, error: 0.3, thesis: 0.2 };

function scoreGroup(list) {
  const o = list.map((it) => it.outcome);
  const hits = o.map(hitScore).filter((x) => x !== null);
  const errs = o.map((x) => x?.error_pct).filter((e) => typeof e === 'number' && Number.isFinite(e)).map(Math.abs);
  const theses = o.map(thesisScore).filter((x) => x !== null);
  const hit_rate = mean(hits);
  const avg_error_pct = mean(errs);
  const thesis = mean(theses);
  const parts = [];
  if (hit_rate !== null) parts.push([WEIGHTS.hit, hit_rate]);
  if (avg_error_pct !== null) parts.push([WEIGHTS.error, Math.max(0, 1 - avg_error_pct / 100)]);
  if (thesis !== null) parts.push([WEIGHTS.thesis, thesis]);
  const wsum = parts.reduce((a, [w]) => a + w, 0);
  const composite = wsum ? parts.reduce((a, [w, v]) => a + w * v, 0) / wsum : null;
  return {
    count: list.length,
    n_hit: hits.length,
    hit_rate,
    n_error: errs.length,
    avg_error_pct,
    n_thesis: theses.length,
    thesis,
    composite,
  };
}

const mode = (arr) => {
  const c = new Map();
  for (const x of arr) if (x) c.set(x, (c.get(x) ?? 0) + 1);
  let best = null;
  let n = 0;
  for (const [k, v] of c) if (v > n) [best, n] = [k, v];
  return best;
};

/**
 * @param {object[]} allItems  manifest analyst 항목 전체 (대표 소속·표시명 결정용)
 * @param {{minEvals?:number}} opt
 */
export function buildAnalystBoard(allItems, { minEvals = 5 } = {}) {
  // 1) 전체 항목으로 개인별 대표 소속·표시명 결정
  const firmVotes = new Map();
  const nameVotes = new Map();
  const resolved = allItems.map((it) => ({ it, r: resolveItem(it) }));
  for (const { r } of resolved) {
    if (r.kind !== 'individual') continue;
    const k = r.person.key;
    if (!firmVotes.has(k)) firmVotes.set(k, []), nameVotes.set(k, []);
    firmVotes.get(k).push(r.firm);
    nameVotes.get(k).push(r.person.display);
  }
  const personFirm = new Map([...firmVotes].map(([k, v]) => [k, mode(v)]));
  const personName = new Map([...nameVotes].map(([k, v]) => [k, mode(v)]));

  // 2) 평가 완료분 귀속
  const people = new Map();
  const firms = new Map();
  const excluded = { panel: 0, media: 0, anonymous: 0, consensus: 0 };
  const push = (map, key, it) => (map.has(key) ? map.get(key).push(it) : map.set(key, [it]));
  for (const { it, r } of resolved) {
    if (!it.outcome?.evaluated_at) continue;
    if (r.kind === 'individual') {
      push(people, r.person.key, it);
      const f = personFirm.get(r.person.key);
      if (f) push(firms, f, it);
    } else if (r.kind === 'firm') {
      push(firms, r.firm, it);
    } else {
      excluded[r.reason] = (excluded[r.reason] ?? 0) + 1;
    }
  }

  const rank = (rows) =>
    rows.sort((a, b) => (b.composite ?? -1) - (a.composite ?? -1) || b.count - a.count || a.name.localeCompare(b.name));
  const personRows = [...people].map(([key, list]) => ({
    key,
    name: personName.get(key) ?? key,
    firm: personFirm.get(key) ?? null,
    ...scoreGroup(list),
  }));
  const firmRows = [...firms].map(([key, list]) => ({
    key,
    name: key,
    people: new Set(list.map((it) => resolveItem(it)).filter((r) => r.kind === 'individual').map((r) => r.person.key)).size,
    ...scoreGroup(list),
  }));
  return {
    minEvals,
    individuals: rank(personRows.filter((r) => r.count >= minEvals)),
    firms: rank(firmRows.filter((r) => r.count >= minEvals)),
    lowSample: {
      individuals: personRows.filter((r) => r.count < minEvals).sort((a, b) => b.count - a.count || a.name.localeCompare(b.name)),
      firms: firmRows.filter((r) => r.count < minEvals).sort((a, b) => b.count - a.count || a.name.localeCompare(b.name)),
    },
    excluded,
  };
}
