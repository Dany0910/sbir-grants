"""
搜尋快取模組 - LRU 快取機制

提升常見查詢的回應速度
"""

import hashlib
from typing import Optional


class SearchCache:
    """搜尋結果快取（LRU 策略）"""
    
    def __init__(self, max_size=100):
        """
        初始化快取
        
        Args:
            max_size: 最大快取數量
        """
        self.cache = {}
        self.max_size = max_size
        self.access_count = {}
        self.access_order = []
    
    def _hash_query(self, query: str, category: str) -> str:
        """
        生成查詢的雜湊值
        
        Args:
            query: 查詢字串
            category: 分類
        
        Returns:
            MD5 雜湊值
        """
        key = f"{query}:{category}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, query: str, category: str = "all") -> Optional[str]:
        """
        獲取快取結果
        
        Args:
            query: 查詢字串
            category: 分類
        
        Returns:
            快取的結果，如果不存在則返回 None
        """
        key = self._hash_query(query, category)
        
        if key in self.cache:
            # 更新訪問計數和順序
            self.access_count[key] = self.access_count.get(key, 0) + 1
            
            # 更新 LRU 順序
            if key in self.access_order:
                self.access_order.remove(key)
            self.access_order.append(key)
            
            return self.cache[key]
        
        return None
    
    def set(self, query: str, category: str, results: str):
        """
        設定快取
        
        Args:
            query: 查詢字串
            category: 分類
            results: 搜尋結果
        """
        key = self._hash_query(query, category)
        
        # LRU 淘汰策略
        if len(self.cache) >= self.max_size and key not in self.cache:
            # 移除最少使用的（最舊的）
            if self.access_order:
                lru_key = self.access_order.pop(0)
                if lru_key in self.cache:
                    del self.cache[lru_key]
                if lru_key in self.access_count:
                    del self.access_count[lru_key]
        
        # 加入快取
        self.cache[key] = results
        self.access_count[key] = 1
        
        # 更新 LRU 順序
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)
    
    def clear(self):
        """清空快取"""
        self.cache.clear()
        self.access_count.clear()
        self.access_order.clear()
    
    def stats(self) -> dict:
        """
        獲取快取統計資訊
        
        Returns:
            統計資訊字典
        """
        return {
            "size": len(self.cache),
            "max_size": self.max_size,
            "total_accesses": sum(self.access_count.values()),
            "most_accessed": max(self.access_count.items(), key=lambda x: x[1])[0] if self.access_count else None
        }


# 全域快取實例
_search_cache = SearchCache(max_size=100)


def get_cache() -> SearchCache:
    """獲取全域快取實例"""
    return _search_cache


if __name__ == "__main__":
    # 測試
    cache = SearchCache(max_size=3)
    
    print("快取測試\n" + "="*50)
    
    # 測試設定和獲取
    cache.set("Phase 1", "all", "結果1")
    cache.set("Phase 2", "all", "結果2")
    cache.set("補助金額", "all", "結果3")
    
    print(f"快取大小: {cache.stats()['size']}/3")
    print(f"獲取 'Phase 1': {cache.get('Phase 1', 'all')}")
    
    # 測試 LRU 淘汰
    cache.set("創新性", "all", "結果4")  # 應該淘汰最舊的
    print(f"\n加入新項目後快取大小: {cache.stats()['size']}/3")
    print(f"獲取 'Phase 1' (應該被淘汰): {cache.get('Phase 1', 'all')}")
    print(f"獲取 'Phase 2' (應該還在): {cache.get('Phase 2', 'all')}")
    
    # 統計
    print(f"\n快取統計: {cache.stats()}")
