[23:28:09.592] Running build in Washington, D.C., USA (East) – iad1
[23:28:09.593] Build machine configuration: 2 cores, 8 GB
[23:28:09.629] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 37e5fd2)
[23:28:09.787] Previous build caches not available
[23:28:09.942] Cloning completed: 312.000ms
[23:28:12.551] Running "vercel build"
[23:28:13.019] Vercel CLI 44.7.2
[23:28:13.608] Installing dependencies...
[23:28:28.746] 
[23:28:28.747] added 447 packages in 15s
[23:28:28.748] 
[23:28:28.748] 142 packages are looking for funding
[23:28:28.748]   run `npm fund` for details
[23:28:28.936] Running "npm run build"
[23:28:29.066] 
[23:28:29.066] > frontend-app@0.1.0 build
[23:28:29.067] > next build
[23:28:29.067] 
[23:28:30.594] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:28:30.598] This information is used to shape Next.js' roadmap and prioritize features.
[23:28:30.598] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:28:30.598] https://nextjs.org/telemetry
[23:28:30.598] 
[23:28:30.878]    ▲ Next.js 15.4.5
[23:28:30.879] 
[23:28:30.894]    Creating an optimized production build ...
[23:28:51.633]  ✓ Compiled successfully in 17.0s
[23:28:51.640]    Linting and checking validity of types ...
[23:28:59.089] Failed to compile.
[23:28:59.089] 
[23:28:59.089] ./src/components/Dashboard.tsx:73:21
[23:28:59.089] Type error: Conversion of type '{ metadata: { generated_at: string; data_range: { start_date: string; end_date: string; }; total_posts: number; total_users: number; total_interactions: number; }; heat_bubble_data: { post_id: string; ... 12 more ...; color: string; }[]; keyword_trends_data: { ...; }[]; topic_treemap_data: { ...; }[]; dashboard_stat...' to type 'DashboardData' may be a mistake because neither type sufficiently overlaps with the other. If this was intentional, convert the expression to 'unknown' first.
[23:28:59.089]   Types of property 'topic_treemap_data' are incompatible.
[23:28:59.089]     Type '{ topic_id: number; topic_name: string; topic_keywords: string[]; post_count: number; average_heat_density: number; total_interactions: number; dominant_sentiment: string; trending_score: number; size: number; color: string; children: { ...; }[]; }[]' is not comparable to type 'TopicTreemapData[]'.
[23:28:59.089]       Type '{ topic_id: number; topic_name: string; topic_keywords: string[]; post_count: number; average_heat_density: number; total_interactions: number; dominant_sentiment: string; trending_score: number; size: number; color: string; children: { ...; }[]; }' is not comparable to type 'TopicTreemapData'.
[23:28:59.090]         Types of property 'topic_id' are incompatible.
[23:28:59.090]           Type 'number' is not comparable to type 'string'.
[23:28:59.090] 
[23:28:59.090] [0m [90m 71 |[39m             console[33m.[39mwarn([32m'Database connection failed, falling back to mock data'[39m)
[23:28:59.090]  [90m 72 |[39m             setUseRealData([36mfalse[39m)
[23:28:59.090] [31m[1m>[22m[39m[90m 73 |[39m             setData(mockData [36mas[39m [33mDashboardData[39m)
[23:28:59.090]  [90m    |[39m                     [31m[1m^[22m[39m
[23:28:59.090]  [90m 74 |[39m           }
[23:28:59.090]  [90m 75 |[39m         } [36mcatch[39m (error) {
[23:28:59.090]  [90m 76 |[39m           console[33m.[39merror([32m'Failed to load real data:'[39m[33m,[39m error)[0m
[23:28:59.114] Next.js build worker exited with code: 1 and signal: null
[23:28:59.133] Error: Command "npm run build" exited with 1