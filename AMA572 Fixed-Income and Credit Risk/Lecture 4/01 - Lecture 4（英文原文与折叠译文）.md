---
course: AMA572 Fixed-Income and Credit Risk
created: "2026-10-20"
source: "01_Lecture4_原课件_Leland-Toft内生违约模型.pdf"
pages: 9
cssclasses:
  - ama-inline-translations
---

> [!info] 阅读方式
> 英文按 PDF 实际页序完整转录；仅合并排版换行与断词。公式、数值、题号及原文疑似笔误保留，译文不替原文纠错。点击段末「中文译文」展开对应中文；各段之间保留留白。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 4/00 - Lecture 4 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/01_Lecture4_原课件_Leland-Toft内生违约模型.pdf|原始 PDF]]

## PDF p.1

# AMA572 Lecture 4. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">AMA572 第 4 讲。</span></details>

**Leland-Toft Endogenous Default Model** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Leland–Toft 内生违约模型（endogenous default model）。</span></details>

### 1 Basic Setting of the Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1 模型的基本设定。</span></details>

#### 1.1 Asset Model <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.1 资产模型。</span></details>

Leland and Toft (1996) assume that under a risk-adjusted probability $P$, the asset value of the firm $V_t$ follows <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Leland 和 Toft（1996）假设，在风险调整概率 P 下，企业资产价值 Vt 服从：</span></details>

$$
\frac{dV_t}{V_t}=(r-\delta)dt+\sigma dW_t,
$$

whose solution is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其解为：</span></details>

$$
V_t=V_0\exp\{(r-\delta-\tfrac12\sigma^2)t+\sigma W_t\},
$$

with $r$ being the constant risk-free interest rate, $\delta$ the total payout rate to the firm’s investors (including both bond and equity holders). Note that under the above risk-adjusted probability $V_t$ is a martingale after proper discounting: $V_t=E[e^{-(r-\delta)(T-t)}V_T|\mathcal F_t]$, where $\mathcal F_t$ is the information up to time $t$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 r 为常数无风险利率，δ 为向企业投资者（包括债券持有人和股东）的总支付率。注意，在上述风险调整概率下，Vt 经适当贴现后为鞅（martingale）：Vt＝E[e^(−(r−δ)(T−t))VT｜Ft]，其中 Ft 表示截至 t 时刻的信息。</span></details>


> [!example] 课堂截图：公司资产GBM与对数过程
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/01_第1页_公司资产GBM与对数过程_截图10-08_1926.png]]


#### 1.2 Debt Issuing and Coupon Payments <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.2 债务发行与票息支付。</span></details>

The setting of debt issuing and coupon payment follows Leland (1994) and Leland and Toft (1996). In the time interval $(t,t+dt)$, the firm issues new debt with par value $pdt$, and maturity profile $\varphi$, where $\varphi(v)=me^{-mv}$, i.e. the maturity of a specific bond is chosen randomly according to an exponentially distributed random variable with mean $1/m$. At any time $t$, the par value of debt maturing in the next moment $(s,s+ds)$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">债务发行和票息支付的设定沿用 Leland（1994）及 Leland 和 Toft（1996）。在区间 (t，t＋dt) 内，企业发行面值 pdt 的新债，到期期限分布（maturity profile）为 φ(v)＝me^(−mv)，即单只债券的期限按均值为 1／m 的指数分布随机选取。在任意时刻 t，于未来区间 (s，s＋ds) 到期的债务面值为：</span></details>

$$
\left(\int_{-\infty}^t p\varphi(s-u)du\right)ds=\left(\int_{-\infty}^t pme^{-m(s-u)}du\right)ds=pe^{-m(s-t)}ds.\tag{1}
$$

The above equation (1) has two implications. First, letting $s=t$ in (1) we have at time $t$ the par value of the debt maturing at the next moment $(t,t+dt)$ is given by $pdt$, which is the same as the par value of the newly-issued debt, achieving a static balance. Secondly, using (1), at time $t$ the par value of all pending debt (with maturity from $t$ to $\infty$) is a constant, equal to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">式（1）有两层含义。第一，令 s＝t，则在 t 时刻紧接着到期的债务面值为 pdt，恰好等于新发行债务的面值，形成静态平衡。第二，由式（1），t 时刻全部未到期债务（到期日从 t 至∞）的面值总额是常数，等于：</span></details>

$$
P=\int_t^{+\infty}pe^{-m(s-t)}ds=p/m.
$$

## PDF p.2

We also assume that before maturity bondholders will receive coupons at rate $\rho$ until default. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">还假设到期前债券持有人按票息率 ρ 收取票息，直到违约发生。</span></details>

