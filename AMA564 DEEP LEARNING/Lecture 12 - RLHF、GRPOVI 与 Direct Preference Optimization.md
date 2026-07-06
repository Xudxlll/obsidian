# Lecture 12 - RLHF、GRPOVI 与 Direct Preference Optimization

> [!info] 资料来源
> - 课件：`Lecture12.pdf`
> - 本笔记只依据 PDF 整理。
> - 本讲延续 RLHF，重点讲 PPO/GRPO、reward variance increase、GRPOVI，以及 Direct Preference Optimization（DPO）。

# 一、本讲的整体地图

## 1.1 PDF 页码索引

| PDF 页码 | 内容 | 学习重点 |
|---|---|---|
| p.1-p.11 | InstructGPT、human preferences、policy gradient、RLHF overview | RLHF 用 reward model 优化人类偏好 |
| p.12-p.18 | Accelerate RLHF with Variance Increase | reward variance 与 RLHF 训练速度有关 |
| p.19-p.27 | Reward adjustment model | 保持 boundedness、expectation、relative preferences，同时增加 variance |
| p.28-p.37 | Enumeration search 与 one-pass search | 从 $O(n^2)$ 到 $O(n)$ 的求解算法 |
| p.38-p.44 | GRPOVI 与实验 | 将 reward adjustment 集成进 GRPO |
| p.45-p.57 | Direct Preference Optimization | 用数学推导绕开显式 reward model/RL 训练 |
| p.58-p.63 | DPO vs PPO | DPO 更简单，但也有适用边界和 reward hacking 讨论 |

# 二、RLHF 回顾

## 2.1 InstructGPT 与人类偏好

对应 PDF：p.2-p.11

InstructGPT 的目标是让语言模型更好地遵循人类指令。Instruction fine-tuning 可以让模型学会任务格式，但模型是否真正符合人类偏好，还需要额外优化。

RLHF（Reinforcement Learning with Human Feedback）使用人类偏好数据训练 reward model，再用强化学习调整 policy model。

一般流程：

$$
\text{SFT model}
\rightarrow
\text{collect preference data}
\rightarrow
\text{train reward model}
\rightarrow
\text{RL fine-tuning}
$$

## 2.2 Policy gradient 的基本直觉

对应 PDF：p.4-p.5

给定 prompt $x$，模型策略为：

$$
\pi_\theta(y\mid x)
$$

reward model 给 response $y$ 打分：

$$
r(x,y)
$$

优化目标是让高 reward response 的概率更高：

$$
\max_\theta
\mathbb{E}_{y\sim\pi_\theta(\cdot\mid x)}
[r(x,y)]
$$

Policy gradient 的直觉：高奖励样本增强，低奖励样本削弱。

# 三、RLHF 中 PPO 与 GRPO

## 3.1 PPO 与 GRPO

对应 PDF：p.12-p.15

课件比较 popular RLHF methods：PPO 和 GRPO。

PPO（Proximal Policy Optimization）是 RLHF 中常见强化学习方法，但计算成本较高。

GRPO（Group Relative Policy Optimization）在一些大模型推理训练中表现出与 PPO 相近的效果，同时计算成本较低。但课件指出，GRPO 在训练后期可能变慢。

问题变成：

> 如何加速 GRPO？

## 3.2 Reward variance 的作用

对应 PDF：p.16-p.18

课件提出：accuracy 和 reward variance 都会影响 RLHF 训练。更高的 reward variance 可以加速训练。

RLHF objective 可以写成：

$$
\mathbb{E}_{x\sim\mathcal{D}}
\mathbb{E}_{y\sim\pi_\theta(\cdot\mid x)}
\left[
r(x,y)
-
\lambda D_{\mathrm{KL}}
(\pi_\theta(\cdot\mid x)\|\pi_{\mathrm{ref}}(\cdot\mid x))
\right]
$$

其中 KL 项限制新 policy 不要偏离 reference policy 太多。

课件中的自然想法是：在保持合理约束的前提下，调整 reward，使每个 prompt 下的 response reward variance 增大。

# 四、Reward Adjustment Model

## 4.1 调整 reward 的要求

对应 PDF：p.19-p.21

对于同一个 prompt $x$，模型产生一组 responses：

$$
y_1,\ldots,y_n
$$

原始 reward 为：

$$
r(x,y_i)
$$

目标是调整成：

$$
\tilde{r}(x,y_i)
$$

但必须满足三个要求：

