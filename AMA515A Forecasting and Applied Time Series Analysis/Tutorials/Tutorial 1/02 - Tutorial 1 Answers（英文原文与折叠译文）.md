---
course: AMA515A Forecasting and Applied Time Series Analysis
source: Tutorial 1 Answers.pdf
pages: 3
cssclasses: [ama-inline-translations]
---

# Tutorial 1 Answers

原始资料：[Tutorial 1 Answers.pdf](<附件/Tutorial 1 Answers.pdf>)

配套资料：[[01 - Tutorial 1 题目（英文原文与折叠译文）|题目]] · [[03 - Ex 1 Q1（手写解答）|Q1 手写解答]] · [[04 - Ex 1 Q2-Q3（手写解答）|Q2–Q3 手写解答]] · [[05 - Ex 1 Q4-Q6（手写解答）|Q4–Q6 手写解答]] · [[00 - Tutorial 1 资料索引|资料索引]]

> [!note] 版本与原文
> 本篇逐页保留印刷答案，不用手写版补齐或替换其中的内容；印刷版未列出的计算仍以原件为准。原文中的 “casual model” 按原文保留，中文按上下文译作“因果模型”。

## PDF p.1

Ans to Ex.1 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 1 答案。</span></details>

1. .(a) Table of expost forecasts: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.（a）事后预测表：</span></details>

| Data | Naïve | 3-point MA | Trend | Causal |
| ---: | ---: | ---: | ---: | ---: |
| 1435.9 | 1365.8 | 1271.8 | 1366.7 | 1444.15 |
| 1521.4 | 1435.9 | 1361.1 | 1433 | 1524.33 |
| 1629.2 | 1521.4 | 1441 | 1499.29 | 1653.13 |
| 1733.7 | 1629.2 | 1528.8 | 1565.59 | 1763.04 |
| 1807.2 | 1733.7 | 1628.1 | 1631.89 | 1871.59 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Data＝实际数据；Naïve＝朴素预测；3-point MA＝三点移动平均；Trend＝趋势模型；Causal＝因果模型。</span></details>

Note: Trend model and Causal model are based on observations between 1990 to 2005. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注：趋势模型和因果模型基于 1990—2005 年的观测数据。</span></details>

Trend equation: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">趋势方程：</span></details>

$$
y_t=239.63+66.3*t
$$

Regression eqn.: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回归方程：</span></details>

$$
y_t=78.7+0.454x_t
$$

(b) & (c) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）与（c）。</span></details>

Obviously the casual model is the best from the expost forecasts. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">从事后预测来看，显然因果模型最好。</span></details>

2. (a), (b), & (c) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.（a）、（b）与（c）。</span></details>

| Year | Data | Naïve | MA | Trend | Causal |
| --- | ---: | ---: | ---: | ---: | ---: |
| 98 | 0.63 | 0.62 | 0.59 | 1.023 | 0.931 |
| 99 | 0.86 | 0.63 | 0.61 | 1.024 | 0.887 |
| 00 | 1.19 | 0.86 | 0.70 | 1.025 | 1.146 |
| 01 | 1.31 | 1.19 | 0.89 | 1.026 | 1.325 |
| 02 | 1.22 | 1.31 | 1.12 | 1.027 | 1.241 |
| 03 | 1.16 | 1.22 | 1.24 | 1.028 | 1.169 |
| 04 | 1.13 | 1.16 | 1.23 | 1.029 | 1.16 |
| 05 | 1.12 | 1.13 | 1.17 | 1.030 | 1.113 |
| 06 | 0.86 | 1.12 | 1.14 | 1.031 | 0.808 |
| 07 | 0.90 | 0.86 | 1.04 | 1.032 | 0.892 |
| 08 | 0.90 | 0.90 | 0.96 | 1.033 | 0.812 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Year＝年份（两位数）；Data＝实际数据；Naïve＝朴素预测；MA＝移动平均；Trend＝趋势模型；Causal＝因果模型。</span></details>

Note: Time has been recoded, namely, 1998 to 2008 has been recoded as 1 to 11. Also the slope of the trend equation given is not accurate, but in the answer above I still use the given equation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注：时间已重新编码，即把 1998—2008 年重新编码为 1—11。另外，题目给定趋势方程的斜率并不准确，但上述答案仍使用给定方程。</span></details>

(d) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）。</span></details>

|  | Naïve | MA | Trend | causal |
| --- | ---: | ---: | ---: | ---: |
| MSE | 0.023 | 0.055 | 0.039 | 0.0096 |
| RMSE | 0.153 | 0.234 | 0.197 | 0.098 |
| MAE | 0.107 | 0.181 | 0.178 | 0.055 |
| MAPE | 10.55% | 17.24% | 19.14% | 7.11% |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">列为朴素、移动平均、趋势和因果模型；行为均方误差、均方根误差、平均绝对误差和平均绝对百分比误差。</span></details>

