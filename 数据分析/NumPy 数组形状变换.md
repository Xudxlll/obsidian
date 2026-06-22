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
> - `.flat` 不创建一维数组，而是返回一个按一维顺序访问原数组的迭代器。
> - `resize()` 与广播解决的是不同问题：前者改变数组数据，后者只在运算中扩展形状。
> - `tolist()` 将数组递归转为 Python 原生嵌套列表，一定复制，主要用于脱离 NumPy 的场景。
> - 有些形状变化受到内存排列限制，因为它们无法只通过修改 `shape` 和 `strides` 完成。

# 1. `shape` 表示什么

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

# 2. `reshape()`：返回另一个形状的数组结果

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

# 3. `.shape = ...`：给属性赋值

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

# 4. `resize()`：原地修改数组

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

## 4.1 扩大元素数量

扩大数组时，新增位置通常用 `0` 填充：

```python
a = np.arange(4)
a.resize(3, 2)

print(a)
# [[0 1]
#  [2 3]
#  [0 0]]
```

## 4.2 减少元素数量

缩小数组时，后面的元素会被截掉：

```python
a = np.arange(8)
a.resize(2, 2)

print(a)
# [[0 1]
#  [2 3]]
```

## 4.3 `resize()` 的限制

改变元素总数可能需要重新分配内存。如果数组不拥有自己的数据、内存不连续，或者其他数组正在引用它的内存，`resize()` 可能报错。

例如，`reshape()` 在条件允许时返回共享数据的视图：

```python
a = np.arange(4)
b = a.reshape(2, 2)

print(b.base is a)              # True
print(b.flags.owndata)          # False
print(np.shares_memory(a, b))   # True
```

此时的数据关系为：

```text
a：真正拥有数据 [0,1,2,3]
└── b：以(2,2)的形状查看a的数据
```

如果执行：

```python
b.resize(2, 2, 2)
```

会报错：

```text
ValueError: cannot resize this array: it does not own its data
```

原因是元素数量发生了变化：

```text
原形状：(2,2)   → 2×2=4个元素
新形状：(2,2,2) → 2×2×2=8个元素
```

从 4 个元素扩展到 8 个元素，需要重新分配内存；但 `b` 只是借用 `a` 的内存，并不拥有数据，因此不能原地扩容。

**解决方法一：先复制，让数组拥有数据**

```python
a = np.arange(4)
b = a.reshape(2, 2).copy()

print(b.flags.owndata)  # True

b.resize(2, 2, 2)

print(b)
# [[[0 1]
#   [2 3]]
#
#  [[0 0]
#   [0 0]]]
```

**解决方法二：一开始就创建正确数量的元素**

如果本来就需要形状 `(2,2,2)`，更自然的写法是：

```python
b = np.arange(8).reshape(2, 2, 2)
```

**解决方法三：使用 `np.resize()` 返回新数组**

```python
a = np.arange(4).reshape(2, 2)
b = np.resize(a, (2, 2, 2))

print(b)
# [[[0 1]
#   [2 3]]
#
#  [[0 1]
#   [2 3]]]
```

`np.resize()` 在空间不足时会重复使用原数据，而不是补 `0`。

> [!warning] `a.resize()` 和 `np.resize()` 不同
> - `a.resize()` 原地修改数组，扩大时新增位置补 `0`，并要求数组能够安全地调整自己的内存。
> - `np.resize(a, new_shape)` 返回新数组，空间不足时会重复使用原数据填充。

## 4.4 `resize()` 和广播不是同一种功能

虽然 `resize()` 可以把一个数组强行改成另一种大小，但它并不比广播“更强大”。二者解决的是完全不同的问题：

```text
resize → 改变数组本身的形状和元素数量
广播   → 不修改原数组，让不同形状的数组参与运算
```

例如，把 `(2,3)` 数组改成 `(2,2,2)`：

```python
a = np.array([
    [0, 1, 2],
    [3, 4, 5]
])

a.resize(2, 2, 2)

print(a)
# [[[0 1]
#   [2 3]]
#
#  [[4 5]
#   [0 0]]]
```

原数组有 6 个元素，目标形状需要 8 个元素，因此 `resize()` 先把数据扩充为：

