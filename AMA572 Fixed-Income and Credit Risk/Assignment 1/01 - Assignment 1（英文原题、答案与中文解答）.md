---
course: AMA572 Fixed-Income and Credit Risk
created: 2026-10-22
type: 作业逐题中英学习版
assignment: 1
question_count: 3
cssclasses:
  - ama-inline-translations
tags:
  - AMA572
  - Assignment
---

# Assignment 1｜英文原题、答案与中文解答

[[AMA572 Fixed-Income and Credit Risk/Assignment 1/00 - Assignment 1 资料索引|返回资料索引]]

**原题日期信息：** Deadline: September 25, 2026。

> [!info] 阅读方式与答案来源
> 每题依次为 **英文原题 → 教师英文答案（如有）→ GPT 英文详解 → 中文解答**。教师部分转录自标有“老师给的”的 Suggested Solutions；GPT 英文与中文部分分别完整整理自项目现有生成稿，中文常驻显示，方便直接学习。
>
> 不把 GPT 稿称为教师标准答案。正文只调整标题层级、分页符与数学排版；重复题干只放一次。原 PDF 与 Markdown 源稿全部保留在本目录附件，具体版本及页码见资料索引。

> [!warning] 本份教师答案的覆盖范围与笔误
> 教师 PDF 只有 Q1、Q2，未提供 Q3；Q2 三年债价格差的一行存在印刷错误，已在原文旁单独标出。现有 GPT 稿的计算口径与讲义勘误另外保留于 [[AMA572 Fixed-Income and Credit Risk/Assignment 1/02 - Assignment 1 计算口径与勘误（中英对照）|计算口径与勘误（中英对照）]]。

## 题目导航

