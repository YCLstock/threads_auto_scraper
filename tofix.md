[22:33:42.415] Running build in Washington, D.C., USA (East) – iad1
[22:33:42.415] Build machine configuration: 2 cores, 8 GB
[22:33:42.427] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: de16013)
[22:33:42.575] Previous build caches not available
[22:33:42.779] Cloning completed: 352.000ms
[22:33:45.172] Running "vercel build"
[22:33:45.617] Vercel CLI 44.7.2
[22:33:46.345] Installing dependencies...
[22:34:01.228] 
[22:34:01.229] added 447 packages in 15s
[22:34:01.231] 
[22:34:01.231] 142 packages are looking for funding
[22:34:01.231]   run `npm fund` for details
[22:34:01.393] Running "npm run build"
[22:34:01.532] 
[22:34:01.532] > frontend-app@0.1.0 build
[22:34:01.533] > next build
[22:34:01.533] 
[22:34:02.424] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[22:34:02.425] This information is used to shape Next.js' roadmap and prioritize features.
[22:34:02.425] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[22:34:02.425] https://nextjs.org/telemetry
[22:34:02.425] 
[22:34:02.534]    ▲ Next.js 15.4.5
[22:34:02.535] 
[22:34:02.598]    Creating an optimized production build ...
[22:34:22.976]  ✓ Compiled successfully in 17.0s
[22:34:22.981]    Linting and checking validity of types ...
[22:34:27.389] 
[22:34:27.389] Failed to compile.
[22:34:27.390] 
[22:34:27.390] ./src/components/Dashboard.tsx
[22:34:27.390] 28:21  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.390] 29:24  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.390] 30:23  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.390] 73:20  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.391] 77:45  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.391] 
[22:34:27.391] ./src/components/charts/HeatBubbleChart.tsx
[22:34:27.391] 82:56  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.392] 158:32  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.392] 
[22:34:27.392] ./src/components/charts/TrendRiverChart.tsx
[22:34:27.392] 79:44  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.392] 118:26  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.393] 148:36  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.393] 238:36  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.393] 330:75  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.393] 334:31  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.393] 336:48  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.394] 340:38  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.394] 340:74  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.394] 342:31  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.394] 344:40  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.395] 347:31  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.395] 349:41  Error: Unexpected any. Specify a different type.  @typescript-eslint/no-explicit-any
[22:34:27.395] 
[22:34:27.395] ./src/lib/api.ts
[22:34:27.395] 183:19  Warning: '_data' is assigned a value but never used.  @typescript-eslint/no-unused-vars
[22:34:27.396] 
[22:34:27.396] info  - Need to disable some ESLint rules? Learn more here: https://nextjs.org/docs/app/api-reference/config/eslint#disabling-rules
[22:34:27.453] Error: Command "npm run build" exited with 1