```text
[0,1,2,3,4,5,0,0]
```

再组织成 `(2,2,2)`。这里真实的数据和内存都发生了改变。

广播则不会修改原数组：

```python
a = np.array([10, 20])  # shape=(2,)
b = np.ones((2, 2, 2)) # shape=(2,2,2)

c = a + b

print(a.shape)  # (2,)，原数组没有改变
print(c.shape)  # (2,2,2)
```

计算时，NumPy 只是把 `a` 想象成：

```text
[[[10,20],
  [10,20]],

 [[10,20],
  [10,20]]]
```

但并没有真的把 `a` 扩充成这个数组。

形状 `(2,3)` 和 `(2,2,2)` 不能广播，是因为从最后一个轴向前比较时，`3` 和 `2` 既不相等，也没有一个是 `1`：

```text
(  2,3)
(2,2,2)
     ↑
     3和2不兼容
```

不应为了绕过广播规则而随意使用 `resize()`，因为它可能补 `0`、截断数据或重复数据，从而破坏原来的业务含义。正确做法是根据各轴含义，使用合理的 `reshape()`、增加长度为 1 的轴，或重新组织数据。

| 对比 | `resize()` | 广播 |
| --- | --- | --- |
| 主要目的 | 改变数组大小和形状 | 让不同形状数组参与运算 |
| 是否修改原数组 | `a.resize()` 会 | 不会 |
| 是否改变真实元素数量 | 可以 | 不会 |
| 扩充方式 | 补 `0`，或由 `np.resize()` 重复数据 | 运算时虚拟扩展 |
| 典型用途 | 调整存储结构 | 向量化的逐元素运算 |

# 5. 三种改变形状方式的对比

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

# 6. `flatten()`：展平并复制数据

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

# 7. `ravel()`：尽量用视图展平

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

# 8. `flatten()`、`ravel()` 和 `.flat` 的区别

`.flat` 是数组的属性，返回一个 `numpy.flatiter` 迭代器。它不会生成一个新的一维 `ndarray`，而是提供一个按一维顺序访问原数组的游标：

```python
a = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

f = a.flat

print(type(f))
# <class 'numpy.flatiter'>
```

可以直接遍历全部元素：

```python
for value in a.flat:
    print(value)
```

输出顺序为：

```text
1 2 3 4 5 6
```

也可以用一维索引访问原数组中的元素：

```python
print(a.flat[0])  # 1
print(a.flat[4])  # 5
```

通过 `.flat` 赋值会修改原数组：

```python
a.flat[0] = 100

print(a)
# [[100   2   3]
#  [  4   5   6]]
```

注意 `.flat` 是属性，不需要括号：

```python
a.flat       # 属性
a.flatten()  # 方法
a.ravel()    # 方法
```

| 写法 | 返回类型 | 是否创建一维数组 | 是否复制数据 | 修改是否影响原数组 |
| --- | --- | --- | --- | --- |
| `a.flatten()` | `ndarray` | 是 | 一定复制 | 不会 |
| `a.ravel()` | `ndarray` | 是 | 尽量不复制，必要时复制 | 可能会 |
| `a.flat` | `flatiter` 迭代器 | 否 | 不创建完整副本 | 会 |

可以简单记忆：

```text
flatten() → 展平并制作独立副本
ravel()   → 展平并尽量共享原数据
flat      → 拿一个游标，按一维顺序访问原数组
```

判断是否共享内存，不要只靠猜测：

```python
np.shares_memory(a, b)
```

# 9. `tolist()`：转为 Python 列表

`tolist()` 把 NumPy 数组转换为标准 Python 列表（嵌套列表）：

```python
a = np.array([1, 2, 3, 4, 5])

lst = a.tolist()

print(lst)       # [1, 2, 3, 4, 5]
print(type(lst)) # <class 'list'>
```

对于多维数组，返回嵌套列表：

```python
a = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

lst = a.tolist()

print(lst)
# [[1, 2, 3], [4, 5, 6]]
```

## 9.1 `tolist()` 一定复制数据

与 `flatten()` 类似，`tolist()` 一定复制数据，返回独立副本：

