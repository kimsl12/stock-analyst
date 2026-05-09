// portfolio_parser.mjs — user_portfolio.md 파서 (단위 테스트 가능 모듈)
// sync_portfolio.mjs 에서 import. 부작용 없음 (순수 함수만).

const RE_TABLE = /^\s*\|.+\|\s*$/;
const RE_SEP = /^\s*\|[\s\-:|]+\|\s*$/;

export function splitRow(line) {
  return line.trim().replace(/^\||\|$/g, '').split('|').map((c) => c.trim());
}

export function findTableAfter(lines, headingRe) {
  for (let i = 0; i < lines.length; i++) {
    if (!headingRe.test(lines[i])) continue;
    for (let j = i + 1; j < Math.min(i + 30, lines.length); j++) {
      if (RE_TABLE.test(lines[j]) && RE_SEP.test(lines[j + 1] ?? '')) {
        const header = splitRow(lines[j]);
        const rows = [];
        for (let k = j + 2; k < lines.length; k++) {
          if (!RE_TABLE.test(lines[k]) || RE_SEP.test(lines[k])) break;
          rows.push(splitRow(lines[k]));
        }
        return { header, rows };
      }
    }
  }
  return null;
}

export function stripBold(s) { return (s ?? '').replace(/\*\*/g, '').trim(); }

