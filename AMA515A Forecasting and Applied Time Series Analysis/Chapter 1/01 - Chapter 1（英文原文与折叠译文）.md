---
course: AMA515A Forecasting and Applied Time Series Analysis
source: Chapter 1.pdf
pages: 10
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 按 PDF 阅读器页码完整转录英文、公式、表格；段末点击“中文译文”展开中文。各页末折叠保留原页，原文疑似笔误不直接改写。手写补充另成两篇，保持各自版本及页序。
> [资料索引](<00 - Chapter 1 资料索引.md>) · [原 PDF](<附件/Chapter 1.pdf>) · [手写笔记（前半）](<02 - Chapter 1 手写笔记（p1 to p5）.md>) · [手写笔记（后半）](<03 - Chapter 1 手写笔记（p6 to p9）.md>)

## PDF p.1

**AMA515A Forecasting and applied time series analysis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 预测与应用时间序列分析。</span></details>

### Chapter 1 : Introduction to forecasting <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 1 章：预测导论。</span></details>

**1. Time series data and forecasts** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 时间序列数据与预测。</span></details>

**1.1 The general setup** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.1 一般框架。</span></details>

To build a forecast model for a time series $Y_t$, a researcher usually collects a sequence of observations from the available data. The data are usually partitioned ( see the chart below) in the following fashion: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为了给时间序列 Yₜ 建立预测模型，研究者通常从可用数据中收集一系列观测值。数据一般按下图所示的方式划分：</span></details>

![Historical data, sample, within-sample, ex post and ex ante periods](<附件/lecture-p01-timeline.png>)

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">图中：Historical Data 为历史数据，sample 为建模样本；within-sample forecast 为样本内预测；Ex post forecast 为实际值已知、可用于检验的事后预测；Ex ante for. 为尚无实际观测值的事前预测。图中各时点与预测值下标按原图保留。</span></details>

- Historical data are provided from time period $Y_{\mathrm{BEG}}$ to $Y_{\mathrm{END}}$. We define $Y_{\mathrm{BEG}}$ as that time period in which data collection on the variable began and $Y_{\mathrm{END}}$ as the most recent observation on the variable. For our purpose $Y_{\mathrm{END}}$ might be considered today's observation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">历史数据从 YBEG 延续到 YEND。YBEG 表示开始收集该变量数据的时期，YEND 表示该变量最新的观测值；在这里，可以把 YEND 看作今天的观测值。</span></details>

- The sample period for analysis, $Y_1,\ldots,Y_n$, is the period over which we will be building or estimating the forecasting model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">分析样本期 Y₁ 至 Yₙ，是用于建立或估计预测模型的数据时期。</span></details>

- The ex post period is defined as the time period from the first observation after the end of the sample period for analysis ($\hat Y_{n+1}$) to the most recent observation ($\hat Y_N$). The most important characteristic of this time period is that the researcher has available the current values of the time series variable $Y_t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">事后预测期指分析样本结束后的第一个观测时点至最新观测时点之间的时期。原文用 Ŷₙ₊₁ 和 ŶN 标记这两个端点。这一时期最重要的特点是，研究者已经拥有时间序列变量 Yₜ 的实际值。</span></details>

- The ex ante forecast period is defined as that time period in which no observations on the time series variable exist. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">事前预测期指该时间序列变量尚不存在实际观测值的时期。</span></details>

**1.2 Measuring the forecast error** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.2 衡量预测误差。</span></details>

Defn. We define the difference between the actual and the forecast values as the forecast error, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定义：实际值与预测值的差称为预测误差。</span></details>

$$
e_t=Y_t-\hat Y_t.
$$

> [!example]- PDF 第 1 页原貌
> ![PDF p.1](<附件/lecture-p01.png>)

## PDF p.2

The following statistical summary measures of a model's forecast accuracy are defined using the absolute errors: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下列预测准确性的统计汇总指标以绝对误差定义：</span></details>

**1. The mean absolute error** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 平均绝对误差。</span></details>

$$
\mathrm{MAE}=\left(\sum_{t=1}^n|e_t|\right)/n.
$$

**2. The mean of the absolute percentage error** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 平均绝对百分比误差。</span></details>

