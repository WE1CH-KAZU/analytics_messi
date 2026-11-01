---
name: sufficient-statistic
description: 技術資料：因子分解定理と十分統計量（定義・解釈・つまずきポイント）
---

# SKILL.md — 因子分解定理と十分統計量（定義・解釈・つまずきポイント）

## 1. 目的
- 「十分統計量」「因子分解定理（Neyman–Fisher factorization）」を、式よりも意味から理解し、試験・実務の尤度操作で迷わない状態にする。
- “平均・分散・中央値” といった代表値の話と混同しない。

---

## 2. 用語の整理（最重要）

### 2.1 統計量（statistic）
- データ $x=(x_1,\dots,x_n)$ の関数 $T(x)$ のこと。
- 例：$\bar x$, $\sum x_i$, $\sum x_i^2$, $\max x_i$, $\min x_i$, 中央値, 最頻値など。
- 「統計量」は形の呼び名であって、良い/悪い・情報を残す/捨てるは別問題。

### 2.2 十分統計量（sufficient statistic）
- 「パラメータ $\theta$ に関する情報を失わない要約」になっている統計量。
- 本質：データ $x$ のうち $\theta$ に効く成分が $T(x)$ に全部入っている。

---

## 3. 因子分解定理（Neyman–Fisher）の定義

標本の同時密度（または同時確率）を $f_\theta(x)$ とする。

### 3.1 因子分解の形
$$
f_\theta(x) = g_\theta(T(x))\, h(x)
$$

- $g_\theta(\cdot)$：$\theta$ を含んでよい（むしろここに $\theta$ 依存が集まる）
- $h(x)$：$\theta$ を含まない（純粋にデータの形だけ）

### 3.2 定理（必要十分条件）
- 上の形に **分解できる** ことと、$T(x)$ が $\theta$ に関して **十分** であることは同値。

---

## 4. 解釈（直感を固定する）

### 4.1 「$\theta$ に効くのは $T(x)$ だけ」
尤度 $L(\theta|x)=f_\theta(x)$ が

$$
L(\theta|x)=g_\theta(T(x))\,h(x)
$$

と書けると、$\theta$ を動かして比較する（最尤・尤度比など）ときに $h(x)$ は定数扱い。
結局、$\theta$ の推定や検定に必要なのは $T(x)$ の値だけになる。

### 4.2 「平均・分散」との関係
- 十分統計量は「平均である」と決め打ちする概念ではない。
- 分布の形（特に指数型分布族）により、$\theta$ 依存が $\sum x_i$ や $\sum x_i^2$ や $\max x_i$ に集約されやすい。
- その結果として、$\bar x$（平均と同値）や最大値などの“見慣れた統計量”が十分になることがある。

---

## 5. ユーザーが理解できていなかった点の整理（盲点と修正）

### 盲点1：「$T(x)$ は何でもいい」＝「何でも十分になる」だと思いがち
- 正：$T(x)$ は“統計量としては”何でも定義できる。
- 誤：どんな $T(x)$ でも十分になる。
- 修正：**分解が成立した $T(x)$ だけが十分**。成立しない $T$ は十分ではない。

### 盲点2：「知りたい量（平均・分散…）と $\theta$ が1つの関数で…」という誤解
- 十分性は「何を知りたいか」とは独立。
- あくまで **同時分布（尤度）の $\theta$ 依存が $T(x)$ に集約できるか**の性質。

### 盲点3：「$h(x)$ は“それ以外の統計量”」という誤解
- $h(x)$ は「平均以外」ではない。
- **$\theta$ を含まない残り全部**をまとめただけ。

### 盲点4：最大値でも十分になるのか
- 一般には十分にならないことが多い（例：正規の位置パラメータで最大値だけでは情報を捨てる）。
- ただし、上限パラメータを持つ一様分布などでは最大値が十分になり得る。

---

## 6. 実戦手順（因子分解で十分性を判定する）
1. $f_\theta(x)$（同時密度/確率）を書く。
2. $\theta$ を含む因子をまとめ、データ依存がどの関数で表現できるかを探す。
3. その関数を $T(x)$ と置く。
4. $f_\theta(x)=g_\theta(T(x))h(x)$ の形に分け、$h(x)$ に $\theta$ が混ざっていないことだけ確認する。

---

## 7. 指示関数（indicator）の読み方（会話で詰まった箇所）
$$
\mathbf{1}(x_i\ge 0\ \forall i)
$$

- 文章：**すべての $i$ で $x_i\ge 0$ が成り立つとき 1、1つでも負なら 0**
- 密度/確率を「条件を満たす領域だけ生かし、それ以外を0にする」ための部品。

---

# 付録A：代表分布の $f_\theta(x)$（同時分布/尤度の素材）

以下、標本 $x=(x_1,\dots,x_n)$。独立同分布（i.i.d.）なら

$$
f_\theta(x)=\prod_{i=1}^n f_\theta(x_i)
$$

で同時分布を作る。

---

## A1. ベルヌーイ分布 $X_i\sim \mathrm{Bernoulli}(\theta)$, $\theta\in(0,1)$
- pmf（1点）：
$$
f_\theta(x_i)=\theta^{x_i}(1-\theta)^{1-x_i},\quad x_i\in\{0,1\}
$$
- 同時確率：
$$
f_\theta(x)=\prod_{i=1}^n \theta^{x_i}(1-\theta)^{1-x_i}
=\theta^{\sum x_i}(1-\theta)^{n-\sum x_i}
$$

---

## A2. 二項分布（1変数）$Y\sim \mathrm{Bin}(n,\theta)$
- pmf：
$$
f_\theta(y)=\binom{n}{y}\theta^y(1-\theta)^{n-y},\quad y=0,1,\dots,n
$$
（標本が複数なら $\prod_j f_\theta(y_j)$）

