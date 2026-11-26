---
course: AMA572 Fixed-Income and Credit Risk
created: "2026-11-26"
source_type: 课堂原图还原（无原始 PDF）
cssclasses:
  - ama-inline-translations
---

# Lecture 9 · Hull–White 模型（原文还原、课堂手写推导与原图）

> [!info] 资料说明与阅读方式
> 截图顶部标签显示 `lec9 (1)`，内容为 Hull–White 模型的 SDE 与显式解（公式 (4)–(5)）及其退化为 Vasicek 模型的情形；本目录未提供独立的 Lecture 9 原 PDF，页码未显示，不补造缺失页。
> 下文先按 5 张截图（228–232）完整还原可见的**英文印刷原文与折叠中文译文**，再整理老师两轮板书的**完整手写推导**，并在末尾按原顺序完整保留各阶段课堂原图与逐图新增批注。
> [[AMA572 Fixed-Income and Credit Risk/Lecture 9/00 - Lecture 9 资料索引|资料索引]] · [[AMA572 Fixed-Income and Credit Risk/Assignment 3/01 - Assignment 3（英文原文与折叠译文）|Assignment 3 原题]] · [[AMA572 Fixed-Income and Credit Risk/课堂字幕/2026-11-19（带时间戳原文）|11.19 课堂字幕]]

## 印刷原文还原（据截图 228–232 合并）

Hull-White model assumes that, under the risk-neutral measure, the spot rate follows a stochastic differential equation <details class="translation-details"><summary>中文译文</summary><span class="translation-body">Hull–White 模型假设，在风险中性测度（risk-neutral measure）下，即期利率（spot rate）服从如下随机微分方程：</span></details>

$$
dr(t) = (\alpha(t) - \beta(t) r(t))\, dt + \sigma(t)\, dW(t), \tag{4}
$$

where $W(t)$ is a standard Brownian motion. Let <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中 W(t) 为标准布朗运动。令：</span></details>

$$
H(t) := \int_{0}^{t} \beta(u)\, du.
$$

Then, we have <details class="translation-details"><summary>中文译文</summary><span class="translation-body">于是我们有：</span></details>

$$
\begin{aligned}
d\left(e^{H(t)} r(t)\right) &= e^{H(t)} \beta(t) r(t)\, dt + e^{H(t)} dr(t) \\
&= e^{H(t)} \left(\beta(t) r(t)\, dt + dr(t)\right) \\
&= e^{H(t)} \left(\alpha(t)\, dt + \sigma(t)\, dW(t)\right),
\end{aligned}
$$

where (4) is used to derive the last equality. In other words, <details class="translation-details"><summary>中文译文</summary><span class="translation-body">其中最后一步等式用到了 (4)。换句话说：</span></details>

$$
e^{H(t)} r(t) = r(0) + \int_{0}^{t} e^{H(u)} \alpha(u)\, du + \int_{0}^{t} e^{H(u)} \sigma(u)\, dW(u).
$$

Thus, we have the solution to (4) is <details class="translation-details"><summary>中文译文</summary><span class="translation-body">因此，方程 (4) 的解为（注：原文 "Thus, we have the solution to (4) is" 照录）：</span></details>

$$
r(t) = e^{-H(t)} r(0) + \int_{0}^{t} e^{H(u) - H(t)} \alpha(u)\, du + \int_{0}^{t} e^{H(u) - H(t)} \sigma(u)\, dW(u). \tag{5}
$$

In particular, if the coefficients are not time varying, i.e. $\alpha(t) = \alpha$, $\beta(t) = \beta$, and $\sigma(t) = \sigma$, then Hull-White model degenerates to the *Vasicek model*, in which <details class="translation-details"><summary>中文译文</summary><span class="translation-body">特别地，如果系数不随时间变化，即 α(t) = α、β(t) = β 且 σ(t) = σ，则 Hull–White 模型退化为 Vasicek 模型，其中：</span></details>

$$
H(t) = \beta t
$$

and <details class="translation-details"><summary>中文译文</summary><span class="translation-body">并且：</span></details>

