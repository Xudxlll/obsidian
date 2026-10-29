> [!info] 资料来源
> - 课件：`Lecture12.pdf`
> - 本文件夹中的原始课件：[[Lecture12.pdf]]。
> - 笔记以课件为主，并包含为理解和准确性补充的说明；扩展解释不代表课件逐字原文。
> - 本讲延续 RLHF，重点讲 PPO/GRPO、reward variance increase、GRPOVI，以及 Direct Preference Optimization（DPO）。

# 一、本讲的整体地图

## 1. PDF 页码索引

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

## 1. InstructGPT 与人类偏好

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

## 2. Policy gradient 的基本直觉

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

Policy gradient 的直觉：相对基线优势为正的样本倾向于被增强，优势为负的样本倾向于被削弱；具体概率变化还取决于参数共享和优化过程。

# 三、RLHF 中 PPO 与 GRPO

## 1. PPO 与 GRPO

对应 PDF：p.12-p.15

课件比较 popular RLHF methods：PPO 和 GRPO。

PPO（Proximal Policy Optimization）是 RLHF 中常见强化学习方法，但计算成本较高。

GRPO（Group Relative Policy Optimization）在一些大模型推理训练中表现出与 PPO 相近的效果，同时计算成本较低。但课件指出，GRPO 在训练后期可能变慢。

问题变成：

> 如何加速 GRPO？

## 2. Reward variance 的作用

对应 PDF：p.16-p.18

课件引用的研究指出，reward model 的准确性和初始策略下的 reward variance 都与训练效率有关。在所研究的设定中，增大方差是潜在加速思路，但并不保证任意任务、奖励函数或训练配置都会更快。课件第 17 页给出的是达到指定奖励提升所需时间的**下界**；仅凭下界随方差下降，不能单独推断实际训练时间必然下降。

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

## 1. 调整 reward 的要求

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

这个非严格排序约束允许原本分数相同的响应在调整后出现不同分数；若业务要求并列偏好仍相等，需要额外加入对应等式约束。

## 2. 优化模型

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

目标函数 $\sum p_i z_i^2$ 是该组响应对二阶矩的贡献。在按课件定义只修改这组响应、其他响应的 reward 保持不变，且按同一策略概率加权保持全空间期望的前提下，增加这一项等价于增加全空间方差；这组概率不必加总为 1。

## 3. 方差增加保证

对应 PDF：p.23

