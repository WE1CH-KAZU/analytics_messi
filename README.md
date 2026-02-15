# Messi Goals Timeline

リオネル・メッシの**全公式戦ゴール**について、日付・キックオフからの経過時間・PKフラグ等を含む**時系列CSV**を生成するツールです。

ゴール時系列CSVは、MessiStats の「[Locations where scored](https://www.messistats.com/en/locationsscored)」ページから全ゴール（総計896ゴール）を抽出して作成します。ページ側に全ゴール分の表がHTMLとして掲載されています。

## 目的

以下を満たす時系列CSVを生成する。

- ゴール日付（Date）
- キックオフからの経過時間（Minute。例: `45+5` を保持しつつ数値化もする）
- PKゴールかどうか（PKフラグ）
- 参照元URL（検証・再現性のため）

## データソース（一次情報）

**MessiStats（StarPlayerStats）**の「Locations where scored」ページ

- テーブルには、ゴールごとに **Date / Competition / Home / Away / Minute / Score / What / How** 等が並ぶ
- "What" 列に **Penalty** が明示されるため、PKフラグはここから判定できる
- ページ上に総計として **Goals 896 / Penalties 112** が表示される

### 利用条件（重要）

MessiStats は、統計データの取得について**出典を [www.messistats.com](http://www.messistats.com) と明記すれば取得は許可**旨を明示している。本README末尾の引用表記を残す前提で利用する。

## 「公式試合」の扱い（フィルタ方針）

MessiStats には **International friendly（親善試合）** が含まれる。ユーザー要件「公式試合」を満たすため、CSV出力時に次をデフォルトで除外する。

- `Competition` が **International friendly** に該当する行

> **注意**: 「公式」の定義が組織や文脈でブレることがあるため、**元データは保持**し、出力CSVでは `is_official` 列を付与して切り替え可能にしている。

## 出力CSV仕様（列定義）

| 列名 | 説明 |
|------|------|
| `goal_index` | MessiStats上の Index（1..896） |
| `date` | ISO形式（YYYY-MM-DD） |
| `competition_code` | CMP（例: PRM, EUR, WCQ） |
| `competition` | Competition文字列 |
| `home_team`, `away_team` | ホーム／アウェイチーム |
| `result` | Result文字列（例: `2-1`） |
| `minute_raw` | 文字列のまま（例: `45+5`, `90+2`, `19`） |
| `minute_base` | 45+5なら45 |
| `minute_added` | 45+5なら5（通常は0） |
| `minute_total` | `minute_base + minute_added` |
| `what` | Field goal / Free kick / Penalty など |
| `how` | Left foot / Head など |
| `is_penalty` | `what == "Penalty"` なら1、それ以外0 |
| `is_official` | 親善試合除外などの判定（1/0） |
| `source_url` | 参照元URL |

## 実行手順

### 1. 依存関係のインストール

```bash
uv sync
```

### 2. CSV生成

```bash
uv run python src/run_create_csv.py
```

### 3. 出力先

- `data/messi_goals_all.csv` … 親善試合を含む全ゴール
- `data/messi_goals_official.csv` … 親善試合を除外した公式戦のみ

## 検証観点（盲点になりやすい点）

- **`minute_raw` vs `minute_total`**: `minute_raw` は `45+5` のようにロスタイム表記がある。分析用途では `minute_total` を使い、表示には `minute_raw` を残す。
- **「公式戦」の厳密定義**: 本コードは `competition` に "friendly" を含むものを除外する単純ルール。クラブのプレシーズン等も含まれている場合は、`competition_code` や `competition` の具体値を見て追加除外するのが望ましい。

## 引用（この README を残す前提で利用）

- MessiStats: [Locations where scored](https://www.messistats.com/en/locationsscored)（全ゴール一覧・列・総計表示）
- MessiStats: [Usage of the stats](https://www.messistats.com/)（出典明記を条件に取得許可）