$$
\mathrm{MAPE}=\frac{\displaystyle\sum_{t=1}^n\frac{|e_t|}{Y_t}}{n}.
$$

where $e_t$ is the forecast error in time period t; <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，eₜ 是第 t 期的预测误差；</span></details>

$Y_t$ is the actual value in time period t; n is the number of forecast observations in the estimation period. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Yₜ 是第 t 期实际值；n 是估计期内用于评价的预测观测数量。</span></details>

The following statistical summary measures of a model's forecast accuracy are defined using the squared errors: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下列预测准确性的统计汇总指标以平方误差定义：</span></details>

**1. The mean squared error** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 均方误差。</span></details>

$$
\mathrm{MSE}=\frac{\sum_{t=1}^n e_t^2}{n}.
$$

**2. The root mean squared error** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2. 均方根误差。</span></details>

$$
\mathrm{RMSE}=\sqrt{\mathrm{MSE}}.
$$

**3. Theil’s U** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">3. Theil 的 U 指标。</span></details>

U is defined as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">U 定义为：</span></details>

$$
U=\frac{\sqrt{\frac1n\sum_{t=1}^n(Y_t-\hat Y_t)^2}}{\sqrt{\frac1n\sum_{t=1}^n\hat Y_t^2}+\sqrt{\frac1n\sum_{t=1}^nY_t^2}},
$$

where $\sum_{t=1}^n(Y_t-\hat Y_t)^2$ = the sum of the squared forecast errors, and $\hat Y_t$ can also be the within sample forecast, also known as fitted value; <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，实际值与预测值之差的平方和是预测误差平方和；Ŷₜ 也可以是样本内预测值，即拟合值；</span></details>

$\sum_{t=1}^n\hat Y_t^2$ = the sum of the squared forecast values; <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测值平方的总和；</span></details>

$\sum_{t=1}^nY_t^2$ = the sum of the squared actual values. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">实际值平方的总和。</span></details>

It is clear that U has a value between 0 and 1. A small value of U indicates a good forecasting model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">显然，U 的取值介于 0 和 1 之间。U 较小表示预测模型较好。</span></details>

> [!example]- PDF 第 2 页原貌
> ![PDF p.2](<附件/lecture-p02.png>)

## PDF p.3

**1.3 Some simple forecast models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.3 一些简单的预测模型。</span></details>

**(a) The naïve forecast** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）朴素预测。</span></details>

$$
\hat Y_{t+1}=Y_t.
$$

**(b) Simple moving average** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）简单移动平均。</span></details>

'k point moving average forecast' = <details class="translation-details"><summary>中文译文</summary><span class="translation-body">“k 点移动平均预测”为：</span></details>

$$
\hat Y_{t+1}=\frac{Y_t+Y_{t-1}+\cdots+Y_{t-(k-1)}}{k}.
$$

**(c) Linear trend forecast** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）线性趋势预测。</span></details>

If we assume a linear regression over time model, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">假定采用对时间进行线性回归的模型：</span></details>

$$
Y_t=\alpha+\beta t+\varepsilon_t;
$$

then the forecast is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则预测由下式给出：</span></details>

$$
\hat Y_t=a+bt.
$$

**(d) Causal regression model** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）因果回归模型。</span></details>

$$
Y_t=\alpha+\beta X_t+\varepsilon_t
$$

where $Y_t$ = actual values for the time series variable; <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，Yₜ 为时间序列变量的实际值；</span></details>

$X_t$ = explanatory variable; <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Xₜ 为解释变量；</span></details>

$\varepsilon_t$ = random error. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">εₜ 为随机误差。</span></details>

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是：</span></details>

$$
\hat Y_t=a+bX_t.
$$

Example: The data below refers to some annual revenues of a certain company. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：下表给出了某公司一些年份的年度收入。</span></details>

| Year | 00 | 01 | 02 | 03 | 04 | 05 | 06 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Rev. | 375.2 | 414.2 | 458.5 | 511.9 | 542 | 588.1 | 656.4 |
| Year | 07 | 08 | 09 | 10 | 11 | 12 | 13 |
| Rev. | 722.5 | 804.2 | 896.8 | 957.4 | 1038.7 | 1069.3 | 1167.9 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表中 Year 为年份，Rev. 为年度收入。所有年份缩写和数据均按原表保留。</span></details>

