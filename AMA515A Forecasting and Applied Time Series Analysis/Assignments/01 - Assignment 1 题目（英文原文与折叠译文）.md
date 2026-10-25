---
course: "AMA515A Forecasting and Applied Time Series Analysis"
source: "AMA515A Assignment 1.pdf"
pages: 3
cssclasses:
  - ama-inline-translations
---

# Assignment 1 题目（英文原文与折叠译文）

[原 PDF](<附件/AMA515A Assignment 1.pdf>) · [完整参考解答](<02 - Assignment 1 完整参考解答.md>) · [Tutorial 资料总索引](<../Tutorials/00 - Tutorials 资料索引.md>)

按 PDF 页序保留全部题目、数据和公式，并提供逐段折叠中文译文。原题条件不擅自增删；所需的稳态假设、测量噪声条件和第 4(d) 题区间对象的区别，只在独立解答中说明。每页底部可展开原图核对。

## PDF p.1


**AMA515A Assignment 1** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 作业 1。</span></details>


**1.** The error in forecasting for period T+1 at the end of period T is defined as $e(T+1)=x_{T+1}-\widehat x_{T+1}(T)$. If the observations are independent random variables, $x_{T+1}$ will be independent of $\widehat x_{T+1}(T)$. Assume simple (single) exponential smoothing is applied to the constant process $x_t=b+\varepsilon_t$, where $\operatorname{var}(\varepsilon_t)=\sigma_\varepsilon^2$. Show that the variance of the forecast error, $\sigma_e^2$, satisfies the relationship $\sigma_e^2=\frac{2}{2-\alpha}\sigma_\varepsilon^2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 1 题：在 T 期末预测 T+1 期的误差定义为实际值减预测值。观测相互独立时，未来观测也独立于根据过去数据形成的预测。对给定常数过程应用一次指数平滑，证明预测误差方差满足所给关系。</span></details>


**2. (a).** Two processes $\{Z_t\}$ and $\{Y_t\}$ are said to be independent if for any time points $t_1,\ldots,t_m$ and $s_1,\ldots,s_n$ the random variables $\{Z_{t_1},\ldots,Z_{t_m}\}$ are independent of the variables $\{Y_{s_1},\ldots,Y_{s_n}\}$. Show that if $\{Z_t\}$ and $\{Y_t\}$ are independent stationary processes, then $W_t=Z_t+Y_t$ is stationary. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 2(a) 题：两个过程独立，是指任意有限组时间点所对应的两组随机变量都独立。证明两个独立平稳过程之和仍平稳。</span></details>


**(b).** Let $\{X_t\}$ be a time series. However, because the measurement process itself is not perfect, we actually observe $Y_t=X_t+e_t$. Assume that $X_t$ and $e_t$ are independent processes. We call $X_t$ the signal and $e_t$ the measurement noise. If $\{X_t\}$ is stationary with autocorrelation function $\rho_k$, show that $\{Y_t\}$ is also stationary with <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 2(b) 题：由于测量不完美，实际观测到的是信号 Xₜ 加测量噪声 eₜ，两个过程独立。若信号平稳且自相关为 ρₖ，证明观测过程也平稳，并满足：</span></details>

$$
\operatorname{Corr}(Y_t,Y_{t-k})=\frac{\rho_k}{1+\sigma_e^2/\sigma_X^2},\qquad k\ge1.
$$

We call $\sigma_X^2/\sigma_e^2$ the signal-to-noise ratio (SNR). Note that the larger the SNR, the closer the autocorrelation function of the observed process $\{Y_t\}$ is to the autocorrelation function of the desired signal $\{X_t\}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">信号方差与噪声方差之比称为信噪比。信噪比越大，观测过程的自相关越接近目标信号的自相关。</span></details>


**3.** The electricity consumption of a certain city (in coded units) from 1991 to 1997 is given in the following table. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 3 题：某城市 1991—1997 年的用电量（编码单位）如下。</span></details>


| Year | Time index (t) | data |
| --- | ---: | ---: |
| 91 | 1 | 676 |
| 92 | 2 | 825 |
| 93 | 3 | 774 |
| 94 | 4 | 716 |
| 95 | 5 | 940 |
| 96 | 6 | 1159 |
| 97 | 7 | 1384 |


**Year / Time index (t) / data** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表头依次为年份、时间序号和用电量。</span></details>


**(a)** It is felt that the data can be fitted by the following linear model: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 3(a) 题：认为数据可以用以下线性模型拟合：</span></details>

$$
X_t=a+b_1t+e_t,\qquad e_t\sim\operatorname{NID}(0,\sigma^2).
$$

The Durbin Watson statistic is defined by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Durbin–Watson 统计量定义为：</span></details>

$$
d=\frac{\sum_{t=2}^n(\widehat e_t-\widehat e_{t-1})^2}{\sum_{t=1}^n\widehat e_t^2},
$$

where $\widehat e_t$ is the residual after fitting the model to the data. It's used to test whether the residuals are autocorrelated or not. The residuals for the data above are: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 êₜ 是模型拟合残差。该统计量用于检验残差是否自相关。给定数据的残差如下，表格续于下一页。</span></details>


> [!example]- PDF 第 1 页原貌
> ![PDF p.1](<附件/assignment1-p01.png>)

## PDF p.2

| t | Residuals $\widehat e_t$ |
| ---: | ---: |
| 1 | 68.071 |
| 2 | 111.429 |
| 3 | -45.214 |
| 4 | -208.857 |
| 5 | -90.5 |
| 6 | 22.857 |
| 7 | 142.214 |


