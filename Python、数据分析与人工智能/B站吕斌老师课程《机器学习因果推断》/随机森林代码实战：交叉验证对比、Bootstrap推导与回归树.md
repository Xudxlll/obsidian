---
title: "随机森林代码实战：交叉验证对比、Bootstrap推导与回归树"
course: "B站吕斌老师课程《机器学习因果推断》"
teacher: "吕斌老师"
source_note: "未命名.md"
note_type: "学习笔记"
created: "2026-07-12"
updated: "2026-07-12"
tags: ["机器学习", "因果推断", "课程笔记", "吕斌老师", "随机森林"]
---
> [!info] 课程
> 随机森林代码实战：交叉验证对比、Bootstrap 推导与回归树应用

> [!info] 整理原则
> 本笔记根据课堂字幕整理，聚焦随机森林的代码实战环节——包括与决策树的交叉验证对比、Bootstrap 的数学推导（37% 袋外数据）、`predict_proba` 投票分析、回归树应用以及经济学案例。更多随机森林原理部分参见 [[04-随机森林原理与经济学应用]]，缺失值填补案例参见 [[05-随机森林实战案例：填补缺失数据、调参的艺术]]。

---

## 一、集成学习概述

### 1.1 什么是集成学习

**一句话说清**：集成学习就是把多个简单的基学习器组合在一起，变成一个更强的模型。其基本思路是「三个臭皮匠，顶一个诸葛亮」——建立很多底层决策树，让它们投票，少数服从多数，投票结果作为最终预测。

同样是红酒数据集，单棵决策树的准确率约 85%，换成随机森林后能稳定在 95% 以上，提升了约 10 个百分点。

### 1.2 集成学习的三大流派

集成学习算法大致分为三类：

| 流派 | 英文 | 核心思想 | 典型算法 |
|---|---|---|---|
| **单模型** | Single | 一个模型一次迭代，直接输出结果 | 决策树 |
| **袋装法** | Bagging | 并行训练多个基学习器，投票/平均 | 随机森林 |
| **提升法** | Boosting | 串行训练，每一轮聚焦前一轮的错题 | AdaBoost、XGBoost、CatBoost |

此外还有 **Stacking（堆叠法）**，属于更高级的集成方式，后续课程会涉及。

### 1.3 Bagging（袋装法）的工作方式

```
原始数据
    │
    ├── Bootstrap 抽样 → 训练子集 1 → 决策树 1 ──┐
    ├── Bootstrap 抽样 → 训练子集 2 → 决策树 2 ──┤
    ├── Bootstrap 抽样 → 训练子集 3 → 决策树 3 ──┤
    │         ...                                  ├── 投票（分类）/ 平均（回归）
    └── Bootstrap 抽样 → 训练子集 N → 决策树 N ──┘
```

每棵树用的特征也不一样（特征随机），所以每棵树「长得千差万别」，投票结果更可靠。

### 1.4 Boosting（提升法）的工作方式

Boosting 的底层逻辑就像**刷题**：

- **第一轮**：100 道题，做对 90 道，10 道没做对
- **第二轮**：专攻那 10 道没做对的题，又做对 4 道，剩 6 道
- **第三轮**：专攻那 6 道还没做对的题……

每一步拟合的都是**上一轮没预测准的部分**。对于分类问题，相当于对「顽固」的、多次预测错的样本**加大权重**——给它复制好多份，让模型更重视它。

凡是名字以 `boost` 结尾的算法（XGBoost、CatBoost、GradientBoosting），底层都是这个思路。

> **社科研究提醒**：老师强调，经济学研究不需要追求最前沿、最复杂的算法。算法越复杂、越黑箱化，越容易被审稿人质疑「是不是在操纵数据」。一个简单 DID 能做的，为什么用大语言模型？经济学讲求模型简单小巧、数据处理过程透明。**随机森林级别的算法对社科研究已经足够。**

---

## 二、随机森林 vs 单棵决策树：代码对比