$$
r(t) = e^{-\beta t} r(0) + \alpha \int_{0}^{t} e^{-\beta(t-u)}\, du + \sigma \int_{0}^{t} e^{-\beta(t-u)}\, dW(u)
$$

> [!note] 截图边界说明
> 截图 228–230 最底端边缘可见上述 Vasicek 表达式下方还有下一行公式的极少量顶部笔画被截断（无法可靠辨认），其余段落与公式在 228–232 中均清晰完整。

---

## 课堂手写推导完整还原（两轮板书汇总）

老师围绕积分因子 $e^{H(t)}$ 分两轮在页面空白处逐步展开推导（第一轮 228–230，清屏后第二轮 231–232）：

1. **积分因子微分与常系数特例（截图 228）**
   $$
   H(t) := \int_{0}^{t} \beta(u)\, du \implies dH(t) = \beta(t)\, dt
   $$
   若 $\beta(u) \equiv \beta$ 为常数（Vasicek 特例），则：
   $$
   H(t) = \int_{0}^{t} \beta\, du = \beta t
   $$

2. **乘积法则展开与提公因式（截图 228–229）**
   对第一项展开：
   $$
   \begin{aligned}
   d\left(e^{H(t)}\right) r(t)
   &= e^{H(t)} dH(t)\, r(t) \\
   &= e^{H(t)} \beta(t)\, dt\, r(t) \\
   &= e^{H(t)} \beta(t) r(t)\, dt
   \end{aligned}
   $$
   结合第二项 $e^{H(t)} dr(t)$ 并提取公因式 $e^{H(t)}$：
   $$
   d\left(e^{H(t)} r(t)\right) = e^{H(t)} \beta(t) r(t)\, dt + e^{H(t)} dr(t) = e^{H(t)}\left(\beta(t) r(t)\, dt + dr(t)\right)
   $$

3. **代入 SDE (4) 抵消漂移项（截图 230）**
   $$
   \begin{aligned}
   \beta(t) r(t)\, dt + dr(t)
   &= \cancel{\beta(t) r(t)}\, dt + \left(\alpha(t) \cancel{- \beta(t) r(t)}\right) dt + \sigma(t)\, dW(t) \\
   &= \alpha(t)\, dt + \sigma(t)\, dW(t)
   \end{aligned}
   $$

4. **两边从 $0$ 到 $t$ 积分并计算初值项（截图 231）**
   计算 $t = 0$ 处的积分因子初值：
   $$
   H(0) = \int_{0}^{0} \beta(u)\, du = 0 \implies e^{H(0)} r(0) = e^{0} r(0) = r(0)
   $$
   两边将变量改写为哑变量 $u$ 并从 $0$ 积分到 $t$：
   $$
   \int_{0}^{t} d\left(e^{H(u)} r(u)\right) = e^{H(t)} r(t) - e^{H(0)} r(0) = e^{H(t)} r(t) - r(0)
   $$
   移项得到：
   $$
   e^{H(t)} r(t) = r(0) + \int_{0}^{t} e^{H(u)} \alpha(u)\, du + \int_{0}^{t} e^{H(u)} \sigma(u)\, dW(u)
   $$

5. **两边同乘 $e^{-H(t)}$ 得到显式解 (5)（截图 232）**
   $$
   r(t) = e^{-H(t)} r(0) + \int_{0}^{t} e^{H(u) - H(t)} \alpha(u)\, du + \int_{0}^{t} e^{H(u) - H(t)} \sigma(u)\, dW(u)
   $$

---

## 各阶段课堂原图与逐图批注记录

### 228 · Hull-White_积分因子定义

- **来源标注**：截图标签 `lec9 (1)`，公式 (4)–(5)；关联 Assignment 3 Q1(a)。来源收集包：11.19。
- **本图板书**：红笔在 $H(t)$ 左侧标注 $dH(t)=\beta(t)\,dt$，并在左侧空白处展开 $d(e^{H(t)})r(t)=e^{H(t)}dH(t)r(t)=e^{H(t)}\beta(t)\,dt\,r(t)=e^{H(t)}\beta(t)r(t)\,dt$；蓝笔在 $H(t)$ 右侧补写常系数特例 $=\int_0^t \beta\,du = \beta t$，并给左端 $r(t)$ 加下划线。