Table 2 gives the actual revenue, naïve, 3-period moving average, & linear trend forecasts for 2006-20133 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表 2 给出实际收入、朴素预测、3 期移动平均预测和线性趋势预测。原文年份范围写作“2006-20133”，按原样保留。</span></details>

> [!example]- PDF 第 3 页原貌
> ![PDF p.3](<附件/lecture-p03.png>)

## PDF p.4

The linear trend equation for 00 to 05 is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">00 至 05 年的线性趋势方程为：</span></details>

$$
R_t=374.41+42.89*t.
$$

Note: In the above regression, t runs from 0 to 5. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：上述回归中的 t 从 0 取到 5。</span></details>

**Table 2 Revenues and forecasts** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表 2：收入及预测值。</span></details>

| Year | Actual | Naïve | 3-period MA | Trend |
| --- | ---: | ---: | ---: | ---: |
| 06 | 656.4 | 588.1 | 547.3 | 631.8 |
| 07 | 722.5 | 656.4 | 595.5 | 674.6 |
| 08 | 804.2 | 722.5 | 655.7 | 717.5 |
| 09 | 896.8 | 804.2 | 727.7 | 760.4 |
| 10 | 957.4 | 896.8 | 807.8 | 803.3 |
| 11 | 1038.7 | 957.4 | 886.1 | 846.2 |
| 12 | 1069.3 | 1038.7 | 964.3 | 889.1 |
| 13 | 1167.9 | 1069.3 | 1021.8 | 932.0 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">各列依次为：年份、实际收入、朴素预测、3 期移动平均预测、趋势预测。</span></details>

**1.4 Simple exponential smoothing (for constant process)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.4 简单指数平滑（适用于恒定水平过程）。</span></details>

Let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设：</span></details>

$$
X_t=b+\varepsilon_t.
$$

And observations are $x_1,x_2,\ldots,x_T$. The setup of the simple exponential smoothing (SES) method is : <details class="translation-details"><summary>中文译文</summary><span class="translation-body">观测值为 x₁、x₂、…、xT。简单指数平滑（SES）方法的设定如下：</span></details>

$$
\hat b(T)=\hat b(T-1)+\alpha[x_T-\hat b(T-1)]
$$

where $0<\alpha<1$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 α 介于 0 与 1 之间。</span></details>

Rationale : We modify the old estimate(forecast) by some fraction of the forecast error, $x_T-\hat b(T-1)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">基本思想：用预测误差的一定比例修正原先的估计（预测）。这里的预测误差是实际观测 xT 减去先前估计 b̂(T−1)。</span></details>

Let $S_T\equiv\hat b(T)$, then we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 ST 等于 b̂(T)，则有：</span></details>

$$
S_T=S_{T-1}+\alpha[x_T-S_{T-1}],
$$

$$
\therefore S_T=\alpha x_T+(1-\alpha)S_{T-1}.
$$

> [!example]- PDF 第 4 页原貌
> ![PDF p.4](<附件/lecture-p04.png>)

## PDF p.5

**1.4.1 Properties of simple exponential smoothing forecast** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.4.1 简单指数平滑预测的性质。</span></details>

Observe <details class="translation-details"><summary>中文译文</summary><span class="translation-body">观察下列展开：</span></details>

$$
\begin{aligned}
S_T&=S_{T-1}+\alpha[x_T-S_{T-1}],\\
S_T&=\alpha x_T+(1-\alpha)[\alpha x_{T-1}+(1-\alpha)S_{T-2}],\\
\Rightarrow S_T&=\alpha\sum_{k=0}^{T-1}(1-\alpha)^kx_{T-k}+(1-\alpha)^TS_0.
\end{aligned}
$$

thus $S_T$ is a weighted average of all past observations. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，ST 是全部历史观测值的加权平均。</span></details>

Moreover <details class="translation-details"><summary>中文译文</summary><span class="translation-body">此外：</span></details>