### 2.1 建模三步走

sklearn 中决策树和随机森林的建模流程完全相同：

```python
# 第一步：实例化（生成空白模型）
clf = DecisionTreeClassifier()
rfc = RandomForestClassifier()

# 第二步：拟合（训练）
clf.fit(X_train, y_train)
rfc.fit(X_train, y_train)

# 第三步：评价（测试）
clf.score(X_test, y_test)
rfc.score(X_test, y_test)
```

决策树在 `sklearn.tree` 模块，随机森林在 `sklearn.ensemble` 模块——因为随机森林是集成学习算法。

### 2.2 红酒数据集上的直接对比

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

# 加载红酒数据
wine = load_wine()
X = wine.data
y = wine.target

# 切分训练集和测试集（7:3）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3
)

# 单棵决策树
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)
print(f"决策树: {clf.score(X_test, y_test):.4f}")

# 随机森林
rfc = RandomForestClassifier()
rfc.fit(X_train, y_train)
print(f"随机森林: {rfc.score(X_test, y_test):.4f}")
```

多次运行后，随机森林的准确率**始终明显高于**单棵决策树，平均高出约 8～15 个百分点。

> **注意**：如果不固定 `random_state`，训练集/测试集的切分每次不一样，结果会有波动。机器学习中很多环节都具有随机性——切分数据有随机性、决策树选特征有随机性、随机森林抽样有随机性。`random_state` 就是用来固定这些随机性，保证结果可复现。

### 2.3 交叉验证对比（10 折）

单次切分波动大，换成交叉验证更稳健：

```python
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

# 实例化两个模型
rfc = RandomForestClassifier()
clf = DecisionTreeClassifier()

# 10 折交叉验证
rfc_scores = cross_val_score(rfc, X, y, cv=10)
clf_scores = cross_val_score(clf, X, y, cv=10)

# 画图对比
plt.plot(range(1, 11), rfc_scores, 'o-', label='随机森林')
plt.plot(range(1, 11), clf_scores, 's-', label='决策树')
plt.xlabel('交叉验证折数')
plt.ylabel('准确率')
plt.legend()
plt.show()

print(f"随机森林平均: {rfc_scores.mean():.4f}")
print(f"决策树平均:   {clf_scores.mean():.4f}")
```

运行结果示例：

| 模型 | 各折准确率范围 | 平均准确率 |
|---|---|---|
| 随机森林 | 0.94 ～ 1.00 | ≈ 0.97 |
| 决策树 | 0.78 ～ 0.94 | ≈ 0.86 |

随机森林表现始终在 95% 以上，且波动更小；决策树波动剧烈，平均低了约 10 个百分点。

### 2.4 10 次 × 10 折交叉验证

如果想更严谨，可以在外层再套一层循环，做 **10 次 10 折交叉验证**（每次 10 折求平均，共得 10 个平均值）：

```python
rfc_means = []
clf_means = []

for i in range(10):
    rfc = RandomForestClassifier()
    clf = DecisionTreeClassifier()
    rfc_means.append(cross_val_score(rfc, X, y, cv=10).mean())
    clf_means.append(cross_val_score(clf, X, y, cv=10).mean())
```

求平均后波动明显减小，随机森林稳定在 0.97 附近，决策树稳定在 0.86 附近。

### 2.5 群体智慧为什么一定有效？（概率论证）

假设单棵决策树的准确率是 80%（即犯错概率 20%），森林中有 25 棵树。

只有当 **13 棵及以上的树同时犯错**，多数投票才会出错。这个概率用排列组合计算：

$$
P(\text{犯错}) = \sum_{i=13}^{25} C_{25}^{i} \times 0.2^{i} \times 0.8^{25-i}
$$

```python
import numpy as np

p_error = 0
for i in range(13, 26):
    p_error += np.math.comb(25, i) * (0.2 ** i) * (0.8 ** (25 - i))

