---
name: crse
description: 技術資料：クラスターロバスト標準誤差（CRSE）で「見かけの有意」を潰し、再現性を評価する
---


# 技術資料：クラスターロバスト標準誤差（CRSE）で「見かけの有意」を潰し、再現性を評価する

## 1. 本資料の狙い
現場データでは、同じ店舗・同じ部署・同じ媒体などの“まとまり”の中で成果が一緒に動きます。このとき通常のOLS標準誤差は過小になり、施策が効いたように見える（見かけの有意）が起きやすい。

本資料は以下を目的とします。  
- **CRSE**により推論（SE・p値・CI）を適正化し、誤った全社展開や誤投資を減らす  
- **相互作用（例：年×施策）**により「X年で効いたからY年でも効くとは限らない」をモデルで検証する  
- 時系列ケースと、指定の3テーマ（研修・予算差異・PR）に適用指針を与える  
- 解析コードは **時系列ケース**と **予算差異**の2ケースのみ提示する（Python/R）

---

## 2. 数式：CRSE（クラスターロバスト標準誤差）

### 2.1 回帰モデル（一般形）
$$
y = X\beta + u
$$

OLS推定量：
$$
\hat{\beta} = (X'X)^{-1}X'y
$$

### 2.2 1方向クラスタ（クラスター $g=1,\dots,G$）
クラスターgに属する観測の行列を $X_g$、残差ベクトルを $\hat{u}_g$ とすると、CRSE分散推定量（サンドイッチ）は：
$$
\widehat{\mathrm{Var}}(\hat{\beta})
=
(X'X)^{-1}
\left(
\sum_{g=1}^{G}
X_g' \hat{u}_g \hat{u}_g' X_g
\right)
(X'X)^{-1}
$$

標準誤差：
$$
\mathrm{SE}(\hat{\beta}_k)=\sqrt{\left[\widehat{\mathrm{Var}}(\hat{\beta})\right]_{kk}}
$$

### 2.3 2方向クラスタ（例：店舗×週、部門×月）
2方向クラスタの代表的合成（Cameron–Gelbach–Miller型）：
$$
\widehat{\mathrm{Var}}_{2\text{way}}
=
\widehat{\mathrm{Var}}_{A}
+
\widehat{\mathrm{Var}}_{B}
-
\widehat{\mathrm{Var}}_{A\cap B}
$$
- $A$：例）店舗、部門、媒体  
- $B$：例）週、月、期  
- $A\cap B$：交差セルで二重カウント調整

### 2.4 CRSEが解決する課題（何が“良くなる”か）
- 誤差相関を無視した **過小SE→過剰な有意判定** を抑える  
- 結果として「効いたから展開」「効かないから停止」の判断が、偶然や集団依存でブレにくくなる  
- 注意：CRSEは **因果の保証**や **欠落変数バイアスの除去**そのものではない（設計・固定効果・相互作用が主役）

---

## 3. テーマ1：時系列（X年春の施策がY年春で再現するか？）

### 3.1 解決したい課題
- X年春の結果を根拠にY年春も踏襲し、効果が再現せずに機会損失・コスト増になる  
- 時系列では同一単位（店舗など）内の自己相関、同一時点の共通ショックで「見かけの有意」が起きやすい  

### 3.2 データ構造（例）
- 店舗 $i$ × 週 $t$（または日）  
- 施策ダミー $D_{it}$（春キャンペーン期間=1）  
- 年ダミー $Y_t$（Y年=1）  

### 3.3 推奨モデル（再現性＝年差を相互作用で検証）
$$
y_{it} = \alpha + \beta D_{it} + \gamma (D_{it}\times Y_t) + \mu_i + \tau_t + u_{it}
$$
- $\beta$：X年の効果  
- $\beta+\gamma$：Y年の効果  
- $\gamma$：再現性の差（Y年で効き方が変わったか）  

### 3.4 クラスタリング設計（推奨）
- **2方向クラスタ（店舗×週）**：  
  - 店舗内の系列相関（同一店舗の誤差相関）  
  - 同一週の共通ショック（市場・天候・ニュース）  
  を同時に許容して推論を硬くする  

### 3.5 施策判断への落とし込み
- $\beta+\gamma$ が十分にプラス：踏襲（ただし監視KPIを定義）  
- $\gamma<0$ が明確：前年踏襲を停止、設計刷新（訴求・チャネル・条件変更）  
- $\beta+\gamma$ が不確実：縮小実施＋テスト設計（対象絞り、A/Bや段階導入）  

---

## 4. テーマ2：研修の効果測定（人事）

### 4.1 解決したい課題
- 研修投資の正当性が説明できず予算が縮小する  
- 部署・上司・受講グループの運用差が成果に強く影響し、研修効果と混同される  

### 4.2 データ構造（例）
- 個人 $i$ × 期 $t$（研修前後の評価や成果、離職など）  
- 受講 $Train_{it}$、年度 $Year_t$、所属部署 $dept(i,t)$  

### 4.3 推奨モデル（最小形）
$$
y_{i,t} = \alpha + \beta Train_{i,t} + \gamma(Train_{i,t}\times Year_t) + \mu_{\text{dept}(i,t)} + \tau_t + u_{i,t}
$$
- 研修の年度再現性は $\gamma$ で検証  

### 4.4 クラスタリング設計（例）
- 部署でクラスタ（部署運用の共通ショック）  
- 反復観測があるなら個人でクラスタ（個人特性の残差相関）  
- 状況により 2方向（部署×期）  

### 4.5 アクション例
- CRSEで研修効果が弱い：全社展開ではなく「対象絞り」「OJT連動」「上司関与」など設計側へ  
- 年度で効果が変動：前年踏襲をやめ、内容や運用の更新を必須化  
- 部署差が支配的：研修以前に育成運用（面談・目標・アサイン）の標準化がボトルネック  

---

## 5. テーマ3：予算差異（Budget vs Actual）のドライバー分析（経理・企画）

### 5.1 解決したい課題
- 差異説明が後付け化し、毎月の説明品質が不安定  
- ドライバーを誤認して、次年度予算や統制（投資配分）を誤る  
- 部門ごとの計上・見積り癖で残差が部門内に相関し、見かけの有意が出やすい  

### 5.2 データ構造（例）
- 部門 $d$ × 月 $t$  
- 目的変数：差異額 $\Delta_{d,t} = Actual - Budget$（または差異率）  
- 説明変数：為替、原料、市況、数量、単価、稼働率など $x_{d,t}$  

### 5.3 推奨モデル
$$
\Delta_{d,t} = \alpha + x'_{d,t}\beta + (x'_{d,t}\times Year_t)\gamma + \mu_d + \tau_t + u_{d,t}
$$
- $\mu_d$：部門固有の運用癖  
- $\tau_t$：月の共通ショック  
- 年度で係数が変わるなら相互作用で吸収  

### 5.4 クラスタリング設計（推奨）
- **2方向クラスタ（部門×月）**  
  - 部門内の残差相関（運用癖・計上タイミング）  
  - 月の共通ショック（全社景況、制度変更）  

### 5.5 アクション例
- 通常SEで有意→CRSEで非有意：原因帰属を保留、説明変数の再設計・追加データで再評価  
- 年度で感度が変化：翌年度は「前年係数踏襲禁止」、係数の年度更新をルール化  
- 部門固定効果が支配的：制度・計上ルール・見積プロセスの標準化や監査設計を優先  

---

## 6. テーマ4：PR施策と指標（広報）

### 6.1 解決したい課題
- 露出は増えたが、流入・問い合わせ・好意度の説明が弱い  
- 媒体ごとの特性（読者層・編集方針）で反応が似て動き、見かけの有意が出やすい  
- 単発のバズに引っ張られて投資配分を誤る  

### 6.2 データ構造（例）
- 媒体 $m$ × 週 $t$  
- 目的変数：流入、問い合わせ、好意度  
- 説明変数：露出量、記事タイプ、配信面など  

### 6.3 推奨モデル（例）
$$
y_{m,t} = \alpha + \beta Exposure_{m,t} + \gamma(Exposure_{m,t}\times Year_t) + \mu_m + \tau_t + u_{m,t}
$$

### 6.4 クラスタリング設計（推奨）
- 2方向クラスタ（媒体×週）  
- 露出効果の年差を相互作用で検証  

### 6.5 アクション例
- CRSEで露出効果が不確実：総量ではなく媒体別・記事タイプ別の配分最適化へ  
- 年差が大：前年の勝ち媒体固定をやめ、毎年テスト枠を確保して更新  
- 媒体固定効果が強い：媒体地力の差を前提に、コンテンツ適合（訴求・文脈）側へ投資  

---

## 7. 実装コード（Python/R）：2ケースのみ

### 7.1 Python（時系列：店舗×週、年×施策、2方向クラスタ）
依存：`numpy`, `pandas`, `statsmodels`

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups

# ----------------------------
# 疑似データ（店舗×週、2年）
# ----------------------------
rng = np.random.default_rng(0)
n_store = 50
n_week = 104  # 52週×2年

df = pd.MultiIndex.from_product(
    [range(n_store), range(n_week)],
    names=["store", "week"]
).to_frame(index=False)

df["year"] = (df["week"] >= 52).astype(int)  # 0=X年, 1=Y年
df["week_in_year"] = df["week"] % 52

# 春キャンペーン：週10〜20
df["D"] = ((df["week_in_year"] >= 10) & (df["week_in_year"] <= 20)).astype(int)

# 真の効果：X年は2.0、Y年は0.5（再現性低下）
beta_x, beta_y = 2.0, 0.5

# 固定効果（店舗/週）
store_fe = rng.normal(0, 3, size=n_store)
week_fe  = rng.normal(0, 2, size=n_week)
df["mu_store"] = df["store"].map(dict(enumerate(store_fe)))
df["tau_week"] = df["week"].map(dict(enumerate(week_fe)))

# 誤差：店舗内AR(1) + 週共通ショック
rho = 0.6
common = rng.normal(0, 1.5, size=n_week)

u = np.zeros(len(df))
for s in range(n_store):
    idx = df.index[df["store"] == s].to_numpy()
    e = rng.normal(0, 1.0, size=n_week)
    ar = np.zeros(n_week)
    for t in range(n_week):
        ar[t] = (rho * ar[t-1] if t > 0 else 0.0) + e[t]
    u[idx] = ar + common

df["u"] = u
df["true_effect"] = np.where(df["year"] == 0, beta_x, beta_y) * df["D"]
df["y"] = 10 + df["mu_store"] + df["tau_week"] + df["true_effect"] + df["u"]

# ----------------------------
# 推定：年×施策 + 店舗FE + 週FE
# ----------------------------
m = smf.ols("y ~ D + D:year + C(store) + C(week)", data=df).fit()

# 2方向クラスタ（店舗×週）
V_2way = cov_cluster_2groups(m, df["store"], df["week"])
se_2way = np.sqrt(np.diag(V_2way))

beta = m.params["D"]
gamma = m.params["D:year"]
effect_y = beta + gamma

print("beta (X year effect) =", beta)
print("gamma (Y-X diff)     =", gamma)
print("Y year effect        =", effect_y)

print("SE_2way(beta)  =", se_2way[m.params.index.get_loc("D")])
print("SE_2way(gamma) =", se_2way[m.params.index.get_loc("D:year")])
```

### 7.2 Python（予算差異：部門×月、ドライバー、2方向クラスタ）
例として主要ドライバーを3つ（fx・raw・volume）にする。

```python
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.sandwich_covariance import cov_cluster_2groups

rng = np.random.default_rng(1)
n_dept = 30
n_month = 36  # 3年
df = pd.MultiIndex.from_product(
    [range(n_dept), range(n_month)],
    names=["dept", "month"]
).to_frame(index=False)

df["year"] = (df["month"] >= 24).astype(int)  # 簡略：最後の1年をY年扱い

# ドライバー（例）
df["fx"] = rng.normal(0, 1, size=len(df))
df["raw"] = rng.normal(0, 1, size=len(df))
df["volume"] = rng.normal(0, 1, size=len(df))

# 固定効果：部門の運用癖、月の共通ショック
dept_fe = rng.normal(0, 2, size=n_dept)
month_fe = rng.normal(0, 1.5, size=n_month)
df["mu_dept"] = df["dept"].map(dict(enumerate(dept_fe)))
df["tau_month"] = df["month"].map(dict(enumerate(month_fe)))

# 真の係数（年度で変化する想定：Y年でfx感度が変わる）
b_fx, b_raw, b_vol = 1.2, 0.8, 1.5
g_fx = -0.7  # Y年でfxの効きが弱まる（再現性差）

# 誤差：部門内に相関 + 月共通ショック
common = rng.normal(0, 1.0, size=n_month)
u = rng.normal(0, 1.0, size=len(df))
u += df["month"].map(dict(enumerate(common)))  # 月の共通ショック
u += df["dept"].map(dict(enumerate(rng.normal(0, 0.8, size=n_dept))))  # 部門成分

df["Delta"] = (
    5
    + df["mu_dept"] + df["tau_month"]
    + b_fx * df["fx"] + b_raw * df["raw"] + b_vol * df["volume"]
    + g_fx * (df["fx"] * df["year"])
    + u
)

# 推定：ドライバー + ドライバー×年 + 部門FE + 月FE
m = smf.ols("Delta ~ fx + raw + volume + fx:year + C(dept) + C(month)", data=df).fit()

# 2方向クラスタ（部門×月）
V_2way = cov_cluster_2groups(m, df["dept"], df["month"])
se_2way = np.sqrt(np.diag(V_2way))

print(m.params[["fx", "fx:year", "raw", "volume"]])
print("SE_2way(fx)      =", se_2way[m.params.index.get_loc("fx")])
print("SE_2way(fx:year) =", se_2way[m.params.index.get_loc("fx:year")])
```

### 7.3 R（時系列：店舗×週、年×施策、2方向クラスタ）
依存：`fixest`, `data.table`

```r
library(fixest)
library(data.table)

set.seed(0)
n_store <- 50
n_week <- 104

dt <- CJ(store = 0:(n_store-1), week = 0:(n_week-1))
dt[, year := as.integer(week >= 52)]
dt[, week_in_year := week %% 52]
dt[, D := as.integer(week_in_year >= 10 & week_in_year <= 20)]

beta_x <- 2.0
beta_y <- 0.5

store_fe <- rnorm(n_store, 0, 3)
week_fe  <- rnorm(n_week, 0, 2)
dt[, mu_store := store_fe[store+1]]
dt[, tau_week := week_fe[week+1]]

rho <- 0.6
common <- rnorm(n_week, 0, 1.5)

# 店舗内AR(1) + 週共通ショック
dt[, u := {
  e <- rnorm(n_week, 0, 1.0)
  ar <- numeric(n_week)
  for (t in 1:n_week) {
    ar[t] <- (if (t==1) 0 else rho*ar[t-1]) + e[t]
  }
  ar + common
}, by = store]

dt[, true_effect := ifelse(year==0, beta_x, beta_y) * D]
dt[, y := 10 + mu_store + tau_week + true_effect + u]

# 年別にDの効果を推定（基準年=0）
fit <- feols(y ~ i(year, D, ref = 0) | store + week,
             data = dt,
             vcov = ~ store + week)  # 2方向クラスタ

summary(fit)
```

### 7.4 R（予算差異：部門×月、ドライバー、2方向クラスタ）
依存：`fixest`, `data.table`

```r
library(fixest)
library(data.table)

set.seed(1)
n_dept <- 30
n_month <- 36

dt <- CJ(dept = 0:(n_dept-1), month = 0:(n_month-1))
dt[, year := as.integer(month >= 24)]  # 最後の1年をY年扱い

dt[, fx := rnorm(.N)]
dt[, raw := rnorm(.N)]
dt[, volume := rnorm(.N)]

dept_fe <- rnorm(n_dept, 0, 2)
month_fe <- rnorm(n_month, 0, 1.5)
dt[, mu_dept := dept_fe[dept+1]]
dt[, tau_month := month_fe[month+1]]

b_fx <- 1.2; b_raw <- 0.8; b_vol <- 1.5
g_fx <- -0.7

common <- rnorm(n_month, 0, 1.0)
dt[, u := rnorm(.N, 0, 1.0) + common[month+1] + rnorm(n_dept, 0, 0.8)[dept+1]]

dt[, Delta :=
      5 + mu_dept + tau_month +
      b_fx*fx + b_raw*raw + b_vol*volume +
      g_fx*(fx*year) + u
]

# 年度でfx感度が変わる（fx×year）を推定
fit <- feols(Delta ~ fx + raw + volume + fx:year | dept + month,
             data = dt,
             vcov = ~ dept + month)  # 2方向クラスタ

summary(fit)
```

---

## 8. 最終チェック（運用上の結論の出し方）
- **年差（相互作用）が有意で悪化**：前年踏襲を止め、設計刷新（条件・訴求・運用）  
- **CRSEで有意が消える**：全社展開を保留し、ターゲティング・追加検証・運用改善へ  
- **効果量が小さい**：統計的に有意でも費用対効果で中止候補（効果量を意思決定軸に入れる）  
