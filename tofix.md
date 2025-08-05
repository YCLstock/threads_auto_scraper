[23:31:06.979] Running build in Washington, D.C., USA (East) – iad1
[23:31:06.979] Build machine configuration: 2 cores, 8 GB
[23:31:07.004] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: d1b4f61)
[23:31:07.152] Previous build caches not available
[23:31:07.311] Cloning completed: 307.000ms
[23:31:09.700] Running "vercel build"
[23:31:10.202] Vercel CLI 44.7.2
[23:31:10.802] Installing dependencies...
[23:31:25.845] 
[23:31:25.846] added 447 packages in 15s
[23:31:25.846] 
[23:31:25.847] 142 packages are looking for funding
[23:31:25.847]   run `npm fund` for details
[23:31:25.912] Running "npm run build"
[23:31:26.022] 
[23:31:26.023] > frontend-app@0.1.0 build
[23:31:26.023] > next build
[23:31:26.024] 
[23:31:26.856] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:31:26.857] This information is used to shape Next.js' roadmap and prioritize features.
[23:31:26.857] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:31:26.857] https://nextjs.org/telemetry
[23:31:26.857] 
[23:31:26.963]    ▲ Next.js 15.4.5
[23:31:26.963] 
[23:31:26.981]    Creating an optimized production build ...
[23:31:47.156]  ✓ Compiled successfully in 17.0s
[23:31:47.161]    Linting and checking validity of types ...
[23:31:54.561] Failed to compile.
[23:31:54.561] 
[23:31:54.562] ./src/components/Dashboard.tsx:73:21
[23:31:54.562] Type error: Conversion of type '{ metadata: { generated_at: string; data_range: { start_date: string; end_date: string; }; total_posts: number; total_users: number; total_interactions: number; }; heat_bubble_data: { post_id: string; ... 12 more ...; color: string; }[]; keyword_trends_data: { ...; }[]; topic_treemap_data: { ...; }[]; dashboard_stat...' to type 'DashboardData' may be a mistake because neither type sufficiently overlaps with the other. If this was intentional, convert the expression to 'unknown' first.
[23:31:54.563]   Types of property 'dashboard_stats' are incompatible.
[23:31:54.564]     Type '{ top_trending_topics: { name: string; growth_rate: number; posts_today: number; }[]; top_users: { username: string; total_interactions: number; posts_count: number; avg_engagement: number; }[]; engagement_summary: { ...; }; time_analysis: { ...; }; }' is not comparable to type 'DashboardStats & { top_trending_topics: { name: string; growth_rate: number; posts_today: number; }[]; top_users: { username: string; total_interactions: number; posts_count: number; }[]; }'.
[23:31:54.565]       Type '{ top_trending_topics: { name: string; growth_rate: number; posts_today: number; }[]; top_users: { username: string; total_interactions: number; posts_count: number; avg_engagement: number; }[]; engagement_summary: { ...; }; time_analysis: { ...; }; }' is missing the following properties from type 'DashboardStats': total_posts, total_interactions, active_topics, trending_keywords, and 3 more.
[23:31:54.565] 
[23:31:54.565] [0m [90m 71 |[39m             console[33m.[39mwarn([32m'Database connection failed, falling back to mock data'[39m)
[23:31:54.565]  [90m 72 |[39m             setUseRealData([36mfalse[39m)
[23:31:54.565] [31m[1m>[22m[39m[90m 73 |[39m             setData(mockData [36mas[39m [33mDashboardData[39m)
[23:31:54.565]  [90m    |[39m                     [31m[1m^[22m[39m
[23:31:54.565]  [90m 74 |[39m           }
[23:31:54.565]  [90m 75 |[39m         } [36mcatch[39m (error) {
[23:31:54.565]  [90m 76 |[39m           console[33m.[39merror([32m'Failed to load real data:'[39m[33m,[39m error)[0m
[23:31:54.586] Next.js build worker exited with code: 1 and signal: null
[23:31:54.603] Error: Command "npm run build" exited with 1