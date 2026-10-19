---
course: AMA572 Fixed-Income and Credit Risk
source: 02_Lecture2_补充推导_税盾与破产成本_Ito等距版.pdf
pages: 5
created: "2026-10-15"
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 本文对应 Itô 等距版补充推导的全部 5 页，英文和公式按原文保留，中文译文默认折叠。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 2/00 - Lecture 2 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/02_Lecture2_补充推导_税盾与破产成本_Ito等距版.pdf|原 PDF]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 2/03 - 补充推导（Ito 引理及手写批注版）|另一推导版本]]

> [!tip] 先读术语知识框架
> [[AMA572 Fixed-Income and Credit Risk/Lecture 2/06 - 伊藤随机微积分知识框架|伊藤随机微积分知识框架]]：统一中英文名称，串起布朗运动、伊藤积分、二次变差、零均值／鞅性质、伊藤等距与伊藤引理，并说明本篇推导每一步使用哪个工具。**Itô isometry 就是伊藤等距；伊藤引理不是伊藤等距。**

## PDF p.1

# Lecture 2 <details class="translation-details"><summary>中文译文</summary><span class="translation-body">第 2 讲。</span></details>

**Exercise 1** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">练习 1。</span></details>

### 1 Preliminary <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1 预备知识。</span></details>

Note that $V_t=V(t)$ in Lecture 2. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意，Vₜ 就是第 2 讲中的 V(t)。</span></details>

Consider the following stochastic differential equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">考虑下列随机微分方程：</span></details>

$$
\begin{cases}
dV_t=rV_tdt+\sigma V_tdW_t,\\
V_0=1,
\end{cases}\tag{1}
$$

where $r$ and $\sigma$ are constant. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 r 和 σ 为常数。</span></details>

Let $f(t,V_t)=\ln V_t$. Then, we get <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 f(t, Vₜ) = ln Vₜ，则有：</span></details>

$$
\frac{\partial f}{\partial t}=0,\quad
\frac{\partial f}{\partial V_t}=\frac1{V_t},\quad
\frac{\partial^2f}{\partial V_t^2}=-\frac1{V_t^2}.
$$

Applying Itô Lemma yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">应用伊藤引理得到：</span></details>

$$
\begin{aligned}
d(\ln V_t)&=d(f(t,V_t))\\
&=\left(\frac{\partial f}{\partial t}+\frac{\partial f}{\partial V_t}rV_t+\frac12\frac{\partial^2f}{\partial V_t^2}\sigma^2V_t^2\right)dt
+\frac{\partial f}{\partial V_t}\sigma V_tdW_t\\
&=\left\{0+\frac1{V_t}rV_t+\frac12\left(-\frac1{V_t^2}\right)\sigma^2V_t^2\right\}dt
+\frac1{V_t}\sigma V_tdW_t\\
&=\left(r-\frac12\sigma^2\right)dt+\sigma dW_t.
\end{aligned}\tag{2}
$$

Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\ln V_T-\ln V_t
=\int_t^T\left(r-\frac12\sigma^2\right)ds+\int_t^T\sigma dW_s
=\left(r-\frac12\sigma^2\right)(T-t)+\sigma(W_T-W_t),
$$

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
\ln\left(\frac{V_T}{V_t}\right)
=\left(r-\frac12\sigma^2\right)(T-t)+\sigma(W_T-W_t),
$$

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
V_T=V_t\exp\left(\left(r-\frac12\sigma^2\right)(T-t)+\sigma(W_T-W_t)\right).\tag{3}
$$

> [!example] 课堂截图：布朗运动一阶矩
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/09_补充推导第1页_布朗运动一阶矩_截图09-17_1857.PNG]]
> [!example] 课堂截图：Ito引理与二阶矩
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/10_补充推导第1页_Ito引理与二阶矩_截图09-17_1910.PNG]]

#### 课堂手写例题整理：均值、二阶矩与三阶矩

> [!info] 截图解读与补充推导
> 以下将两张截图中的手写例子统一记作 $S_t$。第一张图推导均值，第二张图应用伊藤引理推导二阶矩，并在底部留下三阶矩的问题。**三阶矩的完整解答及下方交叉核验是补充推导，不是截图中已经写出的答案。**原截图与讲义正文均保留不变。

