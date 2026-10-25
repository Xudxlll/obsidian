---
course: AMA515A Forecasting and Applied Time Series Analysis
source: Tutorial 1.pdf
pages: 4
cssclasses: [ama-inline-translations]
---

# Tutorial 1 题目

原始资料：[Tutorial 1.pdf](<附件/Tutorial 1.pdf>)

配套资料：[[02 - Tutorial 1 Answers（英文原文与折叠译文）|印刷答案]] · [[03 - Ex 1 Q1（手写解答）|Q1 手写解答]] · [[04 - Ex 1 Q2-Q3（手写解答）|Q2–Q3 手写解答]] · [[05 - Ex 1 Q4-Q6（手写解答）|Q4–Q6 手写解答]] · [[00 - Tutorial 1 资料索引|资料索引]]

## PDF p.1

Time series Ex.1 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">时间序列练习 1。</span></details>

1. Using the time-series data on retail sales ($Y_t$) and disposable income ($X_t$) of a country in Table 1 calculate the following: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 利用表 1 中某国零售额（Yₜ）与可支配收入（Xₜ）的时间序列数据，计算以下各项。</span></details>

(a) The ex post forecasts (2006-2010) for the naive, three-period moving average, trend, and causal models. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）分别使用朴素模型、三期移动平均模型、趋势模型和因果模型，计算 2006—2010 年的事后预测。</span></details>

(b) The MAE, MAPE, MSE, and RMSE for the ex post period, 2006-2010. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）计算事后预测期（2006—2010 年）的平均绝对误差（MAE）、平均绝对百分比误差（MAPE）、均方误差（MSE）和均方根误差（RMSE）。</span></details>

(c) Is your choice of the "best" model for the ex post period different from the decision that was made when evaluating over the estimation period? Discuss. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）你在事后预测期选择的“最佳”模型，是否与在估计期内评价时作出的选择不同？请讨论。</span></details>

TABLE 1 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表 1。</span></details>

Historical data for retail sales and disposable personal income (billions of dollars) of a country <details class="translation-details"><summary>中文译文</summary><span class="translation-body">某国零售额与个人可支配收入的历史数据（单位：十亿美元）。</span></details>

| Year | RET_SALES | DIS_PY |
| --- | ---: | ---: |
| 1990 | 375.2 | 710.0 |
| 1991 | 414.2 | 771.8 |
| 1992 | 458.5 | 834.8 |
| 1993 | 511.9 | 943.8 |
| 1994 | 542.0 | 1,033.7 |
| 1995 | 588.1 | 1,138.4 |
| 1996 | 656.4 | 1,248.8 |
| 1997 | 722.5 | 1,375.3 |
| 1998 | 804.2 | 1,546.5 |
| 1999 | 896.8 | 1,724.6 |
| 2000 | 957.4 | 1,914.3 |
| 2001 | 1,038.7 | 2,121.8 |
| 2002 | 1,069.3 | 2,255.1 |
| 2003 | 1,167.9 | 2,424.9 |
| 2004 | 1,281.7 | 2,662.1 |
| 2005 | 1,365.8 | 2,832.1 |
| 2006 | 1,435.9 | 3,007.6 |
| 2007 | 1,521.4 | 3,184.2 |
| 2008 | 1,629.2 | 3,467.9 |
| 2009 | 1,733.7 | 3,710.0 |
| 2010 | 1,807.2 | 3,949.1 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Year＝年份；RET_SALES＝零售额；DIS_PY＝个人可支配收入。</span></details>

<details><summary>查看 PDF p.1 原页</summary>

![[附件/tut1-questions-p01.png]]

</details>

## PDF p.2

2. Suppose that you work for an automobile association that publishes two-year forecasts for the price of leaded gasoline in its annual publication. You have collected the following information on the price of crude oil ($X_t$, dollars per barrel); and the price of leaded gasoline ($Y_t$, dollars per gallon) in order to develop the best forecasting model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 假设你在一家汽车协会工作，该协会在年度刊物中发布未来两年的含铅汽油价格预测。为了建立最佳预测模型，你收集了以下原油价格（Xₜ，美元／桶）及含铅汽油价格（Yₜ，美元／加仑）的资料。</span></details>