**t / Residuals** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">时间序号与对应残差。</span></details>


Using the given residuals, evaluate the Durbin Watson statistic for this model. What is your conclusion from the value of the test statistic? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">使用给定残差计算该模型的 DW 统计量，并解释检验结论。</span></details>


**(b)** Let $\{y_T\}$ be a time series. The Holt's double exponential smoothing algorithm for a trend model is defined as follows: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 3(b) 题：设 yₜ 为时间序列。趋势模型的 Holt 二次指数平滑算法定义如下。</span></details>


**1.** Obtain an updated estimate $a_0(T)$ of the intercept component by using the equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第一步：按下式更新截距／水平分量的估计：</span></details>

$$
a_0(T)=\alpha y_T+(1-\alpha)[a_0(T-1)+b_1(T-1)],\qquad 0<\alpha<1.
$$

**2.** Obtain an updated estimate $b_1(T)$ of the slope component by using the equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第二步：按下式更新斜率分量：</span></details>

$$
b_1(T)=\beta[a_0(T)-a_0(T-1)]+(1-\beta)b_1(T-1),\qquad0<\beta<1.
$$

**3.** A one-step ahead forecast of the future value $y_{T+1}$ made at time T is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第三步：在 T 期形成的下一期预测为：</span></details>

$$
\widehat y_T(1)=a_0(T)+b_1(T).
$$

For the above data, it is given $a_0(0)=502.286$, $b_1(0)=105.643$. $\alpha=0.2$; $\beta=0.1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对上述用电数据，初始水平为 502.286、初始斜率为 105.643，α = 0.2、β = 0.1。</span></details>


**(i)** By using Holt's algorithm, find the one-step-ahead forecasts for the period 1992 to 1996, and calculate the MAE (mean absolute error) of the forecasts. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 3(b)(i) 题：用 Holt 算法计算 1992—1996 年的一步预测及其平均绝对误差 MAE。</span></details>


**(ii)** Find the naive forecasts in the same period and calculate the MAE. By comparing the MAE of these two methods, determine which one is better. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 3(b)(ii) 题：计算同期朴素预测和 MAE，并通过比较判断哪一种方法更好。</span></details>


**4.** The following data set is the amount of coffee (in coded units) produced by a certain company in 2006. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 4 题：以下为某公司 2006 年咖啡产量（编码单位）。</span></details>


| month | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| data | 200 | 145 | 195 | 197.5 | 210 | 175 | 155 | 140 |


**month / data** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第一行为一月至八月，第二行为对应产量。</span></details>


> [!example]- PDF 第 2 页原貌
> ![PDF p.2](<附件/assignment1-p02.png>)

## PDF p.3


A forecaster thinks that a constant model, $X_t=b_1+a_t$, where $a_t\sim\operatorname{NID}(0,\sigma^2)$, is appropriate for the data. He then suggests to use the method of Simple Exponential Smoothing, namely $S_t=\alpha X_t+(1-\alpha)S_{t-1}$, to obtain forecasts for this set of data. Here $0<\alpha<1$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">预测者认为数据适用常数模型，扰动为独立正态噪声，因此建议用一次指数平滑形成预测，平滑系数在 0 与 1 之间。</span></details>


**(a)** Using the January observation as $S_0$, calculate the Simple Exponential Smoothing forecasts for Feb to Aug. Let $\alpha=0.4$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 4(a) 题：以一月观测作为初始平滑值，令 α = 0.4，计算二月至八月的预测。</span></details>


**(b)** It is given that $\operatorname{var}(X_{t+1}-S_t)=\left(\frac{2}{2-\alpha}\right)\sigma^2$. Based on your result in (a), find an estimate of $\sigma^2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 4(b) 题：已知一步预测误差方差与扰动方差的关系，利用 (a) 的结果估计扰动方差。</span></details>


**(c)** Find an estimate of $\operatorname{var}(S_t)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 4(c) 题：估计平滑统计量的方差。</span></details>


**(d)** Use the Simple Exponential Smoothing algorithm to forecast the coffee production in September 2006, and find a 95% confidence interval for the forecast. You may assume the forecast follows an approximate normal distribution. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 4(d) 题：预测 2006 年九月咖啡产量，并给出 95% 区间。可假设有关预测量近似服从正态分布。</span></details>


**5.** Let $\{Z_t\}$ be a sequence of independent normal random variables, each with mean 0 and variance $\sigma^2$ and let a, b and c be constants. Which, if any, of the following processes are stationary? For each stationary process specify the mean and autocovariance function (which includes the variance). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 5 题：设 Zₜ 为独立正态随机变量序列，均值为零、方差为 σ²；a、b、c 为常数。判断下列过程是否平稳；对平稳过程给出均值和自协方差函数（包括方差）。</span></details>

$$
\begin{aligned}
\text{a.}\quad X_t&=a+bZ_t+cZ_{t-2},\\
\text{b.}\quad X_t&=Z_1\cos(ct)+Z_2\sin(ct),\\
\text{c.}\quad X_t&=Z_t\cos(ct)+Z_{t-1}\sin(ct),\\
\text{d.}\quad X_t&=a+bZ_0,\\
\text{e.}\quad X_t&=Z_0\cos(ct).
\end{aligned}
$$

**~~~~~End~~~~~** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">作业结束。</span></details>


> [!example]- PDF 第 3 页原貌
> ![PDF p.3](<附件/assignment1-p03.png>)

