---
course: AMA572 Fixed-Income and Credit Risk
created: 2026-10-22
type: 作业逐题中英学习版
assignment: 2
question_count: 2
cssclasses:
  - ama-inline-translations
tags:
  - AMA572
  - Assignment
---

# Assignment 2｜英文原题、答案与中文解答

[[AMA572 Fixed-Income and Credit Risk/Assignment 2/00 - Assignment 2 资料索引|返回资料索引]]

**原题日期信息：** Due date: October 16, 2026；Midterm: October 22, 2026。

> [!info] 阅读方式与答案来源
> 每题依次为 **英文原题 → 教师英文答案（如有）→ GPT 英文详解 → 中文解答**。教师部分转录自标有“老师给的”的 Suggested Solutions；GPT 英文与中文部分分别完整整理自项目现有生成稿，中文常驻显示，方便直接学习。
>
> 不把 GPT 稿称为教师标准答案。正文只调整标题层级、分页符与数学排版；重复题干只放一次。原 PDF 与 Markdown 源稿全部保留在本目录附件，具体版本及页码见资料索引。

## 题目导航

- [[#第1题｜公司总价值与债务总价值|第1题：公司总价值与债务总价值]]
- [[#第2题｜平滑拼接与内生违约边界|第2题：平滑拼接与内生违约边界]]
- [[#原题附录｜首次穿越时间的 Laplace 变换|原题附录]]

---

## 第1题｜公司总价值与债务总价值

### 英文原题

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment02_2026.pdf#page=1|题目 PDF p.1]]。

Q1. Compute (4) and (5) in Proposition 1 of Lecture 4.

### 教师英文答案

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment02-sol_老师给的.pdf#page=1|教师 Suggested Solutions，PDF pp.1–3]]。重复题干已放在上方，以下为 Solution 部分；长公式仅调整换行。

Solution.

The market value of the firm at time 0 is

$$
\begin{aligned}
v(V;V_B)
&=V+E\left[\int_0^\tau\kappa\rho Pe^{-rt}dt\right]-(1-\alpha)E[V_\tau e^{-r\tau}]\\
&=V+\kappa\rho P\cdot E\left[\int_0^\tau e^{-rt}dt\right]-(1-\alpha)V_BE[e^{-r\tau}]\\
&=V+\kappa\rho P\cdot E\left[\frac1r(1-e^{-r\tau})\right]-(1-\alpha)V_BE[e^{-r\tau}]\\
&=V+\frac{\kappa\rho}{r}P-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]\cdot E[e^{-r\tau}].
\end{aligned}
$$

It follows from (A.1) that we have

$$
E[e^{-r\tau}]=\exp\left\{\log(V_B/V)\cdot\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\right\},
$$

where $\xi=\frac{r-\delta}{\sigma^2}-\frac12$.

Hence, we get

$$
\begin{aligned}
v(V;V_B)
&=V+\frac{\kappa\rho}{r}P-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]
\exp\left\{\log(V_B/V)\cdot\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\right\}\\
&=V+\frac{\kappa\rho}{r}P-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]
(V_B/V)^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi}.
\end{aligned}
$$

Next, let us consider the total debt value of the firm.

At time 0 the price of a bond with face value 1 and maturity $T$ when the firm asset $V_0=V$ is given by

$$
B(V;V_B,T)=E\left[e^{-rT}\mathbf1_{\{\tau>T\}}+e^{-r\tau}\cdot ce^{-r(T-\tau)}\mathbf1_{\{\tau\leq T\}}+\int_0^{\tau\wedge T}\rho e^{-rs}ds\right].
$$

Hence, the value of total debt at time 0 is

$$
\begin{aligned}
D(V;V_B)
&=P\int_0^\infty me^{-mT}B(V;V_B,T)dT\\
&=P\int_0^\infty me^{-mT}E\left[e^{-rT}\mathbf1_{\{\tau>T\}}+e^{-r\tau}\cdot ce^{-r(T-\tau)}\mathbf1_{\{\tau\leq T\}}+\int_0^{\tau\wedge T}\rho e^{-rs}ds\right]dT.
\end{aligned}
$$

The Laplace transform for the bond price, except the recovery part, is given by

$$
\begin{aligned}
&\int_0^\infty e^{-mT}E\left[e^{-rT}I\{\tau>T\}+\int_0^{\tau\wedge T}\rho e^{-rs}ds\right]dT\\
&=E\left\{\int_0^\infty e^{-mT}\left[e^{-rT}I\{\tau>T\}+\frac\rho r(1-e^{-r(\tau\wedge T)})\right]dT\right\}\\
&=E\left\{\int_0^\tau e^{-mT}e^{-rT}dT+\int_0^\tau e^{-mT}\frac\rho r(1-e^{-rT})dT
+\int_\tau^\infty e^{-mT}\frac\rho r(1-e^{-r\tau})dT\right\}\\
&=E\left\{\left(1-\frac\rho r\right)\int_0^\tau e^{-(m+r)T}dT+\int_0^\infty e^{-mT}\frac\rho r dT
-\frac\rho r e^{-r\tau}\int_\tau^\infty e^{-mT}dT\right\}\\
&=E\left\{\left(1-\frac\rho r\right)\frac{1-e^{-(m+r)\tau}}{m+r}+\frac\rho r\frac1m
-\frac\rho r\frac{e^{-(m+r)\tau}}m\right\}\\
&=\frac{\rho+m}{m(r+m)}(1-E[e^{-(r+m)\tau}]),
\end{aligned}
$$

which the first equality follows by changing the order the integration. Now, we only need to compute the Laplace transform of the recovery part

$$
\begin{aligned}
&\int_0^\infty e^{-mT}E\left[e^{-r\tau}\cdot ce^{-r(T-\tau)}I\{\tau\leq T\}\right]dT\\
&=c\int_0^\infty e^{-(m+r)T}E[I\{\tau\leq T\}]dT\\
&=cE\left\{\int_0^\infty e^{-(m+r)T}I\{\tau\leq T\}dT\right\}\\
&=cE\left\{\int_\tau^\infty e^{-(m+r)T}dT\right\}\\
&=\frac c{m+r}E[e^{-(m+r)\tau}].
\end{aligned}
$$

In summary, the Laplace transform of the bond price is given by

$$
\begin{aligned}
&\int_0^\infty e^{-mT}B(V;V_B,T)dT\\
&=\frac{\rho+m}{m(r+m)}(1-E[e^{-(r+m)\tau}])+\frac c{m+r}E[e^{-(m+r)\tau}]\\
&=\frac{\rho+m}{m(r+m)}+\left(\frac c{m+r}-\frac{\rho+m}{m(r+m)}\right)E[e^{-(m+r)\tau}]\\
&=\frac{\rho+m}{m(r+m)}
-\left(\frac\rho r\frac1m+\left(1-\frac\rho r-c\right)\frac1{r+m}\right)
\exp\left\{\log(V_B/V_0)\left(\sqrt{\xi^2+\frac2{\sigma^2}(m+r)}+\xi\right)\right\}.
\end{aligned}
$$

Since $c=\frac{m+r}{m}\frac{\alpha V_B}{P}$, the value of total debt at time 0 is

$$
\begin{aligned}
D(V;V_B)
&=P\int_0^{+\infty}me^{-mT}B(V;V_B,T)dT\\
&=P\frac{\rho+m}{r+m}
-P\left[\frac\rho r+\left(1-\frac\rho r-\frac{m+r}{m}\frac{\alpha V_B}{P}\right)\frac m{r+m}\right]\\
&\qquad\cdot\exp\left\{\log(V_B/V)\left(\sqrt{\xi^2+\frac2{\sigma^2}(m+r)}+\xi\right)\right\}\\
&=P\frac{\rho+m}{r+m}
-P\left[\frac\rho r+\left(1-\frac\rho r-\frac{m+r}{m}\frac{\alpha V_B}{P}\right)\frac m{r+m}\right]
(V_B/V)^{\sqrt{\xi^2+2(m+r)/\sigma^2}+\xi}.
\end{aligned}
$$

### GPT 英文详解

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_Complete_Solutions_EN.md|项目已有 GPT 英文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_Complete_Solutions_EN.pdf#page=1|英文 PDF]]。

#### Q1(a). First-passage transform and total firm value

Use the risk-adjusted measure of Lecture 4. Let $r,m,\sigma,P>0$, $0<V_B<V$, $0\leq\alpha\leq1$, $\rho\geq0$, and $0\leq\kappa<1$. Here $P$ is total debt face value, $\rho$ the coupon rate, $\kappa$ the tax rate, and $\delta$ the asset payout rate. The model is

$$
\frac{dV_t}{V_t}=(r-\delta)\,dt+\sigma\,dW_t,
\qquad
\tau=\inf\{t\geq0:V_t\leq V_B\},\quad V_0=V.
$$

Define, for $q>0$,

$$
\xi=\frac{r-\delta}{\sigma^2}-\frac12,
\qquad
\eta_q=\sqrt{\xi^2+\frac{2q}{\sigma^2}}+\xi,
\qquad
L_q=\mathbb E[e^{-q\tau}].
$$

We set $e^{-q\tau}=0$ on $\{\tau=\infty\}$; eventual default need not have probability one. Since the asset paths are continuous, $V_\tau=V_B$ whenever $\tau<\infty$.

**First-passage transform.** The logarithmic asset process and the lower barrier are

$$
\log\frac{V_t}{V}=\mu t+\sigma W_t,
\qquad \mu=r-\delta-\tfrac12\sigma^2=\sigma^2\xi,
\qquad \ell=\log\frac{V_B}{V}<0.
$$

Applying the $b<0$ case of Appendix (A.1), with $b=\ell$, gives

$$
\begin{aligned}
L_q
&=\exp\left\{\frac{\ell}{\sigma^2}
\left(\sqrt{\mu^2+2\sigma^2q}+\mu\right)\right\}\\
&=\exp\{\ell\eta_q\}
=\left(\frac{V_B}{V}\right)^{\eta_q}.
\end{aligned}
$$

**Total firm value.** Add the present value of tax benefits to $V$ and subtract bankruptcy costs. Using $\int_0^\tau e^{-rt}dt=(1-e^{-r\tau})/r$,

$$
\begin{aligned}
v(V;V_B)
&=V+\kappa\rho P\,\mathbb E\!\left[\int_0^\tau e^{-rt}dt\right]
 -(1-\alpha)V_B L_r\\
&=V+\frac{\kappa\rho P}{r}(1-L_r)-(1-\alpha)V_B L_r.
\end{aligned}
$$

Substituting the first-passage transform proves Lecture 4, equation (4):

$$
\boxed{
v(V;V_B)=V+\frac{\kappa\rho}{r}P
-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]
\left(\frac{V_B}{V}\right)^{\eta_r}.}
$$

Here $\eta_r=\sqrt{\xi^2+2r/\sigma^2}+\xi$. No numerical parameter values are specified in the assignment, so the required answer is symbolic.

#### Q1(b). Total debt value

A unit-face-value bond with maturity $T$ receives principal if it survives, recovery if default occurs before maturity, and coupons until $\tau\wedge T$. The discounted recovery is $e^{-r\tau}ce^{-r(T-\tau)}=ce^{-rT}$. Thus

$$
\begin{aligned}
B(V;V_B,T)
&=\mathbb E\!\left[e^{-rT}\mathbf1_{\{T<\tau\}}
 +ce^{-rT}\mathbf1_{\{\tau\leq T\}}
 +\rho\int_0^{\tau\wedge T}e^{-rt}dt\right],\\
D(V;V_B)&=P\int_0^\infty me^{-mT}B(V;V_B,T)\,dT,\qquad
c=\frac{r+m}{m}\frac{\alpha V_B}{P}.
\end{aligned}
$$

Integrate the three nonnegative cash-flow terms separately. Tonelli's theorem permits exchanging integrals and expectations. All three expressions below are **per unit of total face value**.

**Coupons.** For a fixed payment time $t$, only maturities $T\geq t$ contribute:

$$
\begin{aligned}
I_C
&=\rho\,\mathbb E\!\left[\int_0^\tau e^{-rt}
 \left(\int_t^\infty me^{-mT}dT\right)dt\right]\\
&=\rho\,\mathbb E\!\left[\int_0^\tau e^{-(r+m)t}dt\right]
=\frac{\rho}{r+m}(1-L_{r+m}).
\end{aligned}
$$

**Principal at maturity** and **recovery after default** give, respectively,

$$
\begin{aligned}
I_M&=\mathbb E\!\left[\int_0^\tau me^{-(r+m)T}dT\right]
=\frac{m}{r+m}(1-L_{r+m}),\\[3pt]
I_R&=c\,\mathbb E\!\left[\int_\tau^\infty me^{-(r+m)T}dT\right]
=\frac{cm}{r+m}L_{r+m}.
\end{aligned}
$$

Using $D=P(I_C+I_M+I_R)$ and $Pcm/(r+m)=\alpha V_B$ yields

$$
\boxed{D(V;V_B)=P\frac{\rho+m}{r+m}
-\left[P\frac{\rho+m}{r+m}-\alpha V_B\right]
\left(\frac{V_B}{V}\right)^{\eta_{r+m}}.}
$$

To recover exactly the coefficient in Lecture 4, equation (5), observe that

$$
\frac{\rho+m}{r+m}-\frac{\alpha V_B}{P}
=\frac{\rho}{r}
+\left(1-\frac{\rho}{r}-\frac{r+m}{m}\frac{\alpha V_B}{P}\right)
\frac{m}{r+m}.
$$

Consequently,

$$
\boxed{\begin{aligned}
D(V;V_B)&=P\frac{\rho+m}{r+m}\\
&\quad-P\left[\frac{\rho}{r}
+\left(1-\frac{\rho}{r}-\frac{r+m}{m}\frac{\alpha V_B}{P}\right)
\frac{m}{r+m}\right]
\left(\frac{V_B}{V}\right)^{\eta_{r+m}}.
\end{aligned}}
$$

This proves (5), since $\eta_{r+m}=\sqrt{\xi^2+2(r+m)/\sigma^2}+\xi$. As a boundary check, $v(V_B;V_B)=D(V_B;V_B)=\alpha V_B$, hence equity is zero at default.

### 中文解答

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_完整解答_CN.md|项目已有 GPT 中文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_完整解答_CN.pdf#page=1|中文 PDF]]。

#### Q1(a) 首次穿越变换与公司总价值

采用 Lecture 4 的风险调整概率测度。设 $r,m,\sigma,P>0$、$0<V_B<V$、$0\leq\alpha\leq1$、$\rho\geq0$、$0\leq\kappa<1$。其中 $P$ 是债务总面值，$\rho$ 是票息率，$\kappa$ 是税率，$\delta$ 是资产总支付率。模型为

$$
\frac{dV_t}{V_t}=(r-\delta)\,dt+\sigma\,dW_t,
\qquad
\tau=\inf\{t\geq0:V_t\leq V_B\},\quad V_0=V.
$$

对任意 $q>0$，定义

$$
\xi=\frac{r-\delta}{\sigma^2}-\frac12,
\qquad
\eta_q=\sqrt{\xi^2+\frac{2q}{\sigma^2}}+\xi,
\qquad
L_q=\mathbb E[e^{-q\tau}].
$$

在 $\{\tau=\infty\}$ 上约定 $e^{-q\tau}=0$，因此不需要假定公司最终必然违约。资产路径连续，所以在 $\tau<\infty$ 时有 $V_\tau=V_B$。

**首次穿越时间的 Laplace 变换。** 对数资产过程和下方边界分别为

$$
\log\frac{V_t}{V}=\mu t+\sigma W_t,
\qquad \mu=r-\delta-\tfrac12\sigma^2=\sigma^2\xi,
\qquad \ell=\log\frac{V_B}{V}<0.
$$

在作业附录 (A.1) 中代入 $b=\ell$，使用 $b<0$ 的情形，得到

$$
\begin{aligned}
L_q
&=\exp\left\{\frac{\ell}{\sigma^2}
\left(\sqrt{\mu^2+2\sigma^2q}+\mu\right)\right\}\\
&=\exp\{\ell\eta_q\}
=\left(\frac{V_B}{V}\right)^{\eta_q}.
\end{aligned}
$$

**公司总价值。** 在当前资产价值 $V$ 上，加上税盾现值、减去破产成本现值。利用 $\int_0^\tau e^{-rt}dt=(1-e^{-r\tau})/r$，有

$$
\begin{aligned}
v(V;V_B)
&=V+\kappa\rho P\,\mathbb E\!\left[\int_0^\tau e^{-rt}dt\right]
 -(1-\alpha)V_B L_r\\
&=V+\frac{\kappa\rho P}{r}(1-L_r)-(1-\alpha)V_B L_r.
\end{aligned}
$$

将首次穿越变换代入，即得到 Lecture 4 的式 (4)：

$$
\boxed{
v(V;V_B)=V+\frac{\kappa\rho}{r}P
-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]
\left(\frac{V_B}{V}\right)^{\eta_r}.}
$$