print(f"集体犯错的概率: {p_error:.6f}")
# 输出: 0.000369（万分之三点七）
```

25 棵树时集体犯错概率仅 **万分之三**左右。单棵树 80% 的准确率看起来不高，但 25 棵组合后几乎不会集体犯错。

---

### 2.6 群体智慧的前提条件

群体智慧不是什么时候都有效。老师画了一张图来说明：

```python
import numpy as np
import matplotlib.pyplot as plt

def ensemble_error(p, n=25):
    """给定单棵树准确率 p，计算 n 棵树集体犯错的概率"""
    err = 0
    for i in range(int(np.ceil(n/2)), n+1):
        err += np.math.comb(n, i) * ((1-p)**i) * (p**(n-i))
    return err

# 不同单棵树准确率下的集成错误率
p_range = np.linspace(0.01, 0.99, 50)
errors = [ensemble_error(p) for p in p_range]

plt.plot(p_range, errors)
plt.axvline(x=0.5, color='red', linestyle='--', label='随机猜测 (0.5)')
plt.axvline(x=0.6, color='orange', linestyle='--', label='阈值 (~0.6)')
plt.xlabel('单棵决策树准确率')
plt.ylabel('集体犯错概率')
plt.legend()
plt.show()
```

**核心结论**：

- 单棵树准确率如果只有 0.5 左右（接近随机猜测），集成效果不会好
- 单棵树准确率**超过 0.6** 以后，集体犯错概率急剧下降
- 所以集成学习要求每个基分类器至少「比瞎猜好一些」，不能拿「文盲」来投票

> **直觉理解**：广泛听取意见是好的，但前提是听取的人有一定判断能力。让一群专家投票有效，让一群不懂的人投票无效。

---

## 三、n_estimators 参数与学习曲线

### 3.1 参数含义

`n_estimators` 是随机森林**最重要的参数**，代表森林中树的数量。

- 树越多 → 模型通常越好（集体犯错概率越低）
- 但树多到一定程度后 → 准确率趋于平稳，再增加只会浪费算力

### 3.2 学习曲线代码

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

super_scores = []
for i in range(1, 201):
    rfc = RandomForestClassifier(n_estimators=i, random_state=0)
    score = cross_val_score(rfc, X, y, cv=10).mean()
    super_scores.append(score)

# 找到最高分及对应的 n_estimators
best_score = max(super_scores)
best_n = super_scores.index(best_score) + 1  # +1 因为 index 从 0 开始

print(f"最高分: {best_score:.4f}, n_estimators: {best_n}")

# 画学习曲线
plt.figure(figsize=(10, 5))
plt.plot(range(1, 201), super_scores)
plt.axvline(x=best_n, color='red', linestyle='--')
plt.xlabel('n_estimators（树的数量）')
plt.ylabel('交叉验证准确率')
plt.show()
```

### 3.3 学习曲线的典型形状

学习曲线通常呈**先快速上升、后高位平稳**的形态：

- 树很少时（如 1～5 棵），准确率低（≈ 单棵决策树）
- 随树增加，准确率快速上升
- 到达某个拐点（如 40～50 棵）后趋于平稳
- 之后再增加树，准确率几乎不变

**选参原则**：在「够用即可」的拐点处取值。太小肯定不行，太大浪费算力。数据集越大、特征越多，需要的树也越多（可能上千棵）。

---

## 四、随机森林的双随机特性

这是随机森林**最核心的特性**，也是它比单棵决策树好的根本原因。

### 4.1 特征随机

每棵决策树在建模时，**不是用全部特征**，而是从全部特征中**随机选一部分**进行分裂。

> **例子**：原始有 10 个特征，第一棵树可能只用特征 1、3、4；第二棵树用特征 2、4、5；第三棵树用特征 3、4、5……每棵树选的特征都不一样。

**为什么要这么做？** 回想决策树章节讲的猫狗大战例子——如果所有猫恰好是黄色、所有狗恰好是白色，树会直接按「皮毛颜色」一刀切。但这个特征实际上是**巧合性的坏特征**。sklearn 通过「只让你看一部分特征」来防止模型对某个坏特征过拟合。

