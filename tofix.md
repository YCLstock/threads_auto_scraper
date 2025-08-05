[23:49:55.024] Running build in Washington, D.C., USA (East) – iad1
[23:49:55.026] Build machine configuration: 2 cores, 8 GB
[23:49:55.069] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: e497f33)
[23:49:55.330] Previous build caches not available
[23:49:55.611] Cloning completed: 541.000ms
[23:49:59.433] Running "vercel build"
[23:49:59.892] Vercel CLI 44.7.2
[23:50:00.466] Installing dependencies...
[23:50:14.615] 
[23:50:14.615] added 447 packages in 14s
[23:50:14.616] 
[23:50:14.616] 142 packages are looking for funding
[23:50:14.616]   run `npm fund` for details
[23:50:14.902] Running "npm run build"
[23:50:15.040] 
[23:50:15.041] > frontend-app@0.1.0 build
[23:50:15.041] > next build
[23:50:15.041] 
[23:50:15.815] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:50:15.816] This information is used to shape Next.js' roadmap and prioritize features.
[23:50:15.816] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:50:15.816] https://nextjs.org/telemetry
[23:50:15.816] 
[23:50:15.924]    ▲ Next.js 15.4.5
[23:50:15.925] 
[23:50:15.958]    Creating an optimized production build ...
[23:50:35.939]  ✓ Compiled successfully in 16.0s
[23:50:35.944]    Linting and checking validity of types ...
[23:50:43.147] Failed to compile.
[23:50:43.148] 
[23:50:43.149] ./src/components/charts/HeatBubbleChart.tsx:74:52
[23:50:43.149] Type error: Argument of type '(d: BubbleData) => number' is not assignable to parameter of type 'number | ((node: SimulationNodeDatum, i: number, nodes: SimulationNodeDatum[]) => number)'.
[23:50:43.149]   Type '(d: BubbleData) => number' is not assignable to type '(node: SimulationNodeDatum, i: number, nodes: SimulationNodeDatum[]) => number'.
[23:50:43.149]     Types of parameters 'd' and 'node' are incompatible.
[23:50:43.149]       Type 'SimulationNodeDatum' is missing the following properties from type 'BubbleData': post_id, username, content, timestamp, and 6 more.
[23:50:43.149] 
[23:50:43.149] [0m [90m 72 |[39m       [33m.[39mforce([32m'charge'[39m[33m,[39m d3[33m.[39mforceManyBody()[33m.[39mstrength([33m-[39m[35m50[39m))
[23:50:43.149]  [90m 73 |[39m       [33m.[39mforce([32m'center'[39m[33m,[39m d3[33m.[39mforceCenter(width [33m/[39m [35m2[39m[33m,[39m height [33m/[39m [35m2[39m))
[23:50:43.150] [31m[1m>[22m[39m[90m 74 |[39m       [33m.[39mforce([32m'collision'[39m[33m,[39m d3[33m.[39mforceCollide()[33m.[39mradius((d[33m:[39m [33mBubbleData[39m) [33m=>[39m radiusScale(d[33m.[39mtotal_interactions) [33m+[39m [35m2[39m))
[23:50:43.150]  [90m    |[39m                                                    [31m[1m^[22m[39m
[23:50:43.150]  [90m 75 |[39m       [33m.[39mforce([32m'x'[39m[33m,[39m d3[33m.[39mforceX(width [33m/[39m [35m2[39m)[33m.[39mstrength([35m0.1[39m))
[23:50:43.150]  [90m 76 |[39m       [33m.[39mforce([32m'y'[39m[33m,[39m d3[33m.[39mforceY(height [33m/[39m [35m2[39m)[33m.[39mstrength([35m0.1[39m))
[23:50:43.150]  [90m 77 |[39m[0m
[23:50:43.169] Next.js build worker exited with code: 1 and signal: null
[23:50:43.185] Error: Command "npm run build" exited with 1