这里 $\eta_r=\sqrt{\xi^2+2r/\sigma^2}+\xi$。本次作业未给定一组数值参数，要求的是上述符号推导。

#### Q1(b) 债务总价值

面值为1、到期时间为 $T$ 的债券，在存续至到期时支付本金，在提前违约时支付回收款，并在 $\tau\wedge T$ 之前持续支付票息。回收款折现到时刻0为 $e^{-r\tau}ce^{-r(T-\tau)}=ce^{-rT}$。因此

$$
\begin{aligned}
B(V;V_B,T)
&=\mathbb E\!\left[e^{-rT}\mathbf1_{\{T<\tau\}}
 +ce^{-rT}\mathbf1_{\{\tau\leq T\}}
 +\rho\int_0^{\tau\wedge T}e^{-rt}dt\right],\\
D(V;V_B)&=P\int_0^\infty me^{-mT}B(V;V_B,T)\,dT,\qquad
c=\frac{r+m}{m}\frac{\alpha V_B}{P}.
\end{aligned}
$$

分别对三类非负现金流积分，利用 Tonelli 定理交换积分与期望。以下三个结果均以**每单位债务总面值**计量，最后再乘以 $P$。

**票息项。** 固定支付时刻 $t$ 后，仅到期时间满足 $T\geq t$ 的债券还会支付票息：