特征随机性越强 → 每棵树差异越大 → 集成效果越好。

### 4.2 样本随机（Bootstrap 自助采样）

除了特征不同，每棵树用的**训练样本也不一样**。

Bootstrap 的做法是**有放回的随机抽样**：

```
原始样本: [A, B, C, D, E]（5 个样本）

Tree 1 训练集: [A, A, C, D, E]   ← A 被抽了两次
Tree 2 训练集: [B, C, D, E, E]   ← E 被抽了两次，A 没抽到
Tree 3 训练集: [A, B, B, D, E]   ← B 被抽了两次，C 没抽到
```

有的样本被用了多次，有的样本一次也没被用到。

### 4.3 OOB（袋外数据）的数学推导

**关键结论**：有 **37%** 的样本一次都不会被抽中！

推导过程：

每次抽样时，某个特定样本**没被抽中**的概率是 $1 - \frac{1}{N}$（$N$ 是样本总数）。$N$ 次独立抽样后，该样本始终没被抽中的概率：

$$
\left(1 - \frac{1}{N}\right)^N
$$

当 $N \to \infty$ 时，这个极限：

$$
\lim_{N \to \infty} \left(1 - \frac{1}{N}\right)^N = \frac{1}{e}
$$

其中 $e \approx 2.71828$，所以 $\frac{1}{e} \approx 0.368 \approx 37\%$。

> **这意味着**：每棵树的训练过程中，有约 37% 的原始样本完全没有参与训练。这部分数据天然形成了一个「袋外测试集」。

#### OOB 的实际意义

这部分袋外数据叫 **Out of Bag（OOB）**，是随机森林特有的「免费」验证集：

| 传统做法 | OOB 做法 |
|---|---|
| 手动划分训练集 + 测试集 | 不需要手动划分 |
| `train_test_split(X, y, test_size=0.3)` | 直接用全部数据训练 |
| 测试集是固定的一份 | 每棵树都有自己天然的袋外测试集 |

### 4.4 Bootstrap 和 OOB Score 代码

```python
# 开启 bootstrap 和 oob_score
rfc = RandomForestClassifier(
    n_estimators=25,
    bootstrap=True,    # 是否使用有放回抽样
    oob_score=True,    # 是否使用袋外数据评估
    random_state=0
)

# 不需要手动划分训练集/测试集，直接用全部数据
rfc.fit(wine.data, wine.target)

# 查看袋外评分
print(f"OOB Score: {rfc.oob_score_:.4f}")
# 输出: 0.9775
```

> `bootstrap=True` 和 `oob_score=True` 一般配合使用。当 `bootstrap=True` 时，37% 的样本天然落在袋外，`oob_score=True` 就用这些袋外数据来评估模型。

### 4.5 双随机的总结

```
随机森林的随机性
├── 特征随机
│   └── 每次分裂从随机选的一部分特征中找最优
├── 样本随机
│   └── Bootstrap 有放回抽样生成每棵树的训练集
└── 效果
    └── 每棵树长得千差万别 → 集成效果好
```

当数据量大、特征多时，双随机的效果更有保障（每棵树的独立性更强）。反过来，如果只有 2 个特征或 10 个样本，随机性无从谈起，集成效果也打折扣。

---

## 五、随机森林的重要属性和方法

### 5.1 查看森林中的每一棵树

```python
rfc = RandomForestClassifier(n_estimators=25, max_depth=3, random_state=0)
rfc.fit(X_train, y_train)

# rfc.estimators_ 返回森林中所有树的列表
for i, tree in enumerate(rfc.estimators_[:3]):
    print(f"Tree {i}: random_state={tree.random_state}")
```

每棵树的 `random_state` 都不一样，印证了特征随机的特性——每棵树看到的是不同的特征子集。

### 5.2 特征重要性

