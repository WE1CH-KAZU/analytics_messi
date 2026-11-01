"""
Run this script to create the CSV files for Messi's goals.
"""

import re
from pathlib import Path

import pandas as pd

SOURCE_URL = "https://www.messistats.com/en/locationsscored"

# 出力先: instructions に従い data フォルダに出力する
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def parse_minute(minute_raw: str) -> tuple[int | None, int | None, int | None]:
    """
    '45+5' -> (45, 5, 50)
    '90'   -> (90, 0, 90)
    """
    s = str(minute_raw).strip()
    m = re.match(r"^(?P<base>\d+)(?:\+(?P<add>\d+))?$", s)
    if not m:
        return None, None, None
    base = int(m.group("base"))
    add = int(m.group("add")) if m.group("add") else 0
    return base, add, base + add


def main() -> None:
    """MessiStats からゴールデータを取得し、data フォルダに CSV を出力する。"""
    # MessiStatsのHTMLテーブルを直接読み取る（ページに全行が載っている）
    tables = pd.read_html(SOURCE_URL)
    if not tables:
        raise RuntimeError("No tables found. The page structure may have changed.")

    # ページ先頭のメインテーブルを想定（環境により複数テーブルになる可能性があるため最大件数のものを採用）
    df = max(tables, key=lambda t: len(t))

    # 列名の揺れを吸収（実ページは '# Index', 'Date Date', 'CMP Competition' 等の複合ヘッダ）
    # 正規化: 先頭の '# ' を除去し、先頭・末尾の単語でマッチ
    rename_map = {}
    for col in df.columns:
        c = str(col).strip().lower().lstrip("# ")
        tokens = c.split()
        first_word = tokens[0] if tokens else ""
        last_word = tokens[-1] if tokens else ""
        if last_word == "index":
            rename_map[col] = "goal_index"
        elif last_word == "date":
            rename_map[col] = "date_raw"
        elif first_word == "cmp" and last_word == "competition":
            rename_map[col] = "competition"
        elif first_word == "cmp":
            rename_map[col] = "competition_code"
        elif last_word == "competition":
            rename_map[col] = "competition"
        elif last_word == "home":
            rename_map[col] = "home_team"
        elif last_word == "away":
            rename_map[col] = "away_team"
        elif last_word == "result":
            rename_map[col] = "result"
        elif last_word == "minute":
            rename_map[col] = "minute_raw"
        elif last_word == "what":
            rename_map[col] = "what"
        elif last_word == "how":
            rename_map[col] = "how"

    df = df.rename(columns=rename_map)
    if "competition_code" not in df.columns and "competition" in df.columns:
        df["competition_code"] = df["competition"]

    required = [
        "goal_index",
        "date_raw",
        "competition_code",
        "competition",
        "home_team",
        "away_team",
        "result",
        "minute_raw",
        "what",
        "how",
    ]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise RuntimeError(f"Missing expected columns: {missing}\nColumns found: {list(df.columns)}")

    # 日付: dd-mm-yyyy -> yyyy-mm-dd
    df["date"] = pd.to_datetime(df["date_raw"], format="%d-%m-%Y", errors="coerce").dt.strftime("%Y-%m-%d")

    # 分数パース
    parsed = df["minute_raw"].apply(parse_minute)
    df["minute_base"] = parsed.apply(lambda x: x[0])
    df["minute_added"] = parsed.apply(lambda x: x[1])
    df["minute_total"] = parsed.apply(lambda x: x[2])

    # PK判定
    df["is_penalty"] = (df["what"].astype(str).str.strip().str.lower() == "penalty").astype(int)

    # 公式戦判定（デフォルト: International friendly を除外）
    # ここはあなたの定義で拡張可能
    comp_lower = df["competition"].astype(str).str.lower()
    df["is_official"] = (~comp_lower.str.contains("friendly")).astype(int)

    # 参照元
    df["source_url"] = SOURCE_URL

    # 出力列（必要に応じて増やす）
    out_cols = [
        "goal_index",
        "date",
        "competition_code",
        "competition",
        "home_team",
        "away_team",
        "result",
        "minute_raw",
        "minute_base",
        "minute_added",
        "minute_total",
        "what",
        "how",
        "is_penalty",
        "is_official",
        "source_url",
    ]

    out = df[out_cols].copy()

    # 時系列に並べ替え（古い順）
    out = out.sort_values(["date", "minute_total", "goal_index"], ascending=[True, True, True])

    # 公式戦のみCSV（ユーザー要件に合わせる）
    out_official = out[out["is_official"] == 1].reset_index(drop=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    out.to_csv(DATA_DIR / "messi_goals_all.csv", index=False, encoding="utf-8-sig")
    out_official.to_csv(DATA_DIR / "messi_goals_official.csv", index=False, encoding="utf-8-sig")

    print("Saved:")
    print(" - data/messi_goals_all.csv (includes friendlies)")
    print(" - data/messi_goals_official.csv (friendlies excluded by default rule)")


if __name__ == "__main__":
    main()