$$
(1-\alpha)^TS_0\to0\quad\text{as }T\to\infty.
$$

Thus <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是：</span></details>

$$
E(S_T)=E\left[\alpha\sum_{k=0}^{\infty}(1-\alpha)^kx_{T-k}\right]=b.
$$

$S_T$ is an unbiased estimate of b, thus it is natural to have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">ST 是 b 的无偏估计，因此自然地采用下列预测：</span></details>

$$
\hat x_{T+\tau}=S_T.
$$

Rem1 : We frequently use the average of the recent observations as $S_0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">备注 1：经常用近期观测值的平均数作为初始值 S₀。</span></details>

Rem2 : In terms of updating, exp. Smoothing is a very convenient procedure. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">备注 2：就更新而言，指数平滑是一种非常方便的方法。</span></details>

**Example: Simple exponential smoothing** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：简单指数平滑。</span></details>

The monthly sales of a kind of TV in the past six momths are shown in the following table. Using $S_0=393.13$, $\alpha=0.1$, the smoothed statistics and the one-step ahead forecasts are shown in the following table. Note that $S_0$ is chosen ‘arbitrarily’. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下表给出某种电视机过去六个月的月销量。取 S₀ = 393.13、α = 0.1，计算出的平滑统计量和向前一期预测也列在表中。注意，S₀ 是“任意”选取的。原文 momths 拼写保留。</span></details>

| Sequence no. | Actual sales, $X_T$ | Smoothed stat, $S_T$ | Forecast (one-step) |
| ---: | ---: | ---: | ---: |
| 1 | 330 | 386.82 | 393 |
| 2 | 410 | 389.14 | 387 |
| 3 | 408 | 391.02 | 389 |
| 4 | 514 | 403.32 | 391 |
| 5 | 402 | 403.19 | 403 |
| 6 | 343 | 397.17 | 403 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头依次为：期序号、实际销量 XT、平滑统计量 ST、向前一期预测值。</span></details>

NOTE : $S_T$ is the forecast made at time T, so it is the forecast of $X_{T+1}$. Many students think $S_T$ is the forecast of $X_T$, which is wrong! <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：ST 是在时点 T 作出的预测，所以它预测的是 XT₊₁。许多学生以为 ST 预测的是 XT，这是错误的！</span></details>

Observe <details class="translation-details"><summary>中文译文</summary><span class="translation-body">观察下页计算：</span></details>

> [!note] 原文核对备注
> 本页先取极限，再称为“unbiased estimate”；有限样本下是否无偏还取决于初始值。上面保留原文措辞及公式，不将补充条件混入英文原文。

> [!example]- PDF 第 5 页原貌
> ![PDF p.5](<附件/lecture-p05.png>)

## PDF p.6

$$
S_1=0.1X_1+0.9S_0
$$

That means <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这意味着：</span></details>

$$
S_1=0.1(330)+0.9(393.13)=386.82,
$$

and that is the forecast of $X_2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">它就是对 X₂ 的预测。</span></details>

Similarly, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">类似地：</span></details>

$$
S_2=0.1X_2+0.9S_1.
$$

So <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以：</span></details>

$$
S_2=0.1(410)+0.9(386.82)=389.14,
$$

and that is the forecast of $X_3$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">它就是对 X₃ 的预测。</span></details>

**1.5 Descriptive techniques** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5 描述性方法。</span></details>

**1.5.1 Trend and seasonality** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5.1 趋势与季节性。</span></details>

Both refer to deterministic variation in the mean of the time series $X_t$, i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">二者都指时间序列 Xₜ 的均值中的确定性变化，即：</span></details>

$$
\mu_t=E(X_t).
$$

Trend : Long term change in $\mu_t$ (e.g. $\mu_t=\alpha+\beta t$). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">趋势：均值 μₜ 的长期变化，例如 μₜ = α + βt。</span></details>

Seasonality : Regular periodic variation in $\mu_t$ (e.g. $\mu_t=\mu_{t+4}$). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">季节性：均值 μₜ 有规律的周期变化，例如 μₜ = μₜ₊₄。</span></details>