At each moment the firm faces two cash outflows and two cash inflows. The two cash outflows are after-tax coupon payment $(1-\kappa)\rho Pdt$ and due principal $pdt$, where $\kappa$ is the tax rate; the two cash inflows are $b_tdt$ from selling new debts, where $b_t$ is the price of the total newly issued bonds, and the total payout from the asset $\delta V_tdt$. If the total cash inflow $(\delta V_t+b_t)dt$ is greater than the cash outflow $((1-\kappa)\rho P+p)dt$, we assume that the difference of the two goes to the equity holders as dividends; otherwise, additional equity will be issued to fulfill the due liability. Note that the difference $[((1-\kappa)\rho P+p)-(\delta V_t+b_t)]dt$ is an infinitesimal quantity. Thus, such a financing strategy is feasible as long as the total equity value remains positive before bankruptcy. Therefore, we need to impose the limited liability constraint on the dynamic of the firm’s equity. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">每一时刻，企业有两项现金流出与两项流入。流出为税后票息 (1−κ)ρPdt 及到期本金 pdt，其中 κ 是税率；流入为发行新债取得的 btdt（bt 是全部新发债券的价格），以及资产总支付 δVtdt。若总流入 (δVt＋bt)dt 大于总流出 ((1−κ)ρP＋p)dt，差额作为股利支付股东；否则增发股权来清偿到期债务。注意两者差额乘以 dt 是无穷小量。因此，只要破产前股权总价值保持为正，这种融资策略就可行。故需要对企业股权动态施加有限责任约束（limited liability constraint）。</span></details>

#### 1.3 Default Payments <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.3 违约支付。</span></details>

As in first passage models, we assume that the default occurs at time $\tau=\inf\{t\geq0:V_t\leq V_B\}$. Upon default, the firm loses $(1-\alpha)$ of $V_\tau$, due to reorganization of the firm, and the debtholders as a whole get the rest of the value left, $\alpha V_\tau$, after reorganization. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与首次穿越模型一样，假设违约发生于 τ＝inf{t≥0：Vt≤VB}。违约时，企业重组损失资产价值 Vτ 的 (1−α) 部分，全部债权人获得重组后的剩余价值 αVτ。</span></details>

To find the total debt value, total equity value, and optimal leverage ratio, it is not necessary to spell out the recovery value for individual bonds with different maturities. However, to model credit spreads we need to specify how the remaining asset of the firm $\alpha V_\tau$ is distributed among bonds with different maturities. Three standard assumptions are recovery at a fraction of par value, of market values, and of corresponding treasury bonds. Here we shall use the assumption of recovery at a fractional treasury bonds. We use this assumption because it makes analytical calculation easier. More precisely, upon default the payoff of a bond with unit face value and maturity $T>\tau$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">计算债务总价值、股权总价值和最优杠杆率，不必规定各期限单只债券的回收价值。但要建模信用利差，就必须说明剩余资产 αVτ 如何分配给不同期限的债券。三种标准假设分别是按面值、市值或对应国债价值的一定比例回收。这里采用国债价值比例回收，因为这样更便于解析计算。具体而言，面值为 1、到期日 T＞τ 的债券在违约时获得：</span></details>

$$
ce^{-r(T-\tau)},\quad0\leq c\leq1.
$$

To determine $c$, we shall match the total payment to bondholder with the total remaining asset $\alpha V_\tau$. By the memoryless property of exponential distribution, the conditional distribution of a bond’s maturity does not change given its maturity is beyond $\tau$. Thus, we have by (1) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为确定 c，令支付债权人的总金额等于剩余资产 αVτ。根据指数分布的无记忆性（memoryless property），给定债券在 τ 之后到期，其剩余期限的条件分布不变。因此由式（1）：</span></details>

$$
\int_\tau^{+\infty}ce^{-r(s-\tau)}\cdot pe^{-m(s-\tau)}ds=\alpha V_\tau,
$$

yielding <details class="translation-details"><summary>中文译文</summary><span class="translation-body">得到：</span></details>

$$
c=\frac{m+r}m\frac{\alpha V_\tau}P=\frac{m+r}m\frac{\alpha V_B}P.
$$


> [!example] 课堂截图：首次触及违约边界与回收
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/02_第2页_首次触及违约边界与回收_截图10-08_1915.png]]


## PDF p.3

To make sure that $0\leq c\leq1$, we shall impose that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">为保证 0≤c≤1，施加条件：</span></details>

$$
\frac{m+r}m\frac{\alpha V_B}P\leq1.\tag{2}
$$

We will see that this assumption is satisfied by the optimal default barrier; see Theorem 1. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">后面会看到，最优违约边界满足这一假设，参见定理 1。</span></details>

We should emphasize that this recovery assumption is irrelevant if one is only interested in understanding debt values as a whole, but is relevant when we consider credit spreads, which in turn depend on cash flows to bonds with different maturities. In particular, our results about optimal default boundary and optimal leverage level will not be affected by the recovery assumption. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">需要强调：若只关心整体债务价值，这一回收假设并不重要；但在研究信用利差时它很重要，因为利差取决于各期限债券的现金流。特别地，关于最优违约边界和最优杠杆水平的结果不受该回收假设影响。</span></details>

