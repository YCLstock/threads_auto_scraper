[23:16:08.272] Running build in Washington, D.C., USA (East) – iad1
[23:16:08.281] Build machine configuration: 2 cores, 8 GB
[23:16:08.303] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 935c8d3)
[23:16:08.509] Previous build caches not available
[23:16:08.798] Cloning completed: 493.000ms
[23:16:11.180] Running "vercel build"
[23:16:11.607] Vercel CLI 44.7.2
[23:16:12.160] Installing dependencies...
[23:16:25.362] 
[23:16:25.363] added 447 packages in 13s
[23:16:25.363] 
[23:16:25.364] 142 packages are looking for funding
[23:16:25.364]   run `npm fund` for details
[23:16:25.414] Running "npm run build"
[23:16:25.517] 
[23:16:25.518] > frontend-app@0.1.0 build
[23:16:25.518] > next build
[23:16:25.518] 
[23:16:26.278] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:16:26.279] This information is used to shape Next.js' roadmap and prioritize features.
[23:16:26.280] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:16:26.280] https://nextjs.org/telemetry
[23:16:26.280] 
[23:16:26.378]    ▲ Next.js 15.4.5
[23:16:26.379] 
[23:16:26.403]    Creating an optimized production build ...
[23:16:46.017]  ✓ Compiled successfully in 16.0s
[23:16:46.022]    Linting and checking validity of types ...
[23:16:50.042] 
[23:16:50.042] ./src/components/Dashboard.tsx
[23:16:50.043] 21:3  Warning: 'HeatBubbleData' is defined but never used.  @typescript-eslint/no-unused-vars
[23:16:50.043] 22:3  Warning: 'KeywordTrendData' is defined but never used.  @typescript-eslint/no-unused-vars
[23:16:50.043] 23:3  Warning: 'TopicTreemapData' is defined but never used.  @typescript-eslint/no-unused-vars
[23:16:50.043] 24:3  Warning: 'DashboardStats' is defined but never used.  @typescript-eslint/no-unused-vars
[23:16:50.044] 
[23:16:50.044] info  - Need to disable some ESLint rules? Learn more here: https://nextjs.org/docs/app/api-reference/config/eslint#disabling-rules
[23:16:52.687] Failed to compile.
[23:16:52.687] 
[23:16:52.687] ./src/components/Dashboard.tsx:30:36
[23:16:52.687] Type error: Cannot find name 'DashboardData'. Did you mean 'DashboardStats'?
[23:16:52.687] 
[23:16:52.687] [0m [90m 28 |[39m
[23:16:52.687]  [90m 29 |[39m [36mexport[39m [36mdefault[39m [36mfunction[39m [33mDashboard[39m() {
[23:16:52.688] [31m[1m>[22m[39m[90m 30 |[39m   [36mconst[39m [data[33m,[39m setData] [33m=[39m useState[33m<[39m[33mDashboardData[39m [33m|[39m [36mnull[39m[33m>[39m([36mnull[39m)
[23:16:52.688]  [90m    |[39m                                    [31m[1m^[22m[39m
[23:16:52.688]  [90m 31 |[39m   [36mconst[39m [activeChart[33m,[39m setActiveChart] [33m=[39m useState[33m<[39m[32m'bubble'[39m [33m|[39m [32m'river'[39m [33m|[39m [32m'treemap'[39m[33m>[39m([32m'bubble'[39m)
[23:16:52.688]  [90m 32 |[39m   [36mconst[39m [isLoading[33m,[39m setIsLoading] [33m=[39m useState([36mtrue[39m)
[23:16:52.688]  [90m 33 |[39m   [36mconst[39m [useRealData[33m,[39m setUseRealData] [33m=[39m useState([36mfalse[39m)[0m
[23:16:52.708] Next.js build worker exited with code: 1 and signal: null
[23:16:52.723] Error: Command "npm run build" exited with 1