# Supabase 設置指南

## 快速開始

目前前端應用支持兩種數據模式：
- **Mock 數據模式**：使用預設的測試數據（默認模式）
- **真實數據模式**：連接 Supabase 數據庫獲取真實數據

## 配置 Supabase（可選）

如果您想使用真實數據庫，請按照以下步驟設置：

### 1. 創建 Supabase 項目

1. 訪問 [Supabase](https://supabase.com)
2. 創建一個新的項目
3. 等待數據庫初始化完成

### 2. 執行數據庫架構

在 Supabase SQL 編輯器中執行 `database_schema.sql` 文件中的 SQL 命令來創建所需的表結構。

### 3. 配置環境變數

編輯 `frontend-app/.env.local` 文件，替換以下值：

```env
# 將這些值替換為您的 Supabase 項目信息
NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here

# 應用配置
NEXT_PUBLIC_APP_ENV=development
NEXT_PUBLIC_USE_MOCK_DATA=false
```

### 4. 獲取 Supabase 配置信息

在您的 Supabase 項目儀表板中：

1. **項目 URL**：在 Settings > API 中找到 "Project URL"
2. **Anon Key**：在 Settings > API 中找到 "Project API keys" 下的 "anon public" key

### 5. 測試連接

重新啟動開發服務器：

```bash
cd frontend-app
npm run dev
```

在瀏覽器中訪問 http://localhost:3003，點擊右上角的 "真實數據" 按鈕測試連接。

## 數據填充

要使用真實數據，您需要：

1. **運行爬蟲腳本**填充原始數據：
   ```bash
   python scraper.py
   ```

2. **運行數據處理腳本**生成分析結果：
   ```bash
   python process_data.py
   ```

## 故障排除

### 連接失敗
- 檢查 Supabase URL 和 API Key 是否正確
- 確認數據庫表已正確創建
- 查看瀏覽器控制台的錯誤信息

### 沒有數據顯示
- 確認已運行爬蟲和數據處理腳本
- 檢查 Supabase 表中是否有數據
- 驗證表結構是否與 `database_schema.sql` 一致

### 權限錯誤
- 確認使用的是 `anon` key 而不是 `service_role` key
- 檢查 Supabase Row Level Security (RLS) 設置

## 不使用 Supabase

如果您不想設置 Supabase，系統會自動使用 Mock 數據模式，功能完全正常。您可以：

1. 保持默認的 "Mock 數據" 模式
2. 瀏覽所有可視化功能
3. 測試完整的用戶界面

所有圖表和功能都可以在 Mock 數據模式下正常工作。