#### 1.4 Debt, Equity, and Market Value of the Firm <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.4 企业的债务、股权和市场价值。</span></details>

At time 0 the price of a bond with face value 1 and maturity $T$ when the firm asset $V_0=V$ is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">零时刻企业资产为 V0＝V 时，面值 1、到期日 T 的债券价格为：</span></details>

$$
\begin{aligned}
B(V;V_B,T)&=E[e^{-rT}\mathbf1_{\{\tau>T\}}+e^{-r\tau}\cdot ce^{-r(T-\tau)}\mathbf1_{\{\tau\leq T\}}]+E\left[\int_0^{\tau\wedge T}\rho e^{-rs}ds\right]\\
&=e^{-rT}P[\tau\geq T]+cE[e^{-rT}\mathbf1_{\{\tau\leq T\}}]+\frac\rho r(1-E[e^{-r(\tau\wedge T)}])\\
&=\left(1-\frac\rho r\right)e^{-rT}P[\tau\geq T]+cE[e^{-rT}\mathbf1_{\{\tau\leq T\}}]+\frac\rho r(1-E[e^{-r\tau}\mathbf1_{\{\tau\leq T\}}]).
\end{aligned}
$$


> [!example] 课堂截图：债券价值与存续情形
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/03_第3页_债券价值与存续情形_截图10-08_1903.png]]


> [!example] 课堂截图：未违约支付项
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/04_第3页_未违约支付项_截图10-08_1904.png]]


> [!example] 课堂截图：到期前违约与回收
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/05_第3页_到期前违约与回收_截图10-08_1905.png]]


In our endogenous model, both $P$ (which is related to the optimal debt/equity ratio) and the endogenous default barrier $V_B$ will be decision variables. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">在本内生模型中，P（与最优债务／股权比率有关）和内生违约边界 VB 都是决策变量。</span></details>

According to the Modigliani-Miller theorem, the total market value of the firm is the asset value plus tax benefits and minus the bankruptcy costs. More precisely, the market value of the firm at time 0 is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据莫迪利安尼–米勒定理（Modigliani–Miller theorem），企业总市场价值等于资产价值加税收收益、减破产成本。具体而言，零时刻企业市场价值为：</span></details>

$$
\begin{aligned}
v(V;V_B)&=V+E\left[\int_0^\tau\kappa\rho Pe^{-rt}dt\right]-(1-\alpha)E[V_\tau e^{-r\tau}]\\
&=V+\kappa\rho P\cdot E\left[\int_0^\tau e^{-rt}dt\right]-(1-\alpha)V_BE[e^{-r\tau}].
\end{aligned}
$$


> [!example] 课堂截图：贴现期望与公司价值
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/06_第3页_贴现期望与公司价值_截图10-08_1908.png]]


> [!example] 课堂截图：税盾积分期望
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/07_第3页_税盾积分期望_截图10-08_1910.png]]


Note that we have to put a constraint on $\rho$, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">注意，必须对 ρ 施加约束：</span></details>

$$
\frac r\kappa>\rho;\tag{3}
$$

otherwise, the total tax benefit, $E[\int_0^\tau\kappa\rho Pe^{-rt}dt]\leq\kappa\rho P\int_0^\infty e^{-rt}dt=\frac{\kappa\rho}rP$, could exceed the face value of the debt $P$, which may create a tax abitrage <details class="translation-details"><summary>中文译文</summary><span class="translation-body">否则，总税收收益 E[∫₀^τ κρPe^(−rt)dt]≤κρP∫₀^∞ e^(−rt)dt＝(κρ／r)P 可能超过债务面值 P，从而产生税收套利</span></details>

## PDF p.4

opportunity. The total equity value equals to the total value of the firm less the total value of bonds, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">机会。股权总价值等于企业总价值减债券总价值：</span></details>

$$
S(V;V_B)=v(V;V_B)-D(V;V_B),
$$

where the total debt $D(V;V_B)$ is equal to <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中，债务总价值 D(V；VB) 为：</span></details>

$$
D(V;V_B)=P\int_0^{+\infty}me^{-mT}B(V;V_B,T)dT.
$$


> [!example] 配套推导
> [[AMA572 Fixed-Income and Credit Risk/Lecture 4/02 - 总债务价值补充推导（课堂原图）|总债务价值的 Laplace 变换：原纸照片及逐步课堂批注]]


We should point out that in this static model (thanks to the exponential maturity profile), the total firm value, total debt and equity values are all Markovian, and are independent of the time horizon. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">需要指出，在这一静态模型中（得益于指数期限分布），企业总价值、债务总价值和股权总价值均具有马尔可夫性（Markovian），且不依赖于时间期限。</span></details>