| Year | Crude oil | Price of leaded regular |
| --- | ---: | ---: |
| 1995 | 10.38 | 0.57 |
| 1996 | 10.89 | 0.59 |
| 1997 | 11.96 | 0.62 |
| 1998 | 19.46 | 0.63 |
| 1999 | 17.72 | 0.86 |
| 2000 | 28.07 | 1.19 |
| 2001 | 35.24 | 1.31 |
| 2002 | 31.87 | 1.22 |
| 2003 | 28.99 | 1.16 |
| 2004 | 28.63 | 1.13 |
| 2005 | 26.75 | 1.12 |
| 2006 | 14.55 | 0.86 |
| 2007 | 17.90 | 0.90 |
| 2008 | 14.71 | 0.90 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Year＝年份；Crude oil＝原油价格；Price of leaded regular＝普通含铅汽油价格。</span></details>

(a) Generate forecasts for the price of leaded gasoline using a naive model and a three-period simple moving average over the period 1998-2008. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）使用朴素模型和三期简单移动平均模型，生成 1998—2008 年的含铅汽油价格预测。</span></details>

(b) Suppose a trend model estimated over the period 1998-2008 yields the following result: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）假设利用 1998—2008 年数据估计的趋势模型得到以下结果：</span></details>

$$
P_{\mathrm{leaded}}=1.022+0.001*\mathrm{TIME}
$$

Generate forecasts for this model. Note that 1998-2008 is recoded as 1-11. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用该模型生成预测值。注意：将 1998—2008 年重新编码为 1—11。</span></details>

(c) Suppose a causal model was estimated over the period 1998-2008; the price of leaded gasoline is a function of the price of oil: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）假设利用 1998—2008 年数据估计了一个因果模型；含铅汽油价格是原油价格的函数：</span></details>

$$
P_{\mathrm{leaded}}=0.444+0.025*P_{\mathrm{crude}}
$$

(d) Calculate the MSE, RMSE, MAE, and MAPE for each of the models. Which model is the best? Why? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）计算每个模型的 MSE、RMSE、MAE 和 MAPE。哪个模型最好？为什么？</span></details>

(e) Forecast the price of leaded gasoline for 2009 and 2010 using the naive model, the simple moving average model, and the trend model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（e）使用朴素模型、简单移动平均模型和趋势模型，预测 2009 年与 2010 年的含铅汽油价格。</span></details>

<details><summary>查看 PDF p.2 原页</summary>

![[附件/tut1-questions-p02.png]]

</details>

## PDF p.3

3. Use the following data on dividends per share (DPS) and earnings per share (EPS) for Weyerhaeuser Company: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. 使用 Weyerhaeuser 公司以下每股股息（DPS）与每股收益（EPS）数据：</span></details>

| Year | DPS | EPS |
| --- | ---: | ---: |
| 1995 | .53 | 1.01 |
| 1996 | .53 | 1.55 |
| 1997 | .53 | 1.53 |
| 1998 | .57 | 2.12 |
| 1999 | .72 | 2.68 |
| 2000 | .87 | 1.65 |
| 2001 | .87 | 1.11 |
| 2002 | .87 | 0.60 |
| 2003 | .87 | 0.91 |
| 2004 | .87 | 1.24 |
| 2005 | .87 | 0.88 |
| 2006 | .87 | 1.27 |
| 2007 | .90 | 2.12 |
| 2008 | 1.15 | 2.68 |
| 2009 | 1.20 | 2.83 |
| 2010 | 1.20 | 1.87 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：Year＝年份；DPS＝每股股息；EPS＝每股收益。</span></details>

(a) Generate naive and three-period moving average forecasts for dividends paid per share over the estimation period 1998-2007. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）使用朴素模型和三期移动平均模型，生成估计期（1998—2007 年）内的每股股息预测。</span></details>

(b) Suppose a trend model estimated over the period 1998-2007 yields the following result: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）假设利用 1998—2007 年数据估计的趋势模型得到以下结果：</span></details>

$$
\mathrm{DPS}_t=0.694+0.024*\mathrm{time}
$$

Generate the forecast values for dividends per share over the period 1998-2007. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">生成 1998—2007 年的每股股息预测值。</span></details>

