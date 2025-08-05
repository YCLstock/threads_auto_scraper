[23:10:37.516] Running build in Washington, D.C., USA (East) – iad1
[23:10:37.517] Build machine configuration: 2 cores, 8 GB
[23:10:37.531] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 8d8c1a1)
[23:10:37.652] Previous build caches not available
[23:10:37.789] Cloning completed: 258.000ms
[23:10:40.325] Running "vercel build"
[23:10:40.775] Vercel CLI 44.7.2
[23:10:41.394] Installing dependencies...
[23:10:54.990] 
[23:10:54.991] added 447 packages in 13s
[23:10:54.991] 
[23:10:54.991] 142 packages are looking for funding
[23:10:54.992]   run `npm fund` for details
[23:10:55.084] Running "npm run build"
[23:10:55.399] 
[23:10:55.399] > frontend-app@0.1.0 build
[23:10:55.399] > next build
[23:10:55.401] 
[23:10:56.778] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:10:56.779] This information is used to shape Next.js' roadmap and prioritize features.
[23:10:56.780] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:10:56.780] https://nextjs.org/telemetry
[23:10:56.780] 
[23:10:57.086]    ▲ Next.js 15.4.5
[23:10:57.086] 
[23:10:57.175]    Creating an optimized production build ...
[23:11:17.900]  ✓ Compiled successfully in 17.0s
[23:11:17.906]    Linting and checking validity of types ...
[23:11:25.043] Failed to compile.
[23:11:25.043] 
[23:11:25.045] ./src/components/Dashboard.tsx:77:15
[23:11:25.045] Type error: Type '{ total_posts: number; total_interactions: number; active_topics: number; trending_keywords: number; last_updated: string; generated_at: string; data_source: string; }' is missing the following properties from type '{ generated_at: string; data_range: { start_date: string; end_date: string; }; total_posts: number; total_users: number; total_interactions: number; data_source?: string | undefined; }': data_range, total_users
[23:11:25.046] 
[23:11:25.046] [0m [90m 75 |[39m
[23:11:25.046]  [90m 76 |[39m             setData({
[23:11:25.047] [31m[1m>[22m[39m[90m 77 |[39m               metadata[33m:[39m {
[23:11:25.047]  [90m    |[39m               [31m[1m^[22m[39m
[23:11:25.047]  [90m 78 |[39m                 generated_at[33m:[39m [36mnew[39m [33mDate[39m()[33m.[39mtoISOString()[33m,[39m
[23:11:25.047]  [90m 79 |[39m                 data_source[33m:[39m [32m'supabase'[39m[33m,[39m
[23:11:25.047]  [90m 80 |[39m                 [33m...[39mstatsData[0m
[23:11:25.084] Next.js build worker exited with code: 1 and signal: null
[23:11:25.112] Error: Command "npm run build" exited with 1