##### 1. 老师举的是什么过程？

老师在页边另举了一个常系数随机过程：

$$
\boxed{
dS_t=\mu\,dt+\sigma\,dW_t,\qquad S_0=0
}
$$

其中：

- $\mu$ 是常数漂移率，决定均值随时间变化的速度；
- $\sigma$ 是常数波动系数；
- $W_t$ 是标准布朗运动，$W_0=0$，且 $W_t\sim N(0,t)$；
- $S_0=0$ 表示过程从 0 出发，不是默认从 1 出发。

这个过程叫作**带漂移的布朗运动（算术布朗运动）**。将随机微分方程积分，可以直接写成：

$$
S_t=\mu t+\sigma W_t.
$$

> [!warning] 不要与正文中的 $V_t$ 混淆
> 手写例子是 $dS_t=\mu\,dt+\sigma\,dW_t$，系数中不含 $S_t$；正文是 $dV_t=rV_tdt+\sigma V_tdW_t$，系数中含 $V_t$，属于几何布朗运动。下列矩公式针对前者，不能不经变换直接套给 $V_t$。

下面用 $E$ 表示期望；若 $W_t$ 是讲义风险调整测度下的布朗运动，则统一将 $E$ 写为 $E^*$，推导形式不变。

##### 2. 一阶矩：求均值 $E[S_t]$

第一张截图中，老师先利用布朗运动增量的均值为 0：

$$
E[dW_t]=0.
$$

对随机微分方程取期望：

$$
\begin{aligned}
dE[S_t]
&=E[dS_t]\\
&=E[\mu\,dt+\sigma\,dW_t]\\
&=\mu\,dt.
\end{aligned}
$$

从 0 积分到 $t$，并使用 $S_0=0$：

$$
E[S_t]-E[S_0]=\int_0^t\mu\,du=\mu t.
$$

因此：

$$
\boxed{E[S_t]=\mu t}
$$

把终点记作老师截图中的 $T$，就是 $E[S_T]=\mu T$。

**直觉：**随机扰动的平均值为 0，所以均值只保留确定性的漂移。

##### 3. 二阶矩：求 $E[S_t^2]$

第二张截图中，老师令：

$$
f(t,s)=s^2.
$$

**第一步：求偏导。**

$$
f_t=0,\qquad f_s=2s,\qquad f_{ss}=2.
$$

**第二步：应用伊藤引理。**

对 $dS_t=\mu\,dt+\sigma\,dW_t$，有：

$$
df(t,S_t)
=\left(f_t+\mu f_s+\frac12\sigma^2f_{ss}\right)dt
+\sigma f_s\,dW_t.
$$

代入上述偏导：

$$
\begin{aligned}
d(S_t^2)
&=\left(0+2\mu S_t+\frac12\sigma^2\times2\right)dt
+2\sigma S_t\,dW_t\\
&=\boxed{(2\mu S_t+\sigma^2)dt+2\sigma S_t\,dW_t}.
\end{aligned}
$$

其中的 $\sigma^2dt$ 就是伊藤引理的二阶修正项，不能按普通链式法则省略。

**第三步：取期望，代入已经求出的均值。**

本例相应的伊藤积分满足均值为 0 的条件，所以随机积分部分取期望后消失，得到：

$$
\begin{aligned}
\frac{d}{dt}E[S_t^2]
&=2\mu E[S_t]+\sigma^2\\
&=2\mu(\mu t)+\sigma^2\\
&=2\mu^2t+\sigma^2.
\end{aligned}
$$

**第四步：从 0 积分到 $t$。**

注意 $E[S_0^2]=0$。将积分变量写成 $u$，避免与积分上限 $t$ 混淆：

$$
\begin{aligned}
E[S_t^2]
&=\int_0^t(2\mu^2u+\sigma^2)\,du\\
&=\left[\mu^2u^2+\sigma^2u\right]_0^t\\
&=\boxed{\mu^2t^2+\sigma^2t}.
\end{aligned}
$$

老师还在图中写出了 $t=1$ 的特例：

$$
\boxed{E[S_1^2]=\mu^2+\sigma^2}
$$

