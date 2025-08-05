[23:42:37.511] Running build in Washington, D.C., USA (East) – iad1
[23:42:37.511] Build machine configuration: 2 cores, 8 GB
[23:42:37.524] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: 5f8fe35)
[23:42:37.653] Previous build caches not available
[23:42:37.795] Cloning completed: 271.000ms
[23:42:40.352] Running "vercel build"
[23:42:40.797] Vercel CLI 44.7.2
[23:42:41.382] Installing dependencies...
[23:42:56.061] 
[23:42:56.062] added 447 packages in 14s
[23:42:56.062] 
[23:42:56.062] 142 packages are looking for funding
[23:42:56.063]   run `npm fund` for details
[23:42:56.241] Running "npm run build"
[23:42:56.368] 
[23:42:56.369] > frontend-app@0.1.0 build
[23:42:56.369] > next build
[23:42:56.369] 
[23:42:57.839] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[23:42:57.840] This information is used to shape Next.js' roadmap and prioritize features.
[23:42:57.840] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[23:42:57.850] https://nextjs.org/telemetry
[23:42:57.851] 
[23:42:58.046]    ▲ Next.js 15.4.5
[23:42:58.046] 
[23:42:58.116]    Creating an optimized production build ...
[23:43:19.743]  ✓ Compiled successfully in 17.0s
[23:43:19.749]    Linting and checking validity of types ...
[23:43:27.392] Failed to compile.
[23:43:27.393] 
[23:43:27.393] ./src/components/Dashboard.tsx:281:9
[23:43:27.393] Type error: Type '{ hidden: { opacity: number; y: number; }; visible: { opacity: number; y: number; transition: { duration: number; ease: number[]; }; }; }' is not assignable to type 'Variants'.
[23:43:27.393]   Property 'visible' is incompatible with index signature.
[23:43:27.393]     Type '{ opacity: number; y: number; transition: { duration: number; ease: number[]; }; }' is not assignable to type 'Variant'.
[23:43:27.393]       Type '{ opacity: number; y: number; transition: { duration: number; ease: number[]; }; }' is not assignable to type 'TargetAndTransition'.
[23:43:27.393]         Type '{ opacity: number; y: number; transition: { duration: number; ease: number[]; }; }' is not assignable to type '{ transition?: Transition<any> | undefined; transitionEnd?: ResolvedValues | undefined; }'.
[23:43:27.394]           Types of property 'transition' are incompatible.
[23:43:27.394]             Type '{ duration: number; ease: number[]; }' is not assignable to type 'Transition<any> | undefined'.
[23:43:27.394]               Type '{ duration: number; ease: number[]; }' is not assignable to type 'TransitionWithValueOverrides<any>'.
[23:43:27.394]                 Type '{ duration: number; ease: number[]; }' is not assignable to type 'ValueAnimationTransition<any>'.
[23:43:27.394]                   Types of property 'ease' are incompatible.
[23:43:27.394]                     Type 'number[]' is not assignable to type 'Easing | Easing[] | undefined'.
[23:43:27.394]                       Type 'number[]' is not assignable to type 'EasingFunction | Easing[]'.
[23:43:27.394]                         Type 'number[]' is not assignable to type 'Easing[]'.
[23:43:27.395]                           Type 'number' is not assignable to type 'Easing'.
[23:43:27.395] 
[23:43:27.395] [0m [90m 279 |[39m       [33m<[39m[33mmotion[39m[33m.[39msection
[23:43:27.395]  [90m 280 |[39m         key[33m=[39m{activeChart}
[23:43:27.395] [31m[1m>[22m[39m[90m 281 |[39m         variants[33m=[39m{chartContainerVariants}
[23:43:27.395]  [90m     |[39m         [31m[1m^[22m[39m
[23:43:27.395]  [90m 282 |[39m         initial[33m=[39m[32m"hidden"[39m
[23:43:27.395]  [90m 283 |[39m         animate[33m=[39m[32m"visible"[39m
[23:43:27.395]  [90m 284 |[39m         className[33m=[39m[32m"mb-8"[39m[0m
[23:43:27.417] Next.js build worker exited with code: 1 and signal: null
[23:43:27.435] Error: Command "npm run build" exited with 1