[21:34:19.834] Running build in Washington, D.C., USA (East) – iad1
[21:34:19.834] Build machine configuration: 2 cores, 8 GB
[21:34:19.882] Cloning github.com/YCLstock/threads_auto_scraper (Branch: master, Commit: a8429a7)
[21:34:20.016] Previous build caches not available
[21:34:20.239] Cloning completed: 356.000ms
[21:34:22.660] Running "vercel build"
[21:34:23.108] Vercel CLI 44.7.2
[21:34:23.957] Installing dependencies...
[21:34:38.858] 
[21:34:38.858] added 447 packages in 15s
[21:34:38.859] 
[21:34:38.859] 142 packages are looking for funding
[21:34:38.859]   run `npm fund` for details
[21:34:39.105] Running "npm run build"
[21:34:39.251] 
[21:34:39.252] > frontend-app@0.1.0 build
[21:34:39.252] > next build
[21:34:39.253] 
[21:34:40.502] Attention: Next.js now collects completely anonymous telemetry regarding usage.
[21:34:40.503] This information is used to shape Next.js' roadmap and prioritize features.
[21:34:40.503] You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
[21:34:40.503] https://nextjs.org/telemetry
[21:34:40.503] 
[21:34:40.608]    ▲ Next.js 15.4.5
[21:34:40.609] 
[21:34:40.623]    Creating an optimized production build ...
[21:34:50.579] Failed to compile.
[21:34:50.579] 
[21:34:50.579] ./src/components/charts/TopicTreemap.tsx
[21:34:50.579] Module parse failed: Identifier 'useEffect' has already been declared (360:9)
[21:34:50.579] File was processed with these loaders:
[21:34:50.579]  * ./node_modules/next/dist/build/webpack/loaders/next-flight-client-module-loader.js
[21:34:50.580]  * ./node_modules/next/dist/build/webpack/loaders/next-swc-loader.js
[21:34:50.580] You may need an additional loader to handle the result of these loaders.
[21:34:50.580] |     });
[21:34:50.580] | }
[21:34:50.580] > import { useEffect, useRef, useState } from 'react';
[21:34:50.580] | import * as d3 from 'd3';
[21:34:50.580] | import { motion } from 'framer-motion';
[21:34:50.580] 
[21:34:50.580] Import trace for requested module:
[21:34:50.580] ./src/components/charts/TopicTreemap.tsx
[21:34:50.580] ./src/components/Dashboard.tsx
[21:34:50.580] 
[21:34:50.585] 
[21:34:50.586] > Build failed because of webpack errors
[21:34:50.612] Error: Command "npm run build" exited with 1