Smoothing may be used to isolate trend and/or seasonality. An alternative is trigonometric regression, e.g., might postulate <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可以用平滑方法分离趋势及／或季节性。另一种方法是三角函数回归，例如可以假设：</span></details>

$$
X_t=\mu+\alpha t+\beta\cos\omega t+\gamma\sin\omega t+Z_t
$$

where $Z_t$ is iid $N(0,\sigma^2)$ as possible model for data. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 Zₜ 独立同分布于 N(0, σ²)，从而构成数据的一种可能模型。</span></details>

**1.5.2 Stochastic trend** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5.2 随机趋势。</span></details>

Ex. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：</span></details>

$$
X_t=X_{t-1}+Z_t,\qquad Z_t\sim\operatorname{NID}(0,\sigma^2).
$$

Let $X_0=0$, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 X₀ = 0，则：</span></details>

$$
X_t=\sum_{n=1}^t Z_n\sim N(0,t\sigma^2).
$$

then $\operatorname{var}(X_t)=t\sigma^2$, which shows an increasing trend in the variance, called a stochastic trend. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">此时 Xₜ 的方差为 tσ²，方差随时间增加，这称为随机趋势。</span></details>

Define a differencing operation by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定义差分运算：</span></details>

$$
\nabla X_t=X_t-X_{t-1}
$$

then in (2.1), <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则在式（2.1）中，有下页所示结果。原文交叉编号“(2.1)”保留。</span></details>

> [!example]- PDF 第 6 页原貌
> ![PDF p.6](<附件/lecture-p06.png>)

## PDF p.7

$$
\nabla X_t=Z_t\sim N(0,\sigma^2),\quad\text{for all }t.
$$

Thus differencing can eliminate stochastic trend. Similarly, if <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，差分可以消除随机趋势。类似地，若：</span></details>

$$
X_t=\mu+\alpha t+Z_t,\qquad Z_t\sim\operatorname{NID}(0,\sigma^2).
$$

Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$
\nabla X_t=\alpha+(Z_t-Z_{t-1})\sim\operatorname{NID}(\alpha,2\sigma^2),
$$

so differencing can eliminate deterministic trend. Similarly , seasonal differencing , <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以差分可以消除确定性趋势。类似地，季节差分：</span></details>

$$
\nabla_kX_t=X_t-X_{t-k}
$$

can be useful. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">也可能有用。</span></details>

> [!note] 原文核对备注
> 上式的 NID 按原文保留。相邻差分共享随机项，因此“独立”的标记存在疑点；这里不改动源公式。

**1.5.3 Causal model and regression over time** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5.3 因果模型与对时间的回归。</span></details>

**(A) Linear model** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（A）线性模型。</span></details>

$$
Y_t=\alpha+\beta X_t+\varepsilon_t\qquad\text{------Causal model}
$$

$$
Y_t=\alpha+\beta t+\varepsilon_t\qquad\text{-------Trend model}
$$

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">上面依次为因果模型、趋势模型。</span></details>

Here $\varepsilon_t$ satisfies (i) $\varepsilon_t\sim N(0,\sigma^2)$; (ii) $\varepsilon_t$'s are independent. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这里 εₜ 满足：（i）服从均值为 0、方差为 σ² 的正态分布；（ii）各期误差相互独立。</span></details>

For (ii), testing the presence of autocorrelations gives the famous Durbin-Watson statistic d, where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">针对条件（ii），可以用著名的 Durbin–Watson 统计量 d 检验是否存在自相关，其中：</span></details>

$$
d=\sum_{t=2}^n(e_t-e_{t-1})^2\Big/\sum_{t=1}^ne_t^2.
$$

Now observe <details class="translation-details"><summary>中文译文</summary><span class="translation-body">现在观察：</span></details>

$$
\frac{\sum(e_t-e_{t-1})^2}{\sum e_t^2}
\cong\frac{2\sum e_t^2-2\sum e_te_{t-1}}{\sum e_t^2}
\cong2(1-\hat r_1).
$$

Thus $0<d<4$, with a value close to zero indicates a +ve correlation, and a value close to 4 indicates a -ve correlation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，d 介于 0 与 4 之间。接近 0 表示正相关，接近 4 表示负相关。</span></details>

