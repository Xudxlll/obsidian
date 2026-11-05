# Chapter 3：字幕重点与考核提醒

> [!important] 老师明确强调
> Week 3 01:32:30—01:32:37：Chapter 3 和 Chapter 4 都重要，要特别注意。下列“课堂推导”不等同于已确认必须在考试中证明。

## AR(1)、MA 与随机游走

- Week 3 01:02—01:31：对于 $X_t=\phi X_{t-1}+\varepsilon_t$ 的零均值因果平稳模型，$|\phi|<1$，$\operatorname{Var}(X_t)=\sigma^2/(1-\phi^2)$，$\rho_k=\phi^{|k|}$；老师从模型乘滞后项和取期望展示递推，也展示 MA($\infty$) 表示。零协方差需要创新与过去不相关等条件，不能只凭创新均值为零把乘积期望拆开。见 [[01 - Chapter 3（英文原文与折叠译文）#3.3.2 First order Autoregressive Process / 一阶自回归过程|3.3.2 AR(1)]]。
- Week 4 00:01—00:17：MA(q) 自协方差由相同创新时点的项产生；超过 q 阶的理论 ACF 为零。例题先算 $\rho_1$ 再结合可逆条件求参数。见 [[01 - Chapter 3（英文原文与折叠译文）#3.3.3 Finite order moving average process / 有限阶移动平均过程|3.3.3 MA(q)]]。
- Week 4 00:28—00:35：随机游走方差随时间增长；一次差分得到白噪声。见 [[01 - Chapter 3（英文原文与折叠译文）#3.3.4 Random Walk / 随机游走|3.3.4 随机游走]]。

## 平稳与可逆：不要混淆

Week 4 01:05—01:14 讲 MA 多项式的根在单位圆外是可逆条件；01:19—01:26 讲 AR 根及平稳的因果解。**有限阶 MA 过程在常见白噪声条件下本身可平稳，却未必可逆**；平稳与可逆是不同性质。Week 3 00:57—00:58 及 Week 4 00:19—00:22 字幕将两者近似等同，不能据此认为二者相同。根的模须严格大于 1。见 [[01 - Chapter 3（英文原文与折叠译文）#3.4.1 Infinite and finite order moving average process / 无限阶与有限阶移动平均过程|3.4.1 可逆性]]。

## AR(2) 证明及低阶题目

Week 4 01:19:55—01:26:47 展示互异根情形的 AR(2) 平稳条件证明：齐次部分随时间衰减，且因果 MA 展开可收敛，联系根模大于 1。01:29:02 老师在一般高阶推导语境说通常处理到二阶、可能要求写公式；01:45:58 对一般情形说先略过。**无法据此确定 AR(2) 证明必考或不考，也不能将该说法推广成全部模型阶数上限**。见 [[01 - Chapter 3（英文原文与折叠译文）#3.4.2 Finite order autoregressive processes / 有限阶自回归过程|3.4.2 有限阶 AR]]。

Week 5 00:12:32—00:13:07、00:53:10—00:53:53 说作业中 $p+q$ 通常较低，常不超过 2、有时为 3；简化时可能更高，因此不是硬性上限。Week 5 00:29:28 提醒 MA(2) 参数限制中原笔记漏了负号；需对照具体原页及符号约定，不能把这一提醒泛化到所有版本。

## ARMA、差分与季节性

Week 5 00:29—00:50 展示 ARMA(1,1) 展开及 ACF、ARMA(2,1) 根据递推求相关系数；注意符号取决于模型写法。01:05—01:18 区分普通差分 $(1-B)^d$ 和季节差分 $(1-B^s)^D$；字幕有时把前者误称 seasonal，以写出的公式及讲义为准。不要过度差分。见 [[01 - Chapter 3（英文原文与折叠译文）#3.5 Integrated process / 单整过程|3.5 单整]]、[[01 - Chapter 3（英文原文与折叠译文）#3.6 Seasonal models / 季节模型|3.6 季节模型]]。

来源：[[字幕课堂整理/附件/week3 FORECASTING AND APPLIED TIME SERIES ANALYSIS - Zoom-source.srt|Week 3]]、[[字幕课堂整理/附件/week4 FORECASTING AND APPLIED TIME SERIES ANALYSIS - Zoom-source.srt|Week 4]]、[[字幕课堂整理/附件/week5 FORECASTING AND APPLIED TIME SERIES ANALYSIS - Zoom-source.srt|Week 5]]；[[00 - 考核事项与重点（待完整核对）|考核事项汇总]]。
