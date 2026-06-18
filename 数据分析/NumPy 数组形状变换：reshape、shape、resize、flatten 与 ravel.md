---
title: NumPy 数组形状变换：reshape、shape、resize、flatten 与 ravel
date: 2026-06-18
tags:
  - Python
  - NumPy
  - ndarray
  - reshape
---

# NumPy 数组形状变换：reshape、shape、resize、flatten 与 ravel

> [!abstract] 本文主线
> - `reshape()` 返回另一个形状的数组结果，通常不修改原数组。
> - `.shape = ...` 是给属性赋值，直接修改当前数组的形状。
> - `resize()` 是原地修改方法，还可以改变元素总数。
> - `flatten()` 和 `ravel()` 都能展平数组，但前者一定复制，后者尽量共享内存。
> - 有些形状变化受到内存排列限制，因为它们无法只通过修改 `shape` 和 `strides` 完成。

## 1. `shape` 表示什么

`shape` 是 NumPy 数组对象的属性，表示数组每个轴的长度：

```python
import numpy as np

a = np.arange(8)

print(a)
# [0 1 2 3 4 5 6 7]

print(a.shape)  # (8,)
```

`shape=(8,)` 表示数组只有一个轴，这个轴上有 8 个元素。

形状中各数字的乘积等于数组元素总数：

```text
(8,)     → 8个元素
(2, 4)   → 2×4=8个元素
(2, 2, 2) → 2×2×2=8个元素
```

## 2. `reshape()`：返回另一个形状的数组结果

```python
a = np.arange(8)
b = a.reshape(2, 4)

print(a.shape)  # (8,)
print(b.shape)  # (2, 4)
```

`reshape()` 没有直接修改 `a`，而是把结果交给了 `b`。

在这个例子中，`b` 是新的数组对象，但与 `a` 共享底层内存：

```python
print(a is b)                  # False
print(np.shares_memory(a, b))  # True
```

修改 `b` 会影响 `a`：

```python
b[0, 0] = 100

print(a)
# [100   1   2   3   4   5   6   7]
```

`reshape()` 会尽量返回视图；如果当前内存排列无法直接表示目标形状，则可能复制数据。

新形状的元素总数必须和原数组相同：

```python
a.reshape(4, 2)  # 可以，4×2=8
a.reshape(2, 2, 2)  # 可以，2×2×2=8

# a.reshape(3, 3)  # 报错，3×3不等于8
```

如果希望用新形状替换变量 `a`，可以重新赋值：

```python
a = a.reshape(2, 4)
```

## 3. `.shape = ...`：给属性赋值

```python
a = np.arange(8)
a.shape = (2, 4)

print(a)
# [[0 1 2 3]
#  [4 5 6 7]]
```

`shape` 是属性，不是方法：

```text
a.shape           → 读取属性
a.shape = (2, 4)  → 修改属性
a.reshape(2, 4)   → 调用方法
```

给 `shape` 赋值会直接改变当前数组对象，不会返回另一个数组。

它不能改变元素总数：

```python
a.shape = (4, 2)  # 可以，4×2=8

# a.shape = (3, 3)  # 报错，3×3不等于8
```

这种写法要求 NumPy 能够在不复制、不移动底层数据的情况下完成形状变化，因此可能受到内存排列限制。实际代码中通常更推荐使用：

```python
a = a.reshape(2, 4)
```

## 4. `resize()`：原地修改数组

`resize()` 是 `ndarray` 对象的方法：

```python
a = np.arange(8)
a.resize(2, 2, 2)

print(a.shape)  # (2, 2, 2)
print(a)
# [[[0 1]
#   [2 3]]
#
#  [[4 5]
#   [6 7]]]
```

`resize()` 直接修改 `a`，返回值是 `None`：

```python
result = a.resize(4, 2)
print(result)  # None
```

### 4.1 扩大元素数量

扩大数组时，新增位置通常用 `0` 填充：

```python
a = np.arange(4)
a.resize(3, 2)

print(a)
# [[0 1]
#  [2 3]
#  [0 0]]
```

### 4.2 减少元素数量

缩小数组时，后面的元素会被截掉：

```python
a = np.arange(8)
a.resize(2, 2)

print(a)
# [[0 1]
#  [2 3]]
```

### 4.3 `resize()` 的限制

改变元素总数可能需要重新分配内存。如果数组不拥有自己的数据、内存不连续，或者其他数组正在引用它的内存，`resize()` 可能报错。

> [!warning] `a.resize()` 和 `np.resize()` 不同
> `a.resize()` 原地修改数组；`np.resize(a, new_shape)` 返回新数组，而且空间不足时可能重复使用原数据填充。

## 5. 三种改变形状方式的对比

```python
a = np.arange(8)
b = a.reshape(2, 4)
a.shape = (2, 4)
a.resize(2, 2, 2)
```

执行过程：

```text
a = np.arange(8)    → a.shape是(8,)
b = a.reshape(2,4)  → b.shape是(2,4)，a仍是(8,)
a.shape = (2,4)     → 直接把a改成(2,4)
a.resize(2,2,2)     → 直接把a改成(2,2,2)
```

| 操作 | 是否直接修改当前数组 | 是否返回数组结果 | 能否改变元素数量 |
| --- | --- | --- | --- |
| `a.reshape(...)` | 否 | 是 | 否 |
| `a.shape = (...)` | 是 | 否 | 否 |
| `a.resize(...)` | 是 | 否，返回 `None` | 可以 |

