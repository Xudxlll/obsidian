# AMA572 · Assignment 2

**Complete Solutions** · Due: October 16, 2026

## Q1(a). First-passage transform and total firm value

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

\newpage

## Q1(b). Total debt value

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

\newpage

## Q2. Smooth-pasting condition and the default barrier

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