##### 4. 三阶矩：补全老师留下的 $E[S_t^3]$

思路与二阶矩完全相同，只是改取：

$$
f(t,s)=s^3.
$$

**第一步：求偏导。**

$$
f_t=0,\qquad f_s=3s^2,\qquad f_{ss}=6s.
$$

**第二步：应用伊藤引理。**

$$
\begin{aligned}
d(S_t^3)
&=\left(0+3\mu S_t^2+\frac12\sigma^2\times6S_t\right)dt
+3\sigma S_t^2\,dW_t\\
&=\boxed{(3\mu S_t^2+3\sigma^2S_t)dt+3\sigma S_t^2\,dW_t}.
\end{aligned}
$$

**第三步：取期望，依次代入二阶矩和一阶矩。**

随机积分部分的期望为 0，因此：

$$
\begin{aligned}
\frac{d}{dt}E[S_t^3]
&=3\mu E[S_t^2]+3\sigma^2E[S_t]\\
&=3\mu(\mu^2t^2+\sigma^2t)+3\sigma^2(\mu t)\\
&=3\mu^3t^2+6\mu\sigma^2t.
\end{aligned}
$$

这里两个 $3\mu\sigma^2t$ 需要相加，不能漏掉其中一个。

**第四步：从 0 积分到 $t$。**

因为 $E[S_0^3]=0$：

$$
\begin{aligned}
E[S_t^3]
&=\int_0^t\left(3\mu^3u^2+6\mu\sigma^2u\right)du\\
&=\left[\mu^3u^3+3\mu\sigma^2u^2\right]_0^t\\
&=\boxed{\mu^3t^3+3\mu\sigma^2t^2}.
\end{aligned}
$$

因此，老师截图底部问题的答案是：

$$
\boxed{E[S_T^3]=\mu^3T^3+3\mu\sigma^2T^2}
$$

当 $t=1$ 时：

$$
\boxed{E[S_1^3]=\mu^3+3\mu\sigma^2}
$$

##### 5. 为什么随机项取期望后可以消失？

这里使用的是：**适应且平方可积的伊藤积分均值为 0**。本例在任意有限时间区间内，所需的各阶矩均有限，因此可以使用：

$$
E\left[\int_0^t\sigma\,dW_u\right]=0,\qquad
E\left[\int_0^t2\sigma S_u\,dW_u\right]=0,\qquad
E\left[\int_0^t3\sigma S_u^2\,dW_u\right]=0.
$$

这不是说随机项本身等于 0，也不是对任意随机系数都可以无条件地“把 $E[dW_t]=0$ 代进去”。先写成积分再取期望，是上述手写微分步骤更准确的理解方式。

这里求二阶矩、三阶矩用的是**伊藤引理与伊藤积分的零均值性质**；不是直接调用后文的伊藤等距公式。后文等距公式用于计算随机积分的二阶矩，是另一条计算路线。

##### 6. 三个结果汇总：原点矩不等于中心矩

上述“一、二、三阶矩”均指**原点矩**：$E[S_t]、E[S_t^2]、E[S_t^3]$，不是把均值先算出来再做平方或立方。

| 项目 | 任意 $t$ | $t=1$ |
|---|---|---|
| 一阶矩（均值）$E[S_t]$ | $\mu t$ | $\mu$ |
| 二阶原点矩 $E[S_t^2]$ | $\mu^2t^2+\sigma^2t$ | $\mu^2+\sigma^2$ |
| 三阶原点矩 $E[S_t^3]$ | $\mu^3t^3+3\mu\sigma^2t^2$ | $\mu^3+3\mu\sigma^2$ |

**二阶矩不是方差。**方差要减去均值的平方：

$$
\begin{aligned}
\operatorname{Var}(S_t)
&=E[S_t^2]-(E[S_t])^2\\
&=(\mu^2t^2+\sigma^2t)-\mu^2t^2\\
&=\boxed{\sigma^2t}.
\end{aligned}
$$

同样，三阶原点矩一般不为 0，但三阶中心矩为：

