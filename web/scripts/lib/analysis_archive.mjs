// analysis_archive.mjs — analysis/ 최신 폴더 또는 _archive tarball 에서 파일 읽기
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const execFileP = promisify(execFile);

/** `${analysisDir}_YYYYMMDD.tar.gz` 정확 매칭(NFC 비교). 복수면 날짜 최신. 실제 이름 반환 */
export function findArchiveName(analysisDir, names) {
  const dir = analysisDir.normalize('NFC');
  const hits = [];
  for (const n of names) {
    const m = n.normalize('NFC').match(/^(.*)_(\d{8})\.tar\.gz$/);
    if (m && m[1] === dir) hits.push({ n, d: m[2] });
  }
  if (!hits.length) return null;
  hits.sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : 0));
  return hits[0].n;
}

/** analysis/{dir}/{filename} 우선, 없으면 _archive tarball 스트리밍(tar -xzOf). 없으면 null */
export async function readAnalysisFile(projectRoot, analysisDir, filename) {
  const base = path.join(projectRoot, 'analysis');
  try {
    return await readFile(path.join(base, analysisDir, filename), 'utf8');
  } catch {}
  let names;
  try {
    names = await readdir(path.join(base, '_archive'));
  } catch {
    return null;
  }
  const arch = findArchiveName(analysisDir, names);
  if (!arch) return null;
  // tarball 내부 경로는 NFC/NFD 어느 쪽일 수 있어 둘 다 시도
  for (const d of new Set([analysisDir, analysisDir.normalize('NFC'), analysisDir.normalize('NFD')])) {
    try {
      const { stdout } = await execFileP('tar', ['-xzOf', path.join(base, '_archive', arch), `${d}/${filename}`], {
        maxBuffer: 64 * 1024 * 1024,
      });
      if (stdout) return stdout;
    } catch {}
  }
  return null;
}

/** 파일 위치 확인 — 'live:analysis/<dir>/<file>' | 'archive:analysis/_archive/<tar>' | 'missing' */
export async function locateAnalysisFile(projectRoot, analysisDir, filename) {
  const base = path.join(projectRoot, 'analysis');
  try {
    await readFile(path.join(base, analysisDir, filename));
    return `live:analysis/${analysisDir}/${filename}`;
  } catch {}
  let names;
  try {
    names = await readdir(path.join(base, '_archive'));
  } catch {
    return 'missing';
  }
  const arch = findArchiveName(analysisDir, names);
  if (!arch) return 'missing';
  for (const d of new Set([analysisDir, analysisDir.normalize('NFC'), analysisDir.normalize('NFD')])) {
    try {
      const { stdout } = await execFileP('tar', ['-xzOf', path.join(base, '_archive', arch), `${d}/${filename}`], {
        maxBuffer: 64 * 1024 * 1024,
      });
      if (stdout) return `archive:analysis/_archive/${arch}`;
    } catch {}
  }
  return 'missing';
}
