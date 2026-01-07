"""
SBIR Data MCP Server
專注於經濟部統計處官方 API

功能：
1. 經濟部統計處總體統計資料庫 API
2. 工研院 IEK、資策會 MIC 由 Claude 的 search_web 處理
"""

from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx
import json
from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel

# ============================================
# 資料模型
# ============================================

class MOEAStatData(BaseModel):
    """經濟部統計處數據格式"""
    category: str        # 類別
    period: str          # 統計期間
    value: float         # 數值
    unit: str            # 單位
    source_url: str      # 來源網址

# ============================================
# MCP Server 初始化
# ============================================

app = Server("sbir-data-server")

# ============================================
# 工具定義
# ============================================

@app.list_tools()
async def list_tools() -> list[Tool]:
    """定義可用的工具"""
    return [
        Tool(
            name="query_moea_statistics",
            description="查詢經濟部統計處總體統計資料庫（官方 API）。可查詢產業產值、出口、就業等數據。",
            inputSchema={
                "type": "object",
                "properties": {
                    "industry": {
                        "type": "string",
                        "description": "產業別，如：機械、化工、電子、資通訊"
                    },
                    "stat_type": {
                        "type": "string",
                        "description": "統計類型：產值、出口、就業人數",
                        "enum": ["產值", "出口", "就業人數"]
                    },
                    "start_year": {
                        "type": "integer",
                        "description": "起始年份（西元年）",
                        "default": 2020
                    },
                    "end_year": {
                        "type": "integer",
                        "description": "結束年份（西元年）",
                        "default": 2024
                    }
                },
                "required": ["industry", "stat_type"]
            }
        ),
        Tool(
            name="search_moea_website",
            description="搜尋經濟部統計處網站（當 API 無法滿足需求時使用）",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {
                        "type": "string",
                        "description": "搜尋關鍵字"
                    }
                },
                "required": ["keyword"]
            }
        )
    ]

# ============================================
# 工具執行
# ============================================

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """執行工具"""
    if name == "query_moea_statistics":
        return await query_moea_statistics(
            arguments["industry"],
            arguments["stat_type"],
            arguments.get("start_year", 2020),
            arguments.get("end_year", 2024)
        )
    elif name == "search_moea_website":
        return await search_moea_website(arguments["keyword"])
    else:
        raise ValueError(f"Unknown tool: {name}")

# ============================================
# 核心功能：查詢經濟部統計處 API
# ============================================

async def query_moea_statistics(
    industry: str,
    stat_type: str,
    start_year: int,
    end_year: int
) -> list[TextContent]:
    """
    查詢經濟部統計處總體統計資料庫 API
    
    API 文件：https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sys=100&funid=API
    """
    
    # 產業代碼對應表（需要根據實際 API 文件調整）
    industry_codes = {
        "機械": "C29",
        "化工": "C20",
        "電子": "C26",
        "資通訊": "C26",
        "生技": "C21",
        "服務業": "G-S"
    }
    
    # 統計類型對應表
    stat_type_codes = {
        "產值": "production",
        "出口": "export",
        "就業人數": "employment"
    }
    
    industry_code = industry_codes.get(industry)
    if not industry_code:
        return [TextContent(
            type="text",
            text=f"❌ 不支援的產業別：{industry}\n\n支援的產業：{', '.join(industry_codes.keys())}"
        )]
    
    try:
        # 實際 API 呼叫
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 這裡需要根據實際 API 文件調整
            # 目前先回傳說明訊息
            
            result = f"""
## 經濟部統計處查詢結果

**產業別**：{industry}  
**統計類型**：{stat_type}  
**查詢期間**：{start_year} - {end_year}

---

⚠️ **API 實作說明**：

經濟部統計處提供總體統計資料庫 API，但需要：
1. 查詢「功能代碼」（每個統計表有唯一代碼）
2. 功能代碼列表：https://nstatdb.dgbas.gov.tw/

**建議替代方案**：
由於功能代碼查詢複雜，建議使用 Claude 的 `search_web` 工具：

```
search_web("{industry} {stat_type} site:dgbas.gov.tw OR site:moea.gov.tw")
```

**API 查詢範例**（需要功能代碼）：
```
https://nstatdb.dgbas.gov.tw/dgbasAll/webMain.aspx?sys=100&funid=API
  ?function=[功能代碼]
  &startTime={start_year}-01
  &endTime={end_year}-12
```

---

**來源**：
- 經濟部統計處：https://www.moea.gov.tw/Mns/dos/
- 總體統計資料庫：https://nstatdb.dgbas.gov.tw/
"""
            
            return [TextContent(type="text", text=result)]
            
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"❌ 查詢失敗：{str(e)}\n\n建議使用 Claude 的 search_web 工具作為替代方案。"
        )]

# ============================================
# 輔助功能：搜尋經濟部網站
# ============================================

async def search_moea_website(keyword: str) -> list[TextContent]:
    """提供搜尋建議（實際搜尋由 Claude 的 search_web 執行）"""
    
    result = f"""
## 經濟部統計處搜尋建議

**搜尋關鍵字**：{keyword}

---

**建議使用 Claude 的 `search_web` 工具**：

```
search_web("{keyword} site:dgbas.gov.tw OR site:moea.gov.tw")
```

**推薦查詢網站**：
- 經濟部統計處：https://www.moea.gov.tw/Mns/dos/
- 總體統計資料庫：https://nstatdb.dgbas.gov.tw/
- 產業統計：https://www.moea.gov.tw/Mns/dos/content/SubMenu.aspx?menu_id=6730

**查詢技巧**：
- 加上年份：`{keyword} 2024`
- 指定統計類型：`{keyword} 產值` 或 `{keyword} 出口`
"""
    
    return [TextContent(type="text", text=result)]

# ============================================
# Server 啟動
# ============================================

async def main():
    """啟動 MCP Server"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