$$
\begin{aligned}
E[(S_t-E[S_t])^3]
&=E[S_t^3]-3E[S_t]E[S_t^2]+2(E[S_t])^3\\
&=\boxed{0}.
\end{aligned}
$$

这是因为 $S_t$ 围绕均值对称；在 $\sigma>0、t>0$ 时，其偏度为 0。**不能看到 $E[S_t^3]\ne0$ 就判断分布有偏。**

##### 7. 用布朗运动的显式表达式交叉核验

由 $S_t=\mu t+\sigma W_t$，以及：

$$
E[W_t]=0,\qquad E[W_t^2]=t,\qquad E[W_t^3]=0,
$$

直接展开三次方可得：

$$
\begin{aligned}
E[S_t^3]
&=E[(\mu t+\sigma W_t)^3]\\
&=\mu^3t^3+3\mu^2t^2\sigma E[W_t]
+3\mu t\sigma^2E[W_t^2]+\sigma^3E[W_t^3]\\
&=\mu^3t^3+3\mu\sigma^2t^2.
\end{aligned}
$$

这与伊藤引理推导一致。并且，由布朗运动的正态分布与显式表达式可知：

$$
\boxed{S_t\sim N(\mu t,\sigma^2t)}
$$

这里的正态性来自 $S_t=\mu t+\sigma W_t$，**不是只凭均值和方差就推出正态分布**。

##### 8. 怎样接回讲义正文？

正文已得到：

$$
d(\ln V_t)=\left(r-\frac12\sigma^2\right)dt+\sigma\,dW_t.
$$

令：

$$
S_t=\ln V_t,\qquad \mu=r-\frac12\sigma^2.
$$

因为正文设定 $V_0=1$，所以 $S_0=\ln1=0$，恰好满足老师手写例子的初始条件。于是：

$$
\begin{aligned}
E[\ln V_t]&=\left(r-\frac12\sigma^2\right)t,\\
\operatorname{Var}(\ln V_t)&=\sigma^2t.
\end{aligned}
$$

对正文使用的确定时点 $0\le t<T$，相同思路也给出：

$$
\ln V_T-\ln V_t
=\left(r-\frac12\sigma^2\right)(T-t)+\sigma(W_T-W_t),
$$

其均值为 $\left(r-\frac12\sigma^2\right)(T-t)$，方差为 $\sigma^2(T-t)$。因此，老师在页边举例，是在为后文计算对数资产价值的均值和方差做准备。

> [!summary] 这道例题的核心思路
> 求 $E[S_t^n]$ 时，先对 $f(s)=s^n$ 用伊藤引理，再取期望、代入已经求出的低阶矩，最后按初始条件积分。二阶矩依赖一阶矩，三阶矩依赖二阶矩和一阶矩，按顺序即可逐级求出。

## PDF p.2

Let $X_t=\ln V_t$. Then, it follows from (2) that we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 Xₜ = ln Vₜ，由（2）得到：</span></details>

$$
dX_t=\left(r-\frac12\sigma^2\right)dt+\sigma dW_t.\tag{4}
$$

Taking the expectation for (4) leads to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对（4）取期望得到：</span></details>

$$
d(E^*[X_t])=\left(r-\frac12\sigma^2\right)dt,\tag{5}
$$

since $E^*[dW_t]=0$. Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为 E*[dWₜ] = 0。因此：</span></details>

$$
E^*[X_T-X_t]=E^*[X_T]-E^*[X_t]
=\int_t^T\left(r-\frac12\sigma^2\right)ds
=\left(r-\frac12\sigma^2\right)(T-t).\tag{6}
$$

Let $Y_t=X_t-E[X_t]$. Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 Yₜ = Xₜ − E[Xₜ]，则：</span></details>

$$
\begin{aligned}
dY_t&=dX_t-d(E^*[X_t])\\
&=\left(r-\frac12\sigma^2\right)dt+\sigma dW_t-\left(r-\frac12\sigma^2\right)dt\\
&=\sigma dW_t.
\end{aligned}\tag{7}
$$

Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\begin{aligned}
\operatorname{Var}(X_T-X_t)
&=E^*[(X_T-X_t-E^*[(X_T-X_t)])^2]\\
&=E^*[(Y_T-Y_t)^2]\\
&=E^*\left[\left(\int_t^T dY_s\right)^2\right]\\
&=E^*\left[\left(\int_t^T\sigma dW_s\right)^2\right].
\end{aligned}\tag{8}
$$