(c) Suppose a causal model is estimated over the period 1998-2007; dividends per share are a function of earnings per share: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）假设利用 1998—2007 年数据估计一个因果模型；每股股息是每股收益的函数：</span></details>

$$
\mathrm{DPS}_t=0.961-0.091*\mathrm{EPS}.
$$

Generate the forecast values for dividends per share over the period 1998-2007. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">生成 1998—2007 年的每股股息预测值。</span></details>

<details><summary>查看 PDF p.3 原页</summary>

![[附件/tut1-questions-p03.png]]

</details>

## PDF p.4

(d) Calculate the MAE, MAPE. MSE, and RMSE for the naive, the three-period moving average, the time trend, and the causal models. Which model is the best? By what measure? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）计算朴素模型、三期移动平均模型、时间趋势模型和因果模型的 MAE、MAPE、MSE 与 RMSE。哪个模型最好？依据什么指标？</span></details>

(e) Generate the ex post forecasts for dividends per share for 2008, 2009, and 2010. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（e）生成 2008 年、2009 年和 2010 年的每股股息事后预测。</span></details>

(f) Calculate the MAE, MAPE, MSE, and RMSE for the ex post period. Which model is the best? By what measure? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（f）计算事后预测期内的 MAE、MAPE、MSE 与 RMSE。哪个模型最好？依据什么指标？</span></details>

(g) What conclusions can you draw about model evaluation over the estimation period and its predictive accuracy over an ex post forecast period? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（g）关于估计期内的模型评价及其在事后预测期内的预测准确性，你能得出什么结论？</span></details>

4. Suppose $\operatorname{Cov}(X_t,X_{t-k})=\gamma_k$ is free of $t$ but that $\operatorname{E}(X_t)=3t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4. 假设 Xₜ 与 Xₜ₋ₖ 的协方差为 γₖ，与 t 无关，但 Xₜ 的期望为 3t。</span></details>

(a) Is $\{X_t\}$ stationary? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）序列 {Xₜ} 是否平稳？</span></details>

(b) Let $Z_t=7-3t+X_t$. Is $Z_t$ stationary? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）令 Zₜ＝7−3t＋Xₜ。Zₜ 是否平稳？</span></details>

5. Suppose $Y_t=A+X_t$, where $\{X_t\}$ is stationary and $A$ is random but independent of $\{X_t\}$. Find the mean and covariance function for $\{Y_t\}$ in terms of the mean and autocovariance function for $\{X_t\}$ and the mean and variance of $A$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">5. 假设 Yₜ＝A＋Xₜ，其中 {Xₜ} 平稳，A 是与 {Xₜ} 独立的随机变量。用 {Xₜ} 的均值与自协方差函数，以及 A 的均值与方差，表示 {Yₜ} 的均值函数和协方差函数。</span></details>

6. Let $Y_1=\theta_0+e_1$, and for $t>1$ define $Y_t$ recursively by $Y_t=\theta_0+Y_{t-1}+e_t$. Here $\theta_0$ is a constant and $\{e_t\}$ is a white noise sequence. The process $\{Y_t\}$ is called a random walk with drift. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">6. 令 Y₁＝θ₀＋e₁；当 t &gt; 1 时，递归定义 Yₜ＝θ₀＋Yₜ₋₁＋eₜ。这里 θ₀ 是常数，{eₜ} 是白噪声序列。过程 {Yₜ} 称为带漂移的随机游走。</span></details>

(a) Show that $Y_t$ my be rewritten by $Y_t=t\theta_0+e_t+e_{t-1}+\cdots+e_1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）证明 Yₜ 可以改写为 tθ₀＋eₜ＋eₜ₋₁＋⋯＋e₁。</span></details>

(b) Find the mean function for $Y_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）求 Yₜ 的均值函数。</span></details>

(c) Find autocovariance function for $Y_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）求 Yₜ 的自协方差函数。</span></details>

> [!note] 原文保留
> Q6(a) 原页写作 “my be”，本笔记按原文保留；其语义按 “may be” 翻译。Q3(d) 中 “MAPE. MSE” 的标点也按原页保留。

<details><summary>查看 PDF p.4 原页</summary>

![[附件/tut1-questions-p04.png]]

</details>
