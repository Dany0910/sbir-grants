import asyncio
from vector_search import mmr_sort

# 模擬搜尋結果（故意製造來自同一份文件的重複結果）
mock_results = [
    {
        "name": "Chunk 1", 
        "path": "docs/guide.md", 
        "final_score": 0.95, 
        "content": "SBIR 指南第一章...",
        "metadata": {"file_path": "docs/guide.md"}
    },
    {
        "name": "Chunk 2", 
        "path": "docs/guide.md", 
        "final_score": 0.94, 
        "content": "SBIR 指南第二章...",
        "metadata": {"file_path": "docs/guide.md"}
    },
    {
        "name": "Chunk 3", 
        "path": "docs/guide.md", 
        "final_score": 0.93, 
        "content": "SBIR 指南第三章...",
        "metadata": {"file_path": "docs/guide.md"}
    },
    {
        "name": "Chunk 4", 
        "path": "docs/faq.md", 
        "final_score": 0.90, 
        "content": "常見問題...",
        "metadata": {"file_path": "docs/faq.md"}
    },
    {
        "name": "Chunk 5", 
        "path": "docs/case_study.md", 
        "final_score": 0.85, 
        "content": "成功案例...",
        "metadata": {"file_path": "docs/case_study.md"}
    }
]

print("=== 測試結果多樣性 (MMR) ===\n")

# 1. 原始排序
print("🔴 傳統排序 (只看分數):")
sorted_by_score = sorted(mock_results, key=lambda x: x['final_score'], reverse=True)
for i, r in enumerate(sorted_by_score[:3], 1):
    print(f"{i}. [{r['final_score']}] {r['path']} - {r['name']}")

print("\n-------------------\n")

# 2. MMR 排序
print("🟢 MMR 多樣性排序 (懲罰重複來源):")
# 使用我們實作的 mmr_sort
mmr_results = mmr_sort(mock_results, lambda_param=0.6) # 0.6 代表稍微看重多樣性
for i, r in enumerate(mmr_results[:3], 1):
    print(f"{i}. [{r['final_score']}] {r['path']} - {r['name']}")

print("\n💡 觀察：MMR 應該會把 faq.md 提上來，即便它的原始分數較低，因為 guide.md 已經出現過了。")
