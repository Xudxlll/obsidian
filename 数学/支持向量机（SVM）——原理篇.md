---
title: "支持向量机（SVM）——原理篇"
tags:
  - machine-learning
  - svm
  - classification
  - math
created: 2026-07-02
source: "https://zhuanlan.zhihu.com/p/31886934"
---

# 支持向量机（SVM）——原理篇

## 目录

- [一、SVM 简介](#一svm-简介)
- [二、核心几何直觉](#二核心几何直觉)
  - [2.1 分离超平面](#21-分离超平面)
  - [2.2 几何间隔（Geometric Margin）](#22-几何间隔geometric-margin)
  - [2.3 支持向量](#23-支持向量)
- [三、硬间隔 SVM（线性可分情况）](#三硬间隔-svm线性可分情况)
  - [3.1 问题形式化](#31-问题形式化)
  - [3.2 缩放技巧：从几何间隔到函数间隔](#32-缩放技巧从几何间隔到函数间隔)
  - [3.3 max γ → min ½‖w‖² 的等价转换](#33-max-γ--min-½w²-的等价转换)
  - [3.4 拉格朗日对偶：为什么以及怎么做](#34-拉格朗日对偶为什么以及怎么做)
  - [3.5 KKT 条件详解](#35-kkt-条件详解)
  - [3.6 求解 w 和 b](#36-求解-w-和-b)
- [四、软间隔 SVM（线性不可分情况）](#四软间隔-svm线性不可分情况)
  - [4.1 松弛变量 ξ 的引入](#41-松弛变量-ξ-的引入)
  - [4.2 惩罚参数 C 的意义](#42-惩罚参数-c-的意义)
  - [4.3 软间隔的算法流程](#43-软间隔的算法流程)
- [五、核方法（非线性 SVM）](#五核方法非线性-svm)
  - [5.1 核技巧的核心思想](#51-核技巧的核心思想)
  - [5.2 高斯核（RBF Kernel）](#52-高斯核rbf-kernel)
  - [5.3 非线性 SVM 算法流程](#53-非线性-svm-算法流程)
- [六、总结](#六总结)
- [参考](#参考)

---

## 一、SVM 简介

**支持向量机（Support Vector Machines, SVM）** 是一种二分类模型。它的核心思想是：在特征空间中寻找一个**使得正负样本之间的间隔（margin）最大化**的分离超平面。

SVM 的三个关键词：

| 关键词 | 含义 |
|--------|------|
| **支持向量（Support Vector）** | 距离分离超平面最近的那些训练样本点 |
| **间隔（Margin）** | 正负样本到超平面的最小距离之和 |
| **最大化间隔** | SVM 的目标——找到使间隔最大的超平面 |

SVM 的三层境界：

1. **硬间隔 SVM**（线性可分）：假设训练数据完全可以用一个超平面分开
2. **软间隔 SVM**（近似线性可分）：允许少量样本被错分，引入松弛变量
3. **核方法 SVM**（非线性可分）：通过核函数将数据映射到高维空间，使原本不可分的数据在高维空间变得线性可分

---

## 二、核心几何直觉

### 2.1 分离超平面

在 $n$ 维空间中，超平面用方程表示：

$$
\mathbf{w} \cdot \mathbf{x} + b = 0
$$

其中 $\mathbf{w} = (w_1, w_2, \ldots, w_n)$ 是法向量，决定了超平面的方向；$b$ 是偏置（截距），决定了超平面与原点之间的距离。

> **法向量 $\mathbf{w}$ 的含义**：垂直于超平面的向量。如果你站在超平面上，$\mathbf{w}$ 指向的方向是"正类"一侧。

对于任意一个样本点 $\mathbf{x}$：
- 若 $\mathbf{w} \cdot \mathbf{x} + b > 0$，预测为正类（+1）
- 若 $\mathbf{w} \cdot \mathbf{x} + b < 0$，预测为负类（-1）

### 2.2 几何间隔（Geometric Margin）

**为什么不用函数间隔？**

函数间隔定义为 $\hat{\gamma}_i = y_i(\mathbf{w} \cdot \mathbf{x}_i + b)$。问题在于：如果我们将 $\mathbf{w}$ 和 $b$ 同时放大 2 倍，超平面的位置并没有变化，但函数间隔却变成了原来的 2 倍。函数间隔不能真实反映"距离"。

**几何间隔才是真正的距离。**

从点 $\mathbf{x}_i$ 到超平面 $\mathbf{w} \cdot \mathbf{x} + b = 0$ 的距离是（点到平面距离公式）：

$$
\text{distance} = \frac{|\mathbf{w} \cdot \mathbf{x}_i + b|}{\|\mathbf{w}\|}
$$

乘以 $y_i \in \{+1, -1\}$ 来消除绝对值（正确分类时 $y_i$ 与 $\mathbf{w} \cdot \mathbf{x}_i + b$ 同号），得到**几何间隔**：

$$
\gamma_i = y_i\left(\frac{\mathbf{w}}{\|\mathbf{w}\|} \cdot \mathbf{x}_i + \frac{b}{\|\mathbf{w}\|}\right)
$$

> **直观理解**：$\gamma_i$ 是样本点 $\mathbf{x}_i$ 到超平面的**带符号距离**——距离越远，说明分类越"有把握"。

### 2.3 支持向量

所有样本点中，离超平面最近的点被称为**支持向量（Support Vectors）**。

支持向量到超平面的距离（即所有几何间隔的最小值）称为数据集关于该超平面的**几何间隔**：

$$
\gamma = \min_{i=1,2,\ldots,N} \gamma_i
$$

> **关键性质**：SVM 最终的分类超平面**只由支持向量决定**。非支持向量的样本点即使被移除，也不会改变超平面的位置。这使得 SVM 在中小规模数据集上非常高效。

---

## 三、硬间隔 SVM（线性可分情况）

### 3.1 问题形式化

**目标**：找到一个超平面，使所有样本点到该超平面的最小距离（几何间隔 $\gamma$）尽可能大。

$$
\max_{\mathbf{w}, b} \quad \gamma
$$

$$
\text{s.t.} \quad y_i\left(\frac{\mathbf{w}}{\|\mathbf{w}\|} \cdot \mathbf{x}_i + \frac{b}{\|\mathbf{w}\|}\right) \geq \gamma, \quad i = 1,2,\ldots,N
$$

这个公式读作：在约束条件（每个样本点的几何间隔都不小于 $\gamma$）下，最大化最小的几何间隔 $\gamma$。

### 3.2 缩放技巧：从几何间隔到函数间隔

这是 SVM 推导中**最容易被忽略但最重要的步骤**。让我们拆开来看。

**第一步：两边同时除以 $\gamma$**

将约束不等式两边同时除以 $\gamma$（$\gamma > 0$）：

$$
y_i\left(\frac{\mathbf{w}}{\|\mathbf{w}\|\gamma} \cdot \mathbf{x}_i + \frac{b}{\|\mathbf{w}\|\gamma}\right) \geq 1
$$

**第二步：重参数化（Re-parameterization）**

令：
$$
\mathbf{w}_{\text{new}} = \frac{\mathbf{w}}{\|\mathbf{w}\|\gamma}, \quad b_{\text{new}} = \frac{b}{\|\mathbf{w}\|\gamma}
$$

> **关键理解**：这不是对 $\mathbf{w}$ 做了实质改变，而是换了一组等价的参数。因为超平面 $\mathbf{w} \cdot \mathbf{x} + b = 0$ 和 $k\mathbf{w} \cdot \mathbf{x} + kb = 0$ 表示的是**同一个超平面**（同除以 $k$ 即得原式）。所以把 $\mathbf{w}$ 缩放到新的 $\mathbf{w}_{\text{new}}$ 时，超平面位置不变。

简化记号后得到：

$$
y_i(\mathbf{w} \cdot \mathbf{x}_i + b) \geq 1, \quad i = 1,2,\ldots,N
$$

此时，支持向量满足 $y_i(\mathbf{w} \cdot \mathbf{x}_i + b) = 1$，即支持向量到超平面的函数间隔被归一化为 1。

### 3.3 max γ → min ½‖w‖² 的等价转换

这是第二个关键步骤。回忆刚才的重参数化：

$$
\mathbf{w} = \frac{\mathbf{w}_{\text{old}}}{\|\mathbf{w}_{\text{old}}\|\gamma}
$$

取范数：

$$
\|\mathbf{w}\| = \frac{1}{\gamma}
$$

所以 $\gamma = \frac{1}{\|\mathbf{w}\|}$。**最大化 $\gamma$ 等价于最小化 $\|\mathbf{w}\|$**。

为了后续求导的便利（避免平方根），等价地最小化 $\frac{1}{2}\|\mathbf{w}\|^2$。因子 $\frac{1}{2}$ 纯粹是为了求导后系数变 1，不影响最优解。

最终得到 SVM 的**原始问题（Primal Problem）**：

$$
\min_{\mathbf{w}, b} \quad \frac{1}{2}\|\mathbf{w}\|^2
$$

$$
\text{s.t.} \quad y_i(\mathbf{w} \cdot \mathbf{x}_i + b) \geq 1, \quad i = 1,2,\ldots,N
$$

> **直觉**：间隔 = 1/‖w‖。让 ‖w‖ 尽量小，就是在扩大间隔。同时约束条件确保所有点都在"间隔带"之外。

### 3.4 拉格朗日对偶：为什么以及怎么做

**为什么要转到对偶问题？**

1. **原始问题有约束，不好直接求解**——需要将带约束的优化转为无约束
2. **对偶问题中只出现内积 $\mathbf{x}_i \cdot \mathbf{x}_j$**——这为后续的核方法（kernel trick）铺路
3. **对偶问题的变量数量 = 样本数 N**，当特征维度远大于样本数时，对偶问题更容易求解

**拉格朗日函数**

引入拉格朗日乘子 $\alpha_i \geq 0$（每个约束对应一个乘子），构造拉格朗日函数：

$$
L(\mathbf{w}, b, \boldsymbol{\alpha}) = \frac{1}{2}\|\mathbf{w}\|^2 - \sum_{i=1}^{N} \alpha_i \big(y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1\big)
$$

> **为什么要减？** 这是一种标准构造方式：对不等式约束 $g_i(x) \geq 0$，拉格朗日函数中写 $- \alpha_i g_i(x)$。

现在定义一个函数 $\theta(\mathbf{w})$：

$$
\theta(\mathbf{w}) = \max_{\alpha_i \geq 0} L(\mathbf{w}, b, \boldsymbol{\alpha})
$$

这个函数的行为：
- 如果 $\mathbf{w}, b$ 满足所有约束（即 $y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1 \geq 0$），那么拉格朗日乘子取 0 时 $L = \frac{1}{2}\|\mathbf{w}\|^2$，这就是 $\theta(\mathbf{w})$ 的值
- 如果存在某个约束不满足（即 $y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1 < 0$），令对应 $\alpha_i \to +\infty$，则 $L \to +\infty$，$\theta(\mathbf{w}) \to +\infty$

于是原始问题等价于：

$$
p^* = \min_{\mathbf{w}, b} \theta(\mathbf{w}) = \min_{\mathbf{w}, b} \max_{\alpha_i \geq 0} L(\mathbf{w}, b, \boldsymbol{\alpha})
$$

**对偶问题：交换 min 和 max**

直接求解 $\min \max$ 很困难，考虑交换顺序得到**对偶问题**：

$$
d^* = \max_{\alpha_i \geq 0} \min_{\mathbf{w}, b} L(\mathbf{w}, b, \boldsymbol{\alpha})
$$

在一般情况下 $d^* \leq p^*$（弱对偶），但在满足一定条件时 $d^* = p^*$（强对偶）。SVM 满足强对偶需要的两个条件：

| 条件 | SVM 是否满足 |
|------|-------------|
| ① 优化问题是凸优化问题 | ✅ 目标函数 $\frac{1}{2}\|\mathbf{w}\|^2$ 是凸的，约束是线性的 |
| ② 满足 KKT 条件 | ✅ 详见下节 |

**求解对偶问题**

先固定 $\boldsymbol{\alpha}$，求 $L$ 对 $\mathbf{w}$ 和 $b$ 的最小值。

对 $\mathbf{w}$ 求偏导并令其为 0：

$$
\frac{\partial L}{\partial \mathbf{w}} = \mathbf{w} - \sum_{i=1}^{N} \alpha_i y_i \mathbf{x}_i = 0 \quad\Rightarrow\quad \mathbf{w} = \sum_{i=1}^{N} \alpha_i y_i \mathbf{x}_i
$$

对 $b$ 求偏导并令其为 0：

$$
\frac{\partial L}{\partial b} = -\sum_{i=1}^{N} \alpha_i y_i = 0 \quad\Rightarrow\quad \sum_{i=1}^{N} \alpha_i y_i = 0
$$

> **重要的发现**：最优的 $\mathbf{w}$ 是训练样本的线性组合！每个样本的"贡献"由其 $\alpha_i y_i$ 加权。

将这两个结果代入 $L$（代换过程较繁琐，核心就是消去 $\mathbf{w}$ 和 $b$），得到：

$$
\min_{\mathbf{w}, b} L(\mathbf{w}, b, \boldsymbol{\alpha}) = -\frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j (\mathbf{x}_i \cdot \mathbf{x}_j) + \sum_{i=1}^{N} \alpha_i
$$

再对此式求 $\boldsymbol{\alpha}$ 的极大，等价于以下最小化问题（取负号）：

$$
\min_{\boldsymbol{\alpha}} \quad \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j (\mathbf{x}_i \cdot \mathbf{x}_j) - \sum_{i=1}^{N} \alpha_i
$$

$$
\text{s.t.} \quad \sum_{i=1}^{N} \alpha_i y_i = 0, \quad \alpha_i \geq 0, \; i = 1,2,\ldots,N
$$

这就是 SVM 的**对偶问题** —— 一个关于 $\boldsymbol{\alpha}$ 的二次规划问题，可用 SMO（Sequential Minimal Optimization，序列最小优化）算法高效求解。

> **关键点**：目标函数和约束中只出现了样本之间的内积 $\mathbf{x}_i \cdot \mathbf{x}_j$，不涉及单个样本的特征值！

### 3.5 KKT 条件详解

**KKT（Karush-Kuhn-Tucker）条件** 是最优化理论中的核心概念。对于含有不等式约束的凸优化问题，KKT 条件是全局最优解的充要条件。

SVM 的 KKT 条件包括三条：

$$
\begin{cases}
\alpha_i \geq 0 & \text{(1) 乘子非负} \\[6pt]
y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1 \geq 0 & \text{(2) 原始可行性} \\[6pt]
\alpha_i\big(y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1\big) = 0 & \text{(3) 互补松弛性}
\end{cases}
$$

**互补松弛性是最重要的一条**。它告诉我们：

- 若 $\alpha_i > 0$，则必须 $y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1 = 0$，即该样本位于间隔边界上 → **这是支持向量！**
- 若 $y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1 > 0$（样本在间隔带外），则必须 $\alpha_i = 0$ → 该样本对最终模型没有贡献！

这就解释了为什么 SVM 的模型只依赖于支持向量：非支持向量的 $\alpha_i = 0$，在 $\mathbf{w} = \sum \alpha_i y_i \mathbf{x}_i$ 中贡献为零。

### 3.6 求解 w 和 b

SMO 算法求解出最优的 $\boldsymbol{\alpha}^*$ 后：

**求 $\mathbf{w}^*$**：

$$
\mathbf{w}^* = \sum_{i=1}^{N} \alpha_i^* y_i \mathbf{x}_i
$$

**求 $b^*$**：

由于存在至少一个 $\alpha_j^* > 0$（否则 $\mathbf{w} = 0$，无法构成有效分类器），对此 $j$，由 KKT 互补松弛条件可知：

$$
y_j(\mathbf{w}^* \cdot \mathbf{x}_j + b^*) - 1 = 0
$$

解出：

$$
b^* = y_j - \sum_{i=1}^{N} \alpha_i^* y_i (\mathbf{x}_i \cdot \mathbf{x}_j)
$$

> **实践技巧**：通常取所有支持向量的 $b^*$ 估计值求平均，以获得更稳定的结果。

**分离超平面**：$\mathbf{w}^* \cdot \mathbf{x} + b^* = 0$

**分类决策函数**：$f(\mathbf{x}) = \text{sign}(\mathbf{w}^* \cdot \mathbf{x} + b^*)$

---

## 四、软间隔 SVM（线性不可分情况）

### 4.1 松弛变量 ξ 的引入

现实中极少有完美线性可分的数据。硬间隔要求：

$$
y_i(\mathbf{w} \cdot \mathbf{x}_i + b) \geq 1
$$

如果数据中存在异常点或噪声，这个约束无法满足，问题无解。为此引入了**松弛变量 $\xi_i \geq 0$**：

$$
y_i(\mathbf{w} \cdot \mathbf{x}_i + b) \geq 1 - \xi_i
$$

| $\xi_i$ 的值 | 含义 |
|-------------|------|
| $\xi_i = 0$ | 样本被正确分类且在间隔带外 |
| $0 < \xi_i < 1$ | 样本在间隔带内部但仍被正确分类 |
| $\xi_i \geq 1$ | 样本被错误分类（穿过了超平面） |

> **直观理解**：$\xi_i$ 度量的是"这个样本违反了硬间隔约束的程度"。类似于"对第 i 个样本的宽容度"。

**Hinge Loss（合页损失）**：软间隔使用的损失函数是

$$
\xi_i = \max(0, 1 - y_i(\mathbf{w} \cdot \mathbf{x}_i + b))
$$

如果 $y_i(\mathbf{w} \cdot \mathbf{x}_i + b) \geq 1$（分类正确且有足够把握），损失为 0；
否则损失随偏离而线性增大。这与分类问题中"正确不仅要分类对，还要有足够置信度"的理念一致。

### 4.2 惩罚参数 C 的意义

软间隔的优化目标变为：

$$
\min_{\mathbf{w}, b, \boldsymbol{\xi}} \quad \frac{1}{2}\|\mathbf{w}\|^2 + C\sum_{i=1}^{N} \xi_i
$$

这里有一个**权衡（Trade-off）**：

$$
\underbrace{\frac{1}{2}\|\mathbf{w}\|^2}_{\text{间隔最大（模型简单）}} \;+\; \underbrace{C\sum_{i=1}^{N} \xi_i}_{\text{分类误差最小}}
$$

| C 的取值 | 效果 |
|---------|------|
| **C → +∞** | 不允许任何分类错误，退化为硬间隔 SVM。对噪声极度敏感，容易过拟合 |
| **C 很小** | 允许较多错误，间隔较大，模型更简单、泛化能力更强 |
| **C = 0** | 模型退化，无意义 |

> **实践建议**：C 是最重要的超参数，通常通过交叉验证选择。C 越大，模型越复杂，越容易过拟合。

### 4.3 软间隔的算法流程

经过类似的拉格朗日对偶推导，软间隔的对偶问题与硬间隔几乎一致，唯一的区别在于 $\alpha_i$ 多了一个上界 $C$：

$$
\min_{\boldsymbol{\alpha}} \quad \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j (\mathbf{x}_i \cdot \mathbf{x}_j) - \sum_{i=1}^{N} \alpha_i
$$

$$
\text{s.t.} \quad \sum_{i=1}^{N} \alpha_i y_i = 0, \quad 0 \leq \alpha_i \leq C, \; i = 1,2,\ldots,N
$$

> **$\alpha_i$ 的上界 C** 从何而来？来自松弛变量 $\xi_i$ 对应的拉格朗日乘子，数学上可以推导出 $\alpha_i + \mu_i = C$（其中 $\mu_i \geq 0$ 是 $\xi_i$ 的乘子），因此 $\alpha_i \leq C$。

KKT 条件也相应变为：

$$
\begin{cases}
\alpha_i \geq 0, \; \mu_i \geq 0 \\[4pt]
y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1 + \xi_i \geq 0 \\[4pt]
\alpha_i(y_i(\mathbf{w} \cdot \mathbf{x}_i + b) - 1 + \xi_i) = 0 \\[4pt]
\xi_i \geq 0, \; \mu_i \xi_i = 0
\end{cases}
$$

据此可对 $\alpha_i^*$ 分类：
- $\alpha_i^* = 0$：非支持向量，在间隔带外
- $0 < \alpha_i^* < C$：支持向量，恰好落在间隔边界上（$\xi_i = 0$）
- $\alpha_i^* = C$：支持向量，落在间隔带内或被误分（$\xi_i > 0$）

求 $b^*$ 时，选取满足 $0 < \alpha_j^* < C$ 的 $j$（这类点恰好落在边界上），用相同公式：

$$
b^* = y_j - \sum_{i=1}^{N} \alpha_i^* y_i (\mathbf{x}_i \cdot \mathbf{x}_j)
$$

---

## 五、核方法（非线性 SVM）

### 5.1 核技巧的核心思想

对于非线性可分的数据（例如同心圆分布），无论如何画直线都无法分开。但我们可以：

1. 将原始数据 $\mathbf{x}$ 映射到高维特征空间 $\phi(\mathbf{x})$
2. 在高维空间中寻找线性分离超平面

例如，二维的 XOR 问题映射到三维后可以用平面分开。

**但是**，直接计算 $\phi(\mathbf{x})$ 再在高维空间做内积，计算量可能非常大（甚至无限维）。

**核技巧（Kernel Trick）** 的优雅之处：回顾对偶问题的目标函数和决策函数，它们**只依赖于样本间的内积** $\mathbf{x}_i \cdot \mathbf{x}_j$。如果我们能找到一个函数 $K$：

$$
K(\mathbf{x}, \mathbf{z}) = \phi(\mathbf{x}) \cdot \phi(\mathbf{z})
$$

那么我们就**不需要显式计算 $\phi(\mathbf{x})$**，直接用 $K$ 替代所有内积即可！

$$
\min_{\boldsymbol{\alpha}} \quad \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j \color{red}{K(\mathbf{x}_i, \mathbf{x}_j)} - \sum_{i=1}^{N} \alpha_i
$$

分类决策函数变为：

$$
f(\mathbf{x}) = \text{sign}\left(\sum_{i=1}^{N} \alpha_i^* y_i \color{red}{K(\mathbf{x}, \mathbf{x}_i)} + b^*\right)
$$

> **核心洞见**：我们在低维空间中计算核函数 $K$，却等价于在高维（甚至无限维）空间中做线性分类！

**常用核函数**：

| 核函数 | 公式 | 特点 |
|--------|------|------|
| **线性核** | $K(\mathbf{x}, \mathbf{z}) = \mathbf{x} \cdot \mathbf{z}$ | 退化为线性 SVM |
| **多项式核** | $K(\mathbf{x}, \mathbf{z}) = (\mathbf{x} \cdot \mathbf{z} + c)^d$ | 参数 d 控制映射维度 |
| **高斯核（RBF）** | $K(\mathbf{x}, \mathbf{z}) = \exp\left(-\frac{\|\mathbf{x} - \mathbf{z}\|^2}{2\sigma^2}\right)$ | 最常用，映射到无限维 |
| **Sigmoid 核** | $K(\mathbf{x}, \mathbf{z}) = \tanh(\gamma \mathbf{x} \cdot \mathbf{z} + c)$ | 类似神经网络激活函数 |

### 5.2 高斯核（RBF Kernel）

高斯核（也叫径向基核，RBF Kernel）是最常用的核函数：

$$
K(\mathbf{x}, \mathbf{z}) = \exp\left(-\frac{\|\mathbf{x} - \mathbf{z}\|^2}{2\sigma^2}\right)
$$

> **怎么理解高斯核？**
>
> 考虑两个样本 $\mathbf{x}$ 和 $\mathbf{z}$：
> - 如果 $\mathbf{x} \approx \mathbf{z}$（很相似），$\|\mathbf{x} - \mathbf{z}\|^2 \approx 0$，$K \approx 1$ → 高度相似
> - 如果 $\mathbf{x}$ 和 $\mathbf{z}$ 相距很远，$K \approx 0$ → 几乎无关
>
> **$\sigma$（或参数 $\gamma = 1/2\sigma^2$）的作用**：
> - $\sigma$ 大（$\gamma$ 小）：影响范围大，决策边界平滑，可能导致欠拟合
> - $\sigma$ 小（$\gamma$ 大）：影响范围小，决策边界复杂，可能导致过拟合

高斯核实际上将数据映射到了**无限维空间**（可以通过泰勒展开证明），这赋予了 SVM 极强的拟合能力，但也带来了过拟合的风险。

### 5.3 非线性 SVM 算法流程

**输入**：训练数据集 $T = \{(\mathbf{x}_1, y_1), (\mathbf{x}_2, y_2), \ldots, (\mathbf{x}_N, y_N)\}$，$y_i \in \{+1, -1\}$

**步骤**：

1. 选取核函数 $K(\mathbf{x}, \mathbf{z})$ 和惩罚参数 $C > 0$，构造并求解：

$$
\min_{\boldsymbol{\alpha}} \quad \frac{1}{2}\sum_{i=1}^{N}\sum_{j=1}^{N} \alpha_i \alpha_j y_i y_j K(\mathbf{x}_i, \mathbf{x}_j) - \sum_{i=1}^{N} \alpha_i
$$

$$
\text{s.t.} \quad \sum_{i=1}^{N} \alpha_i y_i = 0, \quad 0 \leq \alpha_i \leq C
$$

得最优解 $\boldsymbol{\alpha}^*$

2. 选择满足 $0 < \alpha_j^* < C$ 的分量，计算：

$$
b^* = y_j - \sum_{i=1}^{N} \alpha_i^* y_i K(\mathbf{x}_i, \mathbf{x}_j)
$$

3. 构造决策函数：

$$
f(\mathbf{x}) = \text{sign}\left(\sum_{i=1}^{N} \alpha_i^* y_i K(\mathbf{x}, \mathbf{x}_i) + b^*\right)
$$

---

## 六、总结

SVM 的完整推导链路：

```
几何直觉（最大化间隔）
    ↓
原始优化问题（min ½‖w‖², s.t. 约束）
    ↓
拉格朗日对偶（消去原始变量 w, b，得到仅含 α 的问题）
    ↓
SMO 算法求解 α
    ↓
硬间隔 → 软间隔（加入松弛变量 ξ 和惩罚参数 C）
    ↓
线性核 → 非线性核（用 K(x,z) 替代内积 x·z）
    ↓
最终决策函数：f(x) = sign(∑ α_i y_i K(x, x_i) + b)
```

**三个核心洞见**：

1. **最大化间隔 = 最小化 ‖w‖²**：SVM 不仅是"找一条线分开"，而是找"最宽的带状区域"分开
2. **拉格朗日对偶让问题变得可解**：将带约束问题转化为无约束，且巧妙的是一阶条件恰好使 w 成为样本的线性组合
3. **核技巧实现了"低维计算，高维效果"**：在原始空间中计算核函数的值，等价于在高维特征空间中做内积，避免了维度灾难

**SVM 的优缺点**：

| 优点 | 缺点 |
|------|------|
| 有严格的数学理论支撑 | 大规模数据（百万级以上）训练慢 |
| 由支持向量决定，模型可解释 | 对参数 C 和核参数敏感，需要仔细调参 |
| 核技巧处理非线性问题能力强 | 二分类问题，多分类需要扩展（OvO/OvR） |
| 泛化能力强，不易过拟合 | 概率输出需要额外处理（Platt Scaling） |

---

## 参考

1. 《统计学习方法》李航
2. 《机器学习》周志华
3. [深入理解拉格朗日乘子法和 KKT 条件](http://blog.csdn.net/xianlingmao/article/details/7919597)
4. [支持向量机通俗导论（理解 SVM 的三层境界）](http://blog.csdn.net/v_july_v/article/details/7624837)