Causal model is best from all criteria. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">按所有评价指标，因果模型都是最好的。</span></details>

<details><summary>查看 PDF p.1 原页</summary>

![[附件/tut1-answers-p01.png]]

</details>

## PDF p.2

(e) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（e）。</span></details>

| Year | Naïve | MA | Trend |
| --- | ---: | ---: | ---: |
| 09 | 0.90 | 0.89 | 1.034 |
| 10 | 0.90 | 0.9 | 1.035 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Year＝年份（两位数）；Naïve＝朴素预测；MA＝移动平均；Trend＝趋势模型。</span></details>

3. (a), (b) & (c). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3.（a）、（b）与（c）。</span></details>

| Year | Data | Naïve | MA | Trend | Causal |
| --- | ---: | ---: | ---: | ---: | ---: |
| 98 | .57 | .53 | .53 | .718 | .768 |
| 99 | .72 | .57 | .54 | .742 | .717 |
| 00 | .87 | .72 | .61 | .766 | .811 |
| 01 | .87 | .87 | .72 | .790 | .860 |
| 02 | .87 | .87 | .82 | .814 | .906 |
| 03 | .87 | .87 | .87 | .838 | .878 |
| 04 | .87 | .87 | .87 | .862 | .848 |
| 05 | .87 | .87 | .87 | .886 | .881 |
| 06 | .87 | .87 | .87 | .910 | .845 |
| 07 | .90 | .87 | .87 | .934 | .768 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Year＝年份（两位数）；Data＝实际数据；Naïve＝朴素预测；MA＝移动平均；Trend＝趋势模型；Causal＝因果模型。</span></details>

(d) Naïve is best by all measures. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）按照所有评价指标，朴素模型最好。</span></details>

(e) Expost forecasts <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（e）事后预测。</span></details>

| Year | Naïve | MA | Trend | causal |
| --- | ---: | ---: | ---: | ---: |
| 08 | 0.9 | 0.88 | 0.958 | 0.717 |
| 09 | 1.15 | 0.97 | 0.982 | 0.703 |
| 10 | 1.2 | 1.08 | 1.006 | 0.791 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Year＝年份（两位数）；其余列依次为朴素、移动平均、趋势和因果模型的预测值。</span></details>

(f) & (g) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（f）与（g）。</span></details>

Naïve forecast is the 'best' by all criteria. The reason is due to the constancy of the dividend payment over the period. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">按所有评价指标，朴素预测都是“最佳”的。原因是该期间的股息支付较为恒定。</span></details>

4. (a) No, as mean depends on t. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.（a）不平稳，因为均值依赖于 t。</span></details>

(b) Yes, as $\operatorname{E}(Z_t)=7-3t+3t=7$, a constant. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）平稳，因为 Zₜ 的期望为 7−3t＋3t＝7，是常数。</span></details>

5. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5。</span></details>

$$
\operatorname{E}(Y_t)=\operatorname{E}(A)+\operatorname{E}(X_t)=\mu_A+\mu_X,
$$

free of t. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与 t 无关。</span></details>

$$
\begin{aligned}
\operatorname{Cov}(Y_t,Y_{t-k})&=\operatorname{cov}(A+X_t,A+X_{t-k})\\
&=\operatorname{cov}(A,A+X_{t-k})+\operatorname{cov}(X_t,A+X_{t-k})\\
&=\operatorname{var}(A)+\operatorname{cov}(X_t,X_{t-k}),
\end{aligned}
$$

free of t as $X_t$ is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 Xₜ 平稳，该协方差与 t 无关。</span></details>

6. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6。</span></details>

$$
\begin{aligned}
Y_t&=\theta_0+Y_{t-1}+e_t=\theta_0+\theta_0+Y_{t-2}+e_{t-1}+e_t\\
&=2\theta_0+Y_{t-2}+e_{t-1}+e_t\\
&=\cdots\\
&=(t-1)\theta_0+Y_1+e_t+e_{t-1}+\cdots+e_2\\
&=t\theta_0+e_t+\cdots+e_1
\end{aligned}
$$

<details><summary>查看 PDF p.2 原页</summary>

![[附件/tut1-answers-p02.png]]

</details>

## PDF p.3

$$
\operatorname{E}(Y_t)=t\theta_0,
$$

dependent on t <details class="translation-details"><summary>中文译文</summary><span class="translation-body">依赖于 t。</span></details>

$$
\begin{aligned}
\operatorname{cov}(Y_t,Y_{t-k})
&=\operatorname{cov}\left(t\theta_0+\sum_{i=1}^{t}e_i,\ (t-k)\theta_0+\sum_{i=1}^{t-k}e_i\right)\\
&=(t-k)\sigma_e^2,
\end{aligned}
$$

dependent on t <details class="translation-details"><summary>中文译文</summary><span class="translation-body">依赖于 t。</span></details>

<details><summary>查看 PDF p.3 原页</summary>

![[附件/tut1-answers-p03.png]]

</details>
