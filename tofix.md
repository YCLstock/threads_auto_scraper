[00:51:43.517] Running build in Washington, D.C., USA (East) – iad1
[00:51:43.517] Build machine configuration: 2 cores, 8 GB
[00:51:43.533] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: d2988a6)
[00:51:43.693] Previous build caches not available
[00:51:43.838] Cloning completed: 304.000ms
[00:51:47.405] Running "vercel build"
[00:51:47.957] Vercel CLI 44.7.2
[00:51:48.560] Installing dependencies...
[00:52:03.523] 
[00:52:03.524] added 447 packages in 15s
[00:52:03.524] 
[00:52:03.524] 142 packages are looking for funding
[00:52:03.525]   run `npm fund` for details
[00:52:03.788] Running "npm run build"
[00:52:03.923] 
[00:52:03.923] > frontend-app@0.1.0 build
[00:52:03.924] > next build
[00:52:03.924] 
[00:52:05.299] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[00:52:05.300] This information is used to shape Next.js' roadmap and prioritize features.
[00:52:05.301] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[00:52:05.301] https://nextjs.org/telemetry
[00:52:05.301] 
[00:52:05.504]    ▲ Next.js 15.4.5
[00:52:05.504] 
[00:52:05.594]    Creating an optimized production build ...
[00:52:26.576]  ✓ Compiled successfully in 17.0s
[00:52:26.583]    Linting and checking validity of types ...
[00:52:33.993] Failed to compile.
[00:52:33.994] 
[00:52:33.994] ./src/components/charts/TrendRiverChart.tsx:160:19
[00:52:33.994] Type error: No overload matches this call.
[00:52:33.994]   Overload 1 of 3, '(format: null): Axis<Date | NumberValue>', gave the following error.
[00:52:33.994]     Argument of type '(date: Date) => string' is not assignable to parameter of type 'null'.
[00:52:33.994]   Overload 2 of 3, '(format: (domainValue: Date | NumberValue, index: number) => string): Axis<Date | NumberValue>', gave the following error.
[00:52:33.994]     Argument of type '(date: Date) => string' is not assignable to parameter of type '(domainValue: Date | NumberValue, index: number) => string'.
[00:52:33.995]       Types of parameters 'date' and 'domainValue' are incompatible.
[00:52:33.995]         Type 'Date | NumberValue' is not assignable to type 'Date'.
[00:52:33.995]           Type 'number' is not assignable to type 'Date'.
[00:52:33.995] 
[00:52:33.995] [0m [90m 158 |[39m     [90m// 创建坐标轴[39m
[00:52:33.995]  [90m 159 |[39m     [36mconst[39m xAxis [33m=[39m d3[33m.[39maxisBottom(xScale)
[00:52:33.995] [31m[1m>[22m[39m[90m 160 |[39m       [33m.[39mtickFormat(formatDate)
[00:52:33.995]  [90m     |[39m                   [31m[1m^[22m[39m
[00:52:33.996]  [90m 161 |[39m       [33m.[39mticks(d3[33m.[39mtimeDay[33m.[39mevery([35m1[39m))
[00:52:33.996]  [90m 162 |[39m
[00:52:33.996]  [90m 163 |[39m     [36mconst[39m yAxis [33m=[39m d3[33m.[39maxisLeft(yScale)[0m
[00:52:34.017] Next.js build worker exited with code: 1 and signal: null
[00:52:34.062] Error: Command "npm run build" exited with 1