$$
\begin{aligned}
I_C
&=\rho\,\mathbb E\!\left[\int_0^\tau e^{-rt}
 \left(\int_t^\infty me^{-mT}dT\right)dt\right]\\
&=\rho\,\mathbb E\!\left[\int_0^\tau e^{-(r+m)t}dt\right]
=\frac{\rho}{r+m}(1-L_{r+m}).
\end{aligned}
$$

**到期本金项**与**违约回收项**分别为

$$
\begin{aligned}
I_M&=\mathbb E\!\left[\int_0^\tau me^{-(r+m)T}dT\right]
=\frac{m}{r+m}(1-L_{r+m}),\\[3pt]
I_R&=c\,\mathbb E\!\left[\int_\tau^\infty me^{-(r+m)T}dT\right]
=\frac{cm}{r+m}L_{r+m}.
\end{aligned}
$$

利用 $D=P(I_C+I_M+I_R)$ 与 $Pcm/(r+m)=\alpha V_B$，得到

$$
\boxed{D(V;V_B)=P\frac{\rho+m}{r+m}
-\left[P\frac{\rho+m}{r+m}-\alpha V_B\right]
\left(\frac{V_B}{V}\right)^{\eta_{r+m}}.}
$$

为了还原 Lecture 4 式 (5) 的系数写法，注意以下恒等式：

