---
cssclasses:
  - course-bilingual
---

# Tutorial 5：题目与中文译文

原件：[[Tutorials/Tutorial 5/附件/ex5.pdf|Exercise 5 PDF]]；对应答案：[[02 - Tutorial 5 答案（原页）|老师提供的答案]]。公式与题号按原件保留。

## 第 1 题：AR(1) 预测

For an AR(1) model with $Y_t=12.2$, $\phi=-0.5$, and $\mu=10.8$,
<details class="translation-details"><summary>中文译文</summary><span class="translation-body">对于一个 AR(1) 模型，已知 Yₜ = 12.2、φ = −0.5、μ = 10.8。</span></details>

(a) Find $\hat Y_t(1)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">求一步预测值。</span></details>

(b) Calculate $\hat Y_t(2)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算两步预测值。</span></details>

(c) Calculate $\hat Y_t(10)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算十步预测值。</span></details>

## 第 2 题：AR(2) 销售预测

Suppose that annual sales (in millions of dollars) of ABC company follow the AR(2) model $Y_t=5+1.1Y_{t-1}-0.5Y_{t-2}+e_t$, with $\sigma_e^2=2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设 ABC 公司的年度销售额（单位：百万美元）服从上述 AR(2) 模型，误差方差为 2。</span></details>

(a) If sales for 2005, 2006, and 2007 were \$9 million, \$11 million, and \$10 million respectively, forecast sales for 2008 and 2009. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若 2005、2006 和 2007 年的销售额分别为 900 万、1100 万和 1000 万美元，预测 2008 年和 2009 年的销售额。</span></details>

(b) Show that $\psi_1=1.1$ for this model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明这个模型的 ψ₁ 等于 1.1。</span></details>

(c) Calculate 95% prediction limit for your forecast in part (a) for 2008. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算第 (a) 小题中 2008 年预测的 95% 预测区间。</span></details>

(d) If sales in 2008 turn out to be \$12 million, update your forecast for 2009. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">如果 2008 年的实际销售额为 1200 万美元，更新对 2009 年销售额的预测。</span></details>

## 第 3 题：带线性趋势的预测

Consider the model $Y_t=\beta_0+\beta_1t+X_t$, where $X_t=\phi X_{t-1}+e_t$. Assume that $\beta_0,\beta_1,\&\phi$ are known. Show that the minimum mean square error $m$-step ahead forecast can be written as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑上述模型，其中 β₀、β₁ 和 φ 均已知。证明最小均方误差意义下的 m 步预测可以写成下式。</span></details>

$$
\hat Y_t(m)=\beta_0+\beta_1(t+m)+\phi^m(Y_t-\beta_0-\beta_1t).
$$

## 第 4 题：季度季节模型

Based on quarterly data, a model of the form <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据季度数据，以下形式的模型已拟合到一个时间序列。</span></details>

$$
Y_t=Y_{t-4}+e_t-\theta_1 e_{t-1}-\theta_2 e_{t-2}
$$

has been fitted to a time series.

(a) Find the first four $\psi$-weights for this model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">求该模型的前四个 ψ 权重。</span></details>

(b) Suppose that $\theta_1=0.5,\theta_2=-0.25$, & $\sigma_e=1$. Find forecast for the next four quarters if data for the last four quarters are <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假设 θ₁ = 0.5、θ₂ = −0.25、σₑ = 1。最近四个季度的数据如下，求未来四个季度的预测。</span></details>

| Quarter | I | II | III | IV |
| --- | ---: | ---: | ---: | ---: |
| Series | 25 | 20 | 25 | 40 |
| residual | 2 | 1 | 2 | 3 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">Quarter：季度；Series：序列值；residual：残差。</span></details>

(c) Find 95% prediction interval for the forecast in (b). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">求第 (b) 小题预测的 95% 预测区间。</span></details>

## 第 5 题：季节模型的方差

Consider the model $Y_t=\Phi Y_{t-12}+e_t-\theta e_{t-1}$. Show that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑上述模型，证明其方差满足下式。</span></details>

$$
\operatorname{var}(Y_t)=\left(\frac{1+\theta^2}{1-\Phi^2}\right)\sigma_e^2.
$$

## 第 6 题：残差诊断

There is a data set deviations.csv in the Data folder of AMA515A. It has 57 time series observations (in coded units) which are deviations from a target value in an industrial process. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 的 Data 文件夹中有一个 deviations.csv 数据集，包含 57 个时间序列观测值（以编码单位表示），代表某工业过程相对于目标值的偏差。</span></details>

(a) It is suggested to use an AR(1) process without constant term to model the data, since they are deviations. Use Excel or any package to estimate the AR coefficient. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于数据是偏差，建议使用不带常数项的 AR(1) 过程建模。使用 Excel 或其他软件估计 AR 系数。</span></details>

(b) The first 16 autocorrelation coefficients of the residuals from the AR(1) model are shown below: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AR(1) 模型残差的前 16 个自相关系数如下。</span></details>

| Lag | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ACF | 0.000 | 0.063 | 0.027 | -0.205 | -0.006 | -0.129 | 0.026 | -0.147 |

| Lag | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ACF | 0.019 | 0.022 | -0.132 | -0.022 | 0.051 | -0.031 | 0.012 | -0.096 |

Calculate the Lung-Box statistic using all the information above. What should be the degrees of freedom for the statistic, and is it significant at 5% significance level? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">利用以上全部信息计算 Ljung–Box 统计量。该统计量的自由度应是多少？它在 5% 显著性水平下是否显著？</span></details>

> [!note] 原文拼写
> 原题写作 “Lung-Box”，通常称为 Ljung–Box 检验。数据文件是否在本地存在另需核对。
