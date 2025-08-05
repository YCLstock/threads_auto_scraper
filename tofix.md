[00:42:43.325] Running build in Washington, D.C., USA (East) – iad1
[00:42:43.325] Build machine configuration: 2 cores, 8 GB
[00:42:43.370] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 0823364)
[00:42:43.685] Previous build caches not available
[00:42:43.933] Cloning completed: 563.000ms
[00:42:46.652] Running "vercel build"
[00:42:47.254] Vercel CLI 44.7.2
[00:42:47.834] Installing dependencies...
[00:43:02.218] 
[00:43:02.218] added 447 packages in 14s
[00:43:02.219] 
[00:43:02.219] 142 packages are looking for funding
[00:43:02.219]   run `npm fund` for details
[00:43:02.513] Running "npm run build"
[00:43:02.635] 
[00:43:02.635] > frontend-app@0.1.0 build
[00:43:02.635] > next build
[00:43:02.635] 
[00:43:03.965] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[00:43:03.966] This information is used to shape Next.js' roadmap and prioritize features.
[00:43:03.966] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[00:43:03.967] https://nextjs.org/telemetry
[00:43:03.967] 
[00:43:04.066]    ▲ Next.js 15.4.5
[00:43:04.067] 
[00:43:04.092]    Creating an optimized production build ...
[00:43:23.923]  ✓ Compiled successfully in 16.0s
[00:43:23.929]    Linting and checking validity of types ...
[00:43:31.336] Failed to compile.
[00:43:31.336] 
[00:43:31.338] ./src/components/charts/TrendRiverChart.tsx:147:29
[00:43:31.338] Type error: No overload matches this call.
[00:43:31.338]   Overload 1 of 4, '(name: string, value: null): Selection<BaseType, unknown, HTMLElement, any>', gave the following error.
[00:43:31.338]     Argument of type '(path: RiverPath) => 1 | 0.2' is not assignable to parameter of type 'null'.
[00:43:31.339]   Overload 2 of 4, '(name: string, value: string | number | boolean, priority?: "important" | null | undefined): Selection<BaseType, unknown, HTMLElement, any>', gave the following error.
[00:43:31.339]     Argument of type '(path: RiverPath) => 1 | 0.2' is not assignable to parameter of type 'string | number | boolean'.
[00:43:31.339]   Overload 3 of 4, '(name: string, value: ValueFn<BaseType, unknown, string | number | boolean | null>, priority?: "important" | null | undefined): Selection<BaseType, unknown, HTMLElement, any>', gave the following error.
[00:43:31.339]     Argument of type '(path: RiverPath) => 1 | 0.2' is not assignable to parameter of type 'ValueFn<BaseType, unknown, string | number | boolean | null>'.
[00:43:31.339]       Types of parameters 'path' and 'datum' are incompatible.
[00:43:31.339]         Type 'unknown' is not assignable to type 'RiverPath'.
[00:43:31.340] 
[00:43:31.340] [0m [90m 145 |[39m         [90m// 高亮当前路径[39m
[00:43:31.340]  [90m 146 |[39m         d3[33m.[39mselectAll([32m'.river-path'[39m)
[00:43:31.340] [31m[1m>[22m[39m[90m 147 |[39m           [33m.[39mstyle([32m'opacity'[39m[33m,[39m (path[33m:[39m [33mRiverPath[39m) [33m=>[39m path[33m.[39mkey [33m===[39m keyword[33m.[39mkeyword [33m?[39m [35m1[39m [33m:[39m [35m0.2[39m)
[00:43:31.340]  [90m     |[39m                             [31m[1m^[22m[39m
[00:43:31.340]  [90m 148 |[39m       })
[00:43:31.340]  [90m 149 |[39m       [33m.[39mon([32m'mouseleave'[39m[33m,[39m [36mfunction[39m() {
[00:43:31.340]  [90m 150 |[39m         setSelectedKeyword([36mnull[39m)[0m
[00:43:31.361] Next.js build worker exited with code: 1 and signal: null
[00:43:31.379] Error: Command "npm run build" exited with 1