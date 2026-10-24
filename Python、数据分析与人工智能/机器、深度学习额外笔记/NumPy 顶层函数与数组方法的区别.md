---
title: NumPy 顶层函数与数组方法的区别
date: 2026-06-22
tags:
  - Python
  - NumPy
  - ndarray
---

# NumPy 顶层函数与数组方法的区别

> [!abstract] 本文主线
> - `a.max()` 和 `np.max(a)` 功能相同，底层实现互相关联，选择取决于使用场景。
> - 顶层函数 `np.函数()` 接受任何 array-like 输入，方法 `a.方法()` 只能在 `ndarray` 上调用。
> - 常见统计函数（`max`、`sum`、`mean` 等）同时存在于两层 API；`median`、`percentile` 等只有顶层函数。
> - 链式调用适合用方法；对列表等非 `ndarray` 输入、命名聚合用顶层函数更合适。

# 1. 两套 API 做同一件事

NumPy 为很多操作提供了两个入口：

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])

a.max()    # 5
np.max(a)  # 5

a.sum()    # 15
np.sum(a)  # 15
```

大多数情况下，`a.max()` 底层就是在调用 `np.max(a)`，结果完全一样。

```python
print(a.max() == np.max(a))  # True
```

但两套 API 在适用范围和使用场景上存在差异。

# 2. 核心区别：顶层函数更"宽容"

`np.函数()` 接受任何 **array-like** 输入：

```python
# 普通 Python list
my_list = [1, 2, 3, 4, 5]

np.sum(my_list)   # ✓ 可以，15
np.max(my_list)   # ✓ 可以，5

# my_list.sum()   # ✗ 报错！list 没有 .sum() 方法
```

方法只能在 `ndarray` 对象上调用。

# 3. 哪些函数有对应方法

## 有对应方法

| 方法 | 顶层函数 |
| --- | --- |
| `a.max()` | `np.max(a)` |
| `a.min()` | `np.min(a)` |
| `a.sum()` | `np.sum(a)` |
| `a.mean()` | `np.mean(a)` |
| `a.std()` | `np.std(a)` |
| `a.var()` | `np.var(a)` |
| `a.prod()` | `np.prod(a)` |
| `a.argmax()` | `np.argmax(a)` |
| `a.argmin()` | `np.argmin(a)` |
| `a.any()` | `np.any(a)` |
| `a.all()` | `np.all(a)` |
| `a.cumsum()` | `np.cumsum(a)` |
| `a.cumprod()` | `np.cumprod(a)` |
| `a.clip(lo, hi)` | `np.clip(a, lo, hi)` |
| `a.round(n)` | `np.round(a, n)` |
| `a.trace()` | `np.trace(a)` |
| `a.diagonal()` | `np.diagonal(a)` |
| `a.transpose()` | `np.transpose(a)` |
| `a.T` | —（属性，不是函数） |

属性 `a.T`、`a.real`、`a.imag` 则没有对应的顶层函数。

## 只有顶层函数，没有对应方法

| 顶层函数 | 说明 |
| --- | --- |
| `np.median(a)` | **没有** `a.median()` |
| `np.percentile(a, q)` | **没有** `a.percentile()` |
| `np.quantile(a, q)` | **没有** `a.quantile()` |
| `np.unique(a)` | **没有** `a.unique()` |
| `np.concatenate([a, b])` | 多个数组参与，不适合作单个数组的方法 |
| `np.where(condition)` | 不是针对单个数组的操作 |
| `np.sort(a)` | 有 `a.sort()`，但 `a.sort()` 是原地排序 |
| `np.argsort(a)` | **没有** `a.argsort()` |

> [!note] `np.sort()` vs `a.sort()`
> `np.sort(a)` 返回排序后的新数组，不修改 `a`；`a.sort()` 原地排序，返回 `None`。这一对是行为不同，不只是入口不同。

# 4. `axis` 参数在两套 API 中的使用

两套 API 都支持 `axis` 参数，用法相同：

```python
a = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

# 方法
print(a.sum(axis=0))  # [5 7 9]
print(a.sum(axis=1))  # [6 15]

# 顶层函数
print(np.sum(a, axis=0))  # [5 7 9]
print(np.sum(a, axis=1))  # [6 15]
```

# 5. 什么时候用方法，什么时候用顶层函数

## 适合用方法：链式调用

```python
result = a.clip(0, 10).astype(int).sum()

# 等价但不如上面流畅
result = np.sum(np.clip(a, 0, 10).astype(int))
```

方法调用从左到右读起来更像流水线。

## 适合用顶层函数：输入不是 `ndarray`

```python
raw_data = [1, 2, 3, 4, 5]

total = np.sum(raw_data)  # 直接传 list
mean  = np.mean(raw_data)  # 自动转换
```

## 适合用顶层函数：没有对应方法

```python
np.median(a)           # 没有 a.median()
np.percentile(a, 90)   # 没有 a.percentile()
```

## 适合用顶层函数：命名聚合

```python
# 需要突出"计算 XX 的平均值"时
avg = np.mean(scores)
```

顶层函数的语义更接近数学公式，阅读时"动词 + 数据"的顺序也符合口语习惯。

# 6. 最终选择原则

```text
想用哪个用哪个，结果一样。

输入是 list → 必须用 np.函数()
输入是 ndarray → 方法、函数都可以
想链式调用 → 用方法
操作没有对应方法 → 只能用 np.函数()
读取时像读数学公式 → np.函数()
```

> [!success] 核心结论
> - `a.方法()` 和 `np.函数(a)` 在大多数情况下等价，底层实现互通。
> - 顶层函数接受 array-like 输入；方法只能在 `ndarray` 上调用。
> - 并非所有顶层函数都有对应方法（`median`、`percentile`、`unique` 等就没有）。
> - 方法适合链式调用，顶层函数适合处理 list 或没有方法的情景。
> - 少数函数（如 `sort`）在两套 API 中行为不同，需要留意。
