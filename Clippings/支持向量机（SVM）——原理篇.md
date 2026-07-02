---
title: "支持向量机（SVM）——原理篇"
source: "https://zhuanlan.zhihu.com/p/31886934"
author:
  - "[[野风]]"
published:
created: 2026-07-02
description: "目录SVM简介 线性SVM算法原理 非线性SVM算法原理 SVM简介支持向量机（support vector machines, SVM）是一种二分类模型，它的基本模型是定义在特征空间上的 间隔最大的线性分类器，间隔最大使它有别于感知机；SVM…"
tags:
  - "clippings"
---
[收录于 · 机器学习笔记](https://www.zhihu.com/column/c_120229701)

1859 人赞同了该文章

## 目录

> SVM简介  
> 线性SVM算法原理  
> 非线性SVM算法原理

## SVM简介

支持向量机（support vector machines, SVM）是一种二分类模型，它的基本模型是定义在特征空间上的 **间隔最大的线性分类器** ，间隔最大使它有别于感知机；SVM还包括 **[核技巧](https://zhida.zhihu.com/search?content_id=4943635&content_type=Article&match_order=1&q=%E6%A0%B8%E6%8A%80%E5%B7%A7&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3ODMxMzU0MzQsInEiOiLmoLjmioDlt6ciLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjo0OTQzNjM1LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.bltmdmMIB36z7y_-6N3xfvQRtvQ0A1vpyk2wdKkgU1o&zhida_source=entity)** ，这使它成为实质上的非线性分类器。SVM的的学习策略就是间隔最大化，可形式化为一个求解凸二次规划的问题，也等价于正则化的合页损失函数的最小化问题。SVM的的学习算法就是求解凸二次规划的最优化算法。

## SVM算法原理

SVM学习的基本想法是求解能够正确划分训练数据集并且几何间隔最大的分离超平面。如下图所示， $\mathbf{\mathit{w}} \cdot x + b = 0$ 即为分离超平面，对于线性可分的数据集来说，这样的超平面有无穷多个（即感知机），但是几何间隔最大的分离超平面却是唯一的。

![](https://pic3.zhimg.com/v2-197913c461c1953c30b804b4a7eddfcc_1440w.jpg)

在推导之前，先给出一些定义。假设给定一个特征空间上的训练数据集

$$
T = \left\{\left(\mathbf{\mathit{x}}_{1} , y_{1}\right) , \left(\mathbf{\mathit{x}}_{2} , y_{2}\right) , . . . , \left(\mathbf{\mathit{x}}_{N} , y_{N}\right)\right\}
$$

其中， $\mathbf{\mathit{x}}_{i} \in \mathbb{R}^{n}$ ， $y_{i} \in \left\{+ 1 , - 1\right\} , i = 1 , 2 , . . . N$ ， $x_{i}$ 为第 $i$ 个特征向量， $y_{i}$ 为类标记，当它等于+1时为正例；为-1时为负例。再假设训练数据集是 **线性可分** 的。

**几何间隔** ：对于给定的数据集 $T$ 和超平面 $w \cdot x + b = 0$ ，定义超平面关于样本点 $\left(x_{i} , y_{i}\right)$ 的几何间隔为

$$
\gamma_{i} = y_{i} \left(\frac{\mathbf{\mathit{w}}}{\left\|\mathbf{\mathit{w}}\right\|} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + \frac{b}{\left\|\mathbf{\mathit{w}}\right\|}\right)
$$

超平面关于所有样本点的几何间隔的最小值为

$$
\gamma = \underset{i = 1 , 2... , N}{min} \gamma_{i}
$$

实际上这个距离就是我们所谓的 **支持向量** 到超平面的距离。

根据以上定义，SVM模型的求解最大分割超平面问题可以表示为以下约束最优化问题

$$
\underset{\mathbf{\mathit{w}} , b}{max} \gamma
$$

$$
s . t . y_{i} \left(\frac{\mathbf{\mathit{w}}}{\left\|\mathbf{\mathit{w}}\right\|} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + \frac{b}{\left\|\mathbf{\mathit{w}}\right\|}\right) \geq \gamma , i = 1 , 2 , . . . , N
$$

将约束条件两边同时除以 $\gamma$ ，得到

$$
y_{i} \left(\frac{\mathbf{\mathit{w}}}{\left\|\mathbf{\mathit{w}}\right\| \gamma} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + \frac{b}{\left\|\mathbf{\mathit{w}}\right\| \gamma}\right) \geq 1
$$

因为 $\left\|\mathbf{\mathit{w}}\right\| ， \gamma$ 都是标量，所以为了表达式简洁起见，令

$$
\mathbf{\mathit{w}} = \frac{\mathbf{\mathit{w}}}{\left\|\mathbf{\mathit{w}}\right\| \gamma}
$$

$$
b = \frac{b}{\left\|\mathbf{\mathit{w}}\right\| \gamma}
$$

得到

$$
y_{i} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) \geq 1 , i = 1 , 2 , . . . , N
$$

又因为最大化 $\gamma$ ，等价于最大化 $\frac{1}{\left\|\mathbf{\mathit{w}}\right\|}$ ，也就等价于最小化 $\frac{1}{2} \left\|\mathbf{\mathit{w}}\right\|^{2}$ （ $\frac{1}{2}$ 是为了后面求导以后形式简洁，不影响结果），因此SVM模型的求解最大分割超平面问题又可以表示为以下约束最优化问题

$$
\underset{\mathbf{\mathit{w}} , b}{min} \frac{1}{2} \left\|\mathbf{\mathit{w}}\right\|^{2}
$$

$$
s . t . y_{i} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) \geq 1 , i = 1 , 2 , . . . , N
$$

这是一个含有不等式约束的凸二次规划问题，可以对其使用拉格朗日乘子法得到其对偶问题（dual problem）。

首先，我们将有约束的原始目标函数转换为无约束的新构造的拉格朗日目标函数

$$
L \left(\mathbf{\mathit{w}} , b , \mathbf{\mathit{\alpha}}\right) = \frac{1}{2} \left\|\mathbf{\mathit{w}}\right\|^{2} - \sum_{i = 1}^{N} \alpha_{i} \left(y_{i} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) - 1\right)
$$

