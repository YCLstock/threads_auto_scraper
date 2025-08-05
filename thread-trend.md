Threads 趨勢儀表板 (Threads Trend Dashboard) 系統規劃書
版本： 2.0 (Serverless Architecture)

日期： 2025年8月1日

文件目的： 本文件旨在定義「Threads 趨勢儀表板」專案的系統目標、架構、核心功能與技術實現路徑，作為開發專案的核心參考文件。

1.0 專案概述 (Project Overview)
本專案旨在開發一個高效能的數據儀表板，用於視覺化分析從 Threads (脆) 平台上爬取的貼文資料。系統將透過直觀的圖表，揭示熱門文章、新興趨勢及關鍵話題，幫助內容創作者、市場分析師或任何對社群趨勢感興趣的使用者，快速洞察社群脈動。

此版本採用現代化的無伺服器 (Serverless) 架構，以實現開發效率、低成本與高擴展性。

2.0 系統目標 (System Goals)
直觀呈現熱點： 透過創新的視覺化圖表，即時呈現當前熱度最高、最新的文章。

洞察內容特徵： 分析高熱度文章的共同特徵（如關鍵字、格式、話題），提供內容創作的策略參考。

趨勢演變追蹤： 視覺化呈現特定關鍵字或迷因（Meme）在時間維度上的聲量消長。

使用者友善： 提供清晰、易於理解的互動介面，讓非技術背景的使用者也能輕鬆探索數據。

3.0 現代化無伺服器架構 (Modern Serverless Architecture)
本系統將傳統的後端伺服器拆分為更靈活、更專注的服務元件，各元件職責如下：

+--------------------------------+
|                                |
|   地端執行環境 (你的電腦)      |
|   1. 執行爬蟲腳本 (`scraper.py`)|----->| 將「原始數據」寫入 |
|   2. 執行數據處理腳本 (`process.py`)|-->| 將「分析結果」寫入 |------+
|                                |     +------------------+      |
+--------------------------------+                             |
                                                                 V
                                                       +---------------------+
                                                       |                     |
                                                       |  Supabase (雲端)    |
                                                       |  - PostgreSQL DB    |
                                                       |  - Auto-Generated API|
                                                       |                     |
                                                       +---------------------+
                                                                 ^
+--------------------------------+                               |
|                                |     | 直接讀取「分析結果」 |------+
|   Vercel (雲端)                |----->| (透過 Supabase API)  |
|   - 託管前端網頁 (React/Next.js)|
|                                |
+--------------------------------+
地端執行環境 (Local/On-Premise Environment):

角色： 數據生產與處理中心。

任務： 定時執行 Python 腳本，負責爬取原始數據，並進行所有複雜的數據運算與分析，最後將結果上傳至 Supabase。

Supabase (Backend-as-a-Service 平台):

角色： 核心數據庫與 API 服務。

任務： 提供 PostgreSQL 資料庫來儲存數據，並自動生成安全、高效能的 API，供前端直接讀取，無需手寫後端 API。

Vercel (前端部署平台):

角色： 視覺化呈現與使用者互動層。

任務： 託管前端應用程式，從 Supabase 獲取預先處理好的分析結果，並將其渲染成互動式圖表。

4.0 資料模型 (Data Model)
資料庫將包含兩種類型的資料表：

原始數據表 (raw_posts): 儲存爬蟲抓取的原始資料。

JSON

// 與前一版相同
{ "post_id": "...", "username": "...", "content": "...", ... }
分析結果表 (Processed Tables): 儲存由地端腳本計算出的結果，供前端直接取用。

範例表 1: processed_post_metrics

post_id (關聯到 raw_posts)

total_interactions (INT)

heat_density (FLOAT)

範例表 2: processed_topic_summary

topic_id (INT)

topic_keywords (TEXT)

post_count (INT)

average_heat_density (FLOAT)

5.0 核心功能模組詳解
儀表板由以下三大視覺化圖表組成，其數據來源均為 Supabase 中的「分析結果表」。

5.1 模組一：熱度氣泡圖 (Heat Bubble Chart)
目標： 直觀展示當前哪些文章又「熱」又「新」。

視覺化呈現： 動態的力導向佈局氣泡叢。

數據處理邏輯：

此計算在「地端數據處理腳本」中完成，並將結果存入 processed_post_metrics 表。