$$
\frac{\rho+m}{r+m}-\frac{\alpha V_B}{P}
=\frac{\rho}{r}
+\left(1-\frac{\rho}{r}-\frac{r+m}{m}\frac{\alpha V_B}{P}\right)
\frac{m}{r+m}.
$$

因此

$$
\boxed{\begin{aligned}
D(V;V_B)&=P\frac{\rho+m}{r+m}\\
&\quad-P\left[\frac{\rho}{r}
+\left(1-\frac{\rho}{r}-\frac{r+m}{m}\frac{\alpha V_B}{P}\right)
\frac{m}{r+m}\right]
\left(\frac{V_B}{V}\right)^{\eta_{r+m}}.
\end{aligned}}
$$

由于 $\eta_{r+m}=\sqrt{\xi^2+2(r+m)/\sigma^2}+\xi$，式 (5) 得证。边界检查也成立：$v(V_B;V_B)=D(V_B;V_B)=\alpha V_B$，故违约时股权价值为0。

---

## 第2题｜平滑拼接与内生违约边界

### 英文原题

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment02_2026.pdf#page=1|题目 PDF p.1]]。

Q2. The total equity value of the firm is given by

$$
\begin{aligned}
S(V;V_B)&=v(V;V_B)-D(V;V_B)\\
&=V+\frac{\kappa\rho}{r}P
-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]
(V_B/V)^{\sqrt{\xi^2+\frac{2}{\sigma^2}r}+\xi}\\
&\quad-P\frac{\rho+m}{r+m}
+P\left[\frac{\rho}{r}+\left(1-\frac{\rho}{r}-\frac{m+r}{m}\frac{\alpha V_B}{P}\right)\frac{m}{r+m}\right]
(V_B/V)^{\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi}.
\end{aligned}
$$

