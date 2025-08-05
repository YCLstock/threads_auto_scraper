[23:45:16.281] Running build in Washington, D.C., USA (East) – iad1
[23:45:16.281] Build machine configuration: 2 cores, 8 GB
[23:45:16.295] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 2411b14)
[23:45:16.423] Previous build caches not available
[23:45:16.793] Cloning completed: 498.000ms
[23:45:19.105] Running "vercel build"
[23:45:19.587] Vercel CLI 44.7.2
[23:45:20.226] Installing dependencies...
[23:45:34.244] 
[23:45:34.245] added 447 packages in 14s
[23:45:34.245] 
[23:45:34.245] 142 packages are looking for funding
[23:45:34.246]   run `npm fund` for details
[23:45:34.309] Running "npm run build"
[23:45:34.455] 
[23:45:34.456] > frontend-app@0.1.0 build
[23:45:34.456] > next build
[23:45:34.456] 
[23:45:35.255] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:45:35.256] This information is used to shape Next.js' roadmap and prioritize features.
[23:45:35.257] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:45:35.257] https://nextjs.org/telemetry
[23:45:35.257] 
[23:45:35.360]    ▲ Next.js 15.4.5
[23:45:35.362] 
[23:45:35.396]    Creating an optimized production build ...
[23:45:56.708]  ✓ Compiled successfully in 17.0s
[23:45:56.715]    Linting and checking validity of types ...
[23:46:04.018] Failed to compile.
[23:46:04.018] 
[23:46:04.019] ./src/components/Dashboard.tsx:281:9
[23:46:04.019] Type error: Type '{ hidden: { opacity: number; y: number; }; visible: { opacity: number; y: number; transition: { duration: number; ease: string; }; }; }' is not assignable to type 'Variants'.
[23:46:04.019]   Property 'visible' is incompatible with index signature.
[23:46:04.019]     Type '{ opacity: number; y: number; transition: { duration: number; ease: string; }; }' is not assignable to type 'Variant'.
[23:46:04.020]       Type '{ opacity: number; y: number; transition: { duration: number; ease: string; }; }' is not assignable to type 'TargetAndTransition'.
[23:46:04.020]         Type '{ opacity: number; y: number; transition: { duration: number; ease: string; }; }' is not assignable to type '{ transition?: Transition<any> | undefined; transitionEnd?: ResolvedValues | undefined; }'.
[23:46:04.020]           Types of property 'transition' are incompatible.
[23:46:04.021]             Type '{ duration: number; ease: string; }' is not assignable to type 'Transition<any> | undefined'.
[23:46:04.021]               Type '{ duration: number; ease: string; }' is not assignable to type 'TransitionWithValueOverrides<any>'.
[23:46:04.021]                 Type '{ duration: number; ease: string; }' is not assignable to type 'ValueAnimationTransition<any>'.
[23:46:04.021]                   Types of property 'ease' are incompatible.
[23:46:04.021]                     Type 'string' is not assignable to type 'Easing | Easing[] | undefined'.
[23:46:04.021] 
[23:46:04.022] [0m [90m 279 |[39m       [33m<[39m[33mmotion[39m[33m.[39msection
[23:46:04.022]  [90m 280 |[39m         key[33m=[39m{activeChart}
[23:46:04.022] [31m[1m>[22m[39m[90m 281 |[39m         variants[33m=[39m{chartContainerVariants}
[23:46:04.022]  [90m     |[39m         [31m[1m^[22m[39m
[23:46:04.022]  [90m 282 |[39m         initial[33m=[39m[32m"hidden"[39m
[23:46:04.022]  [90m 283 |[39m         animate[33m=[39m[32m"visible"[39m
[23:46:04.022]  [90m 284 |[39m         className[33m=[39m[32m"mb-8"[39m[0m
[23:46:04.042] Next.js build worker exited with code: 1 and signal: null
[23:46:04.059] Error: Command "npm run build" exited with 1