---

## A3. ポアソン分布 $X_i\sim \mathrm{Poisson}(\lambda)$, $\lambda>0$
- pmf（1点）：
$$
f_\lambda(x_i)=\frac{e^{-\lambda}\lambda^{x_i}}{x_i!},\quad x_i=0,1,2,\dots
$$
- 同時確率：
$$
f_\lambda(x)=\prod_{i=1}^n \frac{e^{-\lambda}\lambda^{x_i}}{x_i!}
=e^{-n\lambda}\lambda^{\sum x_i}\prod_{i=1}^n \frac{1}{x_i!}
$$

---

## A4. 負の二項分布（パラメータ化の流儀1）$X\sim \mathrm{NB}(r,p)$
ここでは「成功確率 $p$」「成功回数 $r$ が得られるまでの失敗回数 $x$」の形：
- pmf：
$$
f_{r,p}(x)=\binom{x+r-1}{x}(1-p)^x p^r,\quad x=0,1,2,\dots
$$

（別流儀：試行回数や平均分散パラメータ化もあるので、問題文の定義に合わせて読み替える。）

---

## A5. 幾何分布（流儀1）$X\sim \mathrm{Geom}(p)$
ここでは「初成功までの失敗回数 $x$」：
- pmf：
$$
f_p(x)=(1-p)^x p,\quad x=0,1,2,\dots
$$
（「初成功までの試行回数」なら $x=1,2,\dots$ で $f_p(x)=(1-p)^{x-1}p$。）

---

## A6. 超幾何分布 $X\sim \mathrm{Hypergeometric}(N,K,n)$
母集団 $N$ に成功 $K$、標本サイズ $n$、成功数 $x$：
- pmf：
$$
f(x)=\frac{\binom{K}{x}\binom{N-K}{n-x}}{\binom{N}{n}}
$$
- 範囲：
$$
\max(0,n-(N-K))\le x\le \min(n,K)
$$

（通常この分布は“パラメータ”が $(N,K,n)$ で、$\theta$ をどれに取るかは問題設定次第。）

---

## A7. 連続一様分布 $X_i\sim \mathrm{Unif}(0,\theta)$, $\theta>0$
- pdf（1点）：
$$
f_\theta(x_i)=\frac{1}{\theta}\mathbf{1}(0\le x_i\le \theta)
$$
- 同時密度：
$$
f_\theta(x)=\theta^{-n}\mathbf{1}\!\left(0\le x_i\le \theta\ \forall i\right)
=\theta^{-n}\mathbf{1}\!\left(\max_i x_i\le \theta\right)\mathbf{1}(x_i\ge 0\ \forall i)
$$

---

## A8. 正規分布 $X_i\sim \mathcal N(\mu,\sigma^2)$
- pdf（1点）：
$$
f_{\mu,\sigma^2}(x_i)=\frac{1}{\sqrt{2\pi\sigma^2}}
\exp\!\left(-\frac{(x_i-\mu)^2}{2\sigma^2}\right)
$$
- 同時密度：
$$
f_{\mu,\sigma^2}(x)=(2\pi\sigma^2)^{-n/2}
\exp\!\left(-\frac{1}{2\sigma^2}\sum_{i=1}^n (x_i-\mu)^2\right)
$$

---

## A9. 指数分布 $X_i\sim \mathrm{Exp}(\lambda)$, $\lambda>0$
- pdf（1点）：
$$
f_\lambda(x_i)=\lambda e^{-\lambda x_i}\mathbf{1}(x_i\ge 0)
$$
- 同時密度：
$$
f_\lambda(x)=\lambda^n\exp\!\left(-\lambda\sum_{i=1}^n x_i\right)\mathbf{1}(x_i\ge 0\ \forall i)
$$

---

## A10. 対数正規分布 $X_i\sim \mathrm{Lognormal}(\mu,\sigma^2)$
（$\ln X_i \sim \mathcal N(\mu,\sigma^2)$）
- pdf（1点）：
$$
f_{\mu,\sigma^2}(x_i)=\frac{1}{x_i\sigma\sqrt{2\pi}}
\exp\!\left(-\frac{(\ln x_i-\mu)^2}{2\sigma^2}\right)\mathbf{1}(x_i>0)
$$
- 同時密度は積。

---

## A11. ガンマ分布 $X_i\sim \mathrm{Gamma}(\alpha,\beta)$
ここでは shape $\alpha>0$, rate $\beta>0$：
- pdf（1点）：
$$
f_{\alpha,\beta}(x_i)=\frac{\beta^\alpha}{\Gamma(\alpha)}x_i^{\alpha-1}e^{-\beta x_i}\mathbf{1}(x_i\ge 0)
$$
- 同時密度は積。

（scale $\theta=1/\beta$ の流儀もある。）

---

## A12. ベータ分布 $X_i\sim \mathrm{Beta}(\alpha,\beta)$, $\alpha,\beta>0$
- pdf（1点）：
$$
f_{\alpha,\beta}(x_i)=\frac{1}{B(\alpha,\beta)}x_i^{\alpha-1}(1-x_i)^{\beta-1}\mathbf{1}(0<x_i<1)
$$
- 同時密度は積。

---

## 8. 使い方メモ（このSKILLを呼び出すとき）
- 「$T(x)$ が十分か？」は、まず $f_\theta(x)$ を書いて因子分解の形に落とす。
- 迷ったら、$\theta$ を含む部分を徹底的に括り出し、残りを $h(x)$ に押し込む。
- $h(x)$ に $\theta$ が混ざっていないかだけ、最後に機械的にチェックする。
