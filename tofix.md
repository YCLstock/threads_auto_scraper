[23:58:54.895] Running build in Washington, D.C., USA (East) – iad1
[23:58:54.895] Build machine configuration: 2 cores, 8 GB
[23:58:54.914] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 473efc8)
[23:58:55.078] Previous build caches not available
[23:58:55.214] Cloning completed: 298.000ms
[23:58:57.598] Running "vercel build"
[23:58:58.036] Vercel CLI 44.7.2
[23:58:58.580] Installing dependencies...
[23:59:11.161] 
[23:59:11.161] added 447 packages in 12s
[23:59:11.162] 
[23:59:11.162] 142 packages are looking for funding
[23:59:11.162]   run `npm fund` for details
[23:59:11.208] Running "npm run build"
[23:59:11.309] 
[23:59:11.310] > frontend-app@0.1.0 build
[23:59:11.310] > next build
[23:59:11.310] 
[23:59:12.033] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:59:12.034] This information is used to shape Next.js' roadmap and prioritize features.
[23:59:12.034] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:59:12.035] https://nextjs.org/telemetry
[23:59:12.035] 
[23:59:12.136]    ▲ Next.js 15.4.5
[23:59:12.137] 
[23:59:12.160]    Creating an optimized production build ...
[23:59:30.933]  ✓ Compiled successfully in 15.0s
[23:59:30.936]    Linting and checking validity of types ...
[23:59:37.497] Failed to compile.
[23:59:37.497] 
[23:59:37.497] ./src/components/charts/TopicTreemap.tsx:101:46
[23:59:37.497] Type error: Property 'x0' does not exist on type 'HierarchyNode<HierarchyData>'.
[23:59:37.497] 
[23:59:37.497] [0m [90m  99 |[39m       [33m.[39mappend([32m'g'[39m)
[23:59:37.497]  [90m 100 |[39m       [33m.[39mattr([32m'class'[39m[33m,[39m [32m'cell'[39m)
[23:59:37.498] [31m[1m>[22m[39m[90m 101 |[39m       [33m.[39mattr([32m'transform'[39m[33m,[39m d [33m=>[39m [32m`translate(${d.x0},${d.y0})`[39m)
[23:59:37.498]  [90m     |[39m                                              [31m[1m^[22m[39m
[23:59:37.498]  [90m 102 |[39m       [33m.[39mstyle([32m'cursor'[39m[33m,[39m [32m'pointer'[39m)
[23:59:37.498]  [90m 103 |[39m
[23:59:37.498]  [90m 104 |[39m     [90m// 主矩形[39m[0m
[23:59:37.519] Next.js build worker exited with code: 1 and signal: null
[23:59:37.534] Error: Command "npm run build" exited with 1