Applying Itô Isometry yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">应用伊藤等距公式得到：</span></details>

$$
E^*\left[\left(\int_t^T\sigma dW_s\right)^2\right]
=E^*\left[\int_t^T\sigma^2ds\right]=\sigma^2(T-t).\tag{9}
$$

Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此：</span></details>

$$
\operatorname{Var}(X_T-X_t)=\sigma^2(T-t).
$$

Therefore, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以：</span></details>

$$
X_T-X_t\sim N\left(\left(r-\frac12\sigma^2\right)(T-t),\sigma^2(T-t)\right),
$$

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
\ln V_T-\ln V_t\sim N\left(\left(r-\frac12\sigma^2\right)(T-t),\sigma^2(T-t)\right),\tag{10}
$$

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
\ln\left(\frac{V_T}{V_t}\right)
\sim N\left(\left(r-\frac12\sigma^2\right)(T-t),\sigma^2(T-t)\right),
$$

## PDF p.3

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
\ln\left(\frac{V_T}{V_t}\right)-\left(r-\frac12\sigma^2\right)(T-t)
\sim N(0,\sigma^2(T-t)),
$$

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
Z:=\frac{\ln\left(\frac{V_T}{V_t}\right)-(r-\frac12\sigma^2)(T-t)}
{\sigma\sqrt{T-t}}\sim N(0,1).
$$

Hence, using the standard normal variable $Z$, we re-express $V_T$ as <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，借助标准正态变量 Z，可将到期资产价值 V_T 重新表示为：</span></details>

$$
V_T=V_t\exp\left(\left(r-\frac12\sigma^2\right)(T-t)+\sigma\sqrt{T-t}Z\right).\tag{11}
$$

### 2 Black-Scholes-Merton Geometric Brownian Models <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2 Black-Scholes-Merton 几何布朗运动模型。</span></details>

Now let us consider <details class="translation-details"><summary>中文译文</summary><span class="translation-body">现在考虑：</span></details>

$$
\begin{aligned}
P^*(V_T\leq D)
&=P^*\left(\frac{V_T}{V_t}\leq\frac D{V_t}\right)\\
&=P^*\left\{\ln\left(\frac{V_T}{V_t}\right)\leq\ln\left(\frac D{V_t}\right)\right\}\\
&=P^*\left\{\ln\left(\frac{V_T}{V_t}\right)-\left(r-\frac12\sigma^2\right)(T-t)
\leq\ln\left(\frac D{V_t}\right)-\left(r-\frac12\sigma^2\right)(T-t)\right\}\\
&=P^*\left\{
\frac{\ln\left(\frac{V_T}{V_t}\right)-(r-\frac12\sigma^2)(T-t)}{\sigma\sqrt{T-t}}
\leq\frac{\ln\left(\frac D{V_t}\right)-(r-\frac12\sigma^2)(T-t)}{\sigma\sqrt{T-t}}
\right\}\\
&=P(Z\leq-d_2)\\
&=\Phi(-d_2),
\end{aligned}\tag{12}
$$

where $d_2=-\frac{\ln\left(\frac D{V_t}\right)-(r-\frac12\sigma^2)(T-t)}{\sigma\sqrt{T-t}}$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，d₂ 为上述标准化违约阈值的相反数，定义如式所示。</span></details>

At the beginning $t=0$, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在初始时刻 t = 0，有：</span></details>