其中 $\alpha_{i}$ 为拉格朗日乘子，且 $\alpha_{i} \geq 0$ 。现在我们令

$$

$$

当样本点不满足约束条件时，即在可行解区域外：

$$
y_{i} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) < 1
$$

此时，将 $\alpha_{i}$ 设置为无穷大，则 $\theta \left(\mathbf{\mathit{w}}\right)$ 也为无穷大。

当满本点满足约束条件时，即在可行解区域内：

$$
y_{i} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) \geq 1
$$

此时， $\theta \left(\mathbf{\mathit{w}}\right)$ 为原函数本身。于是，将两种情况合并起来就可以得到我们新的目标函数

$$
\theta \left(\mathbf{\mathit{w}}\right) = \begin{cases} \frac{1}{2} \left\|\mathbf{\mathit{w}}\right\|^{2} , \mathbf{\mathit{x}} \in 可行区域 \\ + \infty , \mathbf{\mathit{x}} \in 不可行区域 \end{cases}
$$

于是原约束问题就等价于

$$
\underset{\mathbf{\mathit{w}} , b}{min} \theta \left(\mathbf{\mathit{w}}\right) = \underset{\mathbf{\mathit{w}} , b}{min} \underset{\alpha_{i} \geq 0}{max} L \left(\mathbf{\mathit{w}} , b , \mathbf{\mathit{\alpha}}\right) = p^{*}
$$

看一下我们的新目标函数，先求最大值，再求最小值。这样的话，我们首先就要面对带有需要求解的参数 $\mathbf{\mathit{w}}$ 和 $b$ 的方程，而 $\alpha_{i}$ 又是不等式约束，这个求解过程不好做。所以，我们需要使用拉格朗日函数 **对偶性** ，将最小和最大的位置交换一下，这样就变成了：