export function cleanMoney(s) {
  const t = stripBold(s);
  if (!t || t === '—' || t === '-') return null;
  const v = t.replace(/[$,원\s]/g, '');
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

export function cleanQty(s) {
  const t = stripBold(s);
  if (!t || t === '—' || t === '-') return null;
  const v = t.replace(/[주,\s]/g, '');
  const n = Number(v);
  return Number.isFinite(n) ? n : null;
}

export function cleanPct(s) {
  const t = stripBold(s);
  if (!t || t === '—' || t === '-') return null;
  // 첫 % 직전의 숫자(부호 포함) 추출 — "+10.7% (+$1,337.21)" 같은 부수정보 무시
  const m = t.match(/(-?\+?-?\d+(?:\.\d+)?)\s*%/);
  if (m) {
    const n = Number(m[1].replace(/^\+/, ''));
    if (!Number.isFinite(n)) return null;
    return n === 0 ? 0 : n; // -0 → 0 정규화
  }
  const v = t.replace(/[%+\s,]/g, '');
  const n = Number(v);
  if (!Number.isFinite(n)) return null;
  return n === 0 ? 0 : n;
}

export function extractCurrentSection(md) {
  const m = md.match(/##\s*★\s*CURRENT\s*★\s*$([\s\S]*?)(?=^---\s*$|^##\s+\S)/m);
  if (!m) throw new Error('★ CURRENT ★ 섹션을 찾을 수 없음');
  return m[1];
}

/**
 * frontmatter 의 holdings_table_columns 와 실제 표 헤더 비교 (P1-4)
 * 불일치 시 silent drift 의심 → 명시적 에러로 빌드 차단.
 */
export function extractFrontmatter(md) {
  // 첫 --- ... --- 블록만
  const m = md.match(/^---\s*\n([\s\S]*?)\n---\s*\n/);
  if (!m) return {};
  const out = {};
  for (const raw of m[1].split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const colon = line.indexOf(':');
    if (colon < 1) continue;
    const k = line.slice(0, colon).trim();
    let v = line.slice(colon + 1).trim();
    if (v.startsWith('[') && v.endsWith(']')) {
      // 단순 배열 파싱 [a, b, c]
      v = v.slice(1, -1).split(',').map((s) => s.trim()).filter(Boolean);
    }
    out[k] = v;
  }
  return out;
}

/**
 * frontmatter holdings_table_columns 와 실제 헤더 비교.
 * 일치 → null, 불일치 → 에러 메시지 문자열 반환 (배열 형태로 사용 권장).
 */
export function checkSchemaContract(md) {
  const fm = extractFrontmatter(md);
  const expected = fm.holdings_table_columns;
  if (!expected || !Array.isArray(expected)) return null; // 명세 없음 — 검증 스킵
  const lines = extractCurrentSection(md).split(/\r?\n/);
  const t = findTableAfter(lines, /^###\s+보유\s*종목/);
  if (!t) return '보유 종목 표 미발견 (frontmatter 에 holdings_table_columns 명세는 존재)';
  // 헤더 정규화 (공백 차이 무시)
  const norm = (s) => s.replace(/\s+/g, '').replace(/\(.*?\)/g, '');
  const expNorm = expected.map(norm);
  const actNorm = t.header.map(norm);
  if (expNorm.length !== actNorm.length) {
    return `컬럼 수 불일치: frontmatter ${expNorm.length}컬럼 [${expected.join(', ')}] vs 실제 ${actNorm.length}컬럼 [${t.header.join(', ')}]`;
  }
  for (let i = 0; i < expNorm.length; i++) {
    if (expNorm[i] !== actNorm[i]) {
      return `컬럼 #${i + 1} 불일치: 명세='${expected[i]}' vs 실제='${t.header[i]}'`;
    }
  }
  return null; // 일치
}

export function parseProfile(lines) {
  const t = findTableAfter(lines, /^###\s+투자자\s*프로파일/);
  if (!t) throw new Error('투자자 프로파일 표 미발견');
  const profile = {};
  for (const row of t.rows) {
    if (row.length < 2) continue;
    const k = row[0].trim();
    const v = stripBold(row[1]);
    if (k) profile[k] = v;
  }
  return profile;
}

// 보유 종목 표 컬럼 명세 (v3.16+ 9컬럼 / legacy 8컬럼 자동 감지)
//   8컬럼: 티커|종목명|유형|시장|수량|평가금|비중|수익률
//   9컬럼: 티커|종목명|유형|시장|수량|현재가|평가금|비중|수익률
export function parseHoldings(lines) {
  const t = findTableAfter(lines, /^###\s+보유\s*종목/);
  if (!t) throw new Error('보유 종목 표 미발견');
  const out = [];
  const ncol = t.header.length;
  if (ncol < 8) {
    throw new Error(`보유 종목 표 컬럼 수 ${ncol} (최소 8 필요) — 표 형식 변경 의심`);
  }
  for (const row of t.rows) {
    if (row.length < 8) continue;
    let ticker, name, assetType, market, qty, priceUsd, valueUsd, weight, ret;
    if (ncol >= 9) {
      [ticker, name, assetType, market, qty, priceUsd, valueUsd, weight, ret] = row;
    } else {
      [ticker, name, assetType, market, qty, valueUsd, weight, ret] = row;
      priceUsd = null;
    }
    if (!ticker || ticker.startsWith('---')) continue;
    const isCash = /현금/.test(assetType) || /현금/.test(ticker);
    const normType = isCash ? 'CASH' : (assetType && assetType !== '—' ? assetType.toUpperCase() : null);
    const normMarket = market && market !== '—' ? market : null;
    const qVal = cleanQty(qty) ?? (isCash ? 0 : null);
    const vVal = cleanMoney(valueUsd);
    const wVal = cleanPct(weight);
    const rVal = cleanPct(ret);
    if (qVal == null) continue;
    const pVal = cleanMoney(priceUsd);
    const currentPrice = pVal != null ? pVal : (qVal > 0 && vVal != null ? vVal / qVal : null);
    out.push({
      ticker,
      name: name || ticker,
      asset_type: normType,
      market: normMarket,
      quantity: qVal,
      avg_buy_price: null,
      current_price: currentPrice,
      current_value_usd: vVal,
      weight_pct: wVal,
      return_pct: rVal,
    });
  }
  return out;
}

export function parseTotals(lines) {
  const t = findTableAfter(lines, /^###\s+포트폴리오\s*총액/);
  let totalUsd = null;
  if (t) {
    for (const row of t.rows) {
      if (row.length < 2) continue;
      const label = stripBold(row[0]);
      if (/총액/.test(label)) {
        totalUsd = cleanMoney(row[1]);
        break;
      }
    }
  }
  let fx = null;
  for (const line of lines) {
    if (/환율/.test(line) && /원/.test(line)) {
      const m = line.match(/([\d,]+\.\d+)\s*원/);
      if (m) { fx = cleanMoney(m[1]); break; }
    }
  }
  const totalKrw = totalUsd && fx ? totalUsd * fx : null;
  return { total_value_usd: totalUsd, exchange_rate: fx, total_value_krw: totalKrw };
}

// ────────────────────────────────────────────────────────────────────────
// 무결성 검증 — silent drift 방지 (2026-05-09 9컬럼 사일런트 드리프트 사고 후 추가)
// ────────────────────────────────────────────────────────────────────────
export function validateParsed(parsed) {
  const failures = [];
  const nonCash = (parsed.holdings ?? []).filter((h) => h.asset_type !== 'CASH');
  if (nonCash.length === 0) {
    failures.push('보유 종목(현금 외) 0건 — 표 파싱 실패 의심');
  }
  if (nonCash.length > 0) {
    const wOk = nonCash.filter((h) => h.weight_pct != null && h.weight_pct > 0).length;
    const wRate = wOk / nonCash.length;
    if (wRate < 0.8) {
      failures.push(`weight_pct 추출률 ${(wRate * 100).toFixed(0)}% (${wOk}/${nonCash.length}) — 80% 미만, 표 컬럼 시프트 의심`);
    }
    const rOk = nonCash.filter((h) => h.return_pct != null).length;
    const rRate = rOk / nonCash.length;
    if (rRate < 0.5) {
      failures.push(`return_pct 추출률 ${(rRate * 100).toFixed(0)}% (${rOk}/${nonCash.length}) — 50% 미만, 수익률 컬럼 형식 변경 의심`);
    }
  }
  if (parsed.total_value_usd == null) {
    failures.push('total_value_usd null — 포트폴리오 총액 표 파싱 실패');
  }
  if (!parsed.profile || Object.keys(parsed.profile).length < 3) {
    failures.push(`profile 항목 ${Object.keys(parsed.profile ?? {}).length}건 — 3건 미만, 투자자 프로파일 표 파싱 실패`);
  }
  const totalW = (parsed.holdings ?? [])
    .map((h) => h.weight_pct ?? 0)
    .reduce((a, b) => a + b, 0);
  if (parsed.holdings && parsed.holdings.length > 0 && (totalW < 50 || totalW > 105)) {
    failures.push(`보유 종목 비중 합계 ${totalW.toFixed(1)}% — 50~105% 범위 이탈, 비중 컬럼 매핑 의심`);
  }
  return failures;
}