Show that the solution of

$$
\left.\frac{\partial S(V;V_B^*)}{\partial V}\right|_{V=V_B^*}=0
$$

is given by $V_B^*=\epsilon P$, where

$$
\epsilon=
\frac{
\frac{\rho+m}{r+m}\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)
-\frac{\kappa\rho}{r}\left(\sqrt{\xi^2+\frac{2}{\sigma^2}r}+\xi\right)
}{
1+(1-\alpha)\left(\sqrt{\xi^2+\frac{2}{\sigma^2}r}+\xi\right)
+\alpha\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)
}.
$$

### 教师英文答案

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment02-sol_老师给的.pdf#page=4|教师 Suggested Solutions，PDF pp.4–5]]。重复题干已放在上方，以下为 Solution 部分。

Solution.

It follows from $S(V;V_B)$ that

$$
\begin{aligned}
\frac{\partial S(V;V_B)}{\partial V}
&=1-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]
\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)
\left(\frac{V_B}{V}\right)^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi-1}
\left(-\frac{V_B}{V^2}\right)\\
&\quad+P\left[\frac\rho r+\left(1-\frac\rho r-\frac{m+r}{m}\frac{\alpha V_B}{P}\right)\frac m{r+m}\right]
\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)\\
&\qquad\cdot\left(\frac{V_B}{V}\right)^{\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi-1}
\left(-\frac{V_B}{V^2}\right).
\end{aligned}
$$

