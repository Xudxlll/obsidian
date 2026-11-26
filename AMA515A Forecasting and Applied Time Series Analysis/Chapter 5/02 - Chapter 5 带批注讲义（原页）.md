---
course: "AMA515A Forecasting and Applied Time Series Analysis"
chapter: 5
source: "AMA515A Chapter 5 Scanned Notes.pdf"
pages: 10
cssclasses:
  - ama-inline-translations
---

# Chapter 5 带批注讲义（教师批注全文转录与原页）

> [!info] 版本关系与阅读方式
> 本篇对应带教师批注的扫描版 [AMA515A Chapter 5 Scanned Notes.pdf](<附件/AMA515A Chapter 5 Scanned Notes.pdf>)（共 10 页）。经逐页核对，第 1—9 页的**印刷正文与 [tsf5_ama515A.pdf](<附件/tsf5_ama515A.pdf>) 完全一致**（逐段英文原文与折叠中文译文见 [[01 - Chapter 5 讲义（原页）|01 - Chapter 5 讲义]]），第 9 页无手写批注，第 10 页为双面扫描空白背页。
> 下文按页完整转录全部教师手写批注、印刷笔误更正与额外数值演算，并保留全部 10 页扫描原图。
> [本章资料索引](<05 - Chapter 5 资料索引.md>) · [印刷版讲义（中英双语）](<01 - Chapter 5 讲义（原页）.md>) · [独立手写笔记](<03 - Chapter 5 手写课堂笔记.md>)

## PDF p.1

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.1|5.1 Introduction & general theory（p.1）]]

### 教师手写批注转录

- 在 $X_t = \Phi(B)^{-1}\theta(B)a_t$ 右侧补写：$= \psi(B)a_t$；右侧空白注记 `where` $\psi(B) = \Phi(B)^{-1}\theta(B) = \dfrac{\theta(B)}{\Phi(B)}$，并用红笔标注希腊字母读音：`psi` ($\psi$)、`phi` ($\Phi$)、`theta` ($\theta$)。
- 在 $X_t = a_t + \psi_1 a_{t-1} + \psi_2 a_{t-2} + \cdots$ 下方补写算子展开形式：
  $$
  = (1 + \psi_1 B + \psi_2 B^2 + \psi_3 B^3 + \cdots)a_t
  $$
- 在 $X_i(\ell)$ 下方红笔标注等价记号 $X_{i+\ell}$；在 $\hat{X}_i(\ell) = \psi_\ell^* a_i + \psi_{\ell+1}^* a_{i-1} + \cdots$ 后红笔续写 $+ \psi_{\ell+2}^* a_{i-2} + \psi_{\ell+3}^* a_{i-3} + \cdots$；在 `wts` 下方及右侧注记 `wts = weights`。
- 在 $E\left[\{X_{i+\ell} - \hat{X}_i(\ell)\}^2\right]$ 右侧补写：$= E\left\{[e_i(\ell)]^2\right\}$。

![[Chapter 5/附件/ch5-annotated-p01.png]]

---

## PDF p.2

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.2|5.1 条件期望与误差方差（p.2）]]

### 教师手写批注转录

- 双下划线强调最优权重条件 $\psi_j^* = \psi_j$。
- 在式 (5.5) $\operatorname{Var}(e_i(\ell)) = (1 + \psi_1^2 + \cdots + \psi_{\ell-1}^2)\sigma_a^2$ 下方补写求和记号形式：
  $$
  = \left(\sum_{j=0}^{\ell-1}\psi_j^2\right)\sigma_a^2, \qquad \psi_0 = 1
  $$

![[Chapter 5/附件/ch5-annotated-p02.png]]

---

## PDF p.3

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.3|5.1 预测区间与 5.2 预测步骤（p.3）]]

### 教师手写批注转录