#### 1.5 Preliminary Results for Debt and Equity Values <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1.5 债务和股权价值的初步结果。</span></details>

Similarly the total market value of the firm $v(V;V_B)$ can be computed similarly in a hwk problem, and the total equity of the firm is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">类似地，企业总市场价值 v(V；VB) 可按课后练习中的方法计算，股权总价值为：</span></details>

$$
S(V;V_B)=v(V;V_B)-D(V;V_B).
$$

**Proposition 1.** The total market value of the firm is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">命题 1：企业总市场价值为：</span></details>

$$
v(V;V_B)=V+\frac{\kappa\rho}rP-\left[\frac{\kappa\rho}rP+(1-\alpha)V_B\right](V_B/V)^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi}.\tag{4}
$$

The total debt value of the firm is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">企业债务总价值为：</span></details>

$$
D(V;V_B)=P\frac{\rho+m}{r+m}-P\left(\frac\rho r+\left(1-\frac\rho r-\frac{m+r}m\frac{\alpha V_B}P\right)\frac m{r+m}\right)(V_B/V)^{\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi}.\tag{5}
$$

The total equity value of the firm is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">企业股权总价值为：</span></details>

$$
\begin{aligned}
S(V;V_B)&=v(V;V_B)-D(V;V_B)\\
&=V+\frac{\kappa\rho}rP-\left[\frac{\kappa\rho}rP+(1-\alpha)V_B\right](V_B/V)^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi}\\
&\quad-P\frac{\rho+m}{r+m}+P\left[\frac\rho r+\left(1-\frac\rho r-\frac{m+r}m\frac{\alpha V_B}P\right)\frac m{r+m}\right](V_B/V)^{\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi}.
\end{aligned}\tag{6}
$$


> [!example] 课堂截图：公司债务股权价值命题
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/08_第4页_公司债务股权价值命题_截图10-08_2016.png]]


> [!example] 课堂截图：价值命题求导续写
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/09_第4页_价值命题求导续写_截图10-08_2018.png]]


**Proof.** The market value of the firm at time 0 is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：零时刻企业市场价值为：</span></details>

$$
\begin{aligned}
v(V;V_B)&=V+\kappa\rho P\cdot E\left[\int_0^\tau e^{-rt}dt\right]-(1-\alpha)V_BE[e^{-r\tau}]\\
&=V+\kappa\rho P\cdot E\left[\frac1r(1-e^{-r\tau})\right]-(1-\alpha)V_BE[e^{-r\tau}]\\
&=V+\frac{\kappa\rho}rP-\left[\frac{\kappa\rho}rP+(1-\alpha)V_B\right]\cdot E[e^{-r\tau}].
\end{aligned}
$$

## PDF p.5

Since <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于：</span></details>

$$
E[e^{-r\tau}]=\exp\left\{\log(V_B/V)\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\right\},
$$

where $\xi=\frac{r-\delta}{\sigma^2}-\frac12$, we must have (4). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 ξ＝(r−δ)／σ²−1／2，因此式（4）成立。</span></details>

We know from the previous discussions that the Laplace transform of a bond price, $B(V;V_B,T)$, is given by <details class="translation-details"><summary>中文译文</summary><span class="translation-body">根据前面的讨论，债券价格 B(V；VB，T) 的拉普拉斯变换为：</span></details>

$$
\begin{aligned}
&\int_0^\infty e^{-\beta T}B(V;V_B,T)dT\\
&=\frac{\rho+\beta}{\beta(r+\beta)}-\left(\frac\rho r\frac1\beta+\left(1-\frac\rho r-c\right)\frac1{r+\beta}\right)\cdot\exp\left\{\log(V_B/V)\left(\sqrt{\xi^2+\frac2{\sigma^2}(\beta+r)}+\xi\right)\right\},
\end{aligned}
$$

where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中：</span></details>

$$
\xi=\frac{r-\delta}{\sigma^2}-\frac12,\quad c=\frac{m+r}m\frac{\alpha V_B}P.
$$

Therefore, the value of total debt at time 0 is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，零时刻债务总价值为：</span></details>

$$
\begin{aligned}
D(V;V_B)&=P\int_0^{+\infty}me^{-mT}B(V;V_B,T)dT\\
&=P\frac{\rho+m}{r+m}-P\left(\frac\rho r+\left(1-\frac\rho r-\frac{m+r}m\frac{\alpha V_B}P\right)\frac m{r+m}\right)\\
&\quad\times\exp\left\{\log(V_B/V)\left(\sqrt{\xi^2+\frac2{\sigma^2}(m+r)}+\xi\right)\right\}\\
&=P\frac{\rho+m}{r+m}-P\left(\frac\rho r+\left(1-\frac\rho r-\frac{m+r}m\frac{\alpha V_B}P\right)\frac m{r+m}\right)\cdot(V_B/V)^{\sqrt{\xi^2+2(m+r)/\sigma^2}+\xi},
\end{aligned}
$$

