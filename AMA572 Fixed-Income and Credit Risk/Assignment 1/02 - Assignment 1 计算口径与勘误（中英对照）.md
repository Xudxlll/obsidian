---
course: AMA572 Fixed-Income and Credit Risk
created: 2026-10-22
type: 既有计算口径与勘误
assignment: 1
cssclasses:
  - ama-inline-translations
tags:
  - AMA572
  - Assignment
---

# Assignment 1｜计算口径与勘误（中英对照）

[[AMA572 Fixed-Income and Credit Risk/Assignment 1/01 - Assignment 1（英文原题、答案与中文解答）|返回逐题笔记]]

> [!info] 来源说明
> 以下完整保留项目已有的英文、中文勘误稿，属于 GPT 整理说明，不是教师发布的勘误。文中“同目录”指原项目目录；所提到的解答与源稿在本笔记目录的附件中。文末“数值核验”是原稿记录的核验，不表示本次重新执行了其全部检查。
> 本次另发现的 Assignment 1 教师答案 p.3 价格差笔误，已标在逐题笔记第2题旁，不与原稿提到的 Lecture 1 课内练习笔误混为一处。

## English original

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_Conventions_and_Errata_EN.md|Assignment1_Conventions_and_Errata_EN.md]]。

### Assignment 1: Conventions and Errata

This note explains the differences between the complete solutions and the supplied course materials. Full derivations and answers are provided in **Assignment1_Complete_Solutions_EN.pdf** in the same folder.

#### 1. Q1: Assignment data versus the lecture exercise

In the assignment, two firms move from B to C and three move from A to B. In the lecture exercise, the corresponding counts are one and one. The exposure times, generator matrix, and transition matrix in the old exercise solution therefore cannot be copied directly.

Following the example and calculations in Lecture 1, “ten months later” is interpreted as **month 10 from the beginning of the year**, not ten months after month 7.

#### 2. Q2: The lecture's linear expected-loss convention

The lecture tables multiply each year's discounted loss by an annual default parameter and then sum these terms. The main solution follows this convention: the three-year bond determines the parameter for years 1–3, and the five-year bond determines the parameter for years 4–5:

$$
P_1=3.302518263\%,\qquad P_2=3.637600501\%.
$$

In this linear expression, $P_1$ and $P_2$ are annual default-event probability weights. The lecture also describes them as default intensities or conditional default probabilities. A strictly conditional interpretation, however, requires survival probabilities for preceding years. A continuous-time intensity interpretation additionally requires a specified continuous-time default model. The main solution preserves the lecture convention and explicitly labels the approximation.

##### Alternative: exact annual conditional default probabilities

The following illustrates the effect of a different convention. These parameters should not be mixed with the linear weights in the main solution.

Let $q_1$ be the annual conditional default probability in years 1–3 and $q_2$ the corresponding probability in years 4–5. Continue to place each year's default cash flow at midyear, as specified in the assignment. The unconditional default probabilities in years 1–3 are

$$
q_1,\quad(1-q_1)q_1,\quad(1-q_1)^2q_1,
$$

and those in years 4–5 are

$$
(1-q_1)^3q_2,\quad(1-q_1)^3(1-q_2)q_2.
$$

Weighting the discounted loss coefficients $L_n(j-0.5)$ by these probabilities and solving first for the three-year bond and then for the five-year bond gives

$$
q_1\approx3.414070146\%,\qquad q_2\approx4.120247608\%.
$$

The constant intensities with the same one-year survival probabilities are $-\ln(1-q_i)$: approximately 3.473710906% and 4.207535890% per year. This is only a conversion of one-year survival probabilities; it does not replace the midyear-default valuation model with a continuous-default model.



#### 3. Typographical issues in the lecture exercise solution

The following points were checked against the rendered pages 3–4 of the Lecture 1 exercise solution, including its handwritten annotations.

- The three-year loss table totals $178.4155P_1$, whereas the subsequent printed equation shows $78.4155P_1$. The handwritten annotation restores the leading 1. The printed result of 3.6721% uses the incorrect denominator and should not be carried over.
- The printed five-year table labels every year with $P_2$. The handwritten annotations change the first three rows to $P_1$. The main solution follows this correction: $P_1$ for years 1–3 and $P_2$ for years 4–5.
- The 1.5- and 2.5-year rows in that table contain ordering and numerical alignment issues. The main solution recalculates the remaining cash flows separately at each default date.
- The assignment changes the coupon and interest-rate inputs. The solution uses the assignment's 4.1% coupon, 2.5% risk-free rate, and yields of 4.6% and 4.75%, rather than reusing the old table values.

#### 4. Q3: Integration limits and initial asset value

- When integrating over asset value $v$, the limits are $0$ and $D$.
- After substituting $x=\ln v$, the limits become $-\infty$ and $\ln D$; they cannot remain $0$ and $D$. Some intermediate expressions in the supplementary derivation do not update the limits consistently after substitution.
- In equation (16) on page 4 of the annotated supplement, a printed expression contains $\ln V_T$ where the default threshold requires $\ln D$. This is also corrected by hand.
- The assignment appendix specifies $V_0=1$. Thus the final expression for $C(0)$ contains no additional $V_0$ factor. For a general initial value, it is $(1-\alpha)V_0\Phi(-d_1)$.