$$
\begin{aligned}
P^*(V_T\leq D)
&=\Phi\left(
\frac{\ln\left(\frac D{V_0}\right)-(r-\frac12\sigma^2)(T-0)}{\sigma\sqrt{T-0}}
\right)\\
&=\Phi\left(\frac{\ln D-(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right).
\end{aligned}\tag{13}
$$

## PDF p.4

Hence, the tax credit can be presented by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，税收抵免可以表示为：</span></details>

$$
\begin{aligned}
A(0)&=E^*[e^{-rT}\kappa D\cdot I\{V(T)\geq D\}]\\
&=e^{-rT}\kappa D\cdot E^*[I\{V(T)\geq D\}]\\
&=e^{-rT}\kappa D\cdot P^*(V(T)\geq D)\\
&=e^{-rT}\kappa D\cdot P^*(V_T\geq D)\\
&=e^{-rT}\kappa D(1-P^*(V_T\leq D))\\
&=e^{-rT}\kappa D\left(1-\Phi\left(\frac{\ln D-(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right)\right).
\end{aligned}\tag{14}
$$

It follows from (10) that we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据（10），有：</span></details>

$$
\ln V_T\sim N\left(\left(r-\frac12\sigma^2\right)T,\sigma^2T\right),\tag{15}
$$

for $t=0$. Then, we have its density <details class="translation-details"><summary>中文译文</summary><span class="translation-body">此处 t = 0。于是，其密度为：</span></details>

$$
p^*(V_T)=\frac1{\sqrt{2\pi T}\sigma V_T}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right).\tag{16}
$$

The bankruptcy cost is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">破产成本为：</span></details>

$$
\begin{aligned}
C(0)&=E^*[e^{-rT}(1-\alpha)V(T)\cdot I\{V(T)\leq D\}]\\
&=e^{-rT}(1-\alpha)E^*[V(T)\cdot I\{V(T)\leq D\}]\\
&=e^{-rT}(1-\alpha)E^*[V_T\cdot I\{V_T\leq D\}]\\
&=e^{-rT}(1-\alpha)\int_0^D V_T\cdot p^*(V_T)dV_T\\
&=e^{-rT}(1-\alpha)\int_0^D V_T\cdot\frac1{\sqrt{2\pi T}\sigma V_T}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right)dV_T\\
&=e^{-rT}(1-\alpha)\int_0^D V_T\cdot\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right)d(\ln V_T)\\
&=e^{-rT}(1-\alpha)\int_0^D \exp(\ln V_T)\cdot\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right)d(\ln V_T)\\
&=e^{-rT}(1-\alpha)\int_0^D\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2-2\sigma^2T\ln V_T}{2\sigma^2T}\right)d(\ln V_T)\\
&=e^{-rT}(1-\alpha)\int_0^D\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r+\frac12\sigma^2)T)^2}{2\sigma^2T}\right)\exp(rT)d(\ln V_T)\\
&=(1-\alpha)\int_0^D\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r+\frac12\sigma^2)T)^2}{2\sigma^2T}\right)d(\ln V_T)\\
&=(1-\alpha)\Phi\left(\frac{\ln D-(r+\frac12\sigma^2)T}{\sigma\sqrt T}\right).
\end{aligned}\tag{17}
$$

## PDF p.5

### A Itô Lemma <details class="translation-details"><summary>中文译文</summary><span class="translation-body">附录 A：伊藤引理。</span></details>

In its simplest form, Itô lemma states the following: for an Itô drift-diffusion process <details class="translation-details"><summary>中文译文</summary><span class="translation-body">伊藤引理最简单的形式如下：对于伊藤漂移—扩散过程：</span></details>

$$
dX_t=\mu_tdt+\sigma_tdW_t,
$$

and any twice differentiable scalar function $f(t,x)$ of two real variables $t$ and $x$, one has <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对任意关于两个实变量 t 和 x 的二次可微标量函数 f(t, x)，有：</span></details>

$$
df(t,X_t)=\left(\frac{\partial f}{\partial t}+\mu_t\frac{\partial f}{\partial x}
+\frac{\sigma_t^2}{2}\frac{\partial^2f}{\partial x^2}\right)dt
+\sigma_t\frac{\partial f}{\partial x}dW_t.\tag{18}
$$

### B Itô Isometry <details class="translation-details"><summary>中文译文</summary><span class="translation-body">附录 B：伊藤等距公式。</span></details>

The Itô isometry says that $X_t-X_s$ has variance <details class="translation-details"><summary>中文译文</summary><span class="translation-body">伊藤等距公式指出，Xₜ − Xₛ 的方差满足：</span></details>

$$
E\left[\left(\int_s^t\xi_udW_u\right)^2\right]
=E\left[\int_s^t\xi_u^2du\right].\tag{19}
$$