which is (5). The combination of equation (4) and (5) yields that the total equity value of the firm is given by (6). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即式（5）。将式（4）与式（5）结合，即得到式（6）的企业股权总价值。</span></details>

**Remark:** Note that we are able to compute the total debt value, total equity value, and the total market value analytically, although we can only compute a given bond price via Laplace transforms. This is made possible thanks to our assumption of the exponential maturity profile. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">说明：虽然单只债券的价格只能通过拉普拉斯变换来计算，但债务总价值、股权总价值及企业总市场价值都能解析计算。这得益于指数期限分布的假设。</span></details>


> [!example] 课堂截图：首次穿越Laplace变换补充推导提示
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/10_第5页_首次穿越Laplace变换补充推导提示_截图10-08_1930.png]]


### 2 Optimal Capital Structure and Endogenous Default <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2 最优资本结构与内生违约。</span></details>

In this section, we consider the problem of optimal capital structure and optimal endogenous default barrier, i.e. the choices of optimal debt level $P$ and bankrupt trigger $V_B$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">本节研究最优资本结构和最优内生违约边界，即如何选择最优债务水平 P 与破产触发值 VB。</span></details>

## PDF p.6

#### 2.1 The Solution of a Two-Stage Optimization Problem <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.1 两阶段优化问题的解。</span></details>

Deciding optimal $P$ and choosing optimal $V_B$ are two entangled problems, and cannot be separated easily. For example, when a firm chooses $P$ to maximize the total firm value at time 0, the decision on $P$ obviously depends on the bankruptcy trigger level $V_B$. Similarly, after the debt being issued, the equity holders will choose an optimal $V_B$, which of course depends on how much debt the firm has. Here we shall choose $P$ and $V_B$ according to a two-stage optimization procedure as in Leland (1994) and Leland and Toft (1996). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">决定最优 P 与选择最优 VB 是相互交织的问题，很难分开。例如，企业选择 P 以最大化零时刻企业总价值时，P 的决策显然取决于破产触发值 VB。同样，发债后股东选择的最优 VB 也取决于债务规模。这里沿用 Leland（1994）及 Leland 和 Toft（1996）的两阶段优化程序来选择 P 和 VB。</span></details>

More precisely, for a fixed $P$, the equity holders find the optimal default barrier by maximizing the equity value, subject to the limited liability constraint. It is the equity value that is maximized, because after the debt being issued it is the equity holders who control the firm. Mathematically, the equity holders find the best $V_B$ by solving <details class="translation-details"><summary>中文译文</summary><span class="translation-body">具体而言，给定 P 后，股东在有限责任约束下最大化股权价值，以寻找最优违约边界。最大化的是股权价值，因为发债后控制企业的是股东。数学上，股东求解：</span></details>

$$
\max_{V_B}S(V;V_B)\tag{7}
$$

subject to the limited liability constraint <details class="translation-details"><summary>中文译文</summary><span class="translation-body">满足有限责任约束：</span></details>

$$
S(V';V_B)\geq0,\quad\text{for all }V'\geq V_B\geq0.\tag{8}
$$

The limited liability constraint is imposed so that the equity value is always nonnegative for any future firm asset value $V'$, as long as the asset value $V'$ is above the bankruptcy level $V_B$. The is the first stage optimization problem. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">有限责任约束保证：只要未来资产价值 V′ 高于破产水平 VB，无论 V′ 为何，股权价值都非负。这就是第一阶段优化问题。</span></details>

Clearly the optimal $V_B^*\equiv V_B^*(P)$ to be chosen by the equity holders will depend on $P$. At time 0, the firm will conduct the second stage optimization to maximize the firm value, in anticipation of what the equity holders will do later. More precisely, the second stage optimization is that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">显然，股东选择的最优边界 VB*≡VB*(P) 依赖 P。零时刻企业预见股东之后的行为，进行第二阶段优化，以最大化企业价值。具体为：</span></details>

$$
\max_P v(V;V_B^*(P)).\tag{9}
$$

The two-stage optimization problem partly arises due to the conflict of interests between debt and equity holders. It is obvious that choosing the leverage level $P$ and bankrupt trigger $V_B$ simultaneously will lead to a better market value of the firm. Leland (1998) uses the difference of the two to explain agency costs due to conflicts between the equity and debt holders. Obviously the two-stage optimization is only a rough approximation to complicated decision and negotiation between debt and equity holders. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">两阶段优化部分源于债权人与股东之间的利益冲突。若同时选择杠杆水平 P 和破产触发值 VB，显然可以得到更高的企业市场价值。Leland（1998）用两种结果的差异解释债权人与股东冲突造成的代理成本（agency costs）。显然，两阶段优化只是对双方复杂决策与谈判的粗略近似。</span></details>

Here is the result for the two-stage optimization. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">以下给出两阶段优化的结果。</span></details>

**Theorem 1.** (a) The solution of <details class="translation-details"><summary>中文译文</summary><span class="translation-body">定理 1：（a）方程：</span></details>

$$
\left.\frac{\partial S(V;V_B^*)}{\partial V}\right|_{V=V_B^*}=0\tag{10}
$$

## PDF p.7

is given by $V_B^*=\epsilon P$, where <details class="translation-details"><summary>中文译文</summary><span class="translation-body">的解为 VB*＝εP，其中：</span></details>

$$
\epsilon=\frac{\frac{\rho+m}{r+m}\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)-\frac{\kappa\rho}r\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)}{1+(1-\alpha)\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)+\alpha\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)}.
$$