$$
\underset{\alpha_{i} \geq 0}{max} \underset{\mathbf{\mathit{w}} , b}{min} L \left(\mathbf{\mathit{w}} , b , \mathbf{\mathit{\alpha}}\right) = d^{*}
$$

要有 $p^{*} = d^{*}$ ，需要满足两个条件：

① 优化问题是凸优化问题

② 满足KKT条件

首先，本优化问题显然是一个凸优化问题，所以条件一满足，而要满足条件二，即要求

$$
\begin{cases} \alpha_{i} \geq 0 \\ y_{i} \left(\mathbf{\mathit{w}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) - 1 \geq 0 \\ \alpha_{i} \left(y_{i} \left(\mathbf{\mathit{w}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) - 1\right) = 0 \end{cases}
$$

为了得到求解对偶问题的具体形式，令 $L \left(\mathbf{\mathit{w}} , b , \mathbf{\mathit{\alpha}}\right)$ 对 $\mathbf{\mathit{w}}$ 和 $b$ 的偏导为0，可得

$$
\mathbf{\mathit{w}} = \sum_{i = 1}^{N} \alpha_{i} y_{i} \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}}
$$

$$
\sum_{i = 1}^{N} \alpha_{i} y_{i} = 0
$$

将以上两个等式带入拉格朗日目标函数，消去 $\mathbf{\mathit{w}}$ 和 $b$ ， 得

$$
L \left(\mathbf{\mathit{w}} , b , \mathbf{\mathit{\alpha}}\right) = \frac{1}{2} \sum_{i = 1}^{N} \sum_{j = 1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) - \sum_{i = 1}^{N} \alpha_{i} y_{i} \left(\left(\sum_{j = 1}^{N} \alpha_{j} y_{j} \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) + \sum_{i = 1}^{N} \alpha_{i}
$$

$$
= - \frac{1}{2} \sum_{i = 1}^{N} \sum_{j = 1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) + \sum_{i = 1}^{N} \alpha_{i}
$$

即  
$\underset{\mathbf{\mathit{w}} , b}{min} L \left(\mathbf{\mathit{w}} , b , \mathbf{\mathit{\alpha}}\right) = - \frac{1}{2} \sum_{i = 1}^{N} \sum_{j = 1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) + \sum_{i = 1}^{N} \alpha_{i}$

求 $\underset{\mathbf{\mathit{w}} , b}{min} L \left(\mathbf{\mathit{w}} , b , \mathbf{\mathit{\alpha}}\right)$ 对 $\mathbf{\mathit{\alpha}}$ 的极大，即是对偶问题

$$
\underset{\mathbf{\mathit{\alpha}}}{max} - \frac{1}{2} \sum_{i = 1}^{N} \sum_{j = 1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) + \sum_{i = 1}^{N} \alpha_{i}
$$

$$
s . t . \sum_{i = 1}^{N} \alpha_{i} y_{i} = 0
$$

$$
\alpha_{i} \geq 0 , i = 1 , 2 , . . . , N
$$

把目标式子加一个负号，将求解极大转换为求解极小

$$
\underset{\mathbf{\mathit{\alpha}}}{min} \frac{1}{2} \sum_{i = 1}^{N} \sum_{j = 1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) - \sum_{i = 1}^{N} \alpha_{i}
$$

$$
s . t . \sum_{i = 1}^{N} \alpha_{i} y_{i} = 0
$$

$$
\alpha_{i} \geq 0 , i = 1 , 2 , . . . , N
$$

现在我们的优化问题变成了如上的形式。对于这个问题，我们有更高效的优化算法，即 [序列最小优化](https://zhida.zhihu.com/search?content_id=4943635&content_type=Article&match_order=1&q=%E5%BA%8F%E5%88%97%E6%9C%80%E5%B0%8F%E4%BC%98%E5%8C%96&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3ODMxMzU0MzQsInEiOiLluo_liJfmnIDlsI_kvJjljJYiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjo0OTQzNjM1LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.atV6o0_g6N9Uyiv0NPszuA237m2--loMWlhIzxWTgiM&zhida_source=entity) （SMO）算法。这里暂时不展开关于使用SMO算法求解以上优化问题的细节，下一篇文章再加以详细推导。

我们通过这个优化算法能得到 $\mathbf{\mathit{\alpha}}^{*}$ ，再根据 $\mathbf{\mathit{\alpha}}^{*}$ ，我们就可以求解出 $\mathbf{\mathit{w}}$ 和 $b$ ，进而求得我们最初的目的：找到超平面，即”决策平面”。

前面的推导都是假设满足KKT条件下成立的，KKT条件如下

$$
\begin{cases} \alpha_{i} \geq 0 \\ y_{i} \left(\mathbf{\mathit{w}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) - 1 \geq 0 \\ \alpha_{i} \left(y_{i} \left(\mathbf{\mathit{w}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) - 1\right) = 0 \end{cases}
$$

另外，根据前面的推导，还有下面两个式子成立

$$
\mathbf{\mathit{w}} = \sum_{i = 1}^{N} \alpha_{i} y_{i} \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}}
$$

$$
\sum_{i = 1}^{N} \alpha_{i} y_{i} = 0
$$

由此可知在 $\mathbf{\mathit{\alpha}}^{*}$ 中，至少存在一个 $\alpha_{j}^{*} > 0$ （反证法可以证明，若全为0，则 $\mathbf{\mathit{w}} = 0$ ，矛盾），对此 $j$ 有

$$
y_{j} \left(\mathbf{\mathit{w}}^{*} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}} + b^{*}\right) - 1 = 0
$$

