"""pandas の DataFrame / Series の表示設定。"""

import pandas as pd


def setup_pandas_display(
    *,
    float_sig_figs: int = 4,
) -> None:
    """pandas の表示オプションを設定する。

    連続値（浮動小数）は有効数字を指定し、列表記（Series 内のリスト等）は
    要素数制限なしで表示する。

    Parameters
    ----------
    float_sig_figs : int, optional
        浮動小数点の有効数字。デフォルトは 4。
    """
    # 連続値: 有効数字で表示
    pd.options.display.float_format = lambda x: f"{x:.{float_sig_figs}g}"

    # 列表記: 制限なし（省略しない）
    pd.options.display.max_seq_items = None
