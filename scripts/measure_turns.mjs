/**
 * measure_turns.mjs — 서브에이전트 maxTurns 근접도 계측 (진단 도구)
 *
 * ~/.claude/projects/{프로젝트}/{세션}/subagents/agent-*.jsonl 을 스캔:
 *   - 파일 1개 = 서브에이전트 1회 실행
 *   - attributionAgent 필드 = 에이전트 이름
 *   - assistant 메시지 수 (message.id 디듀프) = 사용 턴 추정치
 *   - 에이전트 frontmatter maxTurns 대조 — 80% 이상 소진 실행 플래그
 *
 * 용도: P2-1/2 (리드 명세 분할) 판단 보조 — "다음 maxTurns 사고를 기다리지 말고
 *       임계 근접 경향을 미리 본다". 정밀 과금 측정이 아닌 경향 파악용.
 *
 * 사용:
 *   node scripts/measure_turns.mjs [--days 14]
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import readline from 'node:readline';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PROJECTS = path.join(os.homedir(), '.claude/projects');
const daysArg = process.argv.indexOf('--days');
const DAYS = daysArg > -1 ? parseInt(process.argv[daysArg + 1], 10) : 14;
const CUTOFF = Date.now() - DAYS * 86400000;

// 에이전트 maxTurns 로드
const maxTurns = {};
const agentsDir = path.join(ROOT, '.claude/agents');
for (const f of fs.readdirSync(agentsDir).filter((x) => x.endsWith('.md'))) {
  const fm = fs.readFileSync(path.join(agentsDir, f), 'utf-8').match(/^---\n([\s\S]*?)\n---/);
  const m = fm?.[1].match(/^maxTurns:\s*(\d+)/m);
  maxTurns[f.replace(/\.md$/, '')] = m ? parseInt(m[1], 10) : null;
}

// 프로젝트 디렉토리 (외장 SSD 경로 인코딩 변형 전부, worktree 제외)
const projectDirs = fs
  .readdirSync(PROJECTS)
  .filter((d) => d.includes('SSD') && !d.includes('worktrees'))
  .map((d) => path.join(PROJECTS, d));

// subagents/agent-*.jsonl 수집
const agentFiles = [];
for (const dir of projectDirs) {
  for (const session of fs.readdirSync(dir)) {
    const sub = path.join(dir, session, 'subagents');
    if (!fs.existsSync(sub) || !fs.statSync(sub).isDirectory()) continue;
    for (const f of fs.readdirSync(sub).filter((x) => x.startsWith('agent-') && x.endsWith('.jsonl'))) {
      const full = path.join(sub, f);
      if (fs.statSync(full).mtimeMs >= CUTOFF) agentFiles.push(full);
    }
  }
}

async function measureFile(file) {
  let agent = null;
  const msgIds = new Set();
  let assistantLines = 0;
  const rl = readline.createInterface({ input: fs.createReadStream(file), crlfDelay: Infinity });
  for await (const line of rl) {
    let d;
    try {
      d = JSON.parse(line);
    } catch {
      continue;
    }
    if (!agent && d.attributionAgent) agent = d.attributionAgent;
    if (d.type === 'assistant') {
      assistantLines += 1;
      const id = d.message?.id ?? d.uuid;
      if (id) msgIds.add(id);
    }
  }
  return { agent: agent ?? '(불명)', turns: msgIds.size || assistantLines };
}

const runs = [];
for (const f of agentFiles) runs.push(await measureFile(f));

const byAgent = new Map();
for (const r of runs) {
  if (!byAgent.has(r.agent)) byAgent.set(r.agent, []);
  byAgent.get(r.agent).push(r.turns);
}

console.log(`[measure_turns] 최근 ${DAYS}일 — 서브에이전트 실행 ${runs.length}회`);
console.log('');
console.log('| 에이전트 | 실행 | 중앙값 | 최대 | maxTurns | 최대/한도 |');
console.log('| --- | --- | --- | --- | --- | --- |');
const flagged = [];
for (const [agent, turns] of [...byAgent.entries()].sort((a, b) => b[1].length - a[1].length)) {
  turns.sort((a, b) => a - b);
  const med = turns[Math.floor(turns.length / 2)];
  const max = turns[turns.length - 1];
  const cap = maxTurns[agent] ?? null;
  const ratio = cap ? `${Math.round((max / cap) * 100)}%` : '—';
  console.log(`| ${agent} | ${turns.length} | ${med} | ${max} | ${cap ?? '미지정'} | ${ratio} |`);
  if (cap && max / cap >= 0.8) flagged.push(`${agent}: 최대 ${max}/${cap} (${ratio})`);
}
console.log('');
if (flagged.length) {
  console.log('[경고] maxTurns 80%+ 근접 실행 감지 — 명세 분할(P2-1/2) 또는 한도 상향 검토 신호:');
  for (const x of flagged) console.log(`  - ${x}`);
} else {
  console.log('임계 근접 실행 없음 (전부 한도 80% 미만).');
}