(b) <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）</span></details>

$$
0<\epsilon<\frac1\alpha\frac{\rho+m}{r+m},\tag{11}
$$

and, therefore, the default barrier $V_B^*$ satisfies (2). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，违约边界 VB* 满足式（2）。</span></details>

(c) The first stage optimization: Given the debt level $P$, the optimal barrier level solving (7) with the constraint in (8) is given by $V_B^*=\epsilon P$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）第一阶段优化：给定债务水平 P，在式（8）的约束下求解式（7）得到最优边界 VB*＝εP。</span></details>

(d) The second stage optimization: After plugging the optimal $V_B^*=\epsilon P$ into the second stage optimization, we have that $v(V;\epsilon P)$ is a concave function of $P\in(0,V/\epsilon)$, which implies that we can find a unique optimal debt level $P$ for the problem (9). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）第二阶段优化：代入最优边界 VB*＝εP 后，v(V；εP) 是 P∈(0，V／ε) 上的凹函数（concave function），意味着可为问题（9）找到唯一的最优债务水平 P。</span></details>

**Proof.** (a) It follows from equation (6) that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">证明：（a）由式（6）得：</span></details>

$$
\begin{aligned}
\frac{\partial S(V;V_B)}{\partial V}={}&1-\left[\frac{\kappa\rho}rP+(1-\alpha)V_B\right]\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\left(\frac{V_B}V\right)^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi-1}\left(-\frac{V_B}{V^2}\right)\\
&+P\left[\frac\rho r+\left(1-\frac\rho r-\frac{m+r}m\frac{\alpha V_B}P\right)\frac m{r+m}\right]\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)\\
&\qquad\times\left(\frac{V_B}V\right)^{\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi-1}\left(-\frac{V_B}{V^2}\right).
\end{aligned}
$$

Hence, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，</span></details>

$$
\begin{aligned}
\left.\frac{\partial S(V;V_B)}{\partial V}\right|_{V=V_B}={}&1-\left[\frac{\kappa\rho}rP+(1-\alpha)V_B\right]\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\left(-\frac1{V_B}\right)\\
&+P\left[\frac\rho r+\left(1-\frac\rho r-\frac{m+r}m\frac{\alpha V_B}P\right)\frac m{r+m}\right]\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)\left(-\frac1{V_B}\right).
\end{aligned}
$$

Letting <details class="translation-details"><summary>中文译文</summary><span class="translation-body">令：</span></details>

$$
\left.\frac{\partial S(V;V_B)}{\partial V}\right|_{V=V_B}=0,
$$


> [!example] 课堂截图：最优违约边界光滑粘贴条件
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/11_第7页_最优违约边界光滑粘贴条件_截图10-08_2022.png]]


## PDF p.8

we obtain <details class="translation-details"><summary>中文译文</summary><span class="translation-body">得到：</span></details>

$$
\begin{aligned}
&1+\frac{\kappa\rho}rP\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\frac1{V_B}+(1-\alpha)\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)\\
&\quad-P\left[\frac\rho r+\left(1-\frac\rho r\right)\frac m{r+m}\right]\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)\frac1{V_B}+\alpha\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)=0,
\end{aligned}
$$

which yields <details class="translation-details"><summary>中文译文</summary><span class="translation-body">解得：</span></details>

$$
V_B^*=\frac{\left[\frac\rho r+\left(1-\frac\rho r\right)\frac m{r+m}\right]\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)-\frac{\kappa\rho}r\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)}{1+(1-\alpha)\left(\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi\right)+\alpha\left(\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi\right)}P.
$$

So $V_B^*=\epsilon P$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因而 VB*＝εP。</span></details>

(b) See a homework problem. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（b）参见课后练习。</span></details>

(c) This part is the most difficult part; see the paper by Chen and Kou (2009). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（c）这一部分最困难，参见 Chen 和 Kou（2009）的论文。</span></details>

(d) By equation (4) we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">（d）由式（4）：</span></details>

