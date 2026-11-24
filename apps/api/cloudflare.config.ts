import { defineConfig } from 'cf/config';

// deploy はまだしない（ローカルの cf dev だけ）。binding は機能を足すときに env へ足す。
export default defineConfig({
  worker: {
    name: 'andon-api',
    entrypoint: 'src/index.ts',
    compatibilityDate: '2026-11-01',
    compatibilityFlags: ['nodejs_compat'],
    observability: {
      enabled: true,
      logs: { enabled: true, invocationLogs: true, headSamplingRate: 1 },
    },
  },
});
