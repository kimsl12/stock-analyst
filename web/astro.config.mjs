// @ts-check
import { defineConfig } from 'astro/config';

// Day 3: 정적 SSG. Day 11(Edge Function)에서 @astrojs/vercel adapter 추가 예정.
// site URL은 Vercel 첫 배포 후 실제 도메인으로 갱신 (현재는 stock-analyst-jungwon1.vercel.app 가정).
export default defineConfig({
  output: 'static',
  site: 'https://stock-analyst-jungwon1.vercel.app',
  build: {
    format: 'directory',
  },
});