因此可以得到

$$
\mathbf{\mathit{w}}^{*} = \sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} \mathbf{\mathit{x}}_{i}
$$

$$
b^{*} = y_{j} - \sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right)
$$

对于任意训练样本 $\left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} , y_{i}\right)$ ，总有 $\alpha_{i} = 0$ 或者 $y_{j} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{j} + b\right) = 1$ 。若 $\alpha_{i} = 0$ ，则该样本不会在最后求解模型参数的式子中出现。若 $\alpha_{i} > 0$ ，则必有 $y_{j} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}} + b\right) = 1$ ，所对应的样本点位于最大间隔边界上，是一个支持向量。这显示出支持向量机的一个重要性质： **训练完成后，大部分的训练样本都不需要保留，最终模型仅与支持向量有关。**

到这里都是基于训练集数据线性可分的假设下进行的，但是实际情况下几乎不存在完全线性可分的数据，为了解决这个问题，引入了“ [软间隔](https://zhida.zhihu.com/search?content_id=4943635&content_type=Article&match_order=1&q=%E8%BD%AF%E9%97%B4%E9%9A%94&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3ODMxMzU0MzQsInEiOiLova_pl7TpmpQiLCJ6aGlkYV9zb3VyY2UiOiJlbnRpdHkiLCJjb250ZW50X2lkIjo0OTQzNjM1LCJjb250ZW50X3R5cGUiOiJBcnRpY2xlIiwibWF0Y2hfb3JkZXIiOjEsInpkX3Rva2VuIjpudWxsfQ.Fqeq2jeA_cz8GEKfI_09b1Wm4bELja2LKaMGmGpWICo&zhida_source=entity) ”的概念，即允许某些点不满足约束

$$
y_{j} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}} + b\right) \geq 1
$$

采用 [hinge损失](https://zhida.zhihu.com/search?content_id=4943635&content_type=Article&match_order=1&q=hinge%E6%8D%9F%E5%A4%B1&zd_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ6aGlkYV9zZXJ2ZXIiLCJleHAiOjE3ODMxMzU0MzQsInEiOiJoaW5nZeaNn-WksSIsInpoaWRhX3NvdXJjZSI6ImVudGl0eSIsImNvbnRlbnRfaWQiOjQ5NDM2MzUsImNvbnRlbnRfdHlwZSI6IkFydGljbGUiLCJtYXRjaF9vcmRlciI6MSwiemRfdG9rZW4iOm51bGx9.5dv4nCLOePnT3ILa_LPcTLA7s6I2cpr_uyt3chUlQGk&zhida_source=entity) ，将原优化问题改写为

$$
\underset{\mathbf{\mathit{w}} , b , \xi_{i}}{min} \frac{1}{2} \left\|\mathbf{\mathit{w}}\right\|^{2} + C \sum_{i = 1}^{m} \xi_{i}
$$

$$
s . t . y_{i} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right) \geq 1 - \xi_{i}
$$

