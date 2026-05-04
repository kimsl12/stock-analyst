/**
 * E2: 최근 본 리포트 — 클라이언트 LocalStorage 헬퍼.
 *
 * 사용:
 *   import { trackView, getRecent } from '../lib/recently-viewed';
 *   trackView({ url, title, type, date });    // 리포트 페이지에서 호출
 *   const recent = getRecent(5);              // 대시보드에서 표시
 */
const STORAGE_KEY = 'sa.recentReports';
const MAX = 20;

export type ViewedItem = {
  url: string;
  title: string;
  type?: string;
  date?: string;
  ts: number; // viewedAt epoch ms
};

export function trackView(it: Omit<ViewedItem, 'ts'>): void {
  if (typeof window === 'undefined') return;
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    const list: ViewedItem[] = raw ? JSON.parse(raw) : [];
    // 동일 url 제거 후 맨 앞에 push
    const filtered = list.filter((x) => x.url !== it.url);
    filtered.unshift({ ...it, ts: Date.now() });
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(filtered.slice(0, MAX)));
  } catch {
    /* localStorage off / quota — silent */
  }
}

export function getRecent(n = 5): ViewedItem[] {
  if (typeof window === 'undefined') return [];
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const list: ViewedItem[] = JSON.parse(raw);
    return list.slice(0, n);
  } catch {
    return [];
  }
}

export function clearRecent(): void {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.removeItem(STORAGE_KEY);
  } catch {
    /* silent */
  }
}
