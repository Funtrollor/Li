#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import re
import argparse
from datetime import datetime

def parse_ptt_date(s):
    """
    把 PTT 的 date 字串轉成 datetime
    例如: "Sat Jan  6 17:03:21 2007"
    """
    return datetime.strptime(s, "%a %b %d %H:%M:%S %Y")

def main():
    p = argparse.ArgumentParser(description="篩選 PTT JSON：前標+日期區間")
    p.add_argument("-i", "--input",  required=True, help="原始 JSON 檔路徑")
    p.add_argument("-o", "--output", required=True, help="輸出 JSON 檔路徑")
    p.add_argument("-s", "--start",  required=True,
                   help="開始日期，格式 YYYY-MM-DD")
    p.add_argument("-e", "--end",    required=True,
                   help="結束日期，格式 YYYY-MM-DD")
    args = p.parse_args()

    # 解析區間
    start_dt = datetime.strptime(args.start, "%Y-%m-%d")
    end_dt   = datetime.strptime(args.end,   "%Y-%m-%d")

    # 讀入 JSON
    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    # 支援兩種結構：純 list 或 {"articles":[…]}
    records = data
    if isinstance(data, dict) and "articles" in data:
        records = data["articles"]

    out = []
    for rec in records:
        title = rec.get("article_title", "")
        # 1) 前標篩選
        m = re.match(r'^\[(情報|新聞)\]', title)
        if not m:
            continue

        # 2) 日期判斷
        try:
            dt = parse_ptt_date(rec.get("date",""))
        except Exception:
            continue
        if dt < start_dt or dt > end_dt:
            continue

        # 3) 構造輸出物件
        new = {
            "article_title":   title,
            "author":          rec.get("author",""),
            "board":           rec.get("board",""),
            "content":         rec.get("content",""),
            "date":            rec.get("date",""),
            "ip":              rec.get("ip",""),
            "message_count":   rec.get("message_count", {}),
            "messages":        []
        }
        # 保留 push_content, push_ipdatetime, push_tag, push_userid
        for m in rec.get("messages", []):
            new["messages"].append({
                "push_content":    m.get("push_content",""),
                "push_ipdatetime": m.get("push_ipdatetime",""),
                "push_tag":        m.get("push_tag",""),
                "push_userid":     m.get("push_userid","")
            })
        out.append(new)

    # 寫入新檔
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"完成：共輸出 {len(out)} 篇文章到 {args.output}")

if __name__ == "__main__":
    main()
