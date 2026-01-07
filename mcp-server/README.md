# SBIR Data MCP Server

混合式市場數據查詢服務，整合台灣官方與法人機構數據來源。

## 功能

### 數據來源

| 來源 | 類型 | 說明 |
|------|------|------|
| 經濟部統計處 | Web Search | 官方產業統計數據 |
| 工研院 IEK | Web Search | 產業趨勢報告 |
| 資策會 MIC | Web Search | 資通訊產業數據 |

### 可用工具

1. **get_industry_market_data**
   - 查詢特定產業的市場數據
   - 自動整合多個來源
   - 參數：產業別、關鍵字、年份

2. **search_moea_statistics**
   - 直接查詢經濟部統計處
   - 參數：查詢關鍵字

## 安裝

```bash
cd /Users/backtrue/Documents/claude-sbir-skills/sbir-grants/mcp-server

# 使用 uv 安裝（推薦）
uv pip install -e .

# 或使用 pip
pip install -e .
```

## 設定 Claude Desktop

編輯 Claude Desktop 設定檔：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sbir-data": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/backtrue/Documents/claude-sbir-skills/sbir-grants/mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

## 使用範例

設定完成後，在 Claude 中：

```
用戶：「我要寫機械產業的問題陳述，請幫我找市場數據」

Claude 自動執行：
1. 呼叫 get_industry_market_data(industry="機械", keyword="市場規模")
2. 整合經濟部統計處、工研院 IEK 數據
3. 格式化為可引用的段落

Claude 回應：
「根據工研院 IEK (2024) 報告，台灣機械產業市場規模達 XX 億元...
根據經濟部統計處，2024 年機械產業產值...」
```

## 目前狀態

⚠️ **注意**：目前版本為架構雛形，Web Search 功能需要進一步實作。

### 待完成項目

- [ ] 整合 Google Custom Search API
- [ ] 實作 Web Scraping（遵守 robots.txt）
- [ ] 或整合 Claude 的 search_web 工具
- [ ] 快取機制（避免重複查詢）
- [ ] 錯誤處理與重試邏輯

### 實作選項

**選項 A：使用 Google Custom Search API**
```python
# 需要 Google API Key
GOOGLE_API_KEY = "your-api-key"
SEARCH_ENGINE_ID = "your-search-engine-id"

async def web_search(query: str):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query
    }
    # ...
```

**選項 B：使用 Claude 的 search_web**
```python
# 透過 MCP 呼叫 Claude 的 search_web 工具
# 需要研究 MCP 的 tool-to-tool 呼叫機制
```

**選項 C：Web Scraping**
```python
from playwright.async_api import async_playwright

async def scrape_iek(industry: str, keyword: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # ...
```

## 開發指引

### 測試 Server

```bash
# 直接執行測試
python server.py

# 或使用 MCP Inspector
npx @modelcontextprotocol/inspector uv --directory . run server.py
```

### 新增數據來源

1. 在 `server.py` 新增查詢函數
2. 在 `get_industry_market_data` 中整合
3. 更新 `format_market_data` 格式化邏輯

## 授權

MIT License
