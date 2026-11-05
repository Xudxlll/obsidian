# Chapter 2：字幕重点与考核提醒

> [!info] 证据说明
> 按 Week 2—3 字幕整理。标注“课堂推导”的内容是老师讲过的过程，并不自动代表老师明确要求考试证明。

## 平稳性、白噪声与自相关

Week 2 00:01—00:14 区分严格平稳与弱平稳；本课程侧重弱平稳：均值为常数、协方差只依赖时间间隔且二阶矩有限。注意字幕常把 stationarity 错识成 seasonality。零均值时协方差才可直接化为乘积期望。见 [[01 - Chapter 2（英文原文与折叠译文）#2.2 Further discussion on weak stationarity / 进一步讨论弱平稳性|2.2 弱平稳]]。

Week 2 00:15—00:27 老师逐步计算 $Z_t=a_t+0.5a_{t-1}$ 的均值、方差、自协方差和 $\rho_1=0.4$；会识别两个时点共有的白噪声项。00:29:36 老师就当时图形说不会只看图回答、强调计算，不能推为不考任何图。01:10—01:18 解释样本 ACF 图和近似界限 $\pm 2/\sqrt n$，其适用性取决于模型和近似条件，不能作为所有模型的通用精确界限。

## 一般线性过程：老师讲过证明

Week 2 01:21:04—01:30:27，老师对 $Y_t=\sum_{i\ge0}\psi_i\varepsilon_{t-i}$ 在系数平方可和等条件下证明弱平稳：均值为零，方差 $\sigma_\varepsilon^2\sum\psi_i^2$ 有限，自协方差（$k\ge0$）为 $\sigma_\varepsilon^2\sum\psi_i\psi_{i+k}$，不依赖 $t$。字幕中个别下标漏掉 $k$，应以时间索引相同的白噪声项为准。**字幕未明确说必须完整证明**。见 [[01 - Chapter 2（英文原文与折叠译文）#2.3 General Linear Process / 一般线性过程|2.3 一般线性过程]]。

## 线性趋势与双重指数平滑

- Week 2 01:31—01:41 展示简单平滑对线性趋势的滞后偏差：在所用长期近似和初始化条件下，$E(S_t)\approx E(X_t)-\frac{1-\alpha}{\alpha}b_2$；不要把长期公式误当作任意初始值下严格有限样本恒等式。见 [[01 - Chapter 2（英文原文与折叠译文）#2.4 Exponential smoothing for a linear trend process / 线性趋势过程的指数平滑|2.4 线性趋势平滑]]。
- Week 3 00:03:28—00:12 老师推导公式 (2.5.2)；00:20:14 要记住直觉：一次平滑滞后原序列，二次平滑滞后一次平滑，在线性趋势设定和相应近似下利用两者之差修正滞后。要会递推 $S_t$、$S_t^{(2)}$ 并计算预测。证明讲过，**未见明确要求考试完整证明**。见 [[01 - Chapter 2（英文原文与折叠译文）#2.5 Double exponential smoothing (for linear trend process) / 双重指数平滑（适用于线性趋势过程）|2.5 双重指数平滑]] 和 [[03 - Proof of (2.5.2) 手写证明|手写证明]]。
- Week 3 00:31:39—00:31:47 老师针对**三重指数平滑及其复杂高阶公式**说只到双重平滑，三重部分看一下即可；00:32:59 又说一般 $n$ 阶展开可以略过。这是该段的课堂提示，后续如有正式范围调整，以最新要求为准。

来源：[[字幕课堂整理/附件/week2 FORECASTING AND APPLIED TIME SERIES ANALYSIS - Zoom-source (1).srt|Week 2]]、[[字幕课堂整理/附件/week3 FORECASTING AND APPLIED TIME SERIES ANALYSIS - Zoom-source.srt|Week 3]]；[[00 - 考核事项与重点（待完整核对）|考核事项汇总]]。