- **笔误更正**：在首行印刷的 $(100-\alpha)\%$ 上方红笔改标为 $100(1-\alpha)\%$。
- 在 `can replace` $\sigma_a^2$ `by its estimate.` 下方补写 $\hat{\sigma}_a^2$，右侧蓝笔补注 `with` $\psi_0 = 1$。
- 用大括号与 $E_i[\cdots]$ 括起两行 $\text{ARMA}(p,q)$ 差分方程，示意两边取条件期望：
  $$
  E_i\left[X_{i+\ell} = \phi_1 X_{i+\ell-1} + \cdots + \phi_p X_{i+\ell-p} + a_{i+\ell} + \theta_1 a_{i+\ell-1} + \cdots + \theta_q a_{i+\ell-q}\right]
  $$
- 在框内式 (5.6) 左端补写等价记号 $\hat{X}_{i+\ell} =$；**红笔更正印刷笔误**：将式 (5.6) 末尾误印的 $\theta_p$ 标箭头改为 $\theta_q$。
- 在框内式 (5.6*) 中下划线强调各滞后下标，并红圈标出 $+ \theta_\ell a_i$ 中的下标 $\ell$ 与 $i$。

![[Chapter 5/附件/ch5-annotated-p03.png]]

---

## PDF p.4

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.4|5.2 Updating ARIMA Forecasts（p.4）]]

### 教师手写批注转录

- 在式 (5.7) $a_{N+1} = X_{N+1} - \hat{X}_N(1)$ 右侧补写等价记号 $= X_{N+1} - \hat{X}_{N+1}$。
- 在更新公式 $\hat{X}_{N+1}(\ell) = \hat{X}_N(\ell+1) + \psi_\ell a_{N+1}$ 左侧补写 $\hat{X}_{N+1+\ell} =$，右侧蓝笔**补标遗漏的公式编号 `(5.8)`**。
- 在 $\hat{X}_{N+1}(\ell) = \psi_\ell a_{N+1} + \cdots$ 左侧蓝笔注记 `with` $i = N+1$。
- 在 `Table 5.1` 第 (A) 行（$i = N$）的 $a_i$ 空白格中蓝笔补填 $a_N$。

![[Chapter 5/附件/ch5-annotated-p04.png]]

---

## PDF p.5

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.5|5.3 例 1—3（p.5）]]

### 教师手写批注转录

- 右上角蓝笔标注 `Example 1 p.7`，在 Ex. 1 右侧标注参数出处 `Ch4 p.16 bottom`。
- 在 Ex. 1 中红笔补标等价记号：$\hat{X}_t(1) = \hat{X}_{122} = 5.81$ 与 $\hat{X}_t(2) = \hat{X}_{123} = 5.488$。
- 在 Ex. 2 右侧红笔补注 $\psi_0 = 1$；在 $\hat{X}_t(2)$ 的 95% 预测限下方黑笔补算出具体区间数值：
  $$
  5.488 \pm 1.3113 = (4.1767,\; 6.7993)
  $$
- 在 Ex. 3 ARMA(1, 1) 右侧红笔展开差分过程：
  $$
  (1 - \phi B)X_t = (1 - \theta B)a_t \Rightarrow X_t - \phi X_{t-1} = a_t - \theta a_{t-1} \Rightarrow X_t = \phi X_{t-1} + a_t - \theta a_{t-1}
  $$
  并注记 $\therefore \hat{X}_t(\ell) = \phi X_{t+\ell-1} + a_{t+\ell} - \theta a_{t+\ell-1}$（取条件期望前），及在 $\ell = 1$ 旁注 `for` $a_{t+1} = 0$、在 $\ell \ge 2$ 旁注 `for` $a_{t+2} = 0$。

![[Chapter 5/附件/ch5-annotated-p05.png]]

---

## PDF p.6

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.6|5.3 例 3 续、例 4—6（p.6）]]

### 教师手写批注转录

- 在 $a_t = X_t - \hat{X}_{t-1}(1)$ 下方红笔补写等价记号 $= X_t - \hat{X}_t$。
- 在 Ex. 4 $(1 - 0.8B)(1 - B)X_{t+\ell} = a_{t+\ell}$ 上方红笔标出阶数：$(1-0.8B)^1$ 对应 $p$、$(1-B)^1$ 对应 $d$；在预测式右侧标注 $\ell = 1$ 与 $\ell = 2$。
- 在 Ex. 5 上方黑笔补写算子形式 $(1 - B)X_t = (1 + \theta_1 B)a_t$；在预测式右侧红笔标注 $\ell = 1,\; a_{t+1} = 0$ 与 `all` $a_{t+\ell} = 0$。
- 在 Ex. 6 底部黑笔补写含常数项的模型方程：$X_t = \mu + X_{t-1} + a_t + \theta_1 a_{t-1}$。