#### 5. Numerical verification

- The Q1 matrix exponential was computed with SciPy and independently checked using uniformization: a Poisson-weighted sum of powers of a stochastic matrix. Nonnegativity, row sums, the absorbing state, and total exposure time were also checked.
- Substituting the unrounded Q2 parameters reproduces the three- and five-year bond price differences of 6.1402312377 and 10.6031508027, respectively.
- The Q3 tax-credit and bankruptcy-cost formulas agree with direct numerical integration of the standard normal density for three parameter sets, covering both $V_0=1$ and a general $V_0>0$.

## 中文原稿

来源：[[AMA572 Fixed-Income and Credit Risk/Assignment 1/附件/Assignment1_口径与讲义勘误说明.md|Assignment1_口径与讲义勘误说明.md]]。

### Assignment 1：计算口径与讲义勘误说明

本说明用于理解参考解答与课堂材料的差别。三道题的正式推导和答案见同目录《Assignment1_完整解答_含推导与计算.pdf》。

#### 1. 第一题：作业数据与课内练习不同

作业中，B→C为2家，A→B为3家；课内练习分别是1家、1家。因此原练习解答里的停留时间、生成矩阵和转移矩阵均不能直接复制。

题目“Ten months later”按Lecture 1同类例题及原解答的计算方式理解为“年初起第10个月”，而不是第7个月之后再过10个月。

#### 2. 第二题：正文采用讲义的线性预期损失法

课堂表格将每年折现违约损失直接乘以一个年度参数，再逐年相加。因此正文沿用该方法，用三年债先确定前3年的参数，再用五年债确定第4—5年的参数：

$$
P_1=3.302518263\%,\qquad P_2=3.637600501\%.
$$

严格来说，在这种线性表达中，$P_1,P_2$是每年违约事件的概率权重。讲义把它们称为“default intensity”或条件违约概率，但若解释为严格的条件违约概率，应加入之前各年的存活概率；若解释为连续时间强度，还需要进一步明确连续违约模型。正文保留讲义的计算口径，并标明近似。

##### 若采用严格的逐年条件违约概率，会得到另一组结果

这一节只是说明口径差别，不应将这里的参数与正文的线性权重混用。

令$q_1$为前3年每年的条件违约概率，$q_2$为第4—5年每年的条件违约概率，仍按题目要求把各年违约现金流集中在年中。则前3年各年的无条件违约概率为

$$
q_1,\quad(1-q_1)q_1,\quad(1-q_1)^2q_1,
$$

第4—5年为

$$
(1-q_1)^3q_2,\quad(1-q_1)^3(1-q_2)q_2.
$$

将正文中各年的折现损失系数$L_n(j-0.5)$分别乘以上述概率，先解三年债、再解五年债，得到

$$
q_1\approx3.414070146\%,\qquad q_2\approx4.120247608\%.
$$

其一年存活概率对应的等效常数强度为$-\ln(1-q_i)$，分别约为3.473710906%／年、4.207535890%／年。这只是对一年存活概率的等效转换，并未把“年中集中违约”的债券定价模型改成连续违约模型。

#### 3. 教师课内练习解答的印刷问题

已对照《Lecture 1课内练习解答》第3—4页的实际页面，而不只依赖文字提取。

- 三年债表格合计为$178.4155P_1$，后面的印刷方程却写成$78.4155P_1$；手写已补上首位1。印刷结果3.6721%对应错误分母，不能沿用。
- 五年债表格印刷版把各年全部标成$P_2$，手写已将前3行改为$P_1$。正确的分段计算应保留这一修改；正文按“前3年$P_1$、后2年$P_2$”处理。
- 五年债表格中的1.5、2.5年顺序及数值搭配有印刷错位；本解答按每个实际违约时点重新计算剩余现金流。
- 作业票息、无风险利率等数据与上述课内练习不同。本解答使用作业的4.1%票息、2.5%无风险利率、4.6%与4.75%的收益率，未复用旧表格数值。

#### 4. 第三题：积分上下限与初始资产值

- 以资产价值$v$积分时，上下限为$0$到$D$。
- 换元$x=\ln v$后，上下限应相应变为$-\infty$到$\ln D$，不能仍写$0$到$D$。补充推导的中间式有未同步换元上下限的地方。
- 含手写批注的补充材料第4页式(16)，印刷公式一处出现$\ln V_T$；计算违约阈值应使用$\ln D$，该处也有手写更正。
- 作业附录指定$V_0=1$。因此最终$C(0)$前不再另出现$V_0$；一般初值时则应为$(1-\alpha)V_0\Phi(-d_1)$。

#### 5. 数值核验

- Q1矩阵指数用SciPy计算，并用生成矩阵均匀化后的Poisson加权矩阵幂独立核对；检查了非负性、行和、吸收态和总停留时间。
- Q2用未舍入的参数回代，三年与五年债券的价格差分别恢复为6.1402312377、10.6031508027。
- Q3的税盾和破产成本公式，在三组参数下与标准正态密度的直接数值积分结果一致，包括$V_0=1$与一般$V_0>0$的情况。