Hence,

$$
\begin{aligned}
\left.\frac{\partial S(V;V_B)}{\partial V}\right|_{V=V_B}
&=1-\left[\frac{\kappa\rho}{r}P+(1-\alpha)V_B\right]
\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\left(-\frac1{V_B}\right)\\
&\quad+P\left[\frac\rho r+\left(1-\frac\rho r-\frac{m+r}{m}\frac{\alpha V_B}{P}\right)\frac m{r+m}\right]\\
&\qquad\cdot\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)\left(-\frac1{V_B}\right).
\end{aligned}
$$

Letting

$$
\left.\frac{\partial S(V;V_B)}{\partial V}\right|_{V=V_B}=0,
$$

we obtain

$$
\begin{aligned}
&1+\frac{\kappa\rho}{r}P\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\frac1{V_B}
+(1-\alpha)\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\\
&\quad-P\left[\frac\rho r+\left(1-\frac\rho r\right)\frac m{r+m}\right]
\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)\frac1{V_B}\\
&\quad+\alpha\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)=0,
\end{aligned}
$$

which yields

$$
V_B^*=
\frac{
\left[\frac\rho r+\left(1-\frac\rho r\right)\frac m{r+m}\right]
\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)
-\frac{\kappa\rho}{r}\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)
}{
1+(1-\alpha)\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)
+\alpha\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)
}P.
$$

So $V_B^*=\epsilon P$.

### GPT 英文详解

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_Complete_Solutions_EN.md|项目已有 GPT 英文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_Complete_Solutions_EN.pdf#page=3|英文 PDF]]。

Introduce the abbreviations

$$
a=\eta_r,\qquad b=\eta_{r+m},\qquad
K=\frac{\kappa\rho}{r},\qquad H=\frac{\rho+m}{r+m}.
$$

The coefficient identity in Q1(b) reduces the given equity value to

$$
\begin{aligned}
S(V;V_B)
&=V+KP-[KP+(1-\alpha)V_B]\left(\frac{V_B}{V}\right)^a\\
&\quad-PH+[PH-\alpha V_B]\left(\frac{V_B}{V}\right)^b.
\end{aligned}
$$

