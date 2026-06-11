/**
 * sw.js — 최소 서비스 워커 (PWA 설치 요건 + 오프라인 폴백)
 *
 * 전략: 페이지·데이터는 network-first (대시보드 데이터 신선도 우선),
 *       네트워크 실패 시에만 캐시 폴백. 정적 아이콘류는 cache-first.
 * 주의: 리포트 HTML 은 매일 갱신되므로 적극적 캐싱 금지.
 */
const CACHE = "stock-analyst-v1";
const STATIC_ASSETS = [
  "/favicon.svg",
  "/icon-192.png",
  "/icon-512.png",
  "/manifest.webmanifest",
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(STATIC_ASSETS)));
  self.skipWaiting();
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)),
        ),
      ),
  );
  self.clients.claim();
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== self.location.origin) return;

  // 정적 자산: cache-first
  if (STATIC_ASSETS.includes(url.pathname)) {
    e.respondWith(caches.match(e.request).then((r) => r || fetch(e.request)));
    return;
  }

  // 그 외: network-first + 성공 응답 캐시 + 실패 시 캐시 폴백
  e.respondWith(
    fetch(e.request)
      .then((res) => {
        if (res.ok && res.type === "basic") {
          const clone = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return res;
      })
      .catch(() => caches.match(e.request)),
  );
});
