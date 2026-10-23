---
course: "AMA515A Forecasting and Applied Time Series Analysis"
chapter: 4
source: "Chapter 4 Updated Notes.pdf"
pages: 18
cssclasses:
  - ama-inline-translations
---

# Chapter 4 — 英文原文与折叠中文译文

[本章资料索引](<00 - Chapter 4 资料索引.md>) · [原始 PDF](<附件/Chapter 4 Updated Notes.pdf>)

英文按原 PDF 页序整理，逐段附默认折叠的中文译文。独立公式和图表另排；每页底部可展开原页核对。原有题目与解答分别保留，不另编解题分析。 本资料是带教师手写批注的扫描版：印刷正文与主要统计表转录；第 12—14 页密集数字表、第 15 页软件图形输出保留清晰原图，标题提供译文。所有手写批注保留在对应原页，不声称已全文转写。

## PDF p.1


**AMA515A Forecasting and applied time series analysis** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA515A 预测与应用时间序列分析。</span></details>


### Chapter 4 : Statistical Analysis in the Time Domain <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 4 章：时域中的统计分析。</span></details>


**4.1 Variance stability transformations** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.1 方差稳定化变换。</span></details>


A common phenomenon in non-stationary time series data is that the variability is related to the average level. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">非平稳时间序列的一个常见现象是：波动程度与平均水平有关。</span></details>


Consider a r.v. X whose distribution is indexed by a parameter $\theta$ such that $E(X)=\theta$ and $\operatorname{Var}(X)=v(X)=v^2(\theta)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑随机变量 X，其分布由参数 θ 决定，且均值为 θ、方差为 v²(θ)。</span></details>


Consider the transformation $Y=h(X)$ s.t. $v(Y)=\sigma^2$, independent of $\theta$. Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑变换 Y = h(X)，使其方差 σ² 不依赖 θ。则：</span></details>