$$
\begin{aligned}
v(V;\epsilon P)&=V+\frac{\kappa\rho}rP-\left[\frac{\kappa\rho}rP+(1-\alpha)\epsilon P\right](\epsilon P/V)^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi}\\
&=V+\frac{\kappa\rho}rP-\left[\frac{\kappa\rho}r+(1-\alpha)\epsilon\right](\epsilon/V)^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi}\cdot P^{\sqrt{\xi^2+\frac2{\sigma^2}r}+\xi+1}.
\end{aligned}
$$

Since <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于：</span></details>

$$
\sqrt{\xi^2+\frac{2r}{\sigma^2}}+\xi+1>\sqrt{\xi^2}+\xi+1\geq1,
$$

it follows that <details class="translation-details"><summary>中文译文</summary><span class="translation-body">可得：</span></details>

$$
P^{\left(\sqrt{\xi^2+\frac{2r}{\sigma^2}}+\xi+1\right)}\text{ is convex},
$$

and consequently <details class="translation-details"><summary>中文译文</summary><span class="translation-body">即上述幂函数为凸函数，因此：</span></details>

$$
-\left[\frac{\kappa\rho}r+(1-\alpha)\epsilon\right]\left(\frac\epsilon V\right)^{\sqrt{\xi^2+\frac{2r}{\sigma^2}}}\cdot P^{\sqrt{\xi^2+\frac{2r}{\sigma^2}}+\xi+1}.
$$

The expression above is concave. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">上式为凹函数。</span></details>

Since $V+\frac{\kappa\rho}rP$ is linear and the sum of a linear function and a concave function is still concave, it follows that the function $v(V;\epsilon P)$ is concave. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">由于 V＋(κρ／r)P 是线性函数，而线性函数与凹函数之和仍为凹函数，因此 v(V；εP) 为凹函数。</span></details>


> [!example] 课堂截图：最优债务水平凹性证明
> ![[AMA572 Fixed-Income and Credit Risk/Lecture 4/附件/课堂截图/12_第8页_最优债务水平凹性证明_截图10-08_2053.png]]


## PDF p.9

#### 2.2 The Optimal Capital Structure <details class="translation-details"><summary>中文译文</summary><span class="translation-body">2.2 最优资本结构。</span></details>

Table 2 shows the effect of various parameters on the optimal leverage level. The parameters are $\kappa=35\%$, $r=8\%$, $\rho=8.162\%$, $\delta=6\%$, $V_0=100$. The riskless rate $r=8\%$ is close to the average historical short-term treasury rate during 1973-1998, and the coupon rate $\rho=8.162\%$ is the par coupon rate for risk-free bonds with semi-annual coupon payments when the continuously compounded interest rate is 8%. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">表 2 展示不同参数对最优杠杆水平的影响。参数为 κ＝35%、r＝8%、ρ＝8.162%、δ＝6%、V0＝100。无风险利率 8% 接近 1973—1998 年短期国债利率的历史平均值；票息率 8.162% 则是在连续复利利率为 8% 时，半年付息无风险债券的平价票息率。</span></details>

Consistent with our intuition, the table shows that the optimal leverage ratio is an increasing function of the fractional remaining asset $\alpha$ and average maturity profile $1/m$, and is a decreasing function of diffusion volatility $\sigma$. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">与直觉一致，表中显示最优杠杆率随剩余资产比例 α 和平均期限 1／m 增大而增大，随扩散波动率 σ 增大而减小。</span></details>

| | $m^{-1}=0.5$ | $m^{-1}=0.5$ | $m^{-1}=1$ | $m^{-1}=1$ | $m^{-1}=2$ | $m^{-1}=2$ | $m^{-1}=5$ | $m^{-1}=5$ |
|---|---|---|---|---|---|---|---|---|
| | $\sigma=0.2$ | $\sigma=0.4$ | $\sigma=0.2$ | $\sigma=0.4$ | $\sigma=0.2$ | $\sigma=0.4$ | $\sigma=0.2$ | $\sigma=0.4$ |
| $\alpha=5\%$ | 7.14% | 1.11% | 11.19% | 2.37% | 17.56% | 5.04% | 30.67% | 12.91% |
| $\alpha=25\%$ | 13.78% | 3.21% | 18.31% | 5.28% | 25.08% | 9.13% | 38.41% | 19.07% |
| $\alpha=50\%$ | 25.44% | 9.22% | 30.30% | 12.63% | 37.29% | 18.27% | 50.52% | 31.19% |

However, the Leland-Toft model cannot explain why many high-tech companies have no debt at all. <details class="translation-details"><summary>中文译文</summary><span class="translation-body">不过，Leland–Toft 模型无法解释为何许多高科技企业完全没有债务。</span></details>

**HWK** <details class="translation-details"><summary>中文译文</summary><span class="translation-body">课后练习。</span></details>

1. Prove (11). <details class="translation-details"><summary>中文译文</summary><span class="translation-body">1. 证明式（11）。</span></details>

##### 解答：证明式（11）

**目标。** 对定理 1 中给定的 $\epsilon$，证明：

