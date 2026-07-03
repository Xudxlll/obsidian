---
title: "DBSCAN 聚类算法介绍与实际应用示例"
source: "https://myapollo.com.tw/blog/dbscan/"
created: 2026-07-03
tags:
  - 机器学习
  - 聚类
  - DBSCAN
  - 无监督学习
  - Python
---

## 背景

之前在开发 Chrome 扩展 [NimoTab](https://chromewebstore.google.com/detail/nimotab/mhhkfkjgnfddpodoepjigdeaaookhfln?hl=zh-TW) 时，有一个功能需要将相似/相同的网页标题聚类在一起。

当时用的是自己拼凑的方法（但其实类似 DBSCAN），后来跟从事机器学习的同事请教有没有更好的做法时，才知道有一个称为 DBSCAN 的算法可以使用。

本文介绍 DBSCAN 这个实用的聚类算法，并以实际示例展示如何将相似的数据聚类在一起。

> **环境**：Python 3

---

## 一、簇（Cluster）与噪声（Noise）

在理解 DBSCAN 算法之前，需要先理解两个机器学习的重要概念。

**聚类（Clustering）** 是机器学习中的一个重要主题，其目标是将一组数据中的相似数据归纳到同一簇。如果数据集中存在多种相似数据，则可以将其分成多个簇。由于聚类属于**无监督学习**技术，它可以应用于没有标准答案的情况。

> 如果每一笔数据都有正确答案或者标签（label）的情况，通常会使用另一种称为**分类（Classification）的技术**。

例如下图可以明显感觉到数据能够分成 2 簇，而剩下的 1 个黑色点无法被归类，这就是**噪声（Noise）**。

![[数分与机器额外笔记/assets/dbscan-clusters-demo.png]]

**噪声**在机器学习中指的是那些不符合任何已知簇特征或模式的数据。这些数据可能是因为异常值、错误而产生，通常无法被机器学习模型很好地解释，甚至可能干扰模型的训练和预测过程，因此通常需要特别处理或排除。

在聚类的应用场景下，噪声通常指那些无法归属于任何一个簇的数据。

---

## 二、DBSCAN 简介

**DBSCAN**（Density-Based Spatial Clustering of Applications with Noise）是一种**基于密度的聚类算法**，针对空间形状不规则的数据进行聚类。

以下是 sklearn 针对多种聚类算法所做的比较图：

![[数分与机器额外笔记/assets/dbscan-cluster-comparison.png]]

其中 DBSCAN 的聚类结果对形状不规则数据的聚类效果相当好：

![[数分与机器额外笔记/assets/dbscan-demo-result.png]]

### DBSCAN 的主要特点

1. **可以自动处理数据中的噪声（Noise）**
2. **不需要预先指定簇的数量**（K-means 需要）
3. **适合用于含有噪声的数据集**

DBSCAN 通过分析数据点的邻近密度来判断哪些点属于相同的簇，并将密度不足的数据点标记为噪声。

---

## 三、DBSCAN 核心概念图解

DBSCAN 有三个重要核心概念：

| 概念                        | 说明                                      |
| ------------------------- | --------------------------------------- |
| **Core Points**（核心点）      | 半径 ε 内的邻居数 ≥ minPoints                  |
| **Reachable Points**（可达点） | 不满足 Core Point 条件，但落在某个 Core Point 的半径内 |
| **Outliers**（离群点/噪声）      | 既不满足 Core Point 也不属于 Reachable Point    |

### 两个关键参数

- **ε（eps）**：半径
- **minPoints**：一个簇所需的最少邻居数

### Core Points（核心点）

如果有一个点 **p**，其周围半径 **ε** 内满足最少邻居数 **minPoints**（包含 p 点自身），那么点 p 就是 **Core Point**：

![[数分与机器额外笔记/assets/dbscan-core-points.png]]

### Reachable Points（可达点）

DBSCAN 从 Core Point p 的邻近点开始，检查每一个邻近点是否满足 Core Point 条件。如果满足，该邻近点也是 Core Point；如果不满足，则属于 **Reachable Point**。

例如下图中 P、Q、R、S 都符合 Core Point 条件，而 T 点无法满足 Core Point 条件（T 的周围半径内只有 Q 点），但 T 仍落在 Q 点的周围半径范围内，所以 T 属于 Reachable Point。P、Q、R、S、T 属于**同一个簇**：

![[数分与机器额外笔记/assets/dbscan-reachable-points.png]]

### Outliers（离群点/噪声）

如果一个点无法满足 Core Point 与 Reachable Point 的条件，就属于 **Outlier**（或称噪声），例如下图的 U 点：

![[数分与机器额外笔记/assets/dbscan-outliers.png]]

正是因为 DBSCAN 会以簇内的每个点为中心，不断寻找周围是否仍有符合 Core Point 条件的点，并借此**扩展簇的范围**，所以它具有对形状不规则数据进行聚类的能力。

> 可以在 [Visualizing DBSCAN Clustering](https://www.naftaliharris.com/blog/visualizing-dbscan-clustering) 交互式体验 DBSCAN 的聚类过程。

---

## 四、DBSCAN 算法伪代码

![[数分与机器额外笔记/assets/dbscan-pseudocode.png]]

关键点：

- **distFunc**（距离函数）：DBSCAN 可以使用**任意距离函数**来衡量数据之间的距离。最简单的距离函数可以使用[欧几里得距离](https://zh.wikipedia.org/zh-cn/%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E8%B7%9D%E7%A6%BB)。
- **eps**：即半径 ε
- **minPts**：即最少邻居数 minPoints

`RangeQuery()` 伪代码如下，它的作用是找出参数 **Q** 点周围半径 **eps** 内有多少笔邻近数据：

![[数分与机器额外笔记/assets/dbscan-range-query.png]]

---

## 五、Python 实现 DBSCAN

### 主函数

```python
def dbscan(data, distance_func, eps, min_points):
    """
    Performs DBSCAN clustering on the given data.

    Args:
        data: A list of data points.
        distance_func: The distance function to use.
        eps: The radius around each point.
        min_points: The minimum number of points required to form a dense region.

    Returns:
        A list of cluster assignments for each data point.
    """
    labels = [None] * len(data)  # Initialize labels as None (undefined)
    cluster_id = 0

    for i in range(len(data)):
        if labels[i] is not None:  # Already assigned to a cluster or noise
            continue

        neighbors = range_query(data, distance_func, i, eps)
        if len(neighbors) < min_points:
            labels[i] = -1  # Mark as noise
        else:
            cluster_id += 1
            labels[i] = cluster_id
            # Expand cluster
            seeds = neighbors.copy()
            for j in seeds:
                if labels[j] == -1:
                    labels[j] = cluster_id

                if labels[j] is not None:
                    continue

                labels[j] = cluster_id

                new_neighbors = range_query(data, distance_func, j, eps)
                if len(new_neighbors) >= min_points:
                    for k in new_neighbors:
                        if k not in seeds:
                          seeds.append(k)
    return labels
```

`dbscan()` 返回值是一个与参数 `data` 长度相同的列表，其中每个元素对应 `data` 的簇编号：
- **-1**：噪声
- **≥1**：簇的编号

### 辅助函数：范围查询

```python
def range_query(data, distance_func, point_index, eps):
    """Finds the neighbors of a point within a given radius (eps)."""
    neighbors = []
    for i in range(len(data)):
        if distance_func(data[point_index], data[i]) <= eps:
            neighbors.append(i)
    return neighbors
```

---

## 六、实际应用：文章标题聚类

### 场景

假设我们有大量新闻文章标题，希望对其进行整理归类。由于通常不知道要将文章分成几类，此时可以使用 DBSCAN 将相似的文章聚类在一起。

### 距离函数选择：Jaccard Index

衡量文章标题相似度的距离函数可以使用 [Jaccard Index](https://myapollo.com.tw/blog/jaccard-index-explaination/)。

### 分词方式：Bigram

使用 bigram 进行分词，好处是实现简单，且可以处理中英文混杂的情况。

> **Bigram**：将字符串切分为长度为 2 的多个子字符串。例如 `我爱算法` 可以切分为 `我爱`、`爱算`、`算法`。

以字符为单位的 bigram 代码：

```python
def bigram_tokenize(text):
    """Tokenizes a text string into bigrams."""
    tokens = []
    for i in range(len(text) - 1):
        tokens.append(text[i:i+2])
    return tokens
```

Jaccard 距离函数：

```python
def jaccard_distance(tokens1, tokens2):
    """Calculates the distance between two token lists using Jaccard distance."""
    set1 = set(tokens1)
    set2 = set(tokens2)
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union == 0:
        return 0
    return 1 - (intersection / union)
```

### 完整流程示例

假设有以下文章标题：

```python
data = [
    'AI technology transforming industries',
    'AI 技术如何改变行业',
    'Introduction to Machine Learning',
    '机器学习入门',
    'Top 10 Python libraries for data science',
]
```

**步骤一**：对每个标题进行 bigram 分词

```python
tokenized_data = [bigram_tokenize(text) for text in data]
```

**步骤二**：调用 DBSCAN 进行聚类

```python
eps = 0.6        # 可根据需要调整半径
min_points = 3   # 可根据需要调整最少数据数
labels = dbscan(tokenized_data, jaccard_distance, eps, min_points)
```

**步骤三**：合并显示聚类结果

```python
from collections import defaultdict
from pprint import pprint

d = defaultdict(list)

for i in range(len(data)):
    cluster_id = labels[i]
    if cluster_id != -1:
        d[cluster_id].append(data[i])

for k, v in d.items():
    print(f"Cluster {k}:")
    pprint(v)
    print('--' * 5)
```

### 聚类结果展示

```
Cluster 1:
['Introduction to Machine Learning',
 'Introduction to Reinforcement Learning',
 'Introduction to cloud computing',
 'Introduction to AI ethics']
----------
Cluster 2:
['人工智能在医疗中的应用',
 '人工智能在网络安全中的应用',
 '人工智能在自动驾驶中的应用',
 '人工智能在个性化医疗中的应用',
 '人工智能在自然灾害预测中的应用',
 '人工智能在零售行业中的应用',
 '机器学习在异常检测中的应用',
 '人工智能在电子商务中的应用',
 '机器学习在医疗中的应用',
 '人工智能在预测性维护中的应用',
 '人工智能在环境可持续性中的应用',
 '人工智能在法律科技中的应用',
 '人工智能在个性化客户体验中的应用',
 '人工智能在公共政策中的应用',
 '人工智能在风险管理中的应用',
 '人工智能在创意产业中的应用',
 '人工智能在游戏中的应用',
 '人工智能在灾难应对中的应用']
----------
Cluster 3:
['Automated machine learning tools',
 'How to train a machine learning model',
 'How to deploy machine learning models',
 'How to learn deep learning',
 'Top machine learning algorithms',
 'AI and machine learning in manufacturing']
----------
Cluster 4:
['人工智能驱动的聊天机器人',
 '人工智能驱动的营销策略',
 '人工智能驱动的推荐系统',
 '人工智能驱动的供应链管理',
 '人工智能驱动的虚拟助理',
 '人工智能驱动的商业智能']
----------
Cluster 5:
['深度学习在计算机视觉中的应用',
 '深度学习在机器人学中的应用',
 '深度学习在语音识别中的应用']
```

可以看到相似的标题被很好地分到了同一簇中。

> [完整代码在 Google Colab](https://colab.research.google.com/drive/1_CzY_J6c-ID_Zh5hJrTwYtSYIMW1_t2j?usp=sharing)

---

## 七、如何调优 DBSCAN 聚类结果

| 调整方向 | 方法 | 效果 |
|----------|------|------|
| 噪声太多 | 增大 **eps**（半径） | 减少噪声数量 |
| 希望成簇条件更严格 | 增大 **minPoints** | 成簇条件变严格，可能导致小簇变成噪声 |
| 改善聚类效果 | 更换合适的**距离函数** | 从根本上提升聚类质量 |

---

## 八、总结

DBSCAN 是一个相当实用的聚类算法，其优点在于：

1. **不需事先设定簇的数量**（K-means 需要）
2. **可以处理噪声**
3. **对形状不规则的数据有较好的聚类能力**

各大机器学习框架都有实现 DBSCAN（例如 [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)），在理解原理后，可以直接使用框架提供的实现。

---

## 参考

- [DBSCAN - Wikipedia](https://en.wikipedia.org/wiki/DBSCAN)
- [DBSCAN, Explained in 5 Minutes](https://towardsdatascience.com/dbscan-explained-in-5-minutes-133f6a9766e4)
- [不要再用 K-means！超实用聚类法 DBSCAN 详解](https://axk51013.medium.com/%E4%B8%8D%E8%A6%81%E5%86%8D%E7%94%A8k-means-%E8%B6%85%E5%AF%A6%E7%94%A8%E5%88%86%E7%BE%A4%E6%B3%95dbscan%E8%A9%B3%E8%A7%A3-a33fa287c0e)
- [sklearn - Clustering](https://scikit-learn.org/stable/modules/clustering.html)