$$
\xi_{i} \geq 0 , i = 1 , 2 , . . . , N
$$

其中 $\xi_{i}$ 为“松弛变量”， $\xi_{i} = max \left(0 , 1 - y_{i} \left(\mathbf{\mathit{w}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} + b\right)\right)$ ，即一个hinge损失函数。每一个样本都有一个对应的松弛变量，表征该样本不满足约束的程度。 $C > 0$ 称为惩罚参数， $C$ 值越大，对分类的惩罚越大。跟线性可分求解的思路一致，同样这里先用拉格朗日乘子法得到拉格朗日函数，再求其对偶问题。

综合以上讨论，我们可以得到 **线性支持向量机学习算法** 如下：

**输入** ：训练数据集 $T = \left\{\left(\mathbf{\mathit{x}}_{1} , y_{1}\right) , \left(\mathbf{\mathit{x}}_{1} , y_{1}\right) , . . . , \left(\mathbf{\mathit{x}}_{N} , y_{N}\right)\right\}$ 其中， $\mathbf{\mathit{x}}_{i} \in \mathbb{R}^{n}$ ， $y_{i} \in \left\{+ 1 , - 1\right\} , i = 1 , 2 , . . . N$ ；

**输出** ：分离超平面和分类决策函数

（1）选择惩罚参数 $C > 0$ ，构造并求解凸二次规划问题

$$
\underset{\mathbf{\mathit{\alpha}}}{min} \frac{1}{2} \sum_{i = 1}^{N} \sum_{j = 1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) - \sum_{i = 1}^{N} \alpha_{i}
$$

$$
s . t . \sum_{i = 1}^{N} \alpha_{i} y_{i} = 0
$$

$$
0 \leq \alpha_{i} \leq C , i = 1 , 2 , . . . , N
$$

得到最优解 $\mathbf{\mathit{\alpha}}^{*} = \left(\alpha_{1}^{*} , \alpha_{2}^{*} , . . . , \alpha_{N}^{*}\right)^{T}$

（2）计算

$$
\mathbf{\mathit{w}}^{*} = \sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} \mathbf{\mathit{x}}_{i}
$$

选择 $\mathbf{\mathit{\alpha}}^{*}$ 的一个分量 $\alpha_{j}^{*}$ 满足条件 $0 < \alpha_{j}^{*} < C$ ，计算

$$
b^{*} = y_{j} - \sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} \cdot \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right)
$$

（3）求分离超平面

$$
\mathbf{\mathit{w}}^{*} \cdot \mathbf{\mathit{x}} + b^{*} = 0
$$

分类决策函数：

$$
f \left(\mathbf{\mathit{x}}\right) = s i g n \left(\mathbf{\mathit{w}}^{*} \cdot \mathbf{\mathit{x}} + b^{*}\right)
$$

## 非线性SVM算法原理

对于输入空间中的非线性分类问题，可以通过非线性变换将它转化为某个维特征空间中的线性分类问题，在高维特征空间中学习线性支持向量机。由于在线性支持向量机学习的对偶问题里，目标函数和分类决策函数都 **只涉及实例和实例之间的内积，所以不需要显式地指定非线性变换** ， **而是用核函数替换当中的内积** 。核函数表示，通过一个非线性转换后的两个实例间的内积。具体地， $K \left(x , z\right)$ 是一个函数，或正定核，意味着存在一个从输入空间到特征空间的映射 $\phi \left(x\right)$ ，对任意输入空间中的 $x , z$ ，有

$$
K \left(x , z\right) = \phi \left(x\right) \cdot \phi \left(z\right)
$$