氣泡大小 (Size): likes + replies + reposts

氣泡顏色 (Color): 當前時間 - timestamp，將計算出的「文章新鮮度」映射到顏色梯度。

前端任務： 從 processed_post_metrics 獲取數據並繪製。

5.2 模組二：趨勢河流圖 (Trend River Chart)
目標： 追蹤特定關鍵字或迷因的歷史聲量變化。

視覺化呈現： 平滑、流動的堆疊面積圖。

數據處理邏輯：

此計算在「地端數據處理腳本」中完成。 腳本會分析 raw_posts 表，計算出每個關鍵字在每天的文章數量，並將結果存入 processed_keyword_trends 表。

前端任務： 從 processed_keyword_trends 獲取時間序列數據並繪製。

5.3 模組三：主題矩陣樹圖 (Topic Treemap)
目標： 鳥瞰所有已爬取文章的話題分佈，並找出最熱門的話題類別。

視覺化呈現： 由大小和顏色各異的矩形構成的區塊圖。

數據處理邏輯：

此計算在「地端數據處理腳本」中完成。 腳本會對 raw_posts 進行聚類分析，計算每個話題的文章數與平均熱度密度，並將結果存入 processed_topic_summary 表。

前端任務： 從 processed_topic_summary 獲取數據並繪製。

6.0 技術棧建議 (Technology Stack Recommendation)
數據處理 (地端): Python + pandas + scikit-learn + supabase-py

數據庫與 API (雲端): Supabase

前端框架 (雲端): React (Next.js) / Vue.js

視覺化庫 (前端): D3.js / ECharts

部署 (雲端): Vercel

7.0 開發階段規劃 (Development Phase Plan)
第一階段：雲端基建與數據採集

創建 Supabase 專案並設計好所有資料表（原始表與結果表）。

完成地端 scraper.py 腳本，實現穩定抓取數據並寫入 Supabase raw_posts 表。

第二階段：核心數據處理

完成地端 process_data.py 腳本，實現從 Supabase 讀取原始數據，進行所有複雜計算，並將結果寫回分析結果表。此為本專案的「大腦」。

第三階段：前端視覺化與部署

使用 Next.js 建立前端專案。

開發三大圖表元件，使其能透過 Supabase 的客戶端庫讀取「分析結果表」中的數據。

完成儀表板的整體佈局與互動設計，並部署到 Vercel。

8.0 未來展望 (Future Outlook)
本架構為專案的快速啟動和未來擴展奠定了堅實的基礎。V2.0 版本可考慮引入 Vercel 的定時任務 (Cron Jobs) 來自動觸發地端腳本（透過 Webhook），實現全自動化數據更新流程。

範例資料格式(爬取下來的結果):
[
  {
    "post_id": "3153f961ca70e14119e8ca10c5daa635",
    "username": "deehsiang",
    "content": "AI軍備競賽仍在加速，這次是 Meta與微軟給市場帶來了驚喜\n今年第一季微軟的資本支出減幅達 5.3%，讓市場擔心科技巨頭對 AI支出放緩，但第二季微軟再次擴大支出達 242億美元，相較第一季增張13.1%，算是打消了市場的疑慮。\n微軟的各項業務也都優於市場預期，主要是受惠於企業與消費者對 AI需求上升，CEO Nadella表示 AI是各行各業轉型的驅動力，微軟正在幫助客戶適應這個新時代。 Meta則是將 2025年全年的資本支出下陷從 640億美元上調至 660億美元，Meta大撒錢並不算甚麼新聞，但過去市場擔憂 Meta的收入無法支撐不斷擴大的支出。\n值得注意的是， Meta第二季廣告營收達 465億美元，遠高於市場預期的 440億美元，打消了市場認為 Meta入不敷出的疑慮。\nCEO Zuckerberg強調 AI在提升廣告投放率。這代表 Meta擴大資本支出也能為營收帶來不小的助益，已經形成正向循環。  \n翻譯",
    "timestamp": "2025-07-31T00:03:47.000Z",
    "likes": 67,
    "replies": 1,
    "reposts": 0,
    "images": [],
    "post_url": "https://www.threads.com/@deehsiang/post/DMwFliLzbzM",
    "scraped_at": "2025-07-31T14:25:12.153355"
  }
]