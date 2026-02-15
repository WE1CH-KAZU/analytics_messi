---
applyTo:
  - "notebook/**/*.py"
  - "notebook/**/*.ipynb"
  - "src/**/*.py"
  - "src/**/*.ipynb"
  - "lib/**/*.py"
  - "lib/**/*.ipynb"
---

# Python コーディング細則

本プロジェクトでは、コードの一貫性と品質を保つため、以下の細則に従って Python コードを記述すること。

---

## 1. Ruff によるスタイル統一

本プロジェクトでは **Ruff** をリンター・フォーマッターとして採用している。コードは Ruff のルールに従うこと。具体的な設定は `pyproject.toml` を参照すること。

### 1.1 新規モジュール作成時の Ruff 設定

**新しくモジュール（パッケージや自前の .py モジュール）を作成した場合は、Ruff の設定を見直すこと。** 特に以下を確認する。

- **`pyproject.toml` の `[tool.ruff.lint.isort]`**  
  自前モジュールを import する際に、isort が「first-party」として扱うよう、`known-first-party` にモジュール名（またはパッケージ名）を追加する。追加し忘れると、import の並び順や未定義扱いでエラーになることがある。
- 必要に応じて **`[tool.ruff]` の `exclude`** や **`[tool.ruff.lint.per-file-ignores]`** で、当該モジュール用の除外・無視ルールを検討する。

---

## 2. import の配置

`import` 文は**一箇所にまとめて記述**すること。ファイル種別ごとに配置を統一する。

### 2.1 .py ファイルの場合

- **ファイルの前半**（docstring の直後）にすべての import をまとめる。

```python
"""モジュールの説明。"""

import os
from pathlib import Path

import pandas as pd

from workshop2026.utils import helper


def main() -> None:
    ...
```

### 2.2 .ipynb（ノートブック）の場合

- **Markdown セル**：`# Import` と記述し、その直後のセルで import を行うことを明示する。
- **最初の Python コードセル**：すべての import 文をまとめる。

| 順序 | 種類 | 内容 |
|------|------|------|
| 1 | Markdown | `# Import` |
| 2 | Code | import 文をすべて記述（最初の Python コードセル） |

---

## 3. ノートブック（.ipynb）のセル構成

ノートブックでは、**関数と実行コードを一つのセルにまとめない**こと。セルは役割ごとに分ける。

### 3.1 関数の記述位置

- **関数が記述されたコードセル**は、Markdown セル `# Functions` の配下にまとめる。
- `# Functions` の直後から、関数定義のみを含むセルを続けて配置する。
- 実行コード（関数の呼び出しやデータ処理など）は別セルに記述する。

### 3.2 セル構成の例

以下は標準的な構成例。import の詳細はセクション 2.2 を参照。

| セル順 | 種類 | 内容 |
|--------|------|------|
| 1 | Markdown | `# Import` |
| 2 | Code | import 文（最初の Python コードセル） |
| 3 | Markdown | `# Functions` |
| 4以降 | Code | 関数定義のみ（1 セルに 1 関数または関連する関数群） |
| ... | Markdown | `# Import data` |
| ... | Code | raw data の読み込み |
| ... | Markdown | `# EDA` |
| ... | Code | 探索的データ分析 |
| ... | Markdown | `# Modeling` |
| ... | Code | モデリング・統計解析 |
| ... | Markdown | その他フェーズの見出し（任意） |
| ... | Code | 検証・特徴量追加・可視化など |

### 3.3 実行フェーズの Markdown 見出し

各フェーズの直前に、以下の Markdown 見出しを用いること。

| 見出し | 配置タイミング |
|--------|----------------|
| `# Import data` | raw data を読み込むコードの直前 |
| `# EDA` | 探索的データ分析（EDA）を行う直前 |
| `# Modeling` | モデリングや統計解析を行う直前 |

その他、個別の検証・特徴量追加・可視化などを行う際も、Markdown で見出しをつけること。上記のフェーズ見出し（`# Import data` 等）とは別に、サブ見出しには `##` から数えて **3 階層まで**（`##`、`###`、`####`）を用いる。

### 3.4 避ける例

```python
# 悪い例：関数と実行コードを同一セルに混在
def process_data(x: int) -> int:
    return x * 2

result = process_data(10)  # 実行コードと一緒に書かない
```

---

## 4. 命名規則

### 4.1 関数の命名

- **snake_case** を使用する（小文字とアンダースコアの組み合わせ）。
- 動詞または動詞句で、処理内容が分かる名前にする。

