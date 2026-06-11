/**
 * lint_agents.mjs — 에이전트/커맨드 명세 정합성 검사 (결정적, LLM 불필요)
 *
 * 검사 항목:
 *   1. 커맨드 frontmatter `agent:` → .claude/agents/{name}.md 존재
 *   2. 에이전트 frontmatter `tools: Agent(...)` 목록의 각 이름 → 에이전트 파일 존재
 *   3. 명세 본문이 참조하는 프로젝트 파일 경로 실존
 *      (scripts/·web/scripts/·reference/·docs/ 의 .py/.mjs/.sh/.md/.json 한정,
 *       {플레이스홀더}·글롭(*)·날짜 변수 포함 경로는 제외)
 *   4. AGENTS.md 에 등장하는 `에이전트명` 백틱 표기 → 파일 존재 (선택적 — AGENTS.md 부패 방지)
 *
 * 사용:
 *   node scripts/lint_agents.mjs          # 검사 + 리포트, 실패 시 exit 1
 *
 * 호출처: 수동 / wiki-linter cross_check / 명세 대량 수정 후 검증.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const AGENTS_DIR = path.join(ROOT, '.claude/agents');
const COMMANDS_DIR = path.join(ROOT, '.claude/commands');

const failures = [];
const warnings = [];

function listMd(dir) {
  return fs.readdirSync(dir).filter((f) => f.endsWith('.md'));
}

const agentFiles = new Set(listMd(AGENTS_DIR).map((f) => f.replace(/\.md$/, '')));

// ── 1. 커맨드 frontmatter agent: ─────────────────────────
for (const f of listMd(COMMANDS_DIR)) {
  const text = fs.readFileSync(path.join(COMMANDS_DIR, f), 'utf-8');
  const fm = text.match(/^---\n([\s\S]*?)\n---/);
  if (!fm) {
    warnings.push(`커맨드 ${f}: frontmatter 없음`);
    continue;
  }
  const agentLine = fm[1].match(/^agent:\s*(\S+)/m);
  if (!agentLine) continue; // agent 미지정 커맨드 허용 (메인 스레드 직접 처리)
  if (!agentFiles.has(agentLine[1])) {
    failures.push(`커맨드 ${f}: agent "${agentLine[1]}" 에이전트 파일 없음`);
  }
}

// ── 2. 에이전트 tools: Agent(...) 목록 ───────────────────
for (const f of listMd(AGENTS_DIR)) {
  const text = fs.readFileSync(path.join(AGENTS_DIR, f), 'utf-8');
  const fm = text.match(/^---\n([\s\S]*?)\n---/);
  if (!fm) {
    failures.push(`에이전트 ${f}: frontmatter 없음`);
    continue;
  }
  const toolsMatch = fm[1].match(/Agent\(([^)]*)\)/);
  if (!toolsMatch) continue;
  for (const name of toolsMatch[1].split(',').map((s) => s.trim()).filter(Boolean)) {
    if (!agentFiles.has(name)) {
      failures.push(`에이전트 ${f}: Agent(...) 의 "${name}" 파일 없음`);
    }
  }
}

// ── 3. 명세 본문 파일 경로 참조 실존 ─────────────────────
const PATH_RE = /(?:^|[\s("'\`])((?:scripts|web\/scripts|reference|docs)\/[\w가-힣.\/-]+\.(?:py|mjs|sh|md|json))/g;
const SKIP_RE = /[{}*$]|YYYYMMDD|날짜|\{.*\}/;

function checkPaths(dir, kind) {
  for (const f of listMd(dir)) {
    const lines = fs.readFileSync(path.join(dir, f), 'utf-8').split('\n');
    const seen = new Set();
    lines.forEach((line, i) => {
      let m;
      PATH_RE.lastIndex = 0;
      while ((m = PATH_RE.exec(line)) !== null) {
        const p = m[1];
        if (seen.has(p) || SKIP_RE.test(p)) continue;
        seen.add(p);
        if (fs.existsSync(path.join(ROOT, p))) continue;
        // "cd web &&" / "cwd=web" 문맥은 web/ 기준 상대 경로 — web/{p} 존재 시 통과
        const webContext = /cd web|cwd\s*=\s*web/.test(line);
        if (webContext && fs.existsSync(path.join(ROOT, 'web', p))) continue;
        failures.push(`${kind} ${f}:${i + 1}: 참조 경로 미존재 — ${p}`);
      }
    });
  }
}
checkPaths(AGENTS_DIR, '에이전트');
checkPaths(COMMANDS_DIR, '커맨드');

// ── 4. AGENTS.md 백틱 에이전트명 ─────────────────────────
const agentsMd = path.join(ROOT, 'AGENTS.md');
if (fs.existsSync(agentsMd)) {
  const text = fs.readFileSync(agentsMd, 'utf-8');
  const named = new Set();
  for (const m of text.matchAll(/`([a-z][a-z0-9-]+)`/g)) {
    const n = m[1];
    // 에이전트명 패턴만 (하이픈 포함 + 알려진 접미어) — 파일명·명령어 오탐 방지
    if (/-(?:lead|analyst|collector|generator|strategist|updater|linter|tracker|scraper|curator|overview|monitor)$/.test(n) || n === 'data-collector') {
      named.add(n);
    }
  }
  for (const n of named) {
    if (!agentFiles.has(n)) failures.push(`AGENTS.md: 에이전트 "${n}" 파일 없음 (문서 부패)`);
  }
}

// ── 리포트 ───────────────────────────────────────────────
console.log(`[lint_agents] 에이전트 ${agentFiles.size}종 / 커맨드 ${listMd(COMMANDS_DIR).length}종 검사`);
for (const w of warnings) console.log(`  WARN: ${w}`);
if (failures.length) {
  console.error(`[lint_agents] 실패 ${failures.length}건:`);
  for (const e of failures) console.error(`  FAIL: ${e}`);
  process.exit(1);
}
console.log('[lint_agents] 통과 — 정합성 문제 없음');