```python
# 特征名和重要性一一对应
feature_importance = [*zip(wine.feature_names, rfc.feature_importances_)]
for name, imp in sorted(feature_importance, key=lambda x: x[1], reverse=True):
    print(f"{name}: {imp:.4f}")
```

和决策树一样，随机森林也能告诉你哪些特征对预测贡献最大。

### 5.3 apply() 方法

```python
# 返回每个测试样本在每棵树中所属的叶子节点索引
leaf_indices = rfc.apply(X_test)
print(leaf_indices.shape)  # (n_samples, n_estimators)
# 比如 (54, 25) — 54 个样本 × 25 棵树
```

因为随机森林有 25 棵树，所以每个样本会返回 25 个叶子节点索引（每棵树一个），形成一个矩阵。

### 5.4 predict() 方法

```python
predictions = rfc.predict(X_test)
print(predictions)
# 输出: array([1, 0, 2, 1, 0, ...])
```

返回的是一维数组，每个元素是经过**多数投票**后的最终分类结果。

### 5.5 predict_proba() —— 看投票票型

这是随机森林一个非常有用的方法，能看出不同树之间的**分歧程度**：

```python
# 返回每个样本属于各类的概率（即投票比例）
proba = rfc.predict_proba(X_test)
print(proba[:5])
# 输出示例:
# [[0.   1.   0.  ]   ← 所有树一致认为是第 1 类
#  [0.   0.   1.  ]   ← 所有树一致认为是第 2 类
#  [0.52 0.32 0.16]   ← 分歧明显！52% 认为是第 0 类，32% 认为是第 1 类
#  [1.   0.   0.  ]   ← 所有树一致认为是第 0 类
#  [0.04 0.96 0.  ]]  ← 96% 认为是第 1 类，分歧很小
```

**解读票型的实际意义**：

- 概率接近 `[1, 0, 0]` → 争议很小，所有树高度一致
- 概率分散如 `[0.5, 0.3, 0.2]` → 争议较大，不同树的判断存在分歧
- 对于争议大的样本，说明它处于分类边界附近，预测的可信度相对较低

---

## 六、随机森林回归

### 6.1 分类器 vs 回归器

随机森林的回归器和分类器参数几乎完全相同（`n_estimators`、`max_depth` 等全都一样），唯一的区别在于**评价指标**：

| | 分类器 | 回归器 |
|---|---|---|
| sklearn 类 | `RandomForestClassifier` | `RandomForestRegressor` |
| $y$ 类型 | 离散（0, 1, 2...） | 连续（房价、收入...） |
| 评价指标 | 准确率 | MSE / MAE / R² |
| 组合方式 | 多数投票 | 取平均值 |

### 6.2 加州房价数据集案例

```python
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score

# 加载数据
housing = fetch_california_housing()
X = housing.data
y = housing.target  # 街区房价中位数（已取对数）

# 随机森林回归
rfr = RandomForestRegressor(n_estimators=100, random_state=88)
rfr_scores = cross_val_score(rfr, X, y, cv=10,
                              scoring='neg_mean_squared_error')
print(f"随机森林 - neg_MSE: {rfr_scores.mean():.4f}")  # ≈ -0.41

# 决策树回归（对比）
dtr = DecisionTreeRegressor(random_state=88)
dtr_scores = cross_val_score(dtr, X, y, cv=10,
                              scoring='neg_mean_squared_error')
print(f"决策树   - neg_MSE: {dtr_scores.mean():.4f}")  # ≈ -0.81
```

| 模型 | neg_MSE（越大越好） | R²（默认评分） |
|---|---|---|
| 随机森林回归 | -0.41 | 0.61 |
| 决策树回归 | -0.81 | 0.23 |

随机森林的 $R^2$（0.61）比决策树（0.23）高出近 3 倍。

> **注意**：`scoring='neg_mean_squared_error'` 中的 `neg_` 表示前面加了负号。因为 MSE 是损失函数（越小越好），sklearn 里统一加负号后变成「越大越好」，方便和其他指标比较。从 -81 提升到 -41，「损失更负得少」就是模型的改善。