- [[#第1题｜信用评级迁移矩阵|第1题：信用评级迁移矩阵]]
- [[#第2题｜分段隐含违约参数|第2题：分段隐含违约参数]]
- [[#第3题｜GBM 下的税盾与破产成本|第3题：GBM 下的税盾与破产成本]]
- [[#原题附录｜Itô 引理与对数正态分布|原题附录]]

---

## 第1题｜信用评级迁移矩阵

### 英文原题

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_作业题目_共3题_截止2026-09-25.pdf#page=1|题目 PDF p.1]]。

Q1. Compute the empirical and generator-based estimators of one-year transition matrix for the following data.

(a) There are four credit classes, A, B, C, D. At the beginning, there are 20 firms in A, B, C, each.

(b) In one month, two B rated firms migrate to C, and two B rated firms migrate to A, and these firms stay there for the rest of the year.

(c) In three months, three A rated firm migrates to B, and stay there for the rest of the year.

(d) In seven months, two C rated firms migrate to B and stay there for the rest of the year. Furthermore, one C rate firm defaults.

(e) Ten months later, two C rated firms default.

### 教师英文答案

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment01_sol_老师给的.pdf#page=1|教师 Suggested Solutions，PDF pp.1–2]]。重复出现的题目已放在上方，以下保留其 Solution 部分。

Solution.

$$
\widehat P_{\mathrm{empirical}}=
\begin{pmatrix}
\frac{17}{20}&\frac3{20}&0&0\\
\frac2{20}&\frac{16}{20}&\frac2{20}&0\\
0&\frac2{20}&\frac{15}{20}&\frac3{20}\\
0&0&0&1
\end{pmatrix}.
$$

We compute generator-based estimators as follows,

$$
N_A=\frac{235}{12},\qquad N_B=\frac{233}{12},\qquad N_C=\frac{81}{4}.
$$

$$
M_{A,B}=3,\qquad M_{A,C}=M_{A,D}=0,
$$

$$
M_{B,A}=2,\qquad M_{B,C}=2,\qquad M_{B,D}=0,
$$

$$
M_{C,A}=0,\qquad M_{C,B}=2,\qquad M_{C,D}=3.
$$

The estimator becomes

$$
\widehat\lambda_{A,B}=\frac{M_{A,B}}{N_A}=\frac{36}{235},\qquad \widehat\lambda_{A,C}=\widehat\lambda_{A,D}=0,
$$

$$
\widehat\lambda_{B,A}=\frac{M_{B,A}}{N_B}=\frac{24}{233},\qquad
\widehat\lambda_{B,C}=\frac{M_{B,C}}{N_B}=\frac{24}{233},\qquad
\widehat\lambda_{B,D}=0,
$$

$$
\widehat\lambda_{C,B}=\frac{M_{C,B}}{N_C}=\frac8{81},\qquad
\widehat\lambda_{C,D}=\frac{M_{C,D}}{N_C}=\frac4{27},\qquad
\widehat\lambda_{C,A}=0.
$$

The estimator of the generator matrix is given by

$$
\widehat\Lambda=
\begin{pmatrix}
-\frac{36}{235}&\frac{36}{235}&0&0\\
\frac{24}{233}&-\frac{48}{233}&\frac{24}{233}&0\\
0&\frac8{81}&-\frac{20}{81}&\frac4{27}\\
0&0&0&0
\end{pmatrix}.
$$

Therefore the one-year transition matrix is estimated by

$$
\begin{aligned}
\widehat P_{\mathrm{generator}}&=e^{\widehat\Lambda}\\
&=\begin{pmatrix}
0.864631&0.128572&0.006462&0.000336\\
0.086450&0.824468&0.082497&0.006584\\
0.004166&0.079102&0.785246&0.131486\\
0.000000&0.000000&0.000000&1.000000
\end{pmatrix}.
\end{aligned}
$$

### GPT 英文详解

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_Complete_Solutions_EN.md|项目已有 GPT 英文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_Complete_Solutions_EN.pdf#page=1|英文 PDF]]。

Use the state order $(A,B,C,D)$, where $D$ is the absorbing default state. Following the corresponding lecture example, interpret “ten months later” as **month 10 measured from the beginning of the year**.

#### 1. Empirical estimator

Count each firm's transition from its initial rating to its year-end rating. The denominator is the number initially in that rating, not the year-end population. The initially B-rated firms that move to A or C remain there for the rest of the year.

| Initial rating | Final A | Final B | Final C | Final D | Initial total |
|:---:|---:|---:|---:|---:|---:|
| A | 17 | 3 | 0 | 0 | 20 |
| B | 2 | 16 | 2 | 0 | 20 |
| C | 0 | 2 | 15 | 3 | 20 |

The empirical estimate is therefore

$$
\boxed{
\widehat P_{\mathrm{emp}}=
\begin{pmatrix}
0.85&0.15&0&0\\
0.10&0.80&0.10&0\\
0&0.10&0.75&0.15\\
0&0&0&1
\end{pmatrix}.}
$$

The last row follows from the assumption that default is absorbing.

#### 2. Total time spent in each rating

Let $N_i$ be the total time spent in rating $i$ by all firms, measured in **firm-years**. Include the time spent after entry by firms that migrate into the rating.

$$
\begin{aligned}
N_A
&=17\times1+3\times\frac3{12}+2\times\frac{11}{12}
=\frac{235}{12},\\[4pt]
N_B
&=16\times1+4\times\frac1{12}
+3\times\frac9{12}+2\times\frac5{12}
=\frac{233}{12},\\[4pt]
N_C
&=15\times1+3\times\frac7{12}
+2\times\frac{10}{12}+2\times\frac{11}{12}
=\frac{243}{12}.
\end{aligned}
$$

For example, $N_C$ includes 15 firms that remain in C all year; three that leave C at month 7 (two move to B and one defaults); two that default at month 10; and two that enter C from B at month 1 and remain for 11 months.



#### 3. Generator-based estimator

Let $M_{ij}$ denote the number of observed transitions from $i$ to $j$. The nonzero counts are

$$
M_{AB}=3,\quad M_{BA}=2,\quad M_{BC}=2,
\quad M_{CB}=2,\quad M_{CD}=3.
$$

For $i\ne j$, estimate the transition intensity by

$$
\widehat\lambda_{ij}=\frac{M_{ij}}{N_i},
\qquad
\widehat\Lambda_{ii}=-\sum_{j\ne i}\widehat\lambda_{ij}.
$$

The estimated generator, in annual units, is

$$
\boxed{
\widehat\Lambda=
\begin{pmatrix}
-\frac{36}{235}&\frac{36}{235}&0&0\\[3pt]
\frac{24}{233}&-\frac{48}{233}&\frac{24}{233}&0\\[3pt]
0&\frac{24}{243}&-\frac{60}{243}&\frac{36}{243}\\[3pt]
0&0&0&0
\end{pmatrix}.}
$$

Numerically,

$$
\widehat\Lambda\approx
\begin{pmatrix}
-0.15319149&0.15319149&0&0\\
0.10300429&-0.20600858&0.10300429&0\\
0&0.09876543&-0.24691358&0.14814815\\
0&0&0&0
\end{pmatrix}.
$$

The one-year transition matrix is the **matrix exponential** $\exp(\widehat\Lambda\times1)$, not the elementwise exponential. Evaluating it using the exact fractions gives

$$
\boxed{
\widehat P_{\mathrm{gen}}\approx
\begin{pmatrix}
0.86463112&0.12857177&0.00646155&0.00033556\\
0.08645026&0.82446825&0.08249711&0.00658438\\
0.00416588&0.07910217&0.78524551&0.13148645\\
0&0&0&1
\end{pmatrix}.}
$$

**Checks.** Each generator row sums to zero. The transition matrix is nonnegative, its rows sum to one up to rounding, and default remains absorbing. The generator model allows multiple transitions within a year, so it can assign a positive A-to-C probability even without an observed direct A-to-C transition.

As a further check, the total time spent in default is

$$
N_D=\frac5{12}+2\times\frac2{12}=\frac9{12},
\qquad
N_A+N_B+N_C+N_D=60\text{ firm-years}.
$$

### 中文解答

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_完整解答_含推导与计算.md|项目已有 GPT 中文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_完整解答_含推导与计算.pdf#page=1|中文 PDF]]。

状态顺序统一取为 $(A,B,C,D)$，其中 $D$ 是违约吸收态。按照讲义同类例题，题目中的“十个月后”解释为**从年初起第10个月**。

#### 1. 经验估计

按每家公司年初和年末的评级计数，而不是按年末各评级的总公司数计算。题目明确迁入 $A,C$ 的原 $B$ 类公司此后不再迁移。

| 年初评级 | 年末A | 年末B | 年末C | 年末D | 年初总数 |
|:---:|---:|---:|---:|---:|---:|
| A | 17 | 3 | 0 | 0 | 20 |
| B | 2 | 16 | 2 | 0 | 20 |
| C | 0 | 2 | 15 | 3 | 20 |

故经验估计为

$$
\boxed{
\widehat P_{\mathrm{emp}}=
\begin{pmatrix}
0.85&0.15&0&0\\
0.10&0.80&0.10&0\\
0&0.10&0.75&0.15\\
0&0&0&1
\end{pmatrix}.}
$$

最后一行由“违约后保持违约”的吸收态假设确定。

#### 2. 各评级累计停留时间

设 $N_i$ 为全部公司在评级 $i$ 的累计停留时间，单位为**公司·年**。迁入某评级的公司也要计入其迁入后的停留时间。

$$
\begin{aligned}
N_A
&=17\times1+3\times\frac3{12}+2\times\frac{11}{12}
=\frac{235}{12},\\[4pt]
N_B
&=16\times1+4\times\frac1{12}
+3\times\frac9{12}+2\times\frac5{12}
=\frac{233}{12},\\[4pt]
N_C
&=15\times1+3\times\frac7{12}
+2\times\frac{10}{12}+2\times\frac{11}{12}
=\frac{243}{12}.
\end{aligned}
$$

例如 $N_C$ 中：15家公司全年留在C；3家公司在第7个月离开C（2家转B、1家违约）；2家公司在第10个月违约；另有2家从B于第1个月迁入，留在C共11个月。



#### 3. 生成矩阵估计

设 $M_{ij}$ 是一年内从 $i$ 到 $j$ 的迁移次数。非零计数为

$$
M_{AB}=3,\quad M_{BA}=2,\quad M_{BC}=2,
\quad M_{CB}=2,\quad M_{CD}=3.
$$

对于 $i\ne j$，生成矩阵的估计量为

$$
\widehat\lambda_{ij}=\frac{M_{ij}}{N_i},
\qquad
\widehat\Lambda_{ii}=-\sum_{j\ne i}\widehat\lambda_{ij}.
$$

因此，按年计的生成矩阵为

$$
\boxed{
\widehat\Lambda=
\begin{pmatrix}
-\frac{36}{235}&\frac{36}{235}&0&0\\[3pt]
\frac{24}{233}&-\frac{48}{233}&\frac{24}{233}&0\\[3pt]
0&\frac{24}{243}&-\frac{60}{243}&\frac{36}{243}\\[3pt]
0&0&0&0
\end{pmatrix}.}
$$

其数值形式为

$$
\widehat\Lambda\approx
\begin{pmatrix}
-0.15319149&0.15319149&0&0\\
0.10300429&-0.20600858&0.10300429&0\\
0&0.09876543&-0.24691358&0.14814815\\
0&0&0&0
\end{pmatrix}.
$$

一年转移矩阵为**矩阵指数** $\exp(\widehat\Lambda\times1)$，不是对每个元素分别取指数。计算时使用上面的精确分数，得到

$$
\boxed{
\widehat P_{\mathrm{gen}}\approx
\begin{pmatrix}
0.86463112&0.12857177&0.00646155&0.00033556\\
0.08645026&0.82446825&0.08249711&0.00658438\\
0.00416588&0.07910217&0.78524551&0.13148645\\
0&0&0&1
\end{pmatrix}.}
$$

**检查：**生成矩阵每行之和为0；转移矩阵元素非负，每行之和为1（显示值有舍入误差）；违约状态保持为吸收态。生成矩阵法允许一年内发生多次迁移，因此即使样本没有直接出现A到C的迁移，估计的该项概率也可以为正。

另一个时间核对：违约状态的累计停留时间为

$$
N_D=\frac5{12}+2\times\frac2{12}=\frac9{12},
\qquad
N_A+N_B+N_C+N_D=60\text{ 公司·年}.
$$

---

## 第2题｜分段隐含违约参数

### 英文原题

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_作业题目_共3题_截止2026-09-25.pdf#page=1|题目 PDF p.1]]。

Q2. A company has issued 3- and 5-year bonds with a coupon payment of 4.1% per year payable annually. The yields on the bonds (in terms of continuous compounding) are 4.6% and 4.75%, respectively. Assume the risk-free rate is 2.5% for all maturities, and the recovery value is 40% of the par value. Also assume default can only take place halfway through each year, i.e. at year 0.5, 1.5, 2.5, etc. Compute $P_1$ and $P_2$, which are the implied default intensities per year for years 1 to 3 and for years 4 and 5, respectively.

### 教师英文答案

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment01_sol_老师给的.pdf#page=3|教师 Suggested Solutions，PDF pp.3–4]]。

Solution.

For 3 years:

| Time (Years) | Default Intensity (per year) | Recovery Value (\$) | Risk-Free Value (\$) | Loss Given Default (\$) | Discount Factor | PV of Expected Loss (\$) |
|---:|:---:|---:|---:|---:|---:|---:|
| 0.5 | $P_1$ | 40 | 105.7911 | 65.7911 | 0.9876 | $64.9738P_1$ |
| 1.5 | $P_1$ | 40 | 104.3176 | 64.3176 | 0.9632 | $61.9504P_1$ |
| 2.5 | $P_1$ | 40 | 102.8068 | 62.8068 | 0.9394 | $59.0016P_1$ |
| | | | | | Total: | $185.9257P_1$ |

Since the yield is 4.6% the corporate bond price is

$$
4.1e^{-0.046*1}+4.1e^{-0.046*2}+104.1e^{-0.046*3}=98.3367.
$$

Similarly, the default-free bond price is

$$
4.1e^{-0.025*1}+4.1e^{-0.025*2}+104.1e^{-0.025*3}=104.4769.
$$

Setting the difference between the corporate bond and default-free bond equal to the PV of the expected loss yields

$$
101.2257-98.3462=185.9257P_1,
$$

> [!warning] 教师原稿此处存在印刷错误（整理时核对）
> 上式按原 PDF p.3 照录，但它与同页刚算出的两项债价不一致，也不能推出下方 $3.3025\%$。根据该页数据，应使用 $104.4769-98.3367=185.9257P_1$。下方 GPT 英文详解与中文解答采用未舍入的正确债价；此旁注是整理核对，不是老师亲自发布的勘误。

i.e. the implied default intensity (or implied one-year default probability given no default yet) is

$$
P_1=3.3025\%.
$$

For 5 years:

| Time (Years) | Default Intensity (per year) | Recovery Value (\$) | Risk-Free Value (\$) | Loss Given Default (\$) | Discount Factor | PV of Expected Loss (\$) |
|---:|:---:|---:|---:|---:|---:|---:|
| 0.5 | $P_1$ | 40 | 108.6297 | 68.6297 | 0.9876 | $67.7772P_1$ |
| 1.5 | $P_1$ | 40 | 107.2281 | 67.2281 | 0.9632 | $64.7538P_1$ |
| 2.5 | $P_1$ | 40 | 105.7911 | 65.7911 | 0.9394 | $61.8050P_1$ |
| 3.5 | $P_2$ | 40 | 104.3176 | 64.3176 | 0.9162 | $58.9290P_2$ |
| 4.5 | $P_2$ | 40 | 102.8068 | 62.8068 | 0.8936 | $56.1240P_2$ |
| | | | | | Total: | $194.3360P_1+115.0530P_2$ |

Now since the yield is 4.75% the corporate bond price is

$$
\begin{aligned}
&4.1e^{-0.0475*1}+4.1e^{-0.0475*2}+4.1e^{-0.0475*3}\\
&\quad+4.1e^{-0.0475*4}+104.1e^{-0.0475*5}=96.6772.
\end{aligned}
$$

Similarly, the default-free bond price is

$$
\begin{aligned}
&4.1e^{-0.025*1}+4.1e^{-0.025*2}+4.1e^{-0.025*3}\\
&\quad+4.1e^{-0.025*4}+104.1e^{-0.025*5}=107.2803.
\end{aligned}
$$

Setting the difference between the corporate bond and default-free bond equal to the PV of the expected loss yields

$$
107.2803-96.6772=194.3360P_1+115.0530P_2,
$$

i.e. the implied default intensity (or implied one-year default probability given no default yet) is

$$
P_2=3.6376\%.
$$

### GPT 英文详解

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_Complete_Solutions_EN.md|项目已有 GPT 英文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_Complete_Solutions_EN.pdf#page=3|英文 PDF]]。

Use the **linear expected-loss approximation** in Lecture 1: match the price difference between a risk-free bond and a corporate bond to weighted discounted default losses. Let $P_1$ apply to years 1–3 and $P_2$ to years 4–5. These are annual default weights under the lecture convention, not exact continuous-time hazard rates.

Take face value 100, annual coupon $c=4.1$, recovery amount $R=40$, and continuously compounded risk-free rate $r=0.025$. Scaling all cash flows by the same factor does not change the estimated parameters.

#### 1. Three-year bond: estimate $P_1$

Using the quoted continuously compounded yield, the corporate bond price is

$$
\begin{aligned}
B_3
&=4.1e^{-0.046}+4.1e^{-0.046\times2}
+104.1e^{-0.046\times3}\\
&=98.33667697.
\end{aligned}
$$

The price of the risk-free bond with identical promised cash flows is

$$
\begin{aligned}
B_3^{\mathrm{rf}}
&=4.1e^{-0.025}+4.1e^{-0.025\times2}
+104.1e^{-0.025\times3}\\
&=104.47690821.
\end{aligned}
$$

Let $V_n^{\mathrm{rf}}(t)$ be the time-$t$ risk-free value of the remaining promised payments of the $n$-year bond. The default loss discounted to time zero is

$$
L_n(t)=\bigl[V_n^{\mathrm{rf}}(t)-40\bigr]e^{-0.025t}.
$$

| Default time $t$ | $V_3^{\mathrm{rf}}(t)$ | Loss | Discount factor | $L_3(t)$ |
|---:|---:|---:|---:|---:|
| 0.5 | 105.791066 | 65.791066 | 0.987578 | 64.973796 |
| 1.5 | 104.317608 | 64.317608 | 0.963194 | 61.950361 |
| 2.5 | 102.806849 | 62.806849 | 0.939413 | 59.001574 |

For example, at $t=0.5$, the remaining payments are due at years 1, 2, and 3:

$$
V_3^{\mathrm{rf}}(0.5)
=4.1e^{-0.025\times0.5}+4.1e^{-0.025\times1.5}
+104.1e^{-0.025\times2.5}.
$$

Matching the price difference to expected losses gives

$$
104.47690821-98.33667697=185.92573146P_1.
$$

Hence,

$$
\boxed{P_1=0.03302518263\approx3.3025\%\text{ per year}.}
$$



#### 2. Five-year bond: estimate $P_2$ for years 4–5

The corporate and risk-free bond prices are

$$
\begin{aligned}
B_5
&=4.1\sum_{k=1}^{4}e^{-0.0475k}+104.1e^{-0.0475\times5}
=96.67716974,\\[3pt]
B_5^{\mathrm{rf}}
&=4.1\sum_{k=1}^{4}e^{-0.025k}+104.1e^{-0.025\times5}
=107.28032055.
\end{aligned}
$$

The discounted losses at the possible default dates are as follows.

| Time $t$ | $V_5^{\mathrm{rf}}(t)$ | Loss | Discount factor | $L_5(t)$ | Weight |
|---:|---:|---:|---:|---:|:---:|
| 0.5 | 108.629741 | 68.629741 | 0.987578 | 67.777209 | $P_1$ |
| 1.5 | 107.228144 | 67.228144 | 0.963194 | 64.753773 | $P_1$ |
| 2.5 | 105.791066 | 65.791066 | 0.939413 | 61.804987 | $P_1$ |
| 3.5 | 104.317608 | 64.317608 | 0.916219 | 58.929006 | $P_2$ |
| 4.5 | 102.806849 | 62.806849 | 0.893597 | 56.124034 | $P_2$ |

The sum of discounted loss coefficients for years 1–3 is

$$
67.77720853+64.75377320+61.80498675=194.33596848.
$$

For years 4–5, the sum is

$$
58.92900611+56.12403367=115.05303978.
$$

The five-year valuation must use the previously estimated $P_1$ together with the unknown $P_2$:

$$
107.28032055-96.67716974
=194.33596848P_1+115.05303978P_2.
$$

Substituting $P_1=0.03302518263$ gives

$$
\begin{aligned}
P_2
&=\frac{10.60315080-194.33596848\times0.03302518263}
{115.05303978}\\[4pt]
&=0.03637600501.
\end{aligned}
$$

Thus, under the lecture's linear approximation,

$$
\boxed{P_1\approx3.3025\%\text{ per year},
\qquad P_2\approx3.6376\%\text{ per year}.}
$$

**Check and interpretation.** Substituting the unrounded estimates reproduces expected losses of 6.14023124 and 10.60315080, equal to the respective bond price differences. Since $P_2$ applies only to years 4–5, it cannot be obtained by dividing the five-year price difference by the sum of all five loss coefficients.

### 中文解答

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_完整解答_含推导与计算.md|项目已有 GPT 中文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_完整解答_含推导与计算.pdf#page=3|中文 PDF]]。

本题沿用Lecture 1的**预期损失线性近似**：用无风险债与公司债的价格差，匹配各年折现违约损失的加权和。$P_1$ 对应前3年，$P_2$ 对应第4—5年；它们采用讲义的年度违约权重口径，不等同于严格连续时间模型中的精确强度。

取面值100，年票息 $c=4.1$，回收金额 $R=40$，无风险连续复利利率 $r=0.025$。按任意相同面值缩放都不影响最终参数。

#### 1. 三年期债券：先求 $P_1$

根据给定的连续复利到期收益率，当前公司债价格为

$$
\begin{aligned}
B_3
&=4.1e^{-0.046}+4.1e^{-0.046\times2}
+104.1e^{-0.046\times3}\\
&=98.33667697.
\end{aligned}
$$

相同现金流对应的无风险债价格为

$$
\begin{aligned}
B_3^{\mathrm{rf}}
&=4.1e^{-0.025}+4.1e^{-0.025\times2}
+104.1e^{-0.025\times3}\\
&=104.47690821.
\end{aligned}
$$

在违约时点 $t$，令 $V_n^{\mathrm{rf}}(t)$ 为剩余承诺现金流按无风险利率折现到 $t$ 的价值。违约损失折现到年初为

$$
L_n(t)=\bigl[V_n^{\mathrm{rf}}(t)-40\bigr]e^{-0.025t}.
$$

| 违约时点 $t$ | $V_3^{\mathrm{rf}}(t)$ | 损失 $V_3^{\mathrm{rf}}(t)-40$ | 折现因子 | $L_3(t)$ |
|---:|---:|---:|---:|---:|
| 0.5 | 105.791066 | 65.791066 | 0.987578 | 64.973796 |
| 1.5 | 104.317608 | 64.317608 | 0.963194 | 61.950361 |
| 2.5 | 102.806849 | 62.806849 | 0.939413 | 59.001574 |

例如，$t=0.5$时，后续票息仍在第1、2、3年支付，因此

$$
V_3^{\mathrm{rf}}(0.5)
=4.1e^{-0.025\times0.5}+4.1e^{-0.025\times1.5}
+104.1e^{-0.025\times2.5}.
$$

建立价格差与预期损失的关系：

$$
104.47690821-98.33667697=185.92573146P_1.
$$

从而

$$
\boxed{P_1=0.03302518263\approx3.3025\%\text{／年}.}
$$



#### 2. 五年期债券：再求第4—5年的 $P_2$

公司债与无风险债价格分别为

$$
\begin{aligned}
B_5
&=4.1\sum_{k=1}^{4}e^{-0.0475k}+104.1e^{-0.0475\times5}
=96.67716974,\\[3pt]
B_5^{\mathrm{rf}}
&=4.1\sum_{k=1}^{4}e^{-0.025k}+104.1e^{-0.025\times5}
=107.28032055.
\end{aligned}
$$

各违约时点对应的损失为

| 时点 $t$ | $V_5^{\mathrm{rf}}(t)$ | 损失 | 折现因子 | $L_5(t)$ | 权重 |
|---:|---:|---:|---:|---:|:---:|
| 0.5 | 108.629741 | 68.629741 | 0.987578 | 67.777209 | $P_1$ |
| 1.5 | 107.228144 | 67.228144 | 0.963194 | 64.753773 | $P_1$ |
| 2.5 | 105.791066 | 65.791066 | 0.939413 | 61.804987 | $P_1$ |
| 3.5 | 104.317608 | 64.317608 | 0.916219 | 58.929006 | $P_2$ |
| 4.5 | 102.806849 | 62.806849 | 0.893597 | 56.124034 | $P_2$ |

前3年的折现损失系数之和为

$$
67.77720853+64.75377320+61.80498675=194.33596848.
$$

第4—5年的折现损失系数之和为

$$
58.92900611+56.12403367=115.05303978.
$$

五年期债券必须同时使用已求出的 $P_1$ 和未知的 $P_2$：

$$
107.28032055-96.67716974
=194.33596848P_1+115.05303978P_2.
$$

代入 $P_1=0.03302518263$，得到

$$
\begin{aligned}
P_2
&=\frac{10.60315080-194.33596848\times0.03302518263}
{115.05303978}\\[4pt]
&=0.03637600501.
\end{aligned}
$$

因此，本题在讲义线性近似下的答案是

$$
\boxed{P_1\approx3.3025\%\text{／年},
\qquad P_2\approx3.6376\%\text{／年}.}
$$

**检查与解释：**用未舍入的参数回代，两种期限的预期损失分别为6.14023124和10.60315080，与债券价格差一致。$P_2$ 只代表第4—5年，不能用五年全部损失系数直接去除五年债的价格差。

---

## 第3题｜GBM 下的税盾与破产成本

### 英文原题

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_作业题目_共3题_截止2026-09-25.pdf#page=1|题目 PDF p.1]]。

Q3. Compute (1) and (2) in Lecture 2 under the Black-Scholes-Merton geometric Brownian motion model.

### 教师英文答案

> [!info] 当前教师答案文件未提供本题解答
> 教师 Suggested Solutions 共4页，只包含 Q1 和 Q2；没有 Q3。以下英文与中文解答来自项目已有的 GPT 生成稿，不标作教师答案。

### GPT 英文详解

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_Complete_Solutions_EN.md|项目已有 GPT 英文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_Complete_Solutions_EN.pdf#page=5|英文 PDF]]。

Equations (1) and (2) on page 4 of Lecture 2 are

$$
A(0)=E^*\!\left[e^{-rT}\kappa D\,\mathbf1_{\{V_T\ge D\}}\right],
$$

$$
C(0)=E^*\!\left[e^{-rT}(1-\alpha)V_T\,\mathbf1_{\{V_T<D\}}\right].
$$

Here $D$ is the face value of debt, $\kappa$ is the tax-credit coefficient, and $\alpha$ is the fraction of asset value retained upon default. Under the risk-neutral measure, the assignment appendix specifies

$$
dV_t=rV_t\,dt+\sigma V_t\,dW_t,\qquad V_0=1.
$$

Assume $T>0$, $D>0$, and $\sigma>0$. Let $\Phi$ denote the standard normal cumulative distribution function.

#### 1. Distribution of $\ln V_T$

For $f(v)=\ln v$, we have $f'(v)=1/v$ and $f''(v)=-1/v^2$. Itô's lemma gives

$$
\begin{aligned}
d\ln V_t
&=\frac1{V_t}(rV_t\,dt+\sigma V_t\,dW_t)
+\frac12\left(-\frac1{V_t^2}\right)\sigma^2V_t^2\,dt\\
&=\left(r-\frac12\sigma^2\right)dt+\sigma\,dW_t.
\end{aligned}
$$

Integrating and using $V_0=1$ yields

$$
\ln V_T=\left(r-\frac12\sigma^2\right)T+\sigma W_T.
$$

Since $W_T\sim N(0,T)$,

$$
\ln V_T\sim N\!\left(\left(r-\frac12\sigma^2\right)T,\sigma^2T\right).
$$

#### 2. Tax credit $A(0)$

Define

$$
d_2=\frac{-\ln D+(r-\frac12\sigma^2)T}{\sigma\sqrt T},
\qquad d_1=d_2+\sigma\sqrt T.
$$

Using $E^*[\mathbf1_E]=P^*(E)$ and

$$
P^*(V_T<D)
=\Phi\!\left(\frac{\ln D-(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right)
=\Phi(-d_2),
$$

we obtain

$$
\boxed{A(0)=\kappa D e^{-rT}\Phi(d_2).}
$$

This is the tax credit multiplied by the probability of survival to maturity, discounted to time zero.



#### 3. Bankruptcy cost $C(0)$

Bankruptcy cost depends on asset value at default. We therefore need the **truncated expectation** $E^*[V_T\mathbf1_{\{V_T<D\}}]$; the random variable $V_T$ cannot simply be taken outside the expectation.

Write

$$
m=\left(r-\frac12\sigma^2\right)T,\qquad
s=\sigma\sqrt T,\qquad \ln V_T=m+sZ,\quad Z\sim N(0,1).
$$

The default event is equivalent to $Z<h$, where $h=(\ln D-m)/s=-d_2$. Thus,

$$
\begin{aligned}
E^*[V_T\mathbf1_{\{V_T<D\}}]
&=\int_{-\infty}^{h}e^{m+sz}\frac1{\sqrt{2\pi}}e^{-z^2/2}\,dz\\
&=e^{m+s^2/2}\int_{-\infty}^{h}
\frac1{\sqrt{2\pi}}e^{-(z-s)^2/2}\,dz\\
&=e^{m+s^2/2}\Phi(h-s)\\
&=e^{rT}\Phi(-d_1).
\end{aligned}
$$

The second equality follows by completing the square:

$$
 m+sz-\frac{z^2}{2}
=m+\frac{s^2}{2}-\frac{(z-s)^2}{2}.
$$

Consequently,

$$
\boxed{C(0)=e^{-rT}(1-\alpha)e^{rT}\Phi(-d_1)
=(1-\alpha)\Phi(-d_1).}
$$

**Final results for the specified initial value $V_0=1$:**

$$
\boxed{
\begin{aligned}
A(0)&=\kappa D e^{-rT}
\Phi\!\left(\frac{-\ln D+(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right),\\[6pt]
C(0)&=(1-\alpha)
\Phi\!\left(\frac{\ln D-(r+\frac12\sigma^2)T}{\sigma\sqrt T}\right).
\end{aligned}}
$$

For a general initial value $V_0>0$, the corresponding formulas are

$$
d_{1,2}=\frac{\ln(V_0/D)+(r\pm\frac12\sigma^2)T}{\sigma\sqrt T},
\quad A(0)=\kappa D e^{-rT}\Phi(d_2),
\quad C(0)=(1-\alpha)V_0\Phi(-d_1).
$$

Use the plus sign for $d_1$ and the minus sign for $d_2$. Since the lognormal distribution is continuous, $P^*(V_T=D)=0$; strict and non-strict inequalities therefore give the same expectations here.

**Sources:** Lecture 1, pp. 6–9 and 13–14; Lecture 2, p. 4, and both supplementary derivations. All inputs follow Assignment 1. The companion *Conventions and Errata* explains the approximation in Q2 and the relevant typographical issues.

### 中文解答

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_完整解答_含推导与计算.md|项目已有 GPT 中文源稿]]；配套排版版：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_完整解答_含推导与计算.pdf#page=5|中文 PDF]]。

Lecture 2第4页的式(1)、式(2)为

$$
A(0)=E^*\!\left[e^{-rT}\kappa D\,\mathbf1_{\{V_T\ge D\}}\right],
$$

$$
C(0)=E^*\!\left[e^{-rT}(1-\alpha)V_T\,\mathbf1_{\{V_T<D\}}\right].
$$

这里 $D$ 为债务面值，$\kappa$ 为税盾系数，$\alpha$ 为违约时保留下来的资产比例。按题目附录，在风险中性测度下

$$
dV_t=rV_t\,dt+\sigma V_t\,dW_t,\qquad V_0=1.
$$

假设 $T>0$、$D>0$、$\sigma>0$；$\Phi$ 表示标准正态分布函数。

#### 1. 求 $\ln V_T$ 的分布

取 $f(v)=\ln v$，则 $f'(v)=1/v$，$f''(v)=-1/v^2$。由Ito引理，

$$
\begin{aligned}
d\ln V_t
&=\frac1{V_t}(rV_t\,dt+\sigma V_t\,dW_t)
+\frac12\left(-\frac1{V_t^2}\right)\sigma^2V_t^2\,dt\\
&=\left(r-\frac12\sigma^2\right)dt+\sigma\,dW_t.
\end{aligned}
$$

由于 $V_0=1$，积分后有

$$
\ln V_T=\left(r-\frac12\sigma^2\right)T+\sigma W_T.
$$

由 $W_T\sim N(0,T)$，可得

$$
\ln V_T\sim N\!\left(\left(r-\frac12\sigma^2\right)T,\sigma^2T\right).
$$

#### 2. 税盾 $A(0)$

定义

$$
d_2=\frac{-\ln D+(r-\frac12\sigma^2)T}{\sigma\sqrt T},
\qquad d_1=d_2+\sigma\sqrt T.
$$

因为 $E^*[\mathbf1_E]=P^*(E)$，且

$$
P^*(V_T<D)
=\Phi\!\left(\frac{\ln D-(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right)
=\Phi(-d_2),
$$

所以

$$
\boxed{A(0)=\kappa D e^{-rT}\Phi(d_2).}
$$

即：税盾金额乘以到期不违约概率，再折现到时点0。



#### 3. 破产成本 $C(0)$

破产成本取决于违约时的资产价值，因此需要求**截断期望** $E^*[V_T\mathbf1_{\{V_T<D\}}]$，不能直接把 $V_T$ 从期望中提出。

记

$$
m=\left(r-\frac12\sigma^2\right)T,\qquad
s=\sigma\sqrt T,\qquad \ln V_T=m+sZ,\quad Z\sim N(0,1).
$$

违约条件等价于 $Z<h$，其中 $h=(\ln D-m)/s=-d_2$。因此

$$
\begin{aligned}
E^*[V_T\mathbf1_{\{V_T<D\}}]
&=\int_{-\infty}^{h}e^{m+sz}\frac1{\sqrt{2\pi}}e^{-z^2/2}\,dz\\
&=e^{m+s^2/2}\int_{-\infty}^{h}
\frac1{\sqrt{2\pi}}e^{-(z-s)^2/2}\,dz\\
&=e^{m+s^2/2}\Phi(h-s)\\
&=e^{rT}\Phi(-d_1).
\end{aligned}
$$

第二步使用配方恒等式

$$
 m+sz-\frac{z^2}{2}
=m+\frac{s^2}{2}-\frac{(z-s)^2}{2}.
$$

于是

$$
\boxed{C(0)=e^{-rT}(1-\alpha)e^{rT}\Phi(-d_1)
=(1-\alpha)\Phi(-d_1).}
$$

**按题目 $V_0=1$ 的最终结果：**

$$
\boxed{
\begin{aligned}
A(0)&=\kappa D e^{-rT}
\Phi\!\left(\frac{-\ln D+(r-\frac12\sigma^2)T}{\sigma\sqrt T}\right),\\[6pt]
C(0)&=(1-\alpha)
\Phi\!\left(\frac{\ln D-(r+\frac12\sigma^2)T}{\sigma\sqrt T}\right).
\end{aligned}}
$$

若保留一般初值 $V_0>0$，则

$$
d_{1,2}=\frac{\ln(V_0/D)+(r\pm\frac12\sigma^2)T}{\sigma\sqrt T},
\quad A(0)=\kappa D e^{-rT}\Phi(d_2),
\quad C(0)=(1-\alpha)V_0\Phi(-d_1).
$$

这里 $d_1$ 取加号、$d_2$ 取减号。对数正态分布连续，$V_T=D$ 的概率为0，因此本题中严格或非严格的不等号不影响期望结果。

**资料依据：**Lecture 1第6—9、13—14页；Lecture 2第4页及两版补充推导。数据以作业为准；计算口径和印刷问题见同目录的《口径与讲义勘误说明》。

---

## 原题附录｜Itô 引理与对数正态分布

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_作业题目_共3题_截止2026-09-25.pdf#page=2|题目 PDF p.2]]。以下是原题提供的工具，不是新增题目。

### A　Itô Lemma

In its simplest form, Itô lemma states the following: for an Itô drift-diffusion process

$$
dX_t=\mu_tdt+\sigma_tdW_t,
$$

and any twice differentiable scalar function $f(t,x)$ of two real variables $t$ and $x$, one has

$$
df(t,X_t)=\left(\frac{\partial f}{\partial t}+\mu_t\frac{\partial f}{\partial x}+\frac{\sigma_t^2}{2}\frac{\partial^2f}{\partial x^2}\right)dt+\sigma_t\frac{\partial f}{\partial x}dW_t.\tag{A.1}
$$

### B　Density of Log-normal Process $V(\cdot)$

Consider the following stochastic differential equation

$$
\begin{cases}
dV_t=rV_tdt+\sigma V_tdW_t,\\
V_0=1,
\end{cases}\tag{B.1}
$$

where $r$ and $\sigma$ are constant.

Then

$$
\ln V_T\sim N\!\left(\left(r-\frac12\sigma^2\right)T,\sigma^2T\right).\tag{B.2}
$$

> [!note] 中文阅读提示
> 附录 A 用于对 $\ln V_t$ 应用 Itô 引理；附录 B 给出 $V_0=1$ 时的终值分布。第3题中文解答已把这两步连同税盾、破产成本的计算展开。

## 课程回链

- [[AMA572 Fixed-Income and Credit Risk/Lecture 1/01 - Lecture 1（英文原文与折叠译文）|Lecture 1]]
- [[AMA572 Fixed-Income and Credit Risk/Lecture 2/00 - Lecture 2 资料索引|Lecture 2]]