Durbin and Watson calculate two more values $d_L$ and $d_U$ to complete the testing procedure. The testing problem is : <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Durbin 和 Watson 还计算了 dL 和 dU 两个临界值以完成检验。检验假设为：</span></details>

$$
H_0:\rho=0,\qquad H_1:\rho>0\text{ or }\rho<0.
$$

Steps: (1) if $d_U<d<4-d_U$, accept $H_0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">步骤：（1）如果 dU &lt; d &lt; 4 − dU，则接受 H₀。此处“接受”沿用原文措辞。</span></details>

> [!example]- PDF 第 7 页原貌
> ![PDF p.7](<附件/lecture-p07.png>)

## PDF p.8

(2) if $d<d_L$, accept $\rho>0$; if $d>4-d_L$, accept $\rho<0$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（2）如果 d &lt; dL，则接受正相关结论；如果 d &gt; 4 − dL，则接受负相关结论。</span></details>

(3) if $d_L<d<d_U$ or $4-d_U<d<4-d_L$, then test is inconclusive. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（3）如果 dL &lt; d &lt; dU，或者 4 − dU &lt; d &lt; 4 − dL，则检验无法给出确定结论。</span></details>

**Estimation and testing** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">估计与检验。</span></details>

This is equivalent to the standard linear regression model case. Thus in <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这与标准线性回归模型的情况等价。因此，在下列模型中：</span></details>

$$
Y_t=\alpha+\beta t+\varepsilon_t,
$$

$$
\hat\beta=b=\frac{c_{yt}}{c_{tt}}
=\frac{\sum(y_t-\bar y)(t-\bar t)}{\sum(t-\bar t)^2},
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$
\hat\alpha=a=\bar y-b\bar t.
$$

For testing the slope coefficient $\beta$, use $t=(b-\beta)/s_b$, on n-2 degrees of freedom, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">检验斜率系数 β 时，使用 t = (b − β) / sb，自由度为 n − 2。</span></details>

where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中：</span></details>

$$
s_b=\sqrt{\mathrm{MSE}/c_{tt}},\qquad
\mathrm{MSE}=\sum e_t^2/(n-2).
$$

**Forecasting with linear trend** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">利用线性趋势预测。</span></details>

$$
y_{t+\tau}=\hat\alpha+\hat\beta(t+\tau).
$$

> [!note] 原文核对备注
> 该行原 PDF 左端显示为 yₜ₊τ，未明确印出预测帽号，此处照录；原页图可核对原始字形。

**Prediction interval** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测区间。</span></details>

$$
\hat y_t\pm t_{\alpha/2}s_e\sqrt{1+\frac1n+\frac{(t_p-\bar t)^2}{c_{tt}}},
$$

where $s_e=\sqrt{\mathrm{MSE}}$ and MSE being from linear regression analysis. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 se 是 MSE 的平方根，MSE 来自线性回归分析。</span></details>

**(B) Curvilinear model** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（B）曲线模型。</span></details>

Tools for detection of nonlinearity: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">识别非线性的工具：</span></details>

1. TS plot <details class="translation-details"><summary>中文译文</summary><span class="translation-body">时间序列图。</span></details>

2. D.W. statistics for residuals from linear regression <details class="translation-details"><summary>中文译文</summary><span class="translation-body">线性回归残差的 Durbin–Watson 统计量。</span></details>

3. Plot of 1st differences --- 1st difference will roughly be a random graph if original data possess only linear trend. If original data come from a quadratic function, then observe <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一阶差分图——如果原始数据只有线性趋势，一阶差分图大致表现为随机图形。如果原始数据来自二次函数，则观察下页所示关系。</span></details>

> [!example]- PDF 第 8 页原貌
> ![PDF p.8](<附件/lecture-p08.png>)

## PDF p.9

$$
a+b(t+1)+c(t+1)^2-a-bt-ct^2=b+2ct+c,
$$

which implies the existence of trend. Thus the presence of trend in the 1st difference indicates a nonlinear model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这意味着差分后仍存在趋势。因此，一阶差分中存在趋势，提示应采用非线性模型。</span></details>

**Model type:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">模型类型：</span></details>