### 6.3 其他回归评价指标

sklearn 支持多种回归评价指标，如：

| 参数 | 含义 | 说明 |
|---|---|---|
| `'r2'` | R²（默认） | 衡量模型解释了多少变异 |
| `'neg_mean_squared_error'` | 负均方误差 | 越小越好（加了负号后越大越好） |
| `'neg_mean_absolute_error'` | 负平均绝对误差 | MSE 用平方，MAE 用绝对值 |
| `'neg_mean_absolute_percentage_error'` | 负平均绝对百分比误差 | 错了百分之多少 |

---

## 七、经济学应用案例

### 7.1 随机森林在因果推断中的角色

课堂提到一个发表在 **AER（American Economic Review，2022）** 上的文章——全球第一的经济学期刊。研究内容：美国将发电权从国家计划下放到市场后产生的收益。

核心方法论挑战：

```
A 地：实行电力市场化交易（处理组）
B 地：仍实行国家计划（对照组，与 A 地相邻）

问题：A 地市场化 → 煤等燃料大量流向 A 地
     → 由于 A 和 B 相邻，B 地的燃料价格也被影响
     → B 地的对照组「不再干净」
```

传统 DID 在这种情况下失效，因为处理组影响了对照组。文章用**随机森林**预测了「假设燃料价格没有变动时，B 地的发电价格应该是多少」——即构建**反事实结果（Counterfactual）**。

```text
做法:
1. 用随机森林预测「如果没有政策冲击时」B 地的燃料价格和发电量
2. 将预测值（反事实）与现实观测值做差
3. 差值 = 政策效果的估计
```

> **核心启示**：顶刊文章的差距不在于算法多炫酷，而在于**对细节问题的讨论深度**。就简简单单一个回归可能发个普通期刊，但把对照组是否干净、干扰如何排除这些问题讨论透彻，文章就能拔高好几个层次。

### 7.2 其他应用场景

- **区域经济学**：评估高铁开通对空气污染的影响时，大气是不断环流的，需要用机器学习预测反事实气象条件
- **异质性处理效应**：用树模型探索「政策效果在不同群体中如何不同」，而非只报告一个平均处理效应
- **缺失数据填补**：用随机森林根据已有特征预测缺失值，参见 [[05-随机森林实战案例：填补缺失数据、调参的艺术]]

---

## 八、随机森林优缺点总结

### 8.1 优点

| 优点 | 说明 |
|---|---|
| **抗过拟合能力强** | 双随机 + 投票机制，不会像单棵树那样过拟合 |
| **处理高维数据** | 不用做特征选择，不用降维，随机森林帮你自动选特征 |
| **白箱程度适中** | 能输出特征重要性，知道哪些变量重要 |
| **训练速度快** | 每棵树独立并行训练，计算效率高 |
| **抗噪声** | 双随机让模型对噪声和异常值更稳健 |

### 8.2 缺点与注意事项

| 缺点 | 说明 |
|---|---|
| **可解释性弱于单棵树** | 无法像单棵决策树那样直接展示完整决策规则 |
| **噪音太大时也无力** | 如果数据本身信噪比极低，集成也救不了 |
| **类别多的特征可能被偏好** | 如受教育程度分很多档次，随机森林可能利用这种特征「做文章」，需谨慎解读 |


> **基学习器不一定非要是决策树**：SVM、逻辑回归等都可以作为集成学习的基分类器。脑子要灵活——任何「弱分类器」都可以用 Bagging 组合起来。

### 8.3 与已有笔记的关系

- [[04-随机森林原理与经济学应用]]：侧重 Bagging/Boosting 理论对比、随机森林基本原理和经济学文献
- [[05-随机森林实战案例：填补缺失数据、调参的艺术]]：侧重随机森林填补缺失值的完整流程和调参方法论
- 本笔记：侧重代码实战、Bootstrap 数学推导、交叉验证对比和回归树应用
