[00:30:39.965] Running build in Washington, D.C., USA (East) – iad1
[00:30:39.968] Build machine configuration: 2 cores, 8 GB
[00:30:40.003] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: c8efe7e)
[00:30:40.227] Previous build caches not available
[00:30:40.545] Cloning completed: 541.000ms
[00:30:43.259] Running "vercel build"
[00:30:43.712] Vercel CLI 44.7.2
[00:30:44.622] Installing dependencies...
[00:30:59.969] 
[00:30:59.970] added 447 packages in 15s
[00:30:59.970] 
[00:30:59.971] 142 packages are looking for funding
[00:30:59.971]   run `npm fund` for details
[00:31:00.262] Running "npm run build"
[00:31:00.393] 
[00:31:00.393] > frontend-app@0.1.0 build
[00:31:00.393] > next build
[00:31:00.393] 
[00:31:01.525] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[00:31:01.526] This information is used to shape Next.js' roadmap and prioritize features.
[00:31:01.526] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[00:31:01.527] https://nextjs.org/telemetry
[00:31:01.527] 
[00:31:01.630]    ▲ Next.js 15.4.5
[00:31:01.630] 
[00:31:01.656]    Creating an optimized production build ...
[00:31:22.496]  ✓ Compiled successfully in 17.0s
[00:31:22.503]    Linting and checking validity of types ...
[00:31:30.133] Failed to compile.
[00:31:30.133] 
[00:31:30.134] ./src/components/charts/TrendRiverChart.tsx:143:29
[00:31:30.134] Type error: No overload matches this call.
[00:31:30.134]   Overload 1 of 4, '(name: string, value: null): Selection<BaseType, unknown, HTMLElement, any>', gave the following error.
[00:31:30.134]     Argument of type '(path: d3.Series<{ date: Date | null; [key: string]: number | Date | null; }, string>) => 1 | 0.2' is not assignable to parameter of type 'null'.
[00:31:30.135]   Overload 2 of 4, '(name: string, value: string | number | boolean, priority?: "important" | null | undefined): Selection<BaseType, unknown, HTMLElement, any>', gave the following error.
[00:31:30.135]     Argument of type '(path: d3.Series<{ date: Date | null; [key: string]: number | Date | null; }, string>) => 1 | 0.2' is not assignable to parameter of type 'string | number | boolean'.
[00:31:30.135]   Overload 3 of 4, '(name: string, value: ValueFn<BaseType, unknown, string | number | boolean | null>, priority?: "important" | null | undefined): Selection<BaseType, unknown, HTMLElement, any>', gave the following error.
[00:31:30.136]     Argument of type '(path: d3.Series<{ date: Date | null; [key: string]: number | Date | null; }, string>) => 1 | 0.2' is not assignable to parameter of type 'ValueFn<BaseType, unknown, string | number | boolean | null>'.
[00:31:30.136]       Types of parameters 'path' and 'datum' are incompatible.
[00:31:30.136]         Type 'unknown' is not assignable to type 'Series<{ [key: string]: number | Date | null; date: Date | null; }, string>'.
[00:31:30.136] 
[00:31:30.136] [0m [90m 141 |[39m         [90m// 高亮当前路径[39m
[00:31:30.137]  [90m 142 |[39m         d3[33m.[39mselectAll([32m'.river-path'[39m)
[00:31:30.137] [31m[1m>[22m[39m[90m 143 |[39m           [33m.[39mstyle([32m'opacity'[39m[33m,[39m (path[33m:[39m d3[33m.[39m[33mSeries[39m[33m<[39m{ date[33m:[39m [33mDate[39m [33m|[39m [36mnull[39m[33m;[39m [key[33m:[39m string][33m:[39m number [33m|[39m [33mDate[39m [33m|[39m [36mnull[39m[33m;[39m }[33m,[39m string[33m>[39m) [33m=>[39m path[33m.[39mkey [33m===[39m keyword[33m.[39mkeyword [33m?[39m [35m1[39m [33m:[39m [35m0.2[39m)
[00:31:30.137]  [90m     |[39m                             [31m[1m^[22m[39m
[00:31:30.137]  [90m 144 |[39m       })
[00:31:30.137]  [90m 145 |[39m       [33m.[39mon([32m'mouseleave'[39m[33m,[39m [36mfunction[39m() {
[00:31:30.137]  [90m 146 |[39m         setSelectedKeyword([36mnull[39m)[0m
[00:31:30.160] Next.js build worker exited with code: 1 and signal: null
[00:31:30.179] Error: Command "npm run build" exited with 1