```python
# 良い例
def calculate_sum(a: int, b: int) -> int: ...
def load_data(path: str) -> pd.DataFrame: ...
def is_valid(value: int) -> bool: ...

# 避ける例
def CalculateSum(...): ...   # PascalCase は不可
def loadData(...): ...       # camelCase は不可
```

### 4.2 引数の命名

- **snake_case** を使用する。
- 意味が伝わる簡潔な名前とする。

```python
# 良い例
def normalize_values(data: list[float], min_val: float, max_val: float) -> list[float]: ...
def process_data(raw_df: pd.DataFrame, output_path: str) -> None: ...

# 避ける例
def process(d, mp, mx): ...  # 意味が不明瞭
def process(DataFrame, str): ...  # 型名を引数名に使わない
```

### 4.3 ネストした関数（マトリョーシカ）の場合

関数の中に関数を入れ込むケースでは、**内側の関数の引数名の冒頭に `_` を付ける**こと。これにより、外側の関数が代表関数であることが分かりやすくなる。

```python
# 良い例：内側の関数の引数に _ を付与
def process_items(items: list[str]) -> list[str]:
    """アイテムリストを処理する代表関数。"""

    def _filter_item(_item: str) -> bool:
        """内側のヘルパー関数。引数は _ で始める。"""
        return len(_item) > 0

    return [item for item in items if _filter_item(item)]
```

```python
# 避ける例：内側・外側の引数が区別しづらい
def process_items(items: list[str]) -> list[str]:
    def filter_item(item: str) -> bool:  # 外側の items と混同しやすい
        return len(item) > 0
    return [item for item in items if filter_item(item)]
```

---

## 5. 型アノテーション

### 5.1 方針

- **厳しすぎず** 実務で十分な範囲で型を付与する。
- **`def` で定義する関数には、型アノテーションの付与を必須とする。**

### 5.2 必須とする箇所

- **関数の引数**：すべての引数に型を付与する。
- **関数の戻り値**：戻り値の型を `-> 型` で明示する。

```python
def calculate_sum(a: int, b: int) -> int:
    """2つの整数の和を返す。"""
    return a + b


def load_data(path: str) -> pd.DataFrame:
    """CSV ファイルを読み込んで DataFrame を返す。"""
    return pd.read_csv(path)
```

### 5.3 必須としない（任意）箇所

- ローカル変数
- クラス属性（必須ではないが、必要に応じて付与可）
- 過度に複雑なジェネリクスや Union を無理に書く必要はない

---

## 6. Docstrings（ドキュメント文字列）

### 6.1 スタイル

**Google スタイル** を使用する。

### 6.2 記述ルール

- **モジュール**：ファイル先頭にモジュールの概要を 1 行以上で記述する。
- **クラス**：クラスの役割を簡潔に記述する。
- **関数・メソッド**：1 行概要を必須とする。引数・戻り値・例外は必要に応じて記述する。

### 6.3 記述例

```python
"""データ分析用のユーティリティモジュール。"""


def normalize_values(
    data: list[float],
    min_val: float = 0.0,
    max_val: float = 1.0,
) -> list[float]:
    """リスト内の値を指定範囲に正規化する。

    Args:
        data: 正規化対象の数値リスト。
        min_val: 正規化後の最小値。デフォルトは 0.0。
        max_val: 正規化後の最大値。デフォルトは 1.0。

    Returns:
        正規化後の数値リスト。

    Raises:
        ValueError: data が空の場合。
    """
    if not data:
        raise ValueError("data must not be empty")
    # ...
    return result


class DataProcessor:
    """データの前処理を行うクラス。"""

    def process(self, raw: pd.DataFrame) -> pd.DataFrame:
        """生データを前処理して返す。"""
        # ...
        return processed
```

### 6.4 簡易な場合

引数や戻り値が自明な場合は、1 行の概要のみでもよい。

```python
def is_valid(x: int) -> bool:
    """正の整数かどうかを判定する。"""
    return x > 0
```

---

## 7. まとめチェックリスト

PR 作成前に以下を確認すること。

- [ ] `ruff check .` でエラーがないこと
- [ ] `ruff format .` でフォーマットが適用済みであること
- [ ] import が一箇所にまとめられていること（.py はファイル前半、.ipynb は最初の Python コードセル）
- [ ] .ipynb で関数と実行コードを同一セルに混在させず、関数は `# Functions` 配下にまとめていること
- [ ] 関数・引数に snake_case の命名規則が適用されていること
- [ ] `def` で定義した関数に型アノテーション（引数・戻り値）が付与されていること
- [ ] モジュール・クラス・関数に Google スタイルの docstring が記入されていること
