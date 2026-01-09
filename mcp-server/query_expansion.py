"""
查詢擴展模組 - 同義詞處理

使用 SBIR 領域同義詞擴展查詢，提升搜尋召回率
"""

# SBIR 領域同義詞字典
SYNONYMS = {
    # 補助相關
    "補助": ["補助金額", "經費", "資金", "款項", "補貼", "補助費"],
    "申請": ["送件", "提案", "投標", "報名", "申報"],
    
    # 階段相關
    "Phase 1": ["第一階段", "先期研究", "創新技術", "Phase1", "phase 1", "一階"],
    "Phase 2": ["第二階段", "研究開發", "研發", "Phase2", "phase 2", "二階"],
    "Phase 2+": ["第三階段", "加值應用", "Phase2+", "phase 2+", "2+"],
    
    # 創新相關
    "創新": ["創新性", "創意", "突破", "新穎", "創新點"],
    "技術": ["技術創新", "科技", "研發技術", "技術研發"],
    "可行性": ["技術可行性", "執行可行性", "feasibility"],
    
    # 市場相關
    "市場": ["市場分析", "市場規模", "目標市場", "市場潛力"],
    "商業化": ["產業化", "市場化", "商品化"],
    
    # 團隊相關
    "團隊": ["研發團隊", "執行團隊", "人力", "人員"],
    "主持人": ["計畫主持人", "負責人", "PI"],
    
    # 文件類型
    "範例": ["案例", "樣本", "示範", "參考", "example"],
    "方法": ["方法論", "做法", "步驟", "流程", "methodology"],
    "檢核": ["檢核清單", "清單", "查核", "檢查", "checklist"],
    "指南": ["指引", "說明", "guide", "教學"],
    
    # 經費相關
    "經費": ["預算", "費用", "成本", "支出"],
    "編列": ["編制", "規劃", "安排"],
    
    # 審查相關
    "審查": ["評審", "評分", "review"],
    "評分": ["評分標準", "評分項目", "分數"],
    
    # 產業相關
    "機械": ["機械產業", "機械業", "機械製造"],
    "生技": ["生物技術", "生技產業", "biotechnology"],
    "ICT": ["資通訊", "資訊", "通訊"],
}


def expand_query(query: str) -> list[str]:
    """
    擴展查詢，加入同義詞
    
    Args:
        query: 原始查詢字串
    
    Returns:
        擴展後的查詢列表（包含原始查詢）
    
    Example:
        >>> expand_query("補助金額")
        ["補助金額", "經費金額", "資金金額", ...]
    """
    expanded = [query]  # 保留原始查詢
    query_lower = query.lower()
    
    # 對每個同義詞組進行替換
    for term, synonyms in SYNONYMS.items():
        term_lower = term.lower()
        
        # 檢查查詢中是否包含此詞
        if term_lower in query_lower:
            # 為每個同義詞生成新查詢
            for syn in synonyms:
                # 保持原始大小寫風格
                if term in query:
                    new_query = query.replace(term, syn)
                else:
                    new_query = query_lower.replace(term_lower, syn)
                
                if new_query not in expanded:
                    expanded.append(new_query)
    
    return expanded


def get_expanded_keywords(query: str) -> list[str]:
    """
    獲取擴展後的關鍵字列表（去重）
    
    Args:
        query: 原始查詢字串
    
    Returns:
        擴展後的關鍵字列表
    
    Example:
        >>> get_expanded_keywords("Phase 1 申請")
        ["phase", "1", "申請", "第一階段", "先期研究", "送件", "提案", ...]
    """
    expanded_queries = expand_query(query)
    keywords = []
    
    for q in expanded_queries:
        # 分詞並轉小寫
        words = [kw.strip().lower() for kw in q.split() if kw.strip()]
        keywords.extend(words)
    
    # 去重但保持順序
    seen = set()
    unique_keywords = []
    for kw in keywords:
        if kw not in seen:
            seen.add(kw)
            unique_keywords.append(kw)
    
    return unique_keywords


if __name__ == "__main__":
    # 測試
    test_queries = [
        "補助金額",
        "Phase 1 申請資格",
        "創新性方法",
        "市場分析範例",
    ]
    
    print("同義詞擴展測試\n" + "="*50)
    for q in test_queries:
        expanded = expand_query(q)
        print(f"\n原始查詢: {q}")
        print(f"擴展數量: {len(expanded)}")
        print(f"擴展結果: {expanded[:5]}...")  # 只顯示前5個