[课件引用的论文](https://arxiv.org/abs/2505.23247)给出 theorem：若这组响应的权重取自所考察策略、其他响应奖励不变，且调整结果是模型的全局最优解，则相应策略下的全响应空间方差不低于原值。原奖励向量本身可行，所以方差未必严格增加：例如原值已是最优时可以相等。

这意味着 reward adjustment 不是随意拉大奖励，而是在保持边界、期望和排序的约束下系统性增大训练信号差异。

# 五、求解算法

## 1. 极点结构

对应 PDF：p.24-p.27

课件指出 reward adjustment model 是非凸优化，通常 NP-hard，但其可行域是有界非空多面体（Polyhedral），目标函数是凸函数。

至少存在一个极点（Extreme Point）是全局最优解。凸函数在多面体上最大化虽一般困难，但课件随后利用这个问题的特殊结构给出高效解法。

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

其中公式要求中间块非空且其权重和为正；若 $k=l$，中间块为空，需单独检查仅由 $M$ 和 $m$ 组成的可行极点，不能代入零分母。这个结构是后续算法设计的基础。

## 2. Enumeration search

对应 PDF：p.28-p.31

枚举搜索（Enumeration Search）枚举 $k$ 和 $l$：

- 内层枚举 $l$；
- 外层枚举 $k$。

复杂度为：

$$
O(n^2)
$$

它可以找到全局最优解，但当 response 数量变多时成本较高。

## 3. One-pass search

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

## 1. 将 variance increase 集成进 GRPO

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
- 论文中的初始策略被设为 reference policy；保证针对这一策略下的奖励方差，不能直接推广成当前策略下的相同保证。

## 2. 实验

对应 PDF：p.41-p.44

课件展示两类实验：

1. 搜索算法比较；
2. 原始 GRPO 和 GRPOVI 在 LLM RLHF training 中的比较。

模型例子包括 Pythia-1B policy model，以及 GRM-Gemma-2-2B、GRM-Llama-3.2-3B reward models。

学习重点：GRPOVI 的目标不是改变 RLHF 的最终任务，而是通过调整 reward variance 提升训练效率。

# 七、Direct Preference Optimization

## 1. DPO 的动机

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

## 2. DPO Loss

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

直觉是：相比 reference policy，优化会推动偏好回答相对于非偏好回答的概率比上升；这不保证每一次更新中偏好回答的绝对概率一定上升，或非偏好回答的绝对概率一定下降。

## 3. DPO 的表现与流行

对应 PDF：p.55-p.57

课件展示特定实验中 DPO 的表现并介绍其流行原因；不同数据、模型和评估指标下，DPO 不保证普遍优于 PPO。它常被采用的原因是：

- 不需要单独训练 reward model；
- 不需要显式运行复杂 RL；
- 训练形式更接近监督学习；
- 实现相对简单。

## 4. DPO vs PPO

对应 PDF：p.58-p.63

PPO 是基于 RL 的 policy optimization，需要 reward model 和 RL loop。DPO 直接用偏好对优化 policy。

比较：

| 方法 | 是否需要 Reward Model | 是否需要 RL Loop | 优点 | 风险 |
|---|---|---|---|---|
| PPO | 需要 | 需要 | 经典 RLHF 方法，灵活 | 复杂、成本高、可能 reward hacking |
| DPO | 不需要显式 reward model | 不需要传统 RL loop | 简单稳定 | 依赖偏好数据质量，适用假设需注意 |

Reward hacking 指模型学会利用 reward model 的漏洞，而不是真正提升人类偏好质量。DPO 尝试减少这类复杂性，但并不代表偏好数据和目标设计不重要。

# 八、本讲复习抓手

## 1. 必须掌握的概念

- RLHF：用人类偏好训练 reward model，并用 RL 优化 policy。
- PPO：常见 RLHF policy optimization 方法。
- GRPO：相对更省资源的 group relative policy optimization。
- Reward Variance：同一 prompt 下不同 response reward 的差异程度。
- Reward Adjustment：在保持边界、期望、排序的同时增加 variance。
- GRPOVI：把 reward variance increase 集成进 GRPO。
- DPO：直接用偏好对优化 policy，绕开显式 reward model 和 RL loop。
- Reward Hacking：模型利用 reward 设计漏洞获得高分。

## 2. 关键公式

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

## 3. 本讲一句话

Lecture 12 重点不是重新解释 RLHF，而是进一步研究如何让 RLHF 训练更快、更稳定：GRPOVI 尝试通过增加初始策略下的 reward variance 加速 GRPO，DPO 则用偏好数据直接优化 policy，减少显式 reward model 和 RL loop 的复杂性。

# 九、补充学习注释与复习路线

## 1. 本讲怎么读

这一讲对应 PDF：p.1-p.63。它比上一讲更深入 RLHF，并进一步介绍 GRPOVI 和 Direct Preference Optimization（DPO）。这讲的重点不是背新缩写，而是理解：**人类偏好如何被转成可优化目标。**

推荐读法：

1. p.1-p.11：复习 InstructGPT、human preferences、policy gradient 和 RLHF pipeline。
2. p.12-p.44：理解通过 reward variance adjustment 加速 RLHF，以及 GRPOVI 如何整合这一思路。
3. p.45-p.63：重点读 DPO，理解它如何绕开显式 reward model 和复杂 RL 训练。

RLHF 的基本链条是：

$$
\text{human preference}\rightarrow r_\phi(x,y)\rightarrow \text{policy optimization}
$$

其中 $r_\phi$ 是奖励模型（Reward Model），$\pi_\theta$ 是要优化的语言模型策略（Policy）。policy gradient 的基本直觉是：相对基线优势为正的输出获得正向更新，优势为负的输出获得负向更新。

p.12-p.27 讨论 reward variance。直观上，如果所有候选回答 reward 很接近，优化信号就弱；如果 reward 差异更清楚，模型更容易知道哪个方向好。但 reward adjustment 又不能随意破坏偏好顺序，因此需要保持 relative preferences、boundedness 和 expectation 等性质。

p.28-p.44 的搜索算法可以看成把理论约束落到可计算过程。Enumeration search 从候选空间里找满足条件的调整，代价可能较高；one-pass search 则试图用一次扫描降低复杂度。GRPOVI 把这个 reward adjustment 思想放进 GRPO 中，旨在提高偏好优化效率；效果需要在具体任务中检验。

DPO 对应 p.45-p.63，是本讲最适合反复推导的部分。它从偏好数据出发：给定同一个 prompt，$y_w$ 是 preferred response，$y_l$ 是 dispreferred response。DPO 的目标可以写成让模型相对于 reference model 更偏向 $y_w$：

$$
\log \frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)}
-
\log \frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}
$$

这个差值越大，说明当前模型相对 reference 更倾向好回答。DPO 的优势是实现相对简单，不需要显式训练 reward model 后再跑 PPO；训练稳定性依数据与配置而定；但它仍依赖偏好数据质量，也不能自动解决所有 reward hacking 或分布外问题。

复习时可以这样区分：

| 方法 | 是否显式 reward model | 是否需要 RL 优化 | 直观特点 |
|---|---|---|---|
| PPO-style RLHF | 需要 | 需要 | pipeline 复杂，但表达灵活 |
| DPO | 不显式需要 | 不需要传统 RL | 直接用偏好对训练，形式更简单 |
| GRPOVI | 使用 reward adjustment 思想 | 与 GRPO 结合 | 关注提升优化信号效率 |

## 2. 做题和复习时的检查清单

- 能不能用自己的话解释本讲的核心问题，而不是只背模型名称。
- 看到公式时，能不能说清每个符号代表什么、输入输出是什么、优化目标是什么。
- 能不能把本讲内容和前后讲联系起来：它继承了什么问题，又为下一讲解决什么问题。
- 能不能分清概念、公式、训练流程和应用场景四个层次。
- 遇到 PDF 中的图或代码时，先判断它是在说明结构、说明训练，还是说明实验结果。

## 3. 结构层级示例

下面这个小节专门用于统一结构编号：在 Obsidian 阅读时，一级结构用中文编号，二级结构用阿拉伯编号，三级结构用层级编号。后续如果继续扩写某个二级标题，可以使用类似 `1.1.1` 的形式继续细分。

### 1.1.1 如何继续扩展本讲

- 如果扩展概念解释，可以放在对应二级标题下面，先写直观含义，再写公式或例子。
- 如果扩展公式推导，先说明目标，再逐步解释每一步变形。
- 如果扩展复习题，可以把题目、解题思路、常见错误分开放，避免把结论堆在一起。