**Differentiate while holding $V_B$ and $P$ fixed.** For a constant exponent $q$,

$$
\frac{\partial}{\partial V}\left(\frac{V_B}{V}\right)^q
=-\frac{q}{V}\left(\frac{V_B}{V}\right)^q.
$$

It follows that, in the continuation region $V>V_B$,

$$
\begin{aligned}
S_V(V;V_B)
&=1+\frac{a[KP+(1-\alpha)V_B]}{V}\left(\frac{V_B}{V}\right)^a\\
&\quad-\frac{b[PH-\alpha V_B]}{V}\left(\frac{V_B}{V}\right)^b.
\end{aligned}
$$

Now take the limit $V\downarrow V_B$, so both power terms equal one:

$$
\begin{aligned}
S_V(V_B+;V_B)
&=1+\frac{a[KP+(1-\alpha)V_B]}{V_B}
-\frac{b[PH-\alpha V_B]}{V_B}\\
&=1+(1-\alpha)a+\alpha b+\frac{P}{V_B}(Ka-Hb).
\end{aligned}
$$

Setting this expression to zero and multiplying by $V_B$ gives

$$
\left[1+(1-\alpha)a+\alpha b\right]V_B
=P(Hb-Ka).
$$

Since $a,b>0$ and $0\leq\alpha\leq1$, the denominator is positive. The resulting solution is

$$
\boxed{V_B^*=\epsilon P,\qquad
\epsilon=\frac{Hb-Ka}{1+(1-\alpha)a+\alpha b}.}
$$

Substituting the definitions of $a,b,K,H$ gives precisely the expression requested:

$$
\epsilon=
\frac{
\dfrac{\rho+m}{r+m}\left(\sqrt{\xi^2+\dfrac{2(r+m)}{\sigma^2}}+\xi\right)
-\dfrac{\kappa\rho}{r}\left(\sqrt{\xi^2+\dfrac{2r}{\sigma^2}}+\xi\right)
}{
1+(1-\alpha)\left(\sqrt{\xi^2+\dfrac{2r}{\sigma^2}}+\xi\right)
+\alpha\left(\sqrt{\xi^2+\dfrac{2(r+m)}{\sigma^2}}+\xi\right)
}.
$$

The order of operations matters: first take the partial derivative in $V$, then evaluate at the barrier. Substituting $V=V_B$ first gives the identity $S(V_B;V_B)=0$ and does not establish smooth pasting. The result above proves the equation asked in Q2; the constrained global-optimality claim is the separate Theorem 1(c) of Lecture 4.

**References:** Assignment 2, pp. 1-2 and Appendix (A.1); Lecture 4, Proposition 1, pp. 3-5, and Theorem 1(a), pp. 6-8. The lecture's economic restrictions $0\leq c\leq1$ and $\kappa\rho<r$ are understood.

### 中文解答

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_完整解答_CN.md|项目已有 GPT 中文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment2_完整解答_CN.pdf#page=3|中文 PDF]]。

为简化书写，定义

$$
a=\eta_r,\qquad b=\eta_{r+m},\qquad
K=\frac{\kappa\rho}{r},\qquad H=\frac{\rho+m}{r+m}.
$$

利用 Q1(b) 中的系数恒等式，将题目给出的股权价值写为

$$
\begin{aligned}
S(V;V_B)
&=V+KP-[KP+(1-\alpha)V_B]\left(\frac{V_B}{V}\right)^a\\
&\quad-PH+[PH-\alpha V_B]\left(\frac{V_B}{V}\right)^b.
\end{aligned}
$$

**固定 $V_B$ 和 $P$，先对 $V$ 求偏导。** 对固定指数 $q$，有

$$
\frac{\partial}{\partial V}\left(\frac{V_B}{V}\right)^q
=-\frac{q}{V}\left(\frac{V_B}{V}\right)^q.
$$

因此，在公司尚未违约的区域 $V>V_B$ 中，

$$
\begin{aligned}
S_V(V;V_B)
&=1+\frac{a[KP+(1-\alpha)V_B]}{V}\left(\frac{V_B}{V}\right)^a\\
&\quad-\frac{b[PH-\alpha V_B]}{V}\left(\frac{V_B}{V}\right)^b.
\end{aligned}
$$

