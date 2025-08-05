[21:16:57.513] Running build in Washington, D.C., USA (East) – iad1
[21:16:57.513] Build machine configuration: 2 cores, 8 GB
[21:16:57.531] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 254b6c8)
[21:16:57.707] Previous build caches not available
[21:16:57.844] Cloning completed: 313.000ms
[21:17:00.452] Running "vercel build"
[21:17:00.903] Vercel CLI 44.7.2
[21:17:01.687] Installing dependencies...
[21:17:15.175] 
[21:17:15.176] added 447 packages in 13s
[21:17:15.176] 
[21:17:15.176] 142 packages are looking for funding
[21:17:15.177]   run `npm fund` for details
[21:17:15.224] Running "npm run build"
[21:17:15.346] 
[21:17:15.347] > frontend-app@0.1.0 build
[21:17:15.347] > next build
[21:17:15.347] 
[21:17:16.123] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[21:17:16.124] This information is used to shape Next.js' roadmap and prioritize features.
[21:17:16.124] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[21:17:16.124] https://nextjs.org/telemetry
[21:17:16.125] 
[21:17:16.228]    ▲ Next.js 15.4.5
[21:17:16.229] 
[21:17:16.256]    Creating an optimized production build ...
[21:17:35.081]  ✓ Compiled successfully in 15.0s
[21:17:35.085]    Linting and checking validity of types ...
[21:17:39.408] 
[21:17:39.409] Failed to compile.
[21:17:39.409] 
[21:17:39.409] ./src/components/Dashboard.tsx
[21:17:39.409] 5:71  Warning: 'Database' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.409] 5:81  Warning: 'Wifi' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.409] 5:87  Warning: 'WifiOff' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.410] 14:3  Warning: 'getHeatBubbleData' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.410] 15:3  Warning: 'getKeywordTrendsData' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.410] 16:3  Warning: 'getTopicTreemapData' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.410] 17:3  Warning: 'getDashboardStats' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.410] 18:3  Warning: 'testConnection' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.410] 22:13  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.410] 23:21  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.410] 24:24  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.410] 25:23  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.410] 26:20  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 266:71  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 287:60  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 
[21:17:39.411] ./src/components/charts/HeatBubbleChart.tsx
[21:17:39.411] 79:51  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 82:56  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 158:32  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 
[21:17:39.411] ./src/components/charts/TopicTreemap.tsx
[21:17:39.411] 32:10  Warning: 'selectedTopic' is assigned a value but never used.  @typescript-eslint/no-unused-vars
[21:17:39.411] 33:91  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 69:32  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.411] 77:11  Warning: 'colorScale' is assigned a value but never used.  @typescript-eslint/no-unused-vars
[21:17:39.411] 
[21:17:39.412] ./src/components/charts/TrendRiverChart.tsx
[21:17:39.412] 26:91  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.412] 66:23  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.412] 74:28  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.412] 86:26  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.412] 
[21:17:39.412] ./src/lib/api.ts
[21:17:39.412] 1:42  Warning: 'RawPost' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.412] 1:51  Warning: 'ProcessedPostMetric' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.412] 1:72  Warning: 'ProcessedTopicSummary' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.413] 1:95  Warning: 'ProcessedKeywordTrend' is defined but never used.  @typescript-eslint/no-unused-vars
[21:17:39.413] 71:43  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.413] 188:13  Warning: 'data' is assigned a value but never used.  @typescript-eslint/no-unused-vars
[21:17:39.413] 
[21:17:39.413] ./src/lib/supabase.ts
[21:17:39.413] 27:12  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[21:17:39.430] 
[21:17:39.430] info  - Need to disable some ESLint rules? Learn more here: https://nextjs.org/docs/app/api-reference/config/eslint#disabling-rules
[21:17:39.449] Error: Command "npm run build" exited with 1