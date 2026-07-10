---
tags:
  - 深度学习
  - CNN
  - ResNet
  - 残差网络
  - 梯度消失
created: 2026-07-09
source: "[[Clippings/2026-07-09-三分钟动画讲解算法——残差思想 _ 是怎么实现的，解决了哪些深层网络的问题]]"
---
<iframe src="https://player.bilibili.com/player.html?aid=115240280786998&bvid=BV1aXpfzhEeW&cid=32525782631&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allow="fullscreen; picture-in-picture" allowfullscreen="true" style="height:100%;width:100%; aspect-ratio: 16 / 9;"> </iframe>

> 🎬 参考视频：[三分钟动画讲解算法——残差思想](https://www.bilibili.com/video/BV1aXpfzhEeW/)

<iframe src="https://player.bilibili.com/player.html?bvid=BV1WUUaBSEzx&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allow="fullscreen; picture-in-picture" allowfullscreen="true" style="height:100%;width:100%; aspect-ratio: 16 / 9;"> </iframe>

> 🎬 参考视频：[大白话讲明白ResNet残差网络](https://www.bilibili.com/video/BV1WUUaBSEzx/)

# 一、残差网络 ResNet 的核心思想

## 1.1 背景：网络越深，效果反而越差

直觉上，网络层数越多、参数量越大，模型的表达能力就应该越强。大语言模型参数量从 million 涨到 billion 之后甚至发生了质变。

但问题是：**仅堆叠网络层数，效果并不会变得更好，甚至还会更差**。

举个例子：假设一个 10 层网络准确率是 80%，再往上加 10 层。理论上，只要后 10 层学到**恒等变换**（输入什么就输出什么），准确率至少不会下降。但实际训练中准确率是**下降的**——因为让神经网络学到恒等变换本身就很难。

---

## 1.2 残差连接（Skip Connection）

传统网络是**串行**的：

```
输入 x → [卷积层1] → [卷积层2] → 输出 y = F(x)
```

ResNet 的做法非常「大道至简」：**从输入直接连一条线到输出，和卷积层的输出相加**。原文称之为 **shortcut**（抄近路）。

```
输入 x ──→ [卷积层1] → [卷积层2] → F(x) ──┬──→ 输出 y = F(x) + x
  │                                        │
  └──────────── shortcut ──────────────────┘
```

设中间两个卷积层为 $F(x)$，则：

- **传统网络**：$y = F(x)$，目标是让 $F(x)$ 逼近最优分布 $H(x)$
- **残差网络**：$y = F(x) + x$，模型不再直接学习 $H(x)$，而是学习**残差函数** $F(x) = H(x) - x$

> 这句话就是说：模型只需要学习「最优输出与输入之间的**差值**」，而不是从头学整个映射。

---

## 1.3 残差连接解决的两大问题

### 1.3.1 问题一：深层网络优化困难

回到 1.1 的例子：传统网络想让新增的 10 层学到恒等变换 $F(x) = x$，这很难。

但在残差网络中，恒等变换等价于让 $F(x) = 0$：

$$y = F(x) + x$$

当 $F(x) = 0$ 时，$y = x$，恒等变换自然成立。

而让网络输出零**在初始化阶段就可以做到**（权重初始化接近零即可）。从感性上理解：模型被给了一个相对合理的初值，只需要拟合出**相对于这个初值的变化量**，学习难度自然大幅降低。

#### Loss 曲面的直观对比

以下数据来自 [Loss Landscape 可视化](https://www.telesens.co/loss-landscape-viz/viewer.html)：

| 网络 | Loss 曲面特征 |
|------|-------------|
| VGG-16 | 曲面光滑，下降方向明确 |
| 56 层无 shortcut | 曲面**非常崎岖**，很难找到最优点 |
| 56 层加 shortcut | 曲面重新变得**光滑** |

**shortcut 让深层网络的优化难度大大降低，这才发挥出了大参数量的优势。**

---

### 1.3.2 问题二：梯度消失

根据链式求导法则，传统网络中层与层之间的梯度是**相乘**的关系。层数越多，越靠近输入端的浅层网络梯度消失的风险就越高。

在残差网络中，输出 $y = F(x) + x$ 对输入 $x$ 求导：

$$\frac{\partial y}{\partial x} = \frac{\partial F(x)}{\partial x} + 1$$

那多出来的 **$+1$** 就是关键——残差连接提供了一条**不受梯度衰减影响的高速通道**，让梯度在反向传播中可以更容易地传到浅层网络。

```
反向传播梯度流：
浅层 ←── 梯度(衰减严重) ←── 中层 ←── 梯度 ←── 深层
浅层 ←── 梯度(直达) ←──────── shortcut ────────── 深层
```

两条路径叠加，即使逐层传播的梯度衰减到很小，shortcut 通道仍然能把有效梯度传回浅层。

---

## 1.4 核心总结

| 维度 | 传统深层网络 | 残差网络 (ResNet) |
|------|------------|------------------|
| **学习目标** | $F(x) \to H(x)$ | $F(x) \to H(x) - x$（学残差） |
| **恒等映射** | 学到 $F(x)=x$，很难 | 学到 $F(x)=0$，初始化即可 |
| **优化难度** | 层数深时 loss 曲面崎岖 | shortcut 使曲面保持光滑 |
| **梯度传播** | 逐层相乘，浅层梯度消失 | shortcut 提供梯度高速通道 |

ResNet 的核心就一句话：**不要直接学答案，学答案与输入之间的差值。** 这个减法看似简单，却让网络层数首次突破了数百层，奠定了现代深层 CNN 的基础。

---

*笔记整理自 B站视频「三分钟动画讲解算法——残差思想」 by 祖安ADAS（2025-09-21）*