1. 保持有界性（Boundedness）；
2. 保持期望（Preserve Reward Expectation）；
3. 保持相对偏好（Preserve Relative Preferences）。

如果原 reward 排序为：

$$
r(x,y_1)\ge r(x,y_2)\ge\cdots\ge r(x,y_n)
$$

调整后也要保持：

$$
z_1\ge z_2\ge\cdots\ge z_n
$$

## 4.2 优化模型

对应 PDF：p.22-p.23

课件提出 reward adjustment model：

$$
\max_{z\in\mathbb{R}^n}
f(z)=\sum_{i=1}^{n}p_i z_i^2
$$

约束包括：

Boundedness：

$$
m\le z_i\le M
$$

Reward expectation：

$$
\sum_{i=1}^{n}p_i z_i
=
\sum_{i=1}^{n}p_i r_i
$$

Relative preferences：

$$
z_i\ge z_{i+1}
$$

其中：

$$
p_i=\pi_{\theta_0}(y_i\mid x)
$$

目标函数 $\sum p_i z_i^2$ 与二阶矩相关，在期望固定时，增加二阶矩等价于增加方差。

## 4.3 方差增加保证

对应 PDF：p.23

课件给出 theorem：如果调整后的 rewards 是 reward adjustment model 的全局最优解，则 policy model 在该 prompt 的 response space 上的 reward variance 可以增加。

这意味着 reward adjustment 不是随意拉大奖励，而是在保持边界、期望和排序的约束下系统性增大训练信号差异。

# 五、求解算法

## 5.1 极点结构

对应 PDF：p.24-p.27

课件指出 reward adjustment model 是非凸优化，通常 NP-hard，但其可行域是有界非空多面体（Polyhedral），目标函数是凸函数。

全局最优解会出现在极点（Extreme Points）上。

极点可以写成特殊结构：

$$
v_1=\cdots=v_k=M
$$

$$
v_{k+1}=\cdots=v_l=\alpha
$$

$$
v_{l+1}=\cdots=v_n=m
$$

其中中间值：

$$
\alpha=
\frac{
\sum_{i=1}^{n}p_ir_i
-M\sum_{i=1}^{k}p_i
-m\sum_{i=l+1}^{n}p_i
}
{\sum_{i=k+1}^{l}p_i}
$$

这个结构是后续算法设计的基础。

## 5.2 Enumeration search

对应 PDF：p.28-p.31

枚举搜索（Enumeration Search）枚举 $k$ 和 $l$：

- 内层枚举 $l$；
- 外层枚举 $k$。

复杂度为：

$$
O(n^2)
$$

它可以找到全局最优解，但当 response 数量变多时成本较高。

## 5.3 One-pass search

对应 PDF：p.32-p.37

课件进一步提出 one-pass search，从两端向中间搜索。利用两个性质：

1. 一旦某个方向上的解不可行，后续同方向解都不可行；
2. 若解可行，目标函数值沿搜索方向单调增加。

因此可以把求解复杂度降到：

$$
O(n)
$$

如果 rewards 没有预排序，需要先排序，成本为：

$$
O(n\log n)
$$

# 六、GRPOVI

## 6.1 将 variance increase 集成进 GRPO

对应 PDF：p.38-p.40

GRPOVI 表示 GRPO with Reward Variance Increase。它把 reward adjustment model 集成到标准 GRPO 中。

流程可以理解为：

1. 当前 policy model 生成 responses；
2. reward model 给 responses 打分；
3. 对同一 prompt 下的 response rewards 做 adjustment；
4. 用调整后的 rewards 更新 policy model。

课件指出：

- responses 来自当前 policy model；
- probabilities 来自 initial policy model 或 reference policy model；
- reward variance increase 的保证可以自然得到。

## 6.2 实验

对应 PDF：p.41-p.44

课件展示两类实验：

1. 搜索算法比较；
2. 原始 GRPO 和 GRPOVI 在 LLM RLHF training 中的比较。

模型例子包括 Pythia-1B policy model，以及 GRM-Gemma-2-2B、GRM-Llama-3.2-3B reward models。

学习重点：GRPOVI 的目标不是改变 RLHF 的最终任务，而是通过调整 reward variance 提升训练效率。

# 七、Direct Preference Optimization

## 7.1 DPO 的动机

对应 PDF：p.45-p.52

直接偏好优化（Direct Preference Optimization, DPO）试图摆脱显式 reward model 和复杂 RL 训练。

