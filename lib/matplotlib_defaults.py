"""matplotlib のデフォルト設定（日本語フォント・グラフサイズ）。"""

import matplotlib as mpl


def setup_matplotlib_defaults(
    *,
    figure_size: tuple[float, float] = (8.0, 6.0),
) -> None:
    """matplotlib のデフォルトを設定する。

    日本語表記（Meiryo を優先、未導入環境では代替フォント）と
    デフォルトのグラフサイズを設定する。

    Parameters
    ----------
    figure_size : tuple[float, float], optional
        デフォルトの figure サイズ (width, height) インチ。デフォルトは (8.0, 6.0)。
    """
    # 日本語フォント: Meiryo を優先し、未導入なら OS 別の代替を利用
    mpl.rcParams["font.family"] = "sans-serif"
    mpl.rcParams["font.sans-serif"] = [
        "Meiryo",
        "Meiryo UI",
        "Yu Gothic",
        "Hiragino Sans",
        "Hiragino Kaku Gothic ProN",
        "IPAexGothic",
        "IPAPGothic",
    ]
    mpl.rcParams["axes.unicode_minus"] = False  # マイナスを文字化けさせない

    # デフォルトグラフサイズ
    mpl.rcParams["figure.figsize"] = list(figure_size)