$$
\begin{aligned}
h(X)&\approx h(\theta)+(X-\theta)h'(\theta)\\
\Rightarrow\{h(X)-h(\theta)\}^2&\approx(X-\theta)^2\{h'(\theta)\}^2\\
\Rightarrow v(Y)&\approx v(X)\{h'(\theta)\}^2,\\
\sigma^2&=v^2(\theta)\{h'(\theta)\}^2.
\end{aligned}\tag{4.1}
$$

(1) Thus assume $v^2(\theta)$ known, we can find $h(\cdot)$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（1）因此，若已知方差函数 v²(θ)，就可以求变换 h。</span></details>


**Example : Poisson data** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：泊松分布数据。</span></details>


(4.1) implies <details class="translation-details"><summary>中文译文</summary><span class="translation-body">式（4.1）意味着：</span></details>

$$
\{h'(\theta)\}^2=\frac{\sigma^2}{v^2(\theta)}\quad\Rightarrow\quad h(\theta)=\int\frac{\sigma}{v(\theta)}\,d\theta.
$$

Thus $v^2(\theta)=\theta$ implies $v(\theta)=\theta^{1/2}$, whence $h(\theta)=\int\sigma/\theta^{0.5}\propto\theta^{1/2}$, i.e., square root transformation stabilizes variance of Poisson data. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而，泊松分布的方差等于 θ，可得到平方根变换；即平方根变换能稳定泊松数据的方差。原印刷积分未写微分项，手写批注作了补充，见原页。</span></details>


(2) $v(\theta)$ unknown, seek $h(\cdot)$ on empirical ground. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（2）若方差函数未知，则根据经验寻找变换 h。</span></details>


A general class of power transformation is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">一般的幂变换族为：</span></details>

$$
h(\theta)=\begin{cases}(\theta^\lambda-1)/\lambda,&\lambda\ne0,\\\log\theta,&\lambda=0,\end{cases}\qquad h'(\theta)=\theta^{\lambda-1}.
$$

Reconsider (4.1) $\sigma=v(\theta)\cdot h'(\theta)$, which implies <details class="translation-details"><summary>中文译文</summary><span class="translation-body">再考虑式（4.1），σ 等于 v(θ) 与 h′(θ) 的乘积，因此：</span></details>


> [!example]- PDF 第 1 页原貌（含原有批注）
> ![PDF p.1](<附件/ch4-updated-p01.png>)

## PDF p.2

$$\log(v(\theta))=\log\sigma+(1-\lambda)\log\bar x,$$

and hence a practical way to estimate $\lambda$ is by using a plot of <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以，一种实际估计 λ 的方法是画出：</span></details>

$$\log(s)=\log\sigma+(1-\lambda)\log\bar x.$$

Namely we divide the time series data into a number of blocks and find the sample standard deviation (s.d.) and sample mean of each block. We then plot the sample standard deviation against the sample mean and find the estimate of $\lambda$ from the slope of the plot. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">具体做法是把时间序列分成若干组，计算每组的样本标准差和样本均值，再依据两者的图形斜率估计 λ。原文的文字表述与上式的对数坐标请结合阅读。</span></details>


**4.2 Partial Autocorrelation** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.2 偏自相关。</span></details>


Correlogram is a crucial tool in recognition of plausible models for time series data. But because of sampling fluctuations, cut-off correlogram is easier to recognize than exponential decay. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">相关图是识别时间序列可能模型的重要工具。但由于抽样波动，截尾通常比指数衰减更容易识别。</span></details>


The notion of partial autocorrelations is designed to help the model identification procedure by exploiting this. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">偏自相关正是利用这一点，帮助进行模型识别。</span></details>


Let $\rho=(\rho_1,\ldots,\rho_k)^T$, the vector of the first k autocorrelations of an AR(k) process. Let $R_k$ be the $k\times k$ matrix with (i,j) element $\rho_{|i-j|}$. Let $\alpha=(\alpha_1,\ldots,\alpha_k)^T$ be the vector of parameters. Recall the Yule-Walker equations <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设 ρ 为 AR(k) 过程前 k 阶自相关构成的向量，Rₖ 的第 (i,j) 元素为 ρ 的 |i−j| 阶值，α 是参数向量。回顾 Yule–Walker 方程：</span></details>

$$\rho=R_k\alpha,\quad\text{thus }\alpha=R_k^{-1}\rho,$$

and so $\alpha_k=|R_k|^{-1}|R_k^*|$, where $R_k^*$ denotes $R_k$ with its final column replaced by $(\rho_1,\ldots,\rho_k)^T$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，αₖ 等于两个行列式之比；Rₖ&#42; 是将 Rₖ 最后一列换成前 k 阶自相关向量得到的矩阵。</span></details>


Now if the process is actually AR(k−1), $\alpha_k=0$. Taking $\widehat R_k$ and $\widehat R_k^*$ to be empirical version of $R_k$ and $R_k^*$, define the partial correlogram to be the set of coefficients <details class="translation-details"><summary>中文译文</summary><span class="translation-body">如果真实过程是 AR(k−1)，那么 αₖ = 0。将两个矩阵换成样本版本，偏相关图定义为下列系数构成的图：</span></details>

$$\widehat\phi_k=\frac{|\widehat R_k^*|}{|\widehat R_k|},\quad k=1,2,\ldots.$$

So, for an AR(p) process, we expect $\widehat\phi_k\approx0$, for all k > p. Also $\widehat\phi_k$ has asymptotic variance $n^{-1}$, so use $\pm2/\sqrt n$ to look for significantly non-zero $\widehat\phi_k$, just as for ordinary correlogram. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以，对于 AR(p) 过程，超过 p 阶的样本偏自相关应接近 0；其渐近方差为 1/n，因此与普通相关图一样，用 ±2/√n 判断是否显著非零。</span></details>


**4.3 Model identification** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.3 模型识别。</span></details>


Within the general framework of (possibly seasonal) ARIMA(p,d,q) processes statistical analysis proceeds in three stages: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在可能包含季节性的 ARIMA(p,d,q) 框架下，统计分析分三步：</span></details>


> [!example]- PDF 第 2 页原貌（含原有批注）
> ![PDF p.2](<附件/ch4-updated-p02.png>)

## PDF p.3


(i) Identify plausible choices for p, d, q. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）识别合理的 p、d、q。</span></details>


(ii) Estimate parameters. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）估计参数。</span></details>


(iii) Check that residuals are consistent with white noise. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（iii）检查残差是否符合白噪声特征。</span></details>


Two major tools in (i) are the correlogram and the partial correlogram defined above. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第一步的两个主要工具是上面定义的自相关图与偏自相关图。</span></details>


Other tools include time plots, differencing, experience and common sense. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其他工具包括时间图、差分，以及经验和常识。</span></details>


• Time plots: essential preliminary to any analysis. Outliers? Non-stationarity? Variance instability? <details class="translation-details"><summary>中文译文</summary><span class="translation-body">时间图：任何分析都必不可少的准备工作。检查是否有异常值、非平稳性、方差不稳定等。</span></details>


• If time series is non-stationary, then ACF typically dies down very slowly from 1. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">如果序列非平稳，ACF 通常从 1 开始非常缓慢地下降。</span></details>


• Differencing: Can eliminate both deterministic and stochastic trends in data. Over differencing tends to increase variability. Under differencing tends to produce a correlogram which decays slowly or not at all. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">差分：可以消除确定性和随机趋势。差分过度往往增大波动；差分不足往往使相关图衰减缓慢或不衰减。</span></details>


• Correlogram: Can resolve doubtful cases of stationarity. More positively, seek to relate correlogram to one of the various distinctive theoretical ACF of sub-classes of ARMA processes (exponential decay, cut-off…). Partial correlogram also help. Conventional error is $\pm2/\sqrt n$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">相关图：帮助判断可疑的平稳性情形；还可以将样本图与不同 ARMA 子类的理论 ACF 特征对应，如指数衰减、截尾。偏相关图也有帮助。惯用误差界限为 ±2/√n。</span></details>


**4.3.1 Behavior of the acf and pacf for non-seasonal ARIMA models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.3.1 非季节 ARIMA 模型的 ACF 和 PACF 特征。</span></details>


| Model | Autocorrelation function | Partial autocorr. function |
| --- | --- | --- |
| Moving average of order q | Cuts off after lag q | Dies down exponentially and/or sinusoidally |
| Autoregressive of order p | Dies down exponentially and/or sinusoidally | Cuts off after lag p |
| Mixed model of order p,q | Dies down exponentially and/or sinusoidally | Dies down exponentially and/or sinusoidally |


**Table: Model / Autocorrelation function / Partial autocorr. function** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表格依次为模型、ACF、PACF。MA(q)：ACF 在 q 阶后截尾，PACF 指数或正弦式衰减；AR(p)：ACF 衰减，PACF 在 p 阶后截尾；混合模型：两者都衰减。</span></details>


> [!example]- PDF 第 3 页原貌（含原有批注）
> ![PDF p.3](<附件/ch4-updated-p03.png>)

## PDF p.4


**4.3.2 Characteristics and equations for the most common Box-Jenkins models [ARIMA(p,d,q)(P,D,Q)L]** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.3.2 常见 Box–Jenkins 模型的特征与方程，包括非季节与季节阶数。</span></details>


Note : both seasonal and nonseasonal models are included. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：下表同时包含季节和非季节模型。</span></details>


| Row | Acf | Pacf | Model |
| --- | --- | --- | --- |
| 1 | Cuts off after lag 1 or 2; no significant spikes at seasonal lags | Dies down | Nonseasonal moving average (q = 1 or 2) |
| 2 | Cuts off after seasonal lag L; no significant spikes at the nonseasonal lags | Dies down | Seasonal moving average (Q = 1) |
| 3 | Cuts off after seasonal lag L; significant spikes also exist at nonseasonal lags 1 or 2 | Dies down | Nonseasonal-seasonal moving average (q = 1 or 2; Q = 1) |
| 4 | Dies down | Cuts off after lags 1 or 2; no significant spikes at seasonal level | Nonseasonal autoregressive (p = 1 or 2) |
| 5 | Dies down | Cuts off after seasonal lag L; no significant spikes at nonseasonal lags | Seasonal autoregressive (P = 1) |
| 6 | Dies down | Cuts off after seasonal lag L; significant spikes also exist at nonseasonal lags 1 or 2 | Nonseasonal-seasonal autoregressive (p = 1 or 2; P = 1) |
| 7 | Dies down | Dies down | Mixed (autoregressive-moving average) |


**Rows 1–3: moving average models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 1 行：ACF 在 1 或 2 阶后截尾，季节滞后无显著尖峰，PACF 衰减，为非季节 MA。第 2 行：ACF 在季节滞后 L 后截尾，非季节滞后无显著尖峰，为季节 MA。第 3 行：ACF 在季节滞后 L 后截尾，非季节滞后 1 或 2 也有显著尖峰，为乘积季节 MA。</span></details>


**Rows 4–7: autoregressive and mixed models** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 4 行：ACF 衰减，PACF 在 1 或 2 阶后截尾、季节滞后无显著尖峰，为非季节 AR。第 5 行：PACF 在 L 后截尾、非季节滞后无显著尖峰，为季节 AR。第 6 行：PACF 在 L 后截尾，非季节滞后 1 或 2 也有显著尖峰，为乘积季节 AR。第 7 行：ACF、PACF 都衰减，为混合模型。</span></details>


**Example equations (in the same row order as the original table)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以下示例方程按原表行序排列；只是为便于阅读从表格中移出，没有合并不同模型。</span></details>

$$
\begin{aligned}
1:\quad X_t&=\mu-\theta_1a_{t-1}+a_t,\quad a_t\sim\operatorname{NID}(0,\sigma^2),\\
2:\quad X_t&=\mu-\theta_{1L}a_{t-L}+a_t,\\
3:\quad X_t&=\mu-\theta_1a_{t-1}-\theta_{1L}a_{t-L}+\theta_1\theta_{1L}a_{t-L-1}+a_t,\\
4:\quad X_t&=\mu+\phi_1X_{t-1}+a_t,\\
5:\quad X_t&=\mu+\phi_{1L}X_{t-L}+a_t,\\
6:\quad X_t&=\mu+\phi_1X_{t-1}+\phi_{1L}X_{t-L}+\phi_1\phi_{1L}X_{t-L-1}+a_t,\\
7\text{ (Nonseasonal)}:\quad X_t&=\mu+\phi_1X_{t-1}+\theta_1a_{t-1}+a_t,\\
7\text{ (Seasonal)}:\quad X_t&=\mu+\phi_{1L}X_{t-L}-\theta_{1L}a_{t-L}+a_t.
\end{aligned}
$$
> [!note] 原文核对提示
> 第 6 行的交叉项在原印刷表中为加号，这里照录；不把可能的勘误直接混进原文。

> [!example]- PDF 第 4 页原貌（含原有批注）
> ![PDF p.4](<附件/ch4-updated-p04.png>)

## PDF p.5


**4.3.3 Additional approach to model identification** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.3.3 模型识别的其他方法。</span></details>


Many approaches to model identification have been proposed since Box and Jenkins' work. A popular one is the Akaike's Information Criterion (AIC, 1973). AIC says to select the model that minimizes <details class="translation-details"><summary>中文译文</summary><span class="translation-body">自 Box 和 Jenkins 的工作以来，出现了许多模型识别方法。常见的一种是赤池信息准则（AIC，1973），选择使以下指标最小的模型：</span></details>

$$\operatorname{AIC}=-2\log(\text{maximum likelihood})+2k,$$

where k = p + q + 1 if the ARMA model contains a constant term, and k = p + q otherwise. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若 ARMA 模型含常数项，k = p + q + 1；否则 k = p + q。</span></details>


Maximum likelihood estimation is discussed in the next section. The addition of the term 2(p + q + 1) or 2(p + q) serves as penalty function to avoid choosing models with many parameters. However it was shown that AIC tends to select models with more parameters in similar models (Shibata, 1976), thus many other information criteria have appeared in literature. Two well-known ones are: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">下一节讨论最大似然估计。增加的 2k 是惩罚项，避免选择参数过多的模型；但研究发现 AIC 在相似模型中仍倾向于选择参数更多的模型，因此还有其他准则。其中两种著名准则为：</span></details>


(a) AICC proposed by Hurvich and Tsai (1979) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（a）原文标为 Hurvich 和 Tsai（1979）提出的 AICC：</span></details>

$$\operatorname{AICC}=\operatorname{AIC}+\frac{2(k+1)(k+2)}{n-k-2},$$

and (b) Bayesian information criterioin (BIC, 1978) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）贝叶斯信息准则（BIC，1978）：</span></details>

$$\operatorname{BIC}=-2\log(\text{maximum likelihood})+k\log(n).$$

Both criteria will tend to selects models with smaller k. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两种准则都倾向于选择 k 更小的模型。</span></details>


**4.4 Parameter estimation** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.4 参数估计。</span></details>


Having identify an ARMA(p,q) process for the suitably differenced data, we need to estimate p and q parameters; we use least squares, i.e., we minimize sum of squared estimated residuals. Alternatively we can use the maximum likelihood approach. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对适当差分后的数据识别出 ARMA(p,q) 模型后，需要估计参数。可以用最小二乘法，使估计残差平方和最小；也可以采用最大似然法。</span></details>


Definition: All ARMA process involve an embedded white noise sequence $\{Z_t\}$. The sequence of values $\{\widehat Z_t\}$ recovered from the data $\{X_t\}$ and the fitted parameters $\widehat\alpha_i,\widehat\beta_j$ are called residuals. If the model is suitable (reasonable), residuals should approximately be a realization of white noise (uncorrelated, zero mean, constant variance). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定义：所有 ARMA 过程都包含一个白噪声序列。从数据和拟合参数还原出的 Ẑₜ 称为残差。若模型合理，残差应近似为白噪声的一次实现：不相关、均值为零、方差恒定。</span></details>


**4.4.1 Autoregressive processes** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.4.1 自回归过程。</span></details>

$$X_t=\sum_{i=1}^p\alpha_iX_{t-i}+Z_t\quad\Longleftrightarrow\quad Z_t=X_t-\sum_{i=1}^p\alpha_iX_{t-i}.$$

> [!example]- PDF 第 5 页原貌（含原有批注）
> ![PDF p.5](<附件/ch4-updated-p05.png>)

## PDF p.6


Estimate $\widehat\alpha_i$ s.t. $\sum_{t=p+1}^n(x_t-\sum_{i=1}^p\alpha_ix_{t-i})^2$ is a minimum. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">估计 αᵢ，使残差平方和达到最小。</span></details>


N.B. Any non-zero mean can be eliminated at the identification stage. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：非零均值可在识别阶段去除。</span></details>


The L.S. solution is given by the Yule-Walker equation, $\alpha=R^{-1}\rho$, where $\rho=(\rho_1,\ldots,\rho_p)^T$, the vector of the first p sample autocorrelation coefficients, and R is the $p\times p$ matrix with (i,j)th elements $\rho_{|i-j|}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">原文称最小二乘解由 Yule–Walker 方程给出，其中 ρ 为前 p 阶样本自相关向量，R 为对应相关矩阵。</span></details>

> [!note] 原文核对提示
> 上述“L.S. solution”照录。有限样本的条件最小二乘估计与使用样本 ACF 的 Yule–Walker 估计一般并不完全相同；不要据此把两种计算法在任何样本中都视为同一结果。

**4.4.2 Moving average processes** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.4.2 移动平均过程。</span></details>

$$X_t=Z_t+\sum_{j=1}^q\theta_jZ_{t-j}\quad\Longleftrightarrow\quad Z_t=X_t-\sum_{j=1}^q\theta_jZ_{t-j}.$$

Residuals must be calculated recursively. Since expectation $E[Z_t]=0$, for all t, take unobservable $Z_0,Z_{-1},\ldots$ zero and calculate <details class="translation-details"><summary>中文译文</summary><span class="translation-body">残差必须递推计算。由于各期白噪声均值为零，把无法观测的初始值设为零，再计算：</span></details>

$$
\begin{aligned}
Z_1^*&=x_1,\\
Z_2^*&=x_2-\theta_1Z_1^*,\\
Z_3^*&=x_3-\theta_1Z_2^*-\theta_2Z_1^*,\\
&\cdots\\
Z_{q+1}^*&=x_{q+1}-\sum_{j=1}^q\theta_jZ_{q+1-j},\ldots
\end{aligned}
$$

Then minimize $\sum_{t=1}^n Z_t^{*2}$ numerically. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">然后数值最小化递推残差的平方和。</span></details>


**4.4.3 Mixed processes** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.4.3 混合过程。</span></details>

$$X_t=\sum_{i=1}^p\alpha_iX_{t-i}+Z_t+\sum_{j=1}^q\beta_jZ_{t-j}\quad\Longleftrightarrow\quad X_t-\sum_{i=1}^p\alpha_iX_{t-i}-\sum_{j=1}^q\beta_jZ_{t-j}=Z_t.$$

Then calculate $Z_t^*$ recursively as above. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">再像上面一样递推计算残差。</span></details>


Ex. ARMA(1,1) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：ARMA(1,1)。</span></details>

$$X_t-\mu=\alpha_1(X_{t-1}-\mu)+Z_t+\beta_1Z_{t-1}.$$

Given N observations $x_1,x_2,\ldots,x_N$, we guess values for $\mu,\alpha_1,\beta_1$. Set $Z_0^*=0$ and $x_0=\mu$, then calculate the residuals recursively <details class="translation-details"><summary>中文译文</summary><span class="translation-body">给定 N 个观测，先试取 μ、α₁、β₁，设初始残差为零、初始 x 为 μ，递推计算残差：</span></details>

$$
\begin{aligned}
Z_1^*&=x_1-\mu,\\
Z_2^*&=x_2-\mu-\alpha_1(x_1-\mu)-\beta_1Z_1^*,\\
&\cdots\\
Z_N^*&=(x_N-\mu)-\alpha_1(x_{N-1}-\mu)-\beta_1Z_{N-1}.
\end{aligned}
$$

The residual sum of squares $\sum_{t=1}^N Z_t^{*2}$ may then be calculated. Then other values of $\alpha_1,\beta_1$ may be tried until the minimum is found. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">随后计算残差平方和，再尝试其他参数值，直到找到最小值。上面末项未加星号，沿用原印刷符号。</span></details>


Note: A more general and rigorous theory on estimation of parameters in ARIMA models is based on maximum likelihood. For interested students, you may <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意：ARIMA 参数估计更一般、更严格的理论以最大似然为基础。有兴趣的同学可以：</span></details>


> [!example]- PDF 第 6 页原貌（含原有批注）
> ![PDF p.6](<附件/ch4-updated-p06.png>)

## PDF p.7


refer to Chapter 3 of Harvey (Time Series Models, 1993) or Ch. 7 of Wei (Time series analysis : univariate and multivariate methods, 1993). A brief account is shown below. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">参阅 Harvey《Time Series Models》（1993）第 3 章，或 Wei《Time series analysis: univariate and multivariate methods》（1993）第 7 章。以下作简要介绍。</span></details>


**4.5 Maximum likelihood estimation** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.5 最大似然估计。</span></details>


We begin with the non-time series case. Suppose that we have a sample of independent observations $X_t$, t = 1, 2, …, N each with pdf $f(X_t)$. Then the joint density function is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">先考虑非时间序列情形。若 N 个观测相互独立，各自的概率密度为 f(Xₜ)，则联合密度为：</span></details>

$$f(X_1,X_2,\ldots,X_N)=\prod_{t=1}^N f(X_t).\tag{4.2}$$

Let $X_t$ contain an unknown parameter $\theta$ (it can also be a vector). The likelihood function is the joint density (4.2), but is regarded as a function of the parameter $\theta$, and as such is written <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设分布含未知参数 θ，也可以是参数向量。把联合密度视为 θ 的函数，就得到似然函数：</span></details>

$$L(\theta)=\prod_{t=1}^N f(X_t;\theta).$$

The maximum likelihood estimates (MLEs) are naturally found by maximizing $L(\theta)$ with respect to $\theta$. A usual trick is to maximize $\log(L(\theta))$ instead of $L(\theta)$. It's because the log function is a concave function. The problem with time series is that the observations are not independent, so that (4.2) is not applicable. If, however, we denote all observations up to and including $X_t$ by $XX_t$ (which is a vector in general) we can write <details class="translation-details"><summary>中文译文</summary><span class="translation-body">最大似然估计通过最大化似然函数得到。通常改为最大化对数似然。原文解释为对数函数是凹函数。时间序列观测不独立，不能直接使用式（4.2）；把截至 t 的全部观测记为向量 XXₜ，则：</span></details>

$$
\begin{aligned}
f(X_1,\ldots,X_N)&=f(X_N\mid XX_{N-1})f(X_1,\ldots,X_{N-1})\\
&=f(X_N\mid XX_{N-1})f(X_{N-1}\mid XX_{N-2})f(X_1,\ldots,X_{N-2}).
\end{aligned}
$$

and so on until <details class="translation-details"><summary>中文译文</summary><span class="translation-body">依此展开，直到：</span></details>

$$f(X_1,\ldots,X_N)=\prod_{t=1}^N f(X_t\mid XX_{t-1}).$$

where $f(X_t\mid XX_{t-1})$ is the conditional distribution of $X_t$ given all observations prior to t. So the likelihood $L(\theta)$ can be written as the product of these conditional distributions. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中每一项都是给定此前所有观测时 Xₜ 的条件分布。因此似然可以写成这些条件密度的乘积。</span></details>

> [!note] 原文核对提示
> 取对数不改变最大值位置的关键是对数严格递增；凹性本身不足以说明这一点。此处另作说明，不替换原文。

**Example 1: AR2 model** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 1：AR(2) 模型。</span></details>


Let the model be $X_t=\phi_1X_{t-1}+\phi_2X_{t-2}+a_t$, where $\{a_t\}$ is a white noise series, or a series of normally distributed, independent random variables with zero mean and variance $\sigma^2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">设模型为 AR(2)，其中 aₜ 为白噪声；此处正态似然计算使用独立、零均值、方差 σ² 的正态噪声。</span></details>


Then the mean of the conditional distribution (which is normal) $f(X_t\mid X_1,X_2,\ldots,X_{t-1})$ is $\phi_1X_{t-1}+\phi_2X_{t-2}$, and the variance of the conditional distribution is $\sigma^2$, and therefore <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则条件分布是正态分布，条件均值为前两期观测的线性组合，条件方差为 σ²，因此：</span></details>


> [!example]- PDF 第 7 页原貌（含原有批注）
> ![PDF p.7](<附件/ch4-updated-p07.png>)

## PDF p.8

$$f(X_t\mid X_1,\ldots,X_{t-1})=\frac1{\sqrt{2\pi\sigma^2}}\exp\left[-\frac{(X_t-\phi_1X_{t-1}-\phi_2X_{t-2})^2}{2\sigma^2}\right].$$

Problems arise for t=1 and t=2 because $f(X_1)$ and $f(X_2\mid X_1)$ are not known. To get around this, we assume that the first two observations $X_1,X_2$ are fixed and define the conditional likelihood as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">前两项密度未知。因此可把前两个观测视为给定，考虑条件似然：</span></details>

$$L(\theta)=\prod_{t=3}^N f(X_t\mid XX_{t-1}).$$

The conditional log-likelihood is therefore <details class="translation-details"><summary>中文译文</summary><span class="translation-body">条件对数似然为：</span></details>

$$\log L(\phi_1,\phi_2)=l(\phi_1,\phi_2)=-\frac{N-2}{2}\log(2\pi\sigma^2)-\frac1{2\sigma^2}\sum_{t=3}^N(X_t-\phi_1X_{t-1}-\phi_2X_{t-2})^2.$$

If $\sigma^2$ is known, maximizing the conditional likelihood is equivalent to minimizing <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若 σ² 已知，最大化条件似然等价于最小化：</span></details>

$$\sum_{t=3}^N(X_t-\phi_1X_{t-1}-\phi_2X_{t-2})^2.\tag{4.3}$$

That means the conditional maximum likelihood estimator is equivalent to the conditional least squares estimator. We stress that this is not always the case. In general we have to use nonlinear optimization techniques, such as the Newton's method. See the next example on MA1 model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">这意味着条件最大似然估计等价于条件最小二乘估计。但必须强调，这并不总是成立；一般可能需要非线性优化，如下面 MA(1) 例子中的牛顿法。</span></details>


If $\sigma^2$ is unknown, it can be shown from direct differentiation that the maximum likelihood estimator of $\sigma^2$ is the minimum sum of squares from (4.3) divided by the number of terms included in the sum. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">若 σ² 未知，直接求导可证明，其最大似然估计是式（4.3）的最小残差平方和除以求和项数。</span></details>


**Note: Newton's method** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注：牛顿法。</span></details>


Let f(x)=0 be a nonlinear algebraic equation in one unknown. Then a well-known algorithm, known as Newton's method, for finding the roots of the equation is given by the following iterative scheme. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对单变量非线性代数方程 f(x) = 0，著名的牛顿求根法使用下列迭代格式。</span></details>

$$x_{n+1}=x_n-\frac{f(x_n)}{f'(x_n)}.$$

Illustration: Find a root of $x^3-2x-5=0$ near 2 to 4 decimal places. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">示例：求该三次方程在 2 附近的根，精确到小数点后四位。</span></details>


Solution: The Newton's scheme is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解：牛顿迭代格式为：</span></details>

$$x_{n+1}=x_n-\frac{x_n^3-2x_n-5}{3x_n^2-2}.$$

Let $x_0=2$, then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">取初值 2，则：</span></details>


> [!example]- PDF 第 8 页原貌（含原有批注）
> ![PDF p.8](<附件/ch4-updated-p08.png>)

## PDF p.9

$$x_1=2-\frac{-1}{10}=2.1,\quad x_2=2.1-\frac{0.0061}{11.23}=2.09457,\quad x_3=2.09455.$$

Thus the root is 2.0946. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以根约为 2.0946。</span></details>

> [!note] 原文核对提示
> 上述分子 0.0061 照录原印刷；代入原方程得到 f(2.1) = 0.061，与印刷分子相差一个小数位。

**Example 2: MA1 model** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例 2：MA(1) 模型。</span></details>


We have a time series data set $\{x_1,x_2,\ldots,x_n\}$ and we believe the model is MA1, i.e., $X_t=\theta a_{t-1}+a_t$, where $\{a_t\}$ is a white noise series as in the above example, i.e., normal variables with mean zero and variance $\sigma^2$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">给定数据，相信其来自 MA(1) 模型；噪声与上例相同，是零均值、方差 σ² 的正态白噪声。</span></details>


We want to estimate $\theta$ & $\sigma^2$. Using similar argument as Example 1, the conditional likelihood is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">目标是估计 θ 和 σ²。与例 1 类似，条件似然为：</span></details>

$$\prod_{t=2}^n\left[\frac1{\sqrt{2\pi\sigma^2}}\exp\left\{-\frac{(x_t-\theta a_{t-1})^2}{2\sigma^2}\right\}\right],$$

and hence the conditional log-likelihood, apart from a constant, is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而，忽略常数项后的条件对数似然为：</span></details>

$$l(\theta,\sigma^2)=l=-\frac{n-1}{2}\log\sigma^2-\frac{\sum_{t=2}^n(x_t-\theta a_t)^2}{2\sigma^2}.$$

To simplify the algebra, let $\sigma^2=s$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为简化代数，令 σ² = s。</span></details>

$$l=-\frac{n-1}{2}\log s-\frac{\sum_{t=2}^n(x_t-\theta a_t)^2}{2s}.\tag{4.4}$$

The maximum likelihood procedure is to solve the two equations $\partial l/\partial\theta=0$, & $\partial l/\partial s=0$. It turns out we basically only need to solve $\partial l/\partial\theta=0$. Note that this is a nonlinear equation in $\theta$. We can use Newton's method. That means we need to deal with <details class="translation-details"><summary>中文译文</summary><span class="translation-body">最大似然估计令两个偏导数为零。主要需解关于 θ 的非线性方程，可使用牛顿法：</span></details>

$$\theta_{n+1}=\theta_n-\left[\left.\frac{\partial^2l}{\partial^2\theta}\right|_{\theta_n}\right]^{-1}\left[\left.\frac{\partial l}{\partial\theta}\right|_{\theta_n}\right].\tag{4.5}$$
> [!note] 原文核对提示
> 本页似然首式为 aₜ₋₁，但随后式（4.4）及下一页导数改写为 aₜ；两处下标照录，不将不一致悄悄统一。牛顿法中的二阶偏导分母也沿用印刷写法。

> [!example]- PDF 第 9 页原貌（含原有批注）
> ![PDF p.9](<附件/ch4-updated-p09.png>)

## PDF p.10


To carry out the iterations in (4.5), we have to calculate the 1st and 2nd derivatives in the equation. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">要执行式（4.5）的迭代，需要计算方程中的一阶与二阶导数。</span></details>


Now $a_t=x_t-\theta a_{t-1}$. This is an important difference from the AR case, because $a_t$ is a function of $\theta$. Thus <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 aₜ 递推依赖 θ，这与 AR 情形有重要区别。因此：</span></details>

$$\frac{\partial a_t}{\partial\theta}=-\theta\frac{\partial a_{t-1}}{\partial\theta}-a_{t-1},\qquad \frac{\partial^2a_t}{\partial\theta^2}=-2\frac{\partial a_{t-1}}{\partial\theta}-\theta\frac{\partial^2a_{t-1}}{\partial\theta^2}.$$

From (4.4), <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由式（4.4）：</span></details>

$$\frac{\partial l}{\partial\theta}=-\frac12\sum_{t=2}^n(-2)\frac{x_t-\theta a_t}{s}\left(\theta\frac{\partial a_t}{\partial\theta}+a_t\right),$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$\frac{\partial^2l}{\partial\theta^2}=\frac1s\sum_{t=2}^n\left\{-\left(\theta\frac{\partial a_t}{\partial\theta}+a_t\right)^2+(x_t-\theta a_t)\left(2\frac{\partial a_t}{\partial\theta}+\theta\frac{\partial^2a_t}{\partial\theta^2}\right)\right\}.$$

Note that we have to make assumptions on the initial values, i.e., $\theta_0,a_0,\partial a_0/\partial\theta$, & $\partial^2a_0/\partial\theta^2$. So the MA case is considerably more complicated than the AR case. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意，需要指定参数、初始噪声及其一阶和二阶导数的初值。MA 情形比 AR 情形复杂得多。</span></details>


Finally, differentiating (4.4) with respect to s gives us <details class="translation-details"><summary>中文译文</summary><span class="translation-body">最后，对 s 求导得到：</span></details>

$$\frac{\partial l}{\partial s}=\sum_{t=2}^n\left[\frac1s-\frac{(x_t-\theta a_t)^2}{s^2}\right]=0\quad\Rightarrow\quad s=\frac{\sum_{t=2}^n(x_t-\widehat\theta a_t)^2}{n-1}.$$

Here $\widehat\theta$ is the estimate of $\theta$ obtained from (4.5). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">θ̂ 是由式（4.5）得到的 θ 的估计。</span></details>

> [!note] 原文核对提示
> 原印刷的 ∂l/∂s 与直接对式（4.4）求导相差一个非零常数因子，设为零的方程不变；公式仍照录。噪声下标问题见上一页。

**4.6 Diagnostic checking (Residual analysis)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">4.6 诊断检验（残差分析）。</span></details>


Check that the estimated residual series $\{\widehat Z_t\}$ is consistent with white noise. Same techniques are relevant here. General guide, use <details class="translation-details"><summary>中文译文</summary><span class="translation-body">检查估计残差序列是否符合白噪声。前面的相关技术同样适用，一般使用：</span></details>


(i) time plot of $\{\widehat Z_t\}$ <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（i）残差时间图。</span></details>


(ii) correlogram of residuals <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（ii）残差相关图。</span></details>


(iii) cumulative periodogram test (a frequency domain technique) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（iii）累积周期图检验（频域方法）。</span></details>


(iv) trial over-fitting, i.e., examine residual sum of squares for chosen model and suitably chose extensions. Usually calculate $100(1-\operatorname{var}(\widehat Z)/\operatorname{var}(X))$, i.e., % of variance explained by model. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（iv）尝试过拟合：比较所选模型及适当扩展模型的残差平方和，常报告所列的模型方差解释百分比。</span></details>


(v) Box-Pierce statistics and Ljung-Box statistics ($\chi^2$ test) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（v）Box–Pierce 与 Ljung–Box 统计量（卡方检验）。</span></details>


> [!example]- PDF 第 10 页原貌（含原有批注）
> ![PDF p.10](<附件/ch4-updated-p10.png>)

## PDF p.11


Box-Pierce: $n\sum_{k=1}^m\widehat r^2(k)$ follows $\chi^2_{m-p-q}$ asymptotically. Good for large samples. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Box–Pierce 统计量渐近服从自由度 m−p−q 的卡方分布，适合大样本。</span></details>


Ljung-Box: $n(n+2)\sum_{k=1}^m\widehat r^2(k)/(n-k)$ follows $\chi^2_{m-p-q}$ asymptotically. Works better for small samples. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Ljung–Box 加入有限样本调整，小样本表现较好；同样使用自由度 m−p−q 的渐近卡方分布。</span></details>


Proposition: Let $e_t$ be a white noise sequence, namely, i.i.d. random variables with zero mean and constant variance 1. Consider the lag-1 autocorrelation coefficient of $e_t$, $\rho_1$, which is given by: <details class="translation-details"><summary>中文译文</summary><span class="translation-body">命题：设 eₜ 为白噪声，即独立同分布、均值为 0、方差为 1 的随机变量。考虑其一阶自相关系数：</span></details>

$$\rho_1=\frac{\sum_{t=1}^{n-1}e_te_{t+1}}{\sum_{t=1}^ne_t^2}.$$

Then $\operatorname{var}(\rho_1)\approx1/n$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">则该系数的方差约为 1/n。</span></details>


Proof: Let $X=\sum_{t=1}^{n-1}e_te_{t+1}$ and $Y=\sum_{t=1}^ne_t^2$, so $\rho_1=X/Y$. Observe $E(X)=\mu_x=0$ and $E(Y)=\mu_y=n$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：将分子和分母分别记为 X 和 Y。它们的均值分别为 0 和 n。</span></details>


For $f(X,Y)=X/Y$, using a Taylor expansion about $(\mu_x,\mu_y)=(0,n)$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对比值函数在 (0,n) 附近作泰勒展开：</span></details>

$$
\begin{aligned}
f(X,Y)&\approx f(\mu_x,\mu_y)+\left.\frac{\partial f}{\partial X}\right|_{(\mu_x,\mu_y)}(X-\mu_x)+\left.\frac{\partial f}{\partial Y}\right|_{(\mu_x,\mu_y)}(Y-\mu_y)\\
&=0+\frac Xn+0.
\end{aligned}
$$

Thus $\operatorname{var}(X/Y)\approx\operatorname{var}(X/n)$. But <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以比值的方差近似为 X/n 的方差。而：</span></details>

$$
\begin{aligned}
\operatorname{var}(X)&=\operatorname{var}\left(\sum_{t=1}^{n-1}e_te_{t+1}\right)=E\left(\sum_{t=1}^{n-1}e_te_{t+1}\right)^2\\
&=E\left(\sum_{t=1}^{n-1}e_t^2e_{t+1}^2\right)+E\left(\sum_t\sum_{t'\ne t}e_te_{t+1}e_{t'}e_{t'+1}\right).
\end{aligned}
$$

The second term vanishes because $e_t$ is white noise and $t\ne t'$. Hence <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在上述独立、零均值假设下，交叉项为零。因此：</span></details>

$$\operatorname{var}(X)=E\left(\sum_{t=1}^{n-1}e_t^2e_{t+1}^2\right)=n-1,\quad \operatorname{var}(\rho_1)\approx\frac{n-1}{n^2}\approx\frac1n.$$

> [!example]- PDF 第 11 页原貌（含原有批注）
> ![PDF p.11](<附件/ch4-updated-p11.png>)

## PDF p.12


**Example on model fitting:** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">模型拟合实例。</span></details>


Data -- US quarterly unemployment data, 1948–1978 (121 observations, from Cryer 1982). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">数据：1948—1978 年美国季度失业率；原文标注 121 个观测，来源 Cryer（1982）。</span></details>


**unemploy / ar2-residuals** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两列分别为失业率和 AR(2) 模型残差。以下保留原始数据表及教师手写批注；数据接续至第 14 页。</span></details>

![Original unemployment data and AR2 residuals, PDF p.12](<附件/ch4-updated-p12.png>)

## PDF p.13


**unemploy / ar2-residuals (continued)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">失业率与 AR(2) 残差表续页，含教师批注。为避免扫描数字转录误差，完整保留原数据表图。</span></details>

![Original unemployment data and AR2 residuals, PDF p.13](<附件/ch4-updated-p13.png>)

## PDF p.14


**unemploy / ar2-residuals (continued)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">失业率与 AR(2) 残差表续页，含教师批注。</span></details>

![Original unemployment data and AR2 residuals, PDF p.14](<附件/ch4-updated-p14.png>)

## PDF p.15


**US quarterly unemployment data — time plot** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">美国季度失业率时间图。Index 表示时间序号，unemploy 为失业率。</span></details>


**MTB > acf c1 / Autocorrelation Function: unemploy / ACF of unemploy** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Minitab 命令及失业率自相关输出。相关图的 ASCII 图形、各阶数值及教师批注完整保留如下；第 16 页顶部接续第 27—30 阶。</span></details>

![Time plot and original ACF output, PDF p.15](<附件/ch4-updated-p15.png>)

## PDF p.16


**ACF of unemploy (continued)** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">失业率 ACF 续页：第 27—30 阶分别为 −0.319、−0.340、−0.364、−0.384。</span></details>


**MTB > pacf 20 c1 / Partial Autocorrelation Function: unemploy / PACF of unemploy** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Minitab 命令及失业率前 20 阶偏自相关输出；原 ASCII 图形及批注见本页原貌。</span></details>


| Lag | PACF | Lag | PACF |
| ---: | ---: | ---: | ---: |
| 1 | .936 | 11 | .018 |
| 2 | -.605 | 12 | .001 |
| 3 | .098 | 13 | .161 |
| 4 | .052 | 14 | -.021 |
| 5 | .120 | 15 | .053 |
| 6 | -.033 | 16 | -.090 |
| 7 | -.049 | 17 | -.136 |
| 8 | .022 | 18 | -.044 |
| 9 | .098 | 19 | -.066 |
| 10 | -.138 | 20 | -.078 |


**ARIMA Model: unemploy / Modified Box-Pierce (Ljung-Box) Chi-Square statistic** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">失业率 ARIMA 模型的修正 Box–Pierce（Ljung–Box）卡方检验结果。Lag 为检验滞后阶数，DF 为自由度。</span></details>


| Lag | 12 | 24 | 36 | 48 |
| --- | ---: | ---: | ---: | ---: |
| Chi-Square | 17.9 | 32.8 | 44.1 | 50.1 |
| DF | 9 | 21 | 33 | 45 |
| P-Value | .036 | .048 | .094 | .278 |


**Series: unemploy / ARIMA(2,0,0) with non-zero mean / Coefficients** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">序列 unemploy，模型为含非零均值的 ARIMA(2,0,0)。下表为系数及标准误。</span></details>


| | ar1 | ar2 | mean |
| --- | ---: | ---: | ---: |
| Coefficients | 1.5476 | -.6450 | 5.0819 |
| s.e. | .0682 | .0687 | .3275 |


**sigma^2 estimated as 0.1318: log likelihood = −49.17 / AIC = 106.34 AICc = 106.68 BIC = 117.52** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">估计噪声方差 0.1318，对数似然 −49.17，AIC、AICc、BIC 分别为 106.34、106.68、117.52。</span></details>


> [!example]- PDF 第 16 页原貌（含原有批注）
> ![PDF p.16](<附件/ch4-updated-p16.png>)

## PDF p.17


**ARIMA Model: unemploy / Modified Box-Pierce (Ljung-Box) Chi-Square statistic** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">另一失业率模型的 Ljung–Box 检验结果。</span></details>


| Lag | 12 | 24 | 36 | 48 |
| --- | ---: | ---: | ---: | ---: |
| Chi-Square | 15.7 | 31.2 | 40.6 | 46.7 |
| DF | 8 | 20 | 32 | 44 |
| P-Value | .047 | .052 | .142 | .362 |


**Series: unemploy / ARIMA(2,0,1) with non-zero mean / Coefficients** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">序列 unemploy，模型为含非零均值的 ARIMA(2,0,1)。下表为系数与标准误。</span></details>


| | ar1 | ar2 | ma1 | mean |
| --- | ---: | ---: | ---: | ---: |
| Coefficients | 1.4194 | -.5245 | .2286 | 5.0834 |
| s.e. | .1133 | .1109 | .1291 | .3651 |


**sigma^2 estimated as 0.1295: log likelihood = −47.65 / AIC = 105.29 AICc = 105.82 BIC = 119.27** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">估计噪声方差 0.1295，对数似然 −47.65，AIC、AICc、BIC 分别为 105.29、105.82、119.27。</span></details>


Hence AIC and AICC choose the ARMA(2,1) model, while BIC chooses AR(2). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，AIC 和 AICC 选择 ARMA(2,1)，BIC 选择 AR(2)。</span></details>


**Example: Calculation of Box-Pierce and Ljung-Box statistics** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">例：计算 Box–Pierce 和 Ljung–Box 统计量。</span></details>


**Modified Box-Pierce (Ljung-Box) Chi-Square statistic** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以下是原文再次列出的检验表。</span></details>


| Lag | 12 | 24 | 36 | 48 |
| --- | ---: | ---: | ---: | ---: |
| Chi-Square | 17.9 | 32.8 | 44.1 | 50.1 |
| DF | 9 | 21 | 33 | 45 |
| P-Value | .036 | .048 | .094 | 0.2 |

> [!note] 原文核对提示
> 本表末项印刷为 0.2，上一页同组统计量的末项为 .278，两个版本分别照录。

**ACF of ar2-err** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AR(2) 残差的自相关系数。原 ASCII 图形保留在本页原貌中。</span></details>


| Lag | ACF | Lag | ACF |
| ---: | ---: | ---: | ---: |
| 1 | .103 | 7 | .190 |
| 2 | -.056 | 8 | -.136 |
| 3 | -.037 | 9 | .072 |
| 4 | -.112 | 10 | .091 |
| 5 | -.040 | 11 | .111 |
| 6 | .133 | 12 | -.095 |

> [!example]- PDF 第 17 页原貌（含原有批注）
> ![PDF p.17](<附件/ch4-updated-p17.png>)

## PDF p.18


Hence the Box-Pierce and Ljung-Box statistics are given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，Box–Pierce 与 Ljung–Box 统计量分别为：</span></details>

$$\mathrm{BP}\text{ (up to 12 terms)}=121\bigl(.103^2+(-.056)^2+\cdots+.111^2+(-.905)^2\bigr)=16.5,$$
$$\mathrm{LB}\text{ (up to 12 terms)}=121(123)\left[\frac{.103^2}{120}+\frac{(-.056)^2}{119}+\cdots+\frac{(-.095)^2}{109}\right]=17.9.$$

As $\chi^2_{9,.05}=16.9$, BP is not significant at 5%, but LB is. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于自由度为 9 的卡方分布 5% 上尾临界值约为 16.9，BP 在 5% 水平不显著，而 LB 显著。</span></details>

> [!note] 原文核对提示
> BP 展开式最后一项原印刷为 −.905，与上一页残差 ACF 和本页 LB 式的 −.095 不一致；这里照录并提示。手写检验区域示意图全部保留在原页中。

> [!example]- PDF 第 18 页原貌（含原有批注）
> ![PDF p.18](<附件/ch4-updated-p18.png>)

