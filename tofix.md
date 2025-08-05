[00:23:57.978] Running build in Washington, D.C., USA (East) – iad1
[00:23:57.978] Build machine configuration: 2 cores, 8 GB
[00:23:58.000] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 62a7a58)
[00:23:58.161] Previous build caches not available
[00:23:58.318] Cloning completed: 318.000ms
[00:24:00.700] Running "vercel build"
[00:24:01.143] Vercel CLI 44.7.2
[00:24:01.762] Installing dependencies...
[00:24:16.296] 
[00:24:16.297] added 447 packages in 14s
[00:24:16.297] 
[00:24:16.297] 142 packages are looking for funding
[00:24:16.297]   run `npm fund` for details
[00:24:16.418] Running "npm run build"
[00:24:16.660] 
[00:24:16.660] > frontend-app@0.1.0 build
[00:24:16.661] > next build
[00:24:16.661] 
[00:24:17.865] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[00:24:17.866] This information is used to shape Next.js' roadmap and prioritize features.
[00:24:17.866] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[00:24:17.866] https://nextjs.org/telemetry
[00:24:17.866] 
[00:24:17.973]    ▲ Next.js 15.4.5
[00:24:17.974] 
[00:24:18.000]    Creating an optimized production build ...
[00:24:38.029]  ✓ Compiled successfully in 16.0s
[00:24:38.035]    Linting and checking validity of types ...
[00:24:45.380] Failed to compile.
[00:24:45.381] 
[00:24:45.381] ./src/components/charts/TopicTreemap.tsx:257:25
[00:24:45.382] Type error: No overload matches this call.
[00:24:45.382]   Overload 1 of 3, '(typenames: string, listener: null): Selection<SVGGElement, HierarchyNode<HierarchyData>, SVGSVGElement | null, unknown>', gave the following error.
[00:24:45.382]     Argument of type '(this: SVGGElement, event: any, d: TreemapNode) => void' is not assignable to parameter of type 'null'.
[00:24:45.382]   Overload 2 of 3, '(typenames: string, listener: (this: SVGGElement, event: any, d: HierarchyNode<HierarchyData>) => void, options?: any): Selection<SVGGElement, HierarchyNode<...>, SVGSVGElement | null, unknown>', gave the following error.
[00:24:45.382]     Argument of type '(this: SVGGElement, event: any, d: TreemapNode) => void' is not assignable to parameter of type '(this: SVGGElement, event: any, d: HierarchyNode<HierarchyData>) => void'.
[00:24:45.383]       Types of parameters 'd' and 'd' are incompatible.
[00:24:45.383]         Type 'HierarchyNode<HierarchyData>' is missing the following properties from type 'TreemapNode': x0, y0, x1, y1
[00:24:45.383] 
[00:24:45.383] [0m [90m 255 |[39m     [90m// 鼠标事件处理[39m
[00:24:45.383]  [90m 256 |[39m     cells
[00:24:45.384] [31m[1m>[22m[39m[90m 257 |[39m       [33m.[39mon([32m'mouseenter'[39m[33m,[39m [36mfunction[39m(event[33m,[39m d[33m:[39m [33mTreemapNode[39m) {
[00:24:45.384]  [90m     |[39m                         [31m[1m^[22m[39m
[00:24:45.384]  [90m 258 |[39m         [36mconst[39m [x[33m,[39m y] [33m=[39m d3[33m.[39mpointer(event[33m,[39m document[33m.[39mbody)
[00:24:45.384]  [90m 259 |[39m         
[00:24:45.384]  [90m 260 |[39m         d3[33m.[39mselect([36mthis[39m)[33m.[39mselect([32m'rect'[39m)[0m
[00:24:45.406] Next.js build worker exited with code: 1 and signal: null
[00:24:45.424] Error: Command "npm run build" exited with 1