课件说：You can get your optimal policy with math。也就是说，在某些假设下，可以从 RLHF 的最优 policy 闭式表达推出一个直接用偏好数据训练的 loss。

传统 RLHF：

$$
\text{preference data}
\rightarrow
\text{reward model}
\rightarrow
\text{RL optimization}
$$

DPO：

$$
\text{preference data}
\rightarrow
\text{direct policy optimization}
$$

## 7.2 DPO Loss

对应 PDF：p.53-p.54

DPO 使用成对偏好数据：

$$
(x,y_w,y_l)
$$

其中 $y_w$ 是 preferred response，$y_l$ 是 less preferred response。

DPO loss 常见形式为：

$$
\mathcal{L}_{\mathrm{DPO}}(\pi_\theta;\pi_{\mathrm{ref}})
=
-\mathbb{E}
\left[
\log\sigma
\left(
\beta
\log
\frac{\pi_\theta(y_w\mid x)}
{\pi_{\mathrm{ref}}(y_w\mid x)}
-
\beta
\log
\frac{\pi_\theta(y_l\mid x)}
{\pi_{\mathrm{ref}}(y_l\mid x)}
\right)
\right]
$$

直觉是：相比 reference policy，当前 policy 应该提高 preferred response 的相对概率，降低 rejected response 的相对概率。

## 7.3 DPO 的表现与流行

对应 PDF：p.55-p.57

课件提到 DPO performs better，并且 DPO is popular。它流行的原因是：

- 不需要单独训练 reward model；
- 不需要显式运行复杂 RL；
- 训练形式更接近监督学习；
- 实现相对简单。

## 7.4 DPO vs PPO

对应 PDF：p.58-p.63

PPO 是基于 RL 的 policy optimization，需要 reward model 和 RL loop。DPO 直接用偏好对优化 policy。

比较：

| 方法 | 是否需要 Reward Model | 是否需要 RL Loop | 优点 | 风险 |
|---|---|---|---|---|
| PPO | 需要 | 需要 | 经典 RLHF 方法，灵活 | 复杂、成本高、可能 reward hacking |
| DPO | 不需要显式 reward model | 不需要传统 RL loop | 简单稳定 | 依赖偏好数据质量，适用假设需注意 |

Reward hacking 指模型学会利用 reward model 的漏洞，而不是真正提升人类偏好质量。DPO 尝试减少这类复杂性，但并不代表偏好数据和目标设计不重要。

# 八、本讲复习抓手

## 8.1 必须掌握的概念

- RLHF：用人类偏好训练 reward model，并用 RL 优化 policy。
- PPO：常见 RLHF policy optimization 方法。
- GRPO：相对更省资源的 group relative policy optimization。
- Reward Variance：同一 prompt 下不同 response reward 的差异程度。
- Reward Adjustment：在保持边界、期望、排序的同时增加 variance。
- GRPOVI：把 reward variance increase 集成进 GRPO。
- DPO：直接用偏好对优化 policy，绕开显式 reward model 和 RL loop。
- Reward Hacking：模型利用 reward 设计漏洞获得高分。

## 8.2 关键公式

RLHF objective：

$$
\mathbb{E}_{x\sim\mathcal{D}}
\mathbb{E}_{y\sim\pi_\theta(\cdot\mid x)}
\left[
r(x,y)
-
\lambda D_{\mathrm{KL}}
(\pi_\theta(\cdot\mid x)\|\pi_{\mathrm{ref}}(\cdot\mid x))
\right]
$$

Reward adjustment objective：

$$
\max_z\sum_{i=1}^{n}p_i z_i^2
$$

Expectation constraint：

$$
\sum_{i=1}^{n}p_i z_i
=
\sum_{i=1}^{n}p_i r_i
$$

DPO loss：

$$
\mathcal{L}_{\mathrm{DPO}}
=
-\mathbb{E}
\left[
\log\sigma
\left(
\beta\log
\frac{\pi_\theta(y_w\mid x)}
{\pi_{\mathrm{ref}}(y_w\mid x)}
-
\beta\log
\frac{\pi_\theta(y_l\mid x)}
{\pi_{\mathrm{ref}}(y_l\mid x)}
\right)
\right]
$$

## 8.3 本讲一句话

Lecture 12 重点不是重新解释 RLHF，而是进一步研究如何让 RLHF 训练更快、更稳定：GRPOVI 通过增加 reward variance 加速 GRPO，DPO 则用偏好数据直接优化 policy，减少显式 reward model 和 RL loop 的复杂性。