## 6. `flatten()`：展平并复制数据

`flatten()` 把多维数组展开成一维数组：

```python
a = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

b = a.flatten()

print(b)
# [1 2 3 4 5 6]

print(b.ndim)   # 1
print(b.shape)  # (6,)
```

`flatten()` 一定复制数据，返回独立副本：

```python
print(np.shares_memory(a, b))  # False

b[0] = 100

print(a)
# [[1 2 3]
#  [4 5 6]]
```

修改 `b` 不会影响原数组 `a`。

## 7. `ravel()`：尽量用视图展平

`ravel()` 也会把多维数组展开成一维：

```python
a = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

b = a.ravel()

print(b)
# [1 2 3 4 5 6]
```

当内存排列允许时，`ravel()` 返回共享底层数据的视图：

```python
print(np.shares_memory(a, b))  # True

b[0] = 100

print(a)
# [[100   2   3]
#  [  4   5   6]]
```

不过，`ravel()` 只是尽量避免复制。如果当前内存排列无法直接展平，它也可能创建副本。

## 8. `flatten()` 和 `ravel()` 的区别

| 方法 | 是否展平为一维 | 是否复制数据 | 修改结果是否可能影响原数组 |
| --- | --- | --- | --- |
| `flatten()` | 是 | 一定复制 | 不会 |
| `ravel()` | 是 | 尽量不复制，必要时复制 | 可能会 |

可以简单记忆：

```text
flatten() → 展平并制作独立副本
ravel()   → 展平并尽量共享原数据
```

判断是否共享内存，不要只靠猜测：

```python
np.shares_memory(a, b)
```

## 9. 为什么修改 `.shape` 会受到内存排列限制

NumPy 数组读取数据时，主要依靠两组信息：

```text
shape   → 每个轴有多少个元素
strides → 沿每个轴移动一步，需要跨过多少字节
```

对于连续存储的一维数组：

```python
a = np.arange(8)

print(a.shape)    # (8,)
print(a.strides)  # int64通常为(8,)
```

执行：

```python
a.shape = (2, 4)
```

不需要移动数据，只需要调整 `shape` 和 `strides`，因此能够成功。

### 转置后的读取顺序

```python
a = np.arange(8).reshape(4, 2)
b = a.T

print(b)
# [[0 2 4 6]
#  [1 3 5 7]]
```

`b` 的逻辑读取顺序是：

```text
0 → 2 → 4 → 6 → 1 → 3 → 5 → 7
```

但是底层内存的实际顺序仍然是：

```text
0 → 1 → 2 → 3 → 4 → 5 → 6 → 7
```

如果执行：

```python
b.shape = (8,)
```

NumPy 无法只通过修改 `shape` 和 `strides` 得到当前逻辑顺序，因此可能报错：

```text
AttributeError: Incompatible shape for in-place modification
```

而 `reshape()` 必要时允许复制和重新排列数据：

```python
c = b.reshape(8)

print(c)
# [0 2 4 6 1 3 5 7]
```

所以核心区别是：

```text
a.shape = (...) → 只能原地修改元数据，不能复制数据
a.reshape(...)  → 优先使用视图，必要时可以复制数据
```

> [!note] 更准确的判断
> 并不是所有不连续数组修改 `.shape` 都一定失败。只有当目标形状无法仅通过调整 `shape` 和 `strides` 表示时，原地修改才会失败。

## 10. 应该选择哪一种方式

| 需求 | 推荐方式 |
| --- | --- |
| 改变形状，但不改变元素数量 | `reshape()` |
| 明确原地修改当前对象的形状 | `.shape = ...`，但需注意内存排列限制 |
| 原地改变形状或元素数量 | `resize()` |
| 展平并需要独立副本 | `flatten()` |
| 展平并尽量节省复制开销 | `ravel()` |

日常改变形状时，优先考虑：

```python
new_array = old_array.reshape(new_shape)
```

它的含义清晰，并且在无法返回视图时可以自动复制数据。

## 11. 综合示例

```python
import numpy as np

a = np.arange(8)

# reshape：返回另一个形状的结果
b = a.reshape(2, 4)
print(a.shape)  # (8,)
print(b.shape)  # (2, 4)

# shape属性：原地修改当前数组形状
a.shape = (2, 4)
print(a.shape)  # (2, 4)

# flatten：展平并复制
c = a.flatten()
print(np.shares_memory(a, c))  # False

# ravel：展平并尽量共享内存
d = a.ravel()
print(np.shares_memory(a, d))  # True

# resize：原地改变形状，也能改变元素数量
a.resize(2, 2, 2)
print(a.shape)  # (2, 2, 2)
```

## 12. 最终记忆清单

> [!success] 核心结论
> - `shape` 是属性，`reshape()`、`resize()`、`flatten()`、`ravel()` 是方法。
> - `reshape()` 通常不修改原数组，而是返回另一个形状的数组结果。
> - `.shape = ...` 原地修改当前数组，不能改变元素总数，也不能通过复制解决内存排列问题。
> - `resize()` 原地修改当前数组，并且可以增加或减少元素数量。
> - `flatten()` 一定复制，修改结果不会影响原数组。
> - `ravel()` 尽量返回视图，修改结果可能影响原数组。
> - 形状变化能否不复制完成，取决于底层数据能否用新的 `shape` 和 `strides` 正确描述。
> - 判断两个数组是否共享内存，使用 `np.shares_memory()`。
