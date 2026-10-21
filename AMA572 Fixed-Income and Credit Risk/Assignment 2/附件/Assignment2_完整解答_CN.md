# AMA572 · Assignment 2

**完整解答（中文版）** · 截止日期：2026年10月16日

## Q1(a) 首次穿越变换与公司总价值

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

\newpage

## Q1(b) 债务总价值

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

\newpage

## Q2 光滑粘贴条件与违约边界

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