接着从上方令 $V\downarrow V_B$。此时两个幂次项均等于1，得到

$$
\begin{aligned}
S_V(V_B+;V_B)
&=1+\frac{a[KP+(1-\alpha)V_B]}{V_B}
-\frac{b[PH-\alpha V_B]}{V_B}\\
&=1+(1-\alpha)a+\alpha b+\frac{P}{V_B}(Ka-Hb).
\end{aligned}
$$

令上式为0，并在两边乘以 $V_B$，有

$$
\left[1+(1-\alpha)a+\alpha b\right]V_B
=P(Hb-Ka).
$$

因为 $a,b>0$ 且 $0\leq\alpha\leq1$，分母为正。于是解得

$$
\boxed{V_B^*=\epsilon P,\qquad
\epsilon=\frac{Hb-Ka}{1+(1-\alpha)a+\alpha b}.}
$$

将 $a,b,K,H$ 的定义代回，即得到题目要求的表达式：

$$
\epsilon=
\frac{
\dfrac{\rho+m}{r+m}\left(\sqrt{\xi^2+\dfrac{2(r+m)}{\sigma^2}}+\xi\right)
-\dfrac{\kappa\rho}{r}\left(\sqrt{\xi^2+\dfrac{2r}{\sigma^2}}+\xi\right)
}{
1+(1-\alpha)\left(\sqrt{\xi^2+\dfrac{2r}{\sigma^2}}+\xi\right)
+\alpha\left(\sqrt{\xi^2+\dfrac{2(r+m)}{\sigma^2}}+\xi\right)
}.
$$

求导顺序很关键：先对 $V$ 求偏导，再在边界处取值。若先代入 $V=V_B$，只会得到恒等式 $S(V_B;V_B)=0$，无法由此证明光滑粘贴条件。以上完成 Q2 所要求的方程求解；有限责任约束下的全局最优性属于课件另外的 Theorem 1(c)。

**参考资料：** Assignment 2 第1–2页及附录 (A.1)；Lecture 4 第3–5页 Proposition 1、第6–8页 Theorem 1(a)。沿用课件的经济限制 $0\leq c\leq1$ 与 $\kappa\rho<r$。

---

## 原题附录｜首次穿越时间的 Laplace 变换

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 2/附件/Assignment02_2026.pdf#page=1|题目 PDF pp.1–2]]；教师答案 PDF p.6 重复了同一附录，此处只转录一次。

### A　Laplace Transforms of First Passage Times

Consider the first passage time

$$
\tau_b=\min\{t\geq0:W_{\mu,\sigma}(t)=b\},
$$

where $W_{\mu,\sigma}(t)$ is a Brownian motion with drift $\mu$ and volatility $\sigma$, i.e. $W_{\mu,\sigma}(t)=\mu t+\sigma W(t)$. Note that $W_{\mu,\sigma}(\tau_b)=b$ on the set $\tau_b<\infty$.

For any $s>0$, the Laplace transform of $\tau_b$ is given by

$$
E[e^{-s\tau_b}]=
\begin{cases}
\exp\left\{-\dfrac{b}{\sigma^2}\left(\sqrt{\mu^2+2\sigma^2s}-\mu\right)\right\},&\text{if }b>0,\\[6pt]
\exp\left\{\dfrac{b}{\sigma^2}\left(\sqrt{\mu^2+2\sigma^2s}+\mu\right)\right\},&\text{if }b<0.
\end{cases}\tag{A.1}
$$

> [!note] 中文阅读提示
> 本作业是资产向下触及违约边界，代入的是 $b=\log(V_B/V)<0$ 的第二种情形。公式中的 $s$ 是变换参数；计算公司价值时取 $s=r$，汇总指数期限分布下的债务价值时取 $s=r+m$。完整对应过程见第1题中文解答。

## 课程回链

- [[AMA572 Fixed-Income and Credit Risk/Lecture 3/00 - Lecture 3 资料索引|Lecture 3]]
- [[AMA572 Fixed-Income and Credit Risk/Lecture 4/00 - Lecture 4 资料索引|Lecture 4]]