```python
a = np.array([10, 20, 30])
lst = a.tolist()

lst[0] = 999

print(lst)  # [999, 20, 30]
print(a)    # [10  20  30]
```

修改 `lst` 不会影响原数组 `a`。

## 9.2 `tolist()` 与 `list()` 的区别

`list(a)` 和 `a.tolist()` 行为不同：

```python
a = np.array([[1, 2], [3, 4]])

list(a)        # [array([1, 2]), array([3, 4])]
a.tolist()     # [[1, 2], [3, 4]]
```

```text
list(a)   → 沿第一轴拆开，元素仍是 ndarray
a.tolist() → 递归转为纯 Python 类型（int、float 等）
```

## 9.3 典型用途

`tolist()` 主要用于需要脱离 NumPy 的场景：

**JSON 序列化：**

```python
import json

a = np.array([1, 2, 3])
json.dumps(a.tolist())  # "[1, 2, 3]"
```

**传给只接受 list 的函数：**

```python
data = np.array([1, 2, 3])
result = some_func(data.tolist())
```

**更好的打印格式：**

```python
print(a)          # [1 2 3]
print(a.tolist())  # [1, 2, 3]
```

# 10. 为什么修改 `.shape` 会受到内存排列限制

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

## 转置后的读取顺序

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

# 11. 应该选择哪一种方式

| 需求 | 推荐方式 |
| --- | --- |
| 改变形状，但不改变元素数量 | `reshape()` |
| 明确原地修改当前对象的形状 | `.shape = ...`，但需注意内存排列限制 |
| 原地改变形状或元素数量 | `resize()` |
| 展平并需要独立副本 | `flatten()` |
| 展平并尽量节省复制开销 | `ravel()` |
| 只想逐个遍历或按一维索引访问原数组 | `.flat` |
| 转为 Python 原生嵌套列表，脱离 NumPy | `tolist()` |
| 让不同形状数组参与逐元素运算 | 广播；必要时先用 `reshape()` 增加长度为 1 的轴 |

日常改变形状时，优先考虑：

```python
new_array = old_array.reshape(new_shape)
```

它的含义清晰，并且在无法返回视图时可以自动复制数据。

# 12. 综合示例

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

# flat：不创建一维数组，通过迭代器访问原数组
print(list(a.flat))
a.flat[0] = 100
print(a[0, 0])  # 100

# resize：原地改变形状，也能改变元素数量
a.resize(2, 2, 2)
print(a.shape)  # (2, 2, 2)

# tolist：转为 Python 原生嵌套列表
lst = a.tolist()
print(type(lst))  # <class 'list'>
print(lst)         # [[[0, 1], [2, 3]], [[4, 5], [6, 7]]]
```

# 13. 最终记忆清单

> [!success] 核心结论
> - `shape` 和 `.flat` 是属性，`reshape()`、`resize()`、`flatten()`、`ravel()` 是方法。
> - `reshape()` 通常不修改原数组，而是返回另一个形状的数组结果。
> - `.shape = ...` 原地修改当前数组，不能改变元素总数，也不能通过复制解决内存排列问题。
> - `resize()` 原地修改当前数组，并且可以增加或减少元素数量。
> - 通过 `reshape()` 得到的视图通常不拥有数据；需要扩容时，应先 `.copy()` 或直接创建正确数量的元素。
> - `a.resize()` 扩大时补 `0`；`np.resize()` 返回新数组，扩大时重复原数据。
> - `resize()` 会真实改变数据；广播只在运算中虚拟扩展形状，不会修改原数组。
> - `flatten()` 一定复制，修改结果不会影响原数组。
> - `ravel()` 尽量返回视图，修改结果可能影响原数组。
> - `.flat` 返回 `flatiter` 迭代器，不生成一维数组；通过它赋值会修改原数组。
> - `tolist()` 将数组递归转为 Python 原生嵌套列表，一定复制，适用于 JSON 序列化等脱离 NumPy 的场景。
> - 形状变化能否不复制完成，取决于底层数据能否用新的 `shape` 和 `strides` 正确描述。
> - 判断两个数组是否共享内存，使用 `np.shares_memory()`。