![[Chapter 5/附件/ch5-annotated-p06.png]]

---

## PDF p.7

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.7|5.3 例 6 续、例 7—8（p.7）]]

### 教师手写批注转录

- 在 Ex. 6 预测式右侧红笔补注 $\ell = 1,\; a_{t+1} = 0$ 与 $a_{t+\ell} = 0$，红圈强调 $\hat{X}_t(1)$ 中的 `1`。
- 在 Ex. 7 季节模型 $(1, 0, 0)(0, 1, 1)_{12}$ 上方红笔标出 $p, d_1, q, d_2$，并用蓝箭头将三个阶数 `1` 分别连向 $(1-\alpha B)$、$(1-B^{12})$ 与 $(1-\theta B^{12})$。
- **三处印刷符号笔误更正（红笔）**：将第 4 行误印的 $X_{t-l-12}$、$X_{t+l--13}$、$a_{t+l--12}$ 分别更正为 $X_{t+l-12}$、$X_{t+l-13}$、$a_{t+l-12}$。
- 在 Ex. 7 预测式右侧红笔标注 $= \hat{X}_{t+1}$ ($\ell = 1, a_{t+1} = 0$) 与 $= \hat{X}_{t+2}$ ($\ell = 2$)。
- 在 Ex. 8 右侧黑笔标注 `AR(2) with constant`；在底行 `101^{th}` 下方蓝笔改标为 $101^{\text{st}}$。

![[Chapter 5/附件/ch5-annotated-p07.png]]

---

## PDF p.8

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.8|5.3 例 8 解答与例 9（p.8）]]

### 教师手写批注转录

- 在 Ex. 8 解答中红笔标注当前起点 $t = 100$。
- 在 Ex. 9 题干左上角黑笔标注模型类型 `ARIMA(1, 1, 1)`；红笔在算子上方分别标注 $d$ ($(1-B)^1$)、$p$ ($(1-0.2B)^1$)、$q$ ($(1-0.5B)^1$)，在 $a_t \sim N(0, 1)$ 上下方标注 `IID` / `NID` / `WN`。
- 在 Ex. 9(a) 中红笔补全完整数值代入，并**额外补充了向前 3 步预测 $\hat{X}_t(3)$**：
  $$
  \begin{aligned}
  \hat{X}_t(1) &= 1.2(4) - 0.2(3) - 0.5(1) = 3.7 \\
  \hat{X}_t(2) &= 1.2(3.7) - 0.2(4) = 3.64 \\
  \hat{X}_t(3) &= 1.2\hat{X}_{t+2} - 0.2\hat{X}_{t+1} = 1.2(3.64) - 0.2(3.7) = 3.628
  \end{aligned}
  $$
- 在 Ex. 9(b)(i) 底部红笔补全 95% 预测区间数值计算：
  $$
  3.64 \pm 1.96\sqrt{1 + 0.7^2} = 3.64 \pm 1.96(1.2207) = 3.64 \pm 2.3925 = (1.2475,\; 6.0325)
  $$

![[Chapter 5/附件/ch5-annotated-p08.png]]

---

## PDF p.9

对应正文：[[01 - Chapter 5 讲义（原页）#PDF p.9|5.3 例 9 Method 2 与讨论（p.9）]]

本页扫描版**无任何教师手写批注**，印刷内容与 `tsf5_ama515A.pdf` 第 9 页完全相同。

![[Chapter 5/附件/ch5-annotated-p09.png]]

---

## PDF p.10

本页为双面扫描产生的**完全空白页**（无印刷正文与手写内容），按原 PDF 页数保留。

![[Chapter 5/附件/ch5-annotated-p10.png]]