![[AMA572 Fixed-Income and Credit Risk/Lecture 9/附件/课堂截图/228_Hull-White_积分因子定义.png|900]]

### 229 · Hull-White_乘积法则

- **来源标注**：截图标签 `lec9 (1)`，公式 (4)–(5)；关联 Assignment 3 Q1(a)。来源收集包：11.19。
- **新增板书**：蓝笔标出乘积法则第二项 $e^{H(t)}dr(t)$ 与左端 $r(t)$ 的对应关系；紫笔圈出两项中的公因式 $e^{H(t)}$ 并在第二行提公因式后的 $e^{H(t)}$ 下划线。

![[AMA572 Fixed-Income and Credit Risk/Lecture 9/附件/课堂截图/229_Hull-White_乘积法则.png|900]]

### 230 · Hull-White_漂移项抵消

- **来源标注**：截图标签 `lec9 (1)`，公式 (4)–(5)；关联 Assignment 3 Q1(a)。来源收集包：11.19。
- **新增板书**：黄笔圈出公式 `(4)`，从第二行引出箭头在右侧展开 $\beta(t)r(t)\,dt + dr(t) = \beta(t)r(t)\,dt + (\alpha(t)-\beta(t)r(t))\,dt + \sigma(t)\,dW(t) = \alpha(t)\,dt + \sigma(t)\,dW(t)$；蓝笔划去相消的 $\beta(t)r(t)$ 与 $-\beta(t)r(t)$。

![[AMA572 Fixed-Income and Credit Risk/Lecture 9/附件/课堂截图/230_Hull-White_漂移项抵消.png|900]]

### 231 · Hull-White_积分初始项

- **来源标注**：截图标签 `lec9 (1)`，公式 (4)–(5)；关联 Assignment 3 Q1(a)。来源收集包：11.19。
- **状态变化与新增板书**：清除了 228–230 的第一轮板书，页面略微上滚露出首段英文；蓝笔在右侧推导 $H(0)=\int_0^0\beta(u)\,du=0$ 及 $e^{H(0)}r(0)=e^0 r(0)=r(0)$，在左端补写 $\int_0^t d(e^{H(u)}r(u)) = e^{H(t)}r(t) - e^{H(0)}r(0) = e^{H(t)}r(t) - r(0)$，并在右端标出对哑变量 $u$ 从 $0$ 到 $t$ 积分及移项后的 $r(0)$。

![[AMA572 Fixed-Income and Credit Risk/Lecture 9/附件/课堂截图/231_Hull-White_积分初始项.png|900]]

### 232 · Hull-White_移回积分因子

- **来源标注**：截图标签 `lec9 (1)`，公式 (4)–(5)；关联 Assignment 3 Q1(a)。来源收集包：11.19。
- **新增板书**：紫笔在下划线对应两个积分项 $\int_0^t e^{H(u)}\alpha(u)\,du$ 与 $\int_0^t e^{H(u)}\sigma(u)\,dW(u)$，并在左侧画折线箭头标注乘以 $e^{-H(t)}$，由此从积分式移回积分因子得到显式解 `(5)`。

![[AMA572 Fixed-Income and Credit Risk/Lecture 9/附件/课堂截图/232_Hull-White_移回积分因子.png|900]]

---

## 字幕与作业关联

- [[AMA572 Fixed-Income and Credit Risk/课堂字幕/2026-11-19（带时间戳原文）|11.19 带时间戳字幕]]
- [[AMA572 Fixed-Income and Credit Risk/Assignment 3/01 - Assignment 3（英文原文与折叠译文）|Assignment 3 原题（英文原文与折叠译文）]]
- [[AMA572 Fixed-Income and Credit Risk/Assignment 3/00 - Assignment 3 资料索引|Assignment 3 资料索引]]
