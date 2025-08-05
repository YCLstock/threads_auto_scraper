[23:18:46.422] Running build in Washington, D.C., USA (East) – iad1
[23:18:46.423] Build machine configuration: 2 cores, 8 GB
[23:18:46.470] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 85d37a8)
[23:18:46.832] Previous build caches not available
[23:18:47.176] Cloning completed: 705.000ms
[23:18:50.330] Running "vercel build"
[23:18:50.820] Vercel CLI 44.7.2
[23:18:51.465] Installing dependencies...
[23:19:06.451] 
[23:19:06.458] added 447 packages in 15s
[23:19:06.458] 
[23:19:06.458] 142 packages are looking for funding
[23:19:06.459]   run `npm fund` for details
[23:19:06.717] Running "npm run build"
[23:19:06.962] 
[23:19:06.963] > frontend-app@0.1.0 build
[23:19:06.963] > next build
[23:19:06.963] 
[23:19:07.919] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:19:07.920] This information is used to shape Next.js' roadmap and prioritize features.
[23:19:07.920] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:19:07.921] https://nextjs.org/telemetry
[23:19:07.921] 
[23:19:08.027]    ▲ Next.js 15.4.5
[23:19:08.029] 
[23:19:08.060]    Creating an optimized production build ...
[23:19:28.546]  ✓ Compiled successfully in 17.0s
[23:19:28.552]    Linting and checking validity of types ...
[23:19:36.416] Failed to compile.
[23:19:36.417] 
[23:19:36.417] ./src/components/Dashboard.tsx:63:15
[23:19:36.417] Type error: Type '{ top_trending_topics: never[]; top_users: never[]; total_posts: number; total_interactions: number; active_topics: number; trending_keywords: number; total_users: number; data_range: { start_date: any; end_date: any; }; last_updated: string; } | { ...; }' is not assignable to type 'DashboardStats & { top_trending_topics: { name: string; growth_rate: number; posts_today: number; }[]; top_users: { username: string; total_interactions: number; posts_count: number; }[]; }'.
[23:19:36.417]   Type '{ top_trending_topics: never[]; top_users: never[]; total_posts: number; total_interactions: number; active_topics: number; trending_keywords: number; last_updated: string; total_users?: undefined; data_range?: undefined; }' is not assignable to type 'DashboardStats & { top_trending_topics: { name: string; growth_rate: number; posts_today: number; }[]; top_users: { username: string; total_interactions: number; posts_count: number; }[]; }'.
[23:19:36.417]     Type '{ top_trending_topics: never[]; top_users: never[]; total_posts: number; total_interactions: number; active_topics: number; trending_keywords: number; last_updated: string; total_users?: undefined; data_range?: undefined; }' is not assignable to type 'DashboardStats'.
[23:19:36.418]       Types of property 'total_users' are incompatible.
[23:19:36.418]         Type 'undefined' is not assignable to type 'number'.
[23:19:36.418] 
[23:19:36.418] [0m [90m 61 |[39m               keyword_trends_data[33m:[39m trendsData[33m,[39m
[23:19:36.418]  [90m 62 |[39m               topic_treemap_data[33m:[39m topicsData[33m,[39m
[23:19:36.418] [31m[1m>[22m[39m[90m 63 |[39m               dashboard_stats[33m:[39m {
[23:19:36.418]  [90m    |[39m               [31m[1m^[22m[39m
[23:19:36.418]  [90m 64 |[39m                 [33m...[39mstatsData[33m,[39m
[23:19:36.418]  [90m 65 |[39m                 top_trending_topics[33m:[39m [][33m,[39m [90m// Placeholder, as getDashboardStats doesn't return this[39m
[23:19:36.418]  [90m 66 |[39m                 top_users[33m:[39m [][33m,[39m [90m// Placeholder, as getDashboardStats doesn't return this[39m[0m
[23:19:36.440] Next.js build worker exited with code: 1 and signal: null
[23:19:36.459] Error: Command "npm run build" exited with 1