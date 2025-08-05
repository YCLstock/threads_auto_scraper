[23:39:30.218] Running build in Washington, D.C., USA (East) – iad1
[23:39:30.221] Build machine configuration: 2 cores, 8 GB
[23:39:30.265] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 27ed0ba)
[23:39:30.597] Previous build caches not available
[23:39:30.852] Cloning completed: 587.000ms
[23:39:33.179] Running "vercel build"
[23:39:33.616] Vercel CLI 44.7.2
[23:39:34.190] Installing dependencies...
[23:39:47.356] 
[23:39:47.357] added 447 packages in 13s
[23:39:47.357] 
[23:39:47.357] 142 packages are looking for funding
[23:39:47.357]   run `npm fund` for details
[23:39:47.409] Running "npm run build"
[23:39:47.512] 
[23:39:47.513] > frontend-app@0.1.0 build
[23:39:47.513] > next build
[23:39:47.513] 
[23:39:48.263] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:39:48.264] This information is used to shape Next.js' roadmap and prioritize features.
[23:39:48.265] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:39:48.265] https://nextjs.org/telemetry
[23:39:48.265] 
[23:39:48.362]    ▲ Next.js 15.4.5
[23:39:48.367] 
[23:39:48.393]    Creating an optimized production build ...
[23:40:08.275]  ✓ Compiled successfully in 17.0s
[23:40:08.280]    Linting and checking validity of types ...
[23:40:15.200] Failed to compile.
[23:40:15.200] 
[23:40:15.200] ./src/components/Dashboard.tsx:281:9
[23:40:15.200] Type error: Type '{ hidden: { opacity: number; y: number; }; visible: { opacity: number; y: number; transition: { duration: number; ease: string; }; }; }' is not assignable to type 'Variants'.
[23:40:15.200]   Property 'visible' is incompatible with index signature.
[23:40:15.200]     Type '{ opacity: number; y: number; transition: { duration: number; ease: string; }; }' is not assignable to type 'Variant'.
[23:40:15.200]       Type '{ opacity: number; y: number; transition: { duration: number; ease: string; }; }' is not assignable to type 'TargetAndTransition'.
[23:40:15.201]         Type '{ opacity: number; y: number; transition: { duration: number; ease: string; }; }' is not assignable to type '{ transition?: Transition<any> | undefined; transitionEnd?: ResolvedValues | undefined; }'.
[23:40:15.201]           Types of property 'transition' are incompatible.
[23:40:15.201]             Type '{ duration: number; ease: string; }' is not assignable to type 'Transition<any> | undefined'.
[23:40:15.201]               Type '{ duration: number; ease: string; }' is not assignable to type 'TransitionWithValueOverrides<any>'.
[23:40:15.201]                 Type '{ duration: number; ease: string; }' is not assignable to type 'ValueAnimationTransition<any>'.
[23:40:15.201]                   Types of property 'ease' are incompatible.
[23:40:15.201]                     Type 'string' is not assignable to type 'Easing | Easing[] | undefined'.
[23:40:15.201] 
[23:40:15.201] [0m [90m 279 |[39m       [33m<[39m[33mmotion[39m[33m.[39msection
[23:40:15.202]  [90m 280 |[39m         key[33m=[39m{activeChart}
[23:40:15.202] [31m[1m>[22m[39m[90m 281 |[39m         variants[33m=[39m{chartContainerVariants}
[23:40:15.202]  [90m     |[39m         [31m[1m^[22m[39m
[23:40:15.202]  [90m 282 |[39m         initial[33m=[39m[32m"hidden"[39m
[23:40:15.202]  [90m 283 |[39m         animate[33m=[39m[32m"visible"[39m
[23:40:15.202]  [90m 284 |[39m         className[33m=[39m[32m"mb-8"[39m[0m
[23:40:15.222] Next.js build worker exited with code: 1 and signal: null
[23:40:15.238] Error: Command "npm run build" exited with 1