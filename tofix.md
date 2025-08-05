[23:47:16.748] Running build in Washington, D.C., USA (East) – iad1
[23:47:16.748] Build machine configuration: 2 cores, 8 GB
[23:47:16.762] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 3853595)
[23:47:16.910] Previous build caches not available
[23:47:17.056] Cloning completed: 294.000ms
[23:47:19.342] Running "vercel build"
[23:47:20.060] Vercel CLI 44.7.2
[23:47:20.782] Installing dependencies...
[23:47:36.036] 
[23:47:36.037] added 447 packages in 15s
[23:47:36.037] 
[23:47:36.038] 142 packages are looking for funding
[23:47:36.038]   run `npm fund` for details
[23:47:36.103] Running "npm run build"
[23:47:36.218] 
[23:47:36.219] > frontend-app@0.1.0 build
[23:47:36.219] > next build
[23:47:36.219] 
[23:47:37.026] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:47:37.027] This information is used to shape Next.js' roadmap and prioritize features.
[23:47:37.028] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:47:37.028] https://nextjs.org/telemetry
[23:47:37.028] 
[23:47:37.134]    ▲ Next.js 15.4.5
[23:47:37.135] 
[23:47:37.163]    Creating an optimized production build ...
[23:47:58.104]  ✓ Compiled successfully in 17.0s
[23:47:58.109]    Linting and checking validity of types ...
[23:48:05.580] Failed to compile.
[23:48:05.581] 
[23:48:05.581] ./src/components/Dashboard.tsx:314:31
[23:48:05.581] Type error: Type 'TopicTreemapData[]' is not assignable to type 'TopicData[]'.
[23:48:05.582]   Type 'TopicTreemapData' is not assignable to type 'TopicData'.
[23:48:05.582]     Types of property 'topic_id' are incompatible.
[23:48:05.582]       Type 'string' is not assignable to type 'number'.
[23:48:05.582] 
[23:48:05.582] [0m [90m 312 |[39m                   通过矩形大小和颜色展示各主题的热度分布
[23:48:05.583]  [90m 313 |[39m                 [33m<[39m[33m/[39m[33mp[39m[33m>[39m
[23:48:05.583] [31m[1m>[22m[39m[90m 314 |[39m                 [33m<[39m[33mTopicTreemap[39m data[33m=[39m{data[33m.[39mtopic_treemap_data} [33m/[39m[33m>[39m
[23:48:05.583]  [90m     |[39m                               [31m[1m^[22m[39m
[23:48:05.583]  [90m 315 |[39m               [33m<[39m[33m/[39m[33mdiv[39m[33m>[39m
[23:48:05.583]  [90m 316 |[39m             )}
[23:48:05.584]  [90m 317 |[39m           [33m<[39m[33m/[39m[33mdiv[39m[33m>[39m[0m
[23:48:05.604] Next.js build worker exited with code: 1 and signal: null
[23:48:05.621] Error: Command "npm run build" exited with 1