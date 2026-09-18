# Lumi JSONL RAG 整合

主要語料：knowledge/lumi_rag/corpus.jsonl。原來 knowledge 裡的 Markdown 留存，但新版索引預設只讀整理過的 JSONL，避免舊版閉氣／穴位建議重新混入。84 筆語料中 A–E 未驗證設計排除，匯入 83 筆。

在 lumi-langchain 專案根目錄執行：

```powershell
python -m rag.build_index --dry-run
python -m rag.build_index
```

第一個指令僅驗證、不呼叫 API；第二個指令使用既有 .env 的 Gemini 金鑰產生 embedding，可能使用 API 配額或產生費用。沒有輸出金鑰。

每次建索引放到獨立的 rag_indexes 子目錄，成功後才更新 rag/index_settings.json。原 chroma_db 與先前新版索引均留存；失败則不切換。建完需重新啟動後端；執行中的服務不會自行熱更新。不要手動搬移或覆蓋正在使用的 Chroma 目錄。

回復索引：停止後端，將 index_settings.json 改回上個已建好的目錄設定並重新啟動；初次整合前沒有此設定檔，移除它會回到原 chroma_db。回復程式：停止後端，從 rag_backups 的對應時間目錄還原原有 build_index.py、retriever.py、rag_service.py；原知識檔沒有修改。

retrieve_relevant_knowledge 預設取 4 筆，原 0.52 閾值保留，尚需用實際查詢校準。source_type／證據限制帶入生成提示，sources 回傳仍為字串陣列，來源為 URL 或檔名及列号。純提示層安全規則不等於完整危機偵測；API 上游仍需獨立安全路由，本次沒有宣稱已完成危機防護。

語料還缺 2 份專案研究／流程資料，未含 53 份問卷或訪談統計。每次更換 corpus.jsonl 後重新 build，成功再重啟後端。