在线性支持向量机学习的对偶问题中，用核函数 $K \left(x , z\right)$ 替代内积，求解得到的就是非线性支持向量机

$$
f \left(x\right) = s i g n \left(\sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} K \left(x , x_{i}\right) + b^{*}\right)
$$

综合以上讨论，我们可以得到 **非线性支持向量机学习算法** 如下：

**输入** ：训练数据集 $T = \left\{\left(\mathbf{\mathit{x}}_{1} , y_{1}\right) , \left(\mathbf{\mathit{x}}_{1} , y_{1}\right) , . . . , \left(\mathbf{\mathit{x}}_{N} , y_{N}\right)\right\}$ 其中， $\mathbf{\mathit{x}}_{i} \in \mathbb{R}^{n}$ ， $y_{i} \in \left\{+ 1 , - 1\right\} , i = 1 , 2 , . . . N$ ；

**输出** ：分离超平面和分类决策函数

（1）选取适当的核函数 $K \left(x , z\right)$ 和惩罚参数 $C > 0$ ，构造并求解凸二次规划问题

$$
\underset{\mathbf{\mathit{\alpha}}}{min} \frac{1}{2} \sum_{i = 1}^{N} \sum_{j = 1}^{N} \alpha_{i} \alpha_{j} y_{i} y_{j} K \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} , \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right) - \sum_{i = 1}^{N} \alpha_{i}
$$

$$
s . t . \sum_{i = 1}^{N} \alpha_{i} y_{i} = 0
$$

$$
0 \leq \alpha_{i} \leq C , i = 1 , 2 , . . . , N
$$

得到最优解 $\mathbf{\mathit{\alpha}}^{*} = \left(\alpha_{1}^{*} , \alpha_{2}^{*} , . . . , \alpha_{N}^{*}\right)^{T}$

（2）计算

选择 $\mathbf{\mathit{\alpha}}^{*}$ 的一个分量 $\alpha_{j}^{*}$ 满足条件 $0 < \alpha_{j}^{*} < C$ ，计算

$$
b^{*} = y_{j} - \sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} K \left(\mathbf{\mathit{x}}_{\mathbf{\mathit{i}}} , \mathbf{\mathit{x}}_{\mathbf{\mathit{j}}}\right)
$$

（3）分类决策函数：

$$
f \left(x\right) = s i g n \left(\sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} K \left(x , x_{i}\right) + b^{*}\right)
$$

介绍一个常用的核函数—— **高斯核函数**

$$
K \left(x , z\right) = exp \left(- \frac{\left\|x - z\right\|^{2}}{2 \sigma^{2}}\right)
$$

对应的SVM是高斯径向基函数分类器，在此情况下，分类决策函数为

$$
f \left(x\right) = s i g n \left(\sum_{i = 1}^{N} \alpha_{i}^{*} y_{i} exp \left(- \frac{\left\|x - z\right\|^{2}}{2 \sigma^{2}}\right) + b^{*}\right)
$$

## 参考

\[1\]《统计学习方法》 李航

\[2\]《机器学习》周志华

\[3\] [Python3《机器学习实战》学习笔记（八）：支持向量机原理篇之手撕线性SVM](https://link.zhihu.com/?target=http%3A//blog.csdn.net/c406495762/article/details/78072313%232-smo%25E7%25AE%2597%25E6%25B3%2595) [Jack-Cui](https://link.zhihu.com/?target=http%3A//blog.csdn.net/c406495762)

\[4\] [深入理解拉格朗日乘子法（Lagrange Multiplier) 和KKT条件](https://link.zhihu.com/?target=http%3A//blog.csdn.net/xianlingmao/article/details/7919597)

\[5\] [支持向量机通俗导论（理解SVM的三层境界）](https://link.zhihu.com/?target=http%3A//blog.csdn.net/v_july_v/article/details/7624837)

\[6\] [Support Vector Machines for Classification](https://link.zhihu.com/?target=https%3A//mubaris.com/2017/10/14/svm-python/)
