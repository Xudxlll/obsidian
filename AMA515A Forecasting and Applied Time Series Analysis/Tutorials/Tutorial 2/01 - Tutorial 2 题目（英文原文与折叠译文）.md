---
course: "AMA515A Forecasting and Applied Time Series Analysis"
source: "Tutorial 2.pdf"
pages: 3
cssclasses: [ama-inline-translations]
---

# Tutorial 2 题目

原始资料：[[附件/Tutorial 2.pdf|PDF 原件]] · [[00 - Tutorial 2 资料索引|资料索引]] · [[02 - Tutorial 2 Answers（英文原文与折叠译文）|印刷答案]]

## PDF p.1

Time Series Ex.2 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">时间序列练习 2。</span></details>

1. It was determined that a quadratic model was the best fit of the trend for 12 years of data. The data are <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 已确定二次模型最适合拟合这 12 年数据的趋势。数据如下。</span></details>

$$
22,18,21,19,17,16,18,21,20,23,22,25
$$

The results from running a multiple regression on these data arc as follows: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对这些数据进行多元回归的结果如下。</span></details>

$$
\operatorname{corr}(Y,t)=.4839\quad b_0=22.95456\quad b_1=-1.8317
$$

t-test for $b_1=-3.2301$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">b₁ 的 t 检验统计量为 −3.2301。</span></details>

$$
\operatorname{corr}(Y,t^2)=.6307\quad b_2=0.1683
$$

t-test for $b_2=3.9642$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">b₂ 的 t 检验统计量为 3.9642。</span></details>

$$
R^2=0.72\quad R_{\mathrm{adj}}^2=0.6592\quad s_e=1.5513
$$

F-test = 11.6362 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">F 检验统计量为 11.6362。</span></details>

Durbin-Watson = 2.3913 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Durbin–Watson 统计量为 2.3913。</span></details>

Correction factor for the 13th time period = 1.438 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 13 期的修正因子为 1.438。</span></details>

Error terms for the model: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">模型的误差项如下。</span></details>

| $t$ | $e_t$ | $t$ | $e_t$ | $t$ | $e_t$ |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 0.7088 | 5 | -1.004 | 9 | -0.1044 |
| 2 | -1.9645 | 6 | -2.024 | 10 | 1.529 |
| 3 | 2.0254 | 7 | -0.381 | 11 | -1.1743 |
| 4 | 0.6788 | 8 | 1.9256 | 12 | -0.9143 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">t 为期数，eₜ 为该期误差。</span></details>

(a) What is the equation for trend? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 趋势方程是什么？</span></details>

(b) Use the Durbin-Watson statistic to test whether the residuals are correlated or not? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 使用 Durbin–Watson 统计量检验残差是否存在相关性。</span></details>

(c) If appropriate, determine the statistical fitness of the model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(c) 如果适用，判断模型在统计意义上的拟合情况。</span></details>

(d) Find and interpret Theil's U. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(d) 求出并解释 Theil 的 U。</span></details>

(e) Was the quadratic a good choice to model the trend in the data? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(e) 用二次模型描述数据趋势是否是一个好的选择？</span></details>

(f) Find the appropriate forecast (point and/or interval) for the 13th time period. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(f) 求第 13 期适当的预测（点预测及／或区间预测）。</span></details>

2. For each of the following sets of data, determine whether a model can be constructed either as a linear trend or a curvilinear trend model by using the following steps: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 对以下每组数据，按下列步骤判断能否建立线性趋势模型或曲线趋势模型。</span></details>

<details><summary>本页原图（核对用）</summary>

![[附件/tut2-questions-p01.png]]

</details>

## PDF p.2

i. Plot the time-series data versus time. Plot first differences of your data. If necessary, plot second differences. Based upon your graphs, what model, either linear or curvilinear, would be appropriate? Explain. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">i. 绘制时间序列数据相对于时间的图，再绘制一阶差分图；必要时绘制二阶差分图。根据图形，线性模型或曲线模型中哪一种更合适？请说明。</span></details>

ii. Calculate the correlation coefficient between the time-series variable and time. Test for statistical significance. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ii. 计算时间序列变量与时间之间的相关系数，并检验其统计显著性。</span></details>

iii. If your choice is linear, run a simple bivariate regression against time. Following the sections outlined in this chapter, test the model for the following: Durbin-Watson statistic; statistical significance of the slope coefficient; statistical significance of the overall regression. Determine if the forecast errors are normally distributed. Calculate the forecast summary statistics, MAE, MAPE, R~SE, and Theil's U. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">iii. 如果选择线性模型，对时间进行简单的双变量回归。按本章所列各节检验模型：Durbin–Watson 统计量、斜率系数的统计显著性以及整体回归的统计显著性。判断预测误差是否服从正态分布。计算预测汇总统计量 MAE、MAPE、R~SE 和 Theil 的 U。</span></details>

> [!note] 原文字符核对
> 本行原 PDF 将通常写作 RMSE 的指标印为形似 `R~SE` 的字符组合；此处按可见原文保留，请结合本页原图核对。