$$
0<\epsilon<\frac1\alpha\frac{\rho+m}{r+m}.
$$

沿用模型通常的参数范围：$r>0$、$m>0$、$\sigma>0$、$\rho\geq0$、$0\leq\kappa<1$、$0<\alpha\leq1$，并使用式（3）的等价条件 $\kappa\rho<r$。这里要求 $\alpha>0$，是因为式（11）含有 $1/\alpha$；$\alpha=0$ 时不把该上界视为有限实数。

**第一步：用简记整理 $\epsilon$。** 令：

$$
a=\sqrt{\xi^2+\frac{2r}{\sigma^2}}+\xi,
\qquad
b=\sqrt{\xi^2+\frac{2(r+m)}{\sigma^2}}+\xi,
$$

$$
d=\frac{\rho+m}{r+m},
\qquad
k=\frac{\kappa\rho}{r}.
$$

其中 $k$ 只是本题的简记，不是原来的税率 $\kappa$。定理中的表达式变为：

$$
\epsilon=\frac{db-ka}{1+(1-\alpha)a+\alpha b}.
$$

因为 $r>0$，所以 $\sqrt{\xi^2+2r/\sigma^2}>|\xi|$，从而 $a>0$。又因为 $m>0$，第二个根号内的数更大，因此：

$$
b>a>0.
$$

此外，$d>0$、$k\geq0$，且分母：

$$
L:=1+(1-\alpha)a+\alpha b>0.
$$

**第二步：证明 $d>k$。** 通分可得：

$$
\begin{aligned}
d-k
&=\frac{\rho+m}{r+m}-\frac{\kappa\rho}{r}\\
&=\frac{r(\rho+m)-\kappa\rho(r+m)}{r(r+m)}\\
&=\frac{(1-\kappa)\rho r+m(r-\kappa\rho)}{r(r+m)}.
\end{aligned}
$$

分母为正；分子第一项非负，第二项由 $m>0$ 和式（3）的 $r-\kappa\rho>0$ 得到严格为正。因此：

$$
d-k>0.
$$

**第三步：证明下界 $\epsilon>0$。** 将分子改写为：

$$
db-ka=d(b-a)+(d-k)a>0.
$$

两项均为正，且分母 $L>0$，所以：

$$
\epsilon=\frac{db-ka}{L}>0.
$$

**第四步：证明上界。** 因为 $ka\geq0$，所以 $db-ka\leq db$；又因为：

$$
L=\alpha b+\left[1+(1-\alpha)a\right]>\alpha b>0,
$$

因此：

$$
\epsilon
=\frac{db-ka}{L}
\leq\frac{db}{L}
<\frac{db}{\alpha b}
=\frac d\alpha
=\frac1\alpha\frac{\rho+m}{r+m}.
$$

这里最后的严格不等号来自 $L>\alpha b$，所以即使 $k=0$，上界仍然是严格的。

结合第三步，得到：

$$
\boxed{0<\epsilon<\frac1\alpha\frac{\rho+m}{r+m}}.
$$

式（11）证毕。关键是先用式（3）证明 $d>k$，再分别比较 $\epsilon$ 的分子与分母。

> [!warning]- 补充核对：式（11）不能直接推出式（2）
> 上面的证明解决的是题目要求的式（11）。但原文在定理 1(b) 后写的“因此最优违约边界满足（2）”，不能仅由式（11）得到。
>
> 代入 $V_B^*=\epsilon P$，式（2）实际要求：
>
> $$
> \frac{m+r}{m}\alpha\epsilon\leq1
> \quad\Longleftrightarrow\quad
> \epsilon\leq\frac{m}{\alpha(m+r)}.
> $$
>
> 而式（11）仅给出 $\epsilon<(\rho+m)/[\alpha(r+m)]$。当 $\rho>0$ 时，这个上界更大、约束更弱，不能据此推出式（2）。
>
> 例如，取 $r=0.05$、$\delta=0.03$、$\sigma=0.2$、$m=0.01$、$\rho=0.05$、$\kappa=0.25$、$\alpha=0.8$。这些参数满足上述基础参数条件及式（3），但 $\xi=0$，且：
>
> $$
> \epsilon
> =\frac{\sqrt3-\frac14\sqrt{5/2}}
> {1+\frac15\sqrt{5/2}+\frac45\sqrt3}
> \approx0.494756.
> $$
>
> 此时式（11）的上界是 $1.25$，确实满足式（11）；但式（2）要求 $\epsilon\leq0.208333\ldots$，不成立。对应的：
>
> $$
> c=\frac{m+r}{m}\alpha\epsilon\approx2.374830>1.
> $$
>
> 因而，若未额外施加式（2）或其他参数限制，它并不由这些基础条件自动成立。这里保留课件原文，仅把这一推论上的问题单独注明；这不影响上面对式（11）本身的证明。
