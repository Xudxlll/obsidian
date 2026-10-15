---
course: AMA572 Fixed-Income and Credit Risk
source: 03_Lecture2_补充推导_税盾与破产成本_Ito引理及手写批注版.pdf
pages: 5
created: "2026-10-15"
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 本文转录 Itô 引理及手写批注版的全部 5 页。印刷原文、公式编号及疑似笔误均保留；各页原貌图片同时保留老师的手写改动。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 2/00 - Lecture 2 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/03_Lecture2_补充推导_税盾与破产成本_Ito引理及手写批注版.pdf|原 PDF]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 2/02 - 补充推导（Ito 等距版，英文原文与折叠译文）|Itô 等距版]]

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

> [!example]- PDF 第 1 页原貌（保留全部手写批注）
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/03-手写批注版-PDF第1页.png]]

## PDF p.2

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
V_T=V_t\exp\left(\left(r-\frac12\sigma^2\right)(T-t)+\sigma(W_T-W_t)\right).\tag{3}
$$

Let $X_t=\ln V_t$. Then, it follows from (12) that we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 Xₜ = ln Vₜ，根据（12）得到：</span></details>

$$
dX_t=\left(r-\frac12\sigma^2\right)dt+\sigma dW_t.\tag{4}
$$

Taking the expectation for (4) leads to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对（4）取期望得到：</span></details>

$$
d(E^*[X_t])=\left(r-\frac12\sigma^2\right)dt,\tag{5}
$$

since $E^*[dW_t]=0$. Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为 E*[dWₜ] = 0。因此：</span></details>

$$
E^*[X_T]-E^*[X_t]=\int_t^T\left(r-\frac12\sigma^2\right)ds
=\left(r-\frac12\sigma^2\right)(T-t).\tag{6}
$$

Let $Y_t=X_t-E[X_t]$. Then <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 Yₜ = Xₜ − E[Xₜ]，则：</span></details>

$$
\begin{aligned}
dY_t&=X_t-E^*[X_t]\\
&=\left(r-\frac12\sigma^2\right)dt+\sigma dW_t-\left(r-\frac12\sigma^2\right)dt\\
&=\sigma dW_t.
\end{aligned}\tag{7}
$$

Let $g(t,Y_t)=Y_t^2$. Then, we get <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令 g(t, Yₜ) = Yₜ²，得到：</span></details>

$$
\frac{\partial g}{\partial t}=0,\quad
\frac{\partial g}{\partial V_t}=2Y_t,\quad
\frac{\partial^2g}{\partial V_t^2}=2.
$$

Applying Itô Lemma yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">应用伊藤引理得到：</span></details>

$$
\begin{aligned}
d(Y_t^2)&=d(g(t,V_t))\\
&=\left(\frac{\partial g}{\partial t}+\frac{\partial g}{\partial Y_t}\times0
+\frac12\frac{\partial^2g}{\partial Y_t^2}\sigma^2\right)dt
+\frac{\partial f}{\partial Y_t}\sigma dW_t\\
&=\left\{0+2Y_t\times0+\frac12\times2\times\sigma^2\right\}dt
+2Y_t\sigma dW_t\\
&=\sigma^2dt+2\sigma Y_tdW_t.
\end{aligned}\tag{8}
$$

Taking the expectation for (8) leads to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">对（8）取期望得到：</span></details>

$$
d(E^*[Y_t^2])=\sigma^2dt,\tag{9}
$$

since $E^*[dW_t]=0$. Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因为 E*[dWₜ] = 0。因此：</span></details>

$$
E^*[Y_T^2]-E^*[Y_t^2]=\int_t^T\sigma^2ds=\sigma^2(T-t).\tag{10}
$$

> [!example]- PDF 第 2 页原貌（保留全部手写批注）
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/03-手写批注版-PDF第2页.png]]

## PDF p.3

Further, we get <details class="translation-details"><summary>中文译文</summary><span class="translation-body">进一步得到：</span></details>

$$
\begin{aligned}
\operatorname{Var}(X_T)-\operatorname{Var}(X_t)
&=E^*[(X_T-E^*[X_T])^2]-E^*[(X_t-E^*[X_t])^2]\\
&=E^*[Y_T^2]-E[Y_t^2]\\
&=\sigma^2(T-t).
\end{aligned}\tag{11}
$$

Therefore, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">所以：</span></details>