iv. If your choice is nonlinear, justify which of the nonlinear specifications (first differences, exponential, logistic, quadratic, or cubic) is appropriate. Your justification should include the appropriate statistical tests of the model, and calculation of the forecast summary statistics (see EX.1). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">iv. 如果选择非线性模型，请说明哪一种非线性设定（一阶差分、指数、逻辑斯蒂、二次或三次）合适。论证应包括适当的模型统计检验，以及预测汇总统计量的计算（见练习 1）。</span></details>

v. Using the correct model (either linear or nonlinear), forecast the next three time periods. Construct the 95 percent prediction interval for each forecast. Graph your results: actual values, forecast values, and the 95 percent prediction interval. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">v. 使用正确的模型（线性或非线性）预测接下来三期，并为每个预测构造 95% 预测区间。将实际值、预测值和 95% 预测区间绘制在图中。</span></details>

(a). The following is revenue data, in millions of dollars, for 1981-1990 from Springs Inc., a textile manufacturer in Fort Mill, South Carolina: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a). 下表是位于南卡罗来纳州 Fort Mill 的纺织制造商 Springs Inc. 在 1981—1990 年的收入数据，单位为百万美元。</span></details>

| Year | Sales |
| ---: | ---: |
| 81 | 917.0 |
| 82 | 874.5 |
| 83 | 894.4 |
| 84 | 945.0 |
| 85 | 1,013.5 |
| 86 | 1,505.0 |
| 87 | 1,661.1 |
| 88 | 1,824.8 |
| 89 | 1,909.3 |
| 90 | 1,878.0 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：年份、销售额（百万美元）。</span></details>

(b). The following table presents the total fish catch (in millions of pounds) in the United States: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b). 下表列出美国的渔获总量，单位为百万磅。</span></details>

| Year | Fish |
| ---: | ---: |
| 1972 | 4,806 |
| 1973 | 4,858 |
| 1974 | 4,967 |
| 1975 | 4,877 |
| 1976 | 5,388 |
| 1977 | 5,271 |
| 1978 | 6,028 |
| 1979 | 6,267 |
| 1980 | 6,482 |
| 1981 | 5,977 |
| 1982 | 6,367 |
| 1983 | 6,439 |
| 1984 | 6,438 |
| 1985 | 6,258 |
| 1986 | 6,031 |
| 1987 | 6,896 |
| 1988 | 7,192 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：年份、渔获量（百万磅）。</span></details>

<details><summary>本页原图（核对用）</summary>

![[附件/tut2-questions-p02.png]]

</details>

## PDF p.3

3. Column 2 of the attached table is the yearly tobacco production of a certain country from 1980-1991. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. 附表第 2 列是某国 1980—1991 年的年度烟草产量。</span></details>

| Year | Tab. Prodn | SES forecast | MA3 forecast |
| ---: | ---: | ---: | ---: |
| 80 | 2315 | | |
| 81 | 2344 | | |
| 82 | 2228 | | |
| 83 | 1855 | | |
| 84 | 1887 | | |
| 85 | 1968 | | |
| 86 | 1710 | 1787 | 1903.33 |
| 87 | 1804 | | |
| 88 | 1906 | | |
| 89 | 1705 | | |
| 90 | 1749 | | |
| 91 | 1742 | | |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头：年份、烟草产量、简单指数平滑预测、三点移动平均预测。</span></details>

We want to compare the forecasting performance of two methods, simple exponential smoothing (SES) and 3-points moving average(MA3). Forecast values for the year 1986 were given. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">我们希望比较简单指数平滑（SES）与三点移动平均（MA3）两种方法的预测表现。1986 年的预测值已经给出。</span></details>

(a) Using the smoothing constant 0.8, calculate SES forecasts for 1987 to 1991. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(a) 使用平滑常数 0.8，计算 1987—1991 年的 SES 预测值。</span></details>

(b) Calculate MA3 forecasts for 1987 to 1991. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(b) 计算 1987—1991 年的 MA3 预测值。</span></details>

(c) Calculate the SSE (total sum of squares for forecast errors) for both methods during 1986-1991 and hence conclude which method is better. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">(c) 计算两种方法在 1986—1991 年间的 SSE（预测误差平方和），据此判断哪种方法更好。</span></details>

4. Consider a linear trend process, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4. 考虑以下线性趋势过程。</span></details>

$$
y_t=b_1+b_2t+\varepsilon_t,\quad\text{where }\varepsilon_t\sim N(0,\sigma^2).
$$

Show that the smoothed statistics of double exponential smoothing, $S_T$ & $S_T^{[2]}$, satisfy the following relationship: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明双重指数平滑的平滑统计量 Sₜ 和 Sₜ⁽²⁾ 满足下列关系（原式下标为大写 T）。</span></details>

$$
\operatorname{E}(S_T^{[2]})=\operatorname{E}(S_T)-\frac{1-\alpha}{\alpha}b_2.
$$

<details><summary>本页原图（核对用）</summary>

![[附件/tut2-questions-p03.png]]

</details>