**(I) Polynomial :** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（I）多项式模型：</span></details>

$$
y_t=a+b_1t+\cdots+b_kt^k+\varepsilon_t,\quad t=1,2,\ldots,n.
$$

Estimation-- Recall from multiple regression theory, if we let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">估计——回顾多元回归理论，令：</span></details>

$$
\boldsymbol\beta=(a\ b_1\ \cdots\ b_k)',\qquad
X=\begin{pmatrix}
1&1&\cdots&1^k\\
1&2&\cdots&2^k\\
\vdots&\vdots&&\vdots\\
1&t&\cdots&t^k
\end{pmatrix},
$$

then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则：</span></details>

$$
\hat{\boldsymbol\beta}=(X^\top X)^{-1}X^\top\mathbf y,
$$

where $\mathbf y=(y_1,y_2,\ldots,y_n)'$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 y 是由 y₁ 至 yₙ 组成的列向量。</span></details>

**(II) Exponential(loglinear) :** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（II）指数（对数线性）模型：</span></details>

$$
\begin{aligned}
y_t&=ae^{bt}\varepsilon_t,\quad\varepsilon_t\sim N(1,\sigma^2),\\
\Rightarrow\ln(y_t)&=a+bt+\eta_t,\quad\eta_t\sim N(0,\sigma_1^2),\\
\Rightarrow\ln(\hat y_t)&=\hat a+\hat b t.
\end{aligned}
$$

> [!note] 原文核对备注
> 此处的乘法截距 a、取对数后的 a，以及 εₜ、ηₜ 的正态分布假设均按原页照录；这几行的符号和分布转换存在疑点。另见后半手写笔记 PDF p.11—p.12，保留为不同来源，不拼接成修订答案。

**(III) Logistic (S-shaped) :** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（III）Logistic（S 形）模型：</span></details>

$$
y_t=\frac{L}{1+\exp(\alpha+\beta t+\varepsilon_t)}
$$

$$
\Rightarrow\hat y_t=\frac{L}{1+\exp(\hat\alpha+\hat\beta t)}.
$$

> [!example]- PDF 第 9 页原貌
> ![PDF p.9](<附件/lecture-p09.png>)

## PDF p.10

**Business forecasting** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">商业预测。</span></details>

### Appendix 1: Prediction interval of trend model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">附录 1：趋势模型的预测区间。</span></details>

Recall the formula for prediction interval is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">回顾预测区间公式：</span></details>

$$
\hat y_t\pm t_{\alpha/2}s_e\sqrt{1+\frac1n+\frac{(t_p-\bar t)^2}{c_{tt}}}.
$$

Using the first 10 obs of Series 1 as example, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以序列 1 的前 10 个观测值为例，有：</span></details>

$$
Y_t=2735.9+18.67t.
$$

Thus predicted value for 11th obs is 2941.27 approximately. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，第 11 个观测值的预测约为 2941.27。</span></details>

| SS1 |
| ---: |
| 2767 |
| 2766 |
| 2782 |
| 2811 |
| 2836 |
| 2850 |
| 2870 |
| 2869 |
| 2898 |
| 2937 |
| 2965 |
| 2994 |
| 3023 |
| 3065 |

<details class="translation-details"><summary>中文译文</summary><span class="translation-body">SS1 为本例展示的序列数据；原表全部 14 个数值均保留，上述拟合仅使用前 10 个观测值。</span></details>

Prediction interval is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测区间为：</span></details>

$$
\begin{aligned}
&2941.27\pm t_{8,0.025}\sqrt{109.2}\sqrt{1+\frac1{10}+\frac{(11-5.5)^2}{c_{tt}}}\\
={}&2941.27\pm2.306\sqrt{109.2}\sqrt{1+\frac1{10}+\frac{(11-5.5)^2}{c_{tt}}}\\
={}&2941.27\pm2.306\sqrt{109.2}\sqrt{1+\frac1{10}+\frac{30.25}{82.5}}\\
={}&(2912.05,\ 2970.39).
\end{aligned}
$$

> [!example]- PDF 第 10 页原貌
> ![PDF p.10](<附件/lecture-p10.png>)