$$
X_T-X_t\sim N\left(\left(r-\frac12\sigma^2\right)(T-t),\sigma^2(T-t)\right),
$$

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
\ln V_T-\ln V_t\sim N\left(\left(r-\frac12\sigma^2\right)(T-t),\sigma^2(T-t)\right),\tag{12}
$$

i.e., <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即：</span></details>

$$
\ln\left(\frac{V_T}{V_t}\right)
\sim N\left(\left(r-\frac12\sigma^2\right)(T-t),\sigma^2(T-t)\right),
$$

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
V_T=V_t\exp\left(\left(r-\frac12\sigma^2\right)(T-t)+\sigma\sqrt{T-t}Z\right).\tag{13}
$$

> [!example]- PDF 第 3 页原貌（保留全部手写批注）
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/03-手写批注版-PDF第3页.png]]

## PDF p.4

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
\end{aligned}\tag{14}
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
\end{aligned}\tag{15}
$$


Hence, the tax credit can be presented by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，税收抵免可以表示为：</span></details>

$$
\begin{aligned}
A(0)&=E^*[e^{-rT}\kappa D\cdot I\{V(T)\geq D\}]\\
&=e^{-rT}\kappa D\cdot E^*[I\{V(T)\geq D\}]\\
&=e^{-rT}\kappa D\cdot P^*(V(T)\geq D)\\
&=e^{-rT}\kappa D\cdot P^*(V_T\geq D)\\
&=e^{-rT}\kappa D(1-P^*(V_T\leq D))\\
&=e^{-rT}\kappa D\left(1-\Phi\left(\frac{\ln V_T-(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right)\right).
\end{aligned}\tag{16}
$$

It follows from (12) that we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据（12），有：</span></details>

$$
\ln V_T\sim N\left(\left(r-\frac12\sigma^2\right)T,\sigma^2T\right),\tag{17}
$$

> [!example]- PDF 第 4 页原貌（保留全部手写批注）
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/03-手写批注版-PDF第4页.png]]

## PDF p.5

for $t=0$. Then, we have its density <details class="translation-details"><summary>中文译文</summary><span class="translation-body">此处 t = 0。于是，其密度为：</span></details>

$$
p^*(V_T)=\frac1{\sqrt{2\pi T}\sigma V_T}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right).\tag{18}
$$

The bankruptcy cost is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">破产成本为：</span></details>

$$
\begin{aligned}
C(0)&=E^*[e^{-rT}(1-\alpha)V(T)\cdot I\{V(T)\leq D\}]\\
&=e^{-rT}(1-\alpha)E^*[V(T)\cdot I\{V(T)\leq D\}]\\
&=e^{-rT}(1-\alpha)E^*[V_T\cdot I\{V_T\leq D\}]\\
&=e^{-rT}(1-\alpha)\int_{-\infty}^D V_T\cdot p^*(V_T)dV_T\\
&=e^{-rT}(1-\alpha)\int_{-\infty}^D V_T\cdot\frac1{\sqrt{2\pi T}\sigma V_T}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right)dV_T\\
&=e^{-rT}(1-\alpha)\int_{-\infty}^D V_T\cdot\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right)d(\ln V_T)\\
&=e^{-rT}(1-\alpha)\int_{-\infty}^D \exp(\ln V_T)\cdot\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2}{2\sigma^2T}\right)d(\ln V_T)\\
&=e^{-rT}(1-\alpha)\int_{-\infty}^D\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r-\frac12\sigma^2)T)^2-2\sigma^2T\ln V_T}{2\sigma^2T}\right)d(\ln V_T)\\
&=e^{-rT}(1-\alpha)\int_{-\infty}^D\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r+\frac12\sigma^2)T)^2}{2\sigma^2T}\right)\exp(rT)d(\ln V_T)\\
&=(1-\alpha)\int_{-\infty}^D\frac1{\sqrt{2\pi T}\sigma}
\exp\left(-\frac{(\ln V_T-(r+\frac12\sigma^2)T)^2}{2\sigma^2T}\right)d(\ln V_T)\\
&=(1-\alpha)\Phi\left(\frac{\ln D-(r+\frac12\sigma^2)T}{\sigma\sqrt T}\right).
\end{aligned}\tag{19}
$$

> [!example]- PDF 第 5 页原貌（保留全部手写批注）
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 2/附件/03-手写批注版-PDF第5页.png]]
