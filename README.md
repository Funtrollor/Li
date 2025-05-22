# 📈 基於 PTT 貼文的股票資料報告生成器

本專案提供一套完整流程，從 PTT 採集資料、篩選到上傳 LLM 模型進行投資建議生成，支援 JSON 結構化資料格式與報告範式設計。

---

## 📦 如何使用

### 1️⃣ 安裝環境

請先安裝相關 Python 套件：

```bash
pip install -r requirements.txt
```

---

### 2️⃣ 執行爬蟲

使用以下指令擷取指定看板資料：

```bash
python crawler.py -b 看板名稱 -i 起始索引 結束索引
```

> ℹ️ 提示：若索引為負數，則代表「倒數第 N 頁」。

---

### 3️⃣ 篩選文章（依日期）

可根據發文日期篩選指定時間範圍內的貼文：

```bash
python filter_ptt_json.py -i "輸入檔名.json" -o 輸出檔名.json -s 起始日期 -e 終止日期
```

---

### 4️⃣ 上傳至 LLM 生成投資建議報告

#### 📋 詢問範式範例：

```
這是 PTT 2025 年 3 月 20 日到 2025 年 4 月 2 日的所有文章資料，幫我做一份投資建議報告。
```

請配合以下格式上傳 JSON 檔案：

```json
{
  "article_title": "文章標題",
  "author": "作者",
  "board": "板名",
  "content": "文章內容",
  "date": "發文時間",
  "ip": "發文位址",
  "message_count": {
    "all": "總數",
    "boo": "噓文數",
    "count": "推文數 - 噓文數",
    "neutral": "→ 數",
    "push": "推文數"
  },
  "messages": [
    {
      "push_content": "推文內容",
      "push_ipdatetime": "推文時間及位址",
      "push_tag": "推/噓/→",
      "push_userid": "推文者 ID"
    }
    // ... 更多推文
  ]
}
```

---

## 📄 JSON 格式規格說明

與第 4 步相同，完整 JSON 範例如下：

```json
{
  "article_title": "文章標題",
  "author": "作者",
  "board": "板名",
  "content": "文章內容",
  "date": "發文時間",
  "ip": "發文位址",
  "message_count": {
    "all": "總數",
    "boo": "噓文數",
    "count": "推文數 - 噓文數",
    "neutral": "→ 數",
    "push": "推文數"
  },
  "messages": [
    {
      "push_content": "推文內容",
      "push_ipdatetime": "推文時間及位址",
      "push_tag": "推/噓/→",
      "push_userid": "推文者 ID"
    }
  ]
}
```

---

## 📚 授權說明

本專案部分程式碼來源於下列開源專案，遵循 [MIT License](https://opensource.org/licenses/MIT)：

🔗 https://github.com/jwlin/ptt-web-crawler
