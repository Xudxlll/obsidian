---
title: NumPy ndarray、数组创建与视图
date: 2026-06-18
tags:
  - Python
  - NumPy
  - 数据分析
  - ndarray
---

# NumPy ndarray、数组创建与视图

> [!abstract] 本文主线
> 1. `numpy` 是包，`np` 是它的别名。
> 2. `np.array()` 是函数，`np.ndarray` 是数组对象所属的类。
> 3. `np.array()` 和 `np.asarray()` 都能创建数组，主要区别在于是否尽量避免复制。
> 4. NumPy 数组之间可能共享同一块底层内存，这就是理解“视图”的关键。
> 5. 判断数组是否共享内存，优先使用 `np.shares_memory()`，不要只看 `.base` 或 `.data`。

## 1. `numpy`、`array` 和 `ndarray` 分别是什么

```python
import numpy as np

ary = np.array([1, 2, 3, 4, 5, 6])
print(type(ary))
```

输出：

```text
<class 'numpy.ndarray'>
```

这里各部分的含义是：

| 名称 | 含义 |
| --- | --- |
| `numpy` | 第三方 Python 包 |
| `np` | 导入 `numpy` 时设置的别名 |
| `np.array()` | NumPy 对外提供的函数，用于创建数组 |
| `np.ndarray` | NumPy 数组对象所属的类 |
| `ary` | `np.array()` 返回的 `ndarray` 对象 |

因此，准确的说法是：

> 调用 NumPy 包提供的 `array()` 函数，创建一个 `ndarray` 类型的对象。

### 函数和方法的区别

```python
np.array([1, 2, 3])  # 通过包调用函数
ary.reshape(1, 3)    # 通过对象调用方法
```

- `np.array()` 是函数。
- `ary.reshape()` 是 `ndarray` 对象的方法。

## 2. 为什么导入包后可以直接调用函数

Python 包通常表现为一个文件夹，其中可以包含多个 `.py` 文件：

```text
mypackage/
├── __init__.py
└── tools.py
```

假设 `tools.py` 中定义了函数：

```python
def hello():
    print("你好")
```

通常可以通过模块调用：

```python
from mypackage import tools

tools.hello()
```

如果包作者在 `__init__.py` 中将它暴露到包的顶层：

```python
from .tools import hello
```

使用者就可以直接写：

```python
import mypackage

mypackage.hello()
```

NumPy 也向使用者提供了许多顶层名称：

```python
np.array
np.ndarray
np.mean
np.sum
```

点号 `.` 可以理解为：到 `np` 代表的包对象中，寻找指定名称。

> [!note] 注意
> 包内部并不是所有函数都能通过“包名.函数名”直接调用。只有包作者公开到相应命名空间中的名称才可以这样使用。

## 3. `np.array()` 和 `np.asarray()` 的区别

两者都可以把 Python 列表转换成 `ndarray`：

```python
lst = [1, 2, 3]

a = np.array(lst)
b = np.asarray(lst)

print(type(a))  # <class 'numpy.ndarray'>
print(type(b))  # <class 'numpy.ndarray'>
```

因为列表不是 `ndarray`，两者都必须创建数组所需的内存。

主要区别出现在输入本身已经是 `ndarray` 时：

```python
original = np.array([1, 2, 3])

a = np.array(original)      # 默认创建副本
b = np.asarray(original)    # 条件符合时直接返回 original

print(a is original)  # False
print(b is original)  # True
```

可以简单记忆：

| 需求 | 推荐写法 |
| --- | --- |
| 明确希望得到一份独立数组 | `np.array()` 或 `.copy()` |
| 只想确保输入是 `ndarray`，并尽量避免复制 | `np.asarray()` |

如果 `asarray()` 需要改变数据类型，就可能必须创建新数组：

```python
a = np.array([1, 2, 3], dtype=np.int64)
b = np.asarray(a, dtype=np.float64)

print(a is b)                  # False
print(np.shares_memory(a, b))  # False
```

这是因为整数数据必须重新转换为浮点数，不能直接复用原来的内存表示。

## 4. 什么是视图

视图是一个新的数组对象，但它通常不复制底层数据，而是用不同的形状、步长或索引方式读取同一块内存。

```python
a = np.array([1, 2, 3])

b = a[:]             # 创建新的视图对象
c = np.asarray(a)    # 通常直接返回 a 本身

print(a is b)  # False
print(a is c)  # True
```

虽然 `a` 和 `b` 不是同一个 Python 对象，但它们共享底层内存：

```python
print(np.shares_memory(a, b))  # True
print(np.shares_memory(a, c))  # True
```

所以修改 `b` 或 `c` 都可能影响 `a`：

```python
b[0] = 100
c[1] = 200

print(a)  # [100 200   3]
```

二者的区别是：

```text
a[:]             → 新的 ndarray 对象，共享底层数据
np.asarray(a)    → 条件符合时就是原来的 a
```

## 5. 哪些操作通常会产生视图

### 5.1 基本切片

```python
a = np.array([1, 2, 3, 4, 5])

b = a[1:4]
c = a[::2]
d = a[:]
```

### 5.2 多维数组的基本索引和切片

```python
a = np.arange(9).reshape(3, 3)

b = a[:, 1]     # 取一列
c = a[1, :]     # 取一行
d = a[:2, :2]   # 取一块区域
```

取单个元素时返回的是 NumPy 标量，而不是数组视图：

```python
x = a[0, 0]
```

### 5.3 转置和轴调整

```python
b = a.T
b = a.transpose()
b = np.swapaxes(a, 0, 1)
b = np.moveaxis(a, 0, 1)
```

这些操作通常只改变数据的读取顺序，不复制底层数据。

### 5.4 改变形状

```python
b = a.reshape(1, 9)
b = np.squeeze(a)
b = np.expand_dims(a, axis=0)
```

`reshape()` 在内存布局允许时返回视图；如果无法只通过改变读取方式完成，则可能需要复制。

### 5.5 `ravel()` 和 `view()`

```python
b = a.ravel()  # 尽量返回视图，必要时复制
c = a.view()   # 显式创建共享数据的新数组对象
```

`flatten()` 与它们不同：

```python
b = a.flatten()  # 总是复制
```

### 5.6 高级索引通常产生副本

整数数组或列表索引：

```python
a = np.array([10, 20, 30, 40, 50])
b = a[[0, 2, 4]]
```

布尔索引：

```python
b = a[a > 20]
```

它们通常返回副本，而不是视图。

### 视图与副本速查

| 操作 | 常见结果 |
| --- | --- |
| 普通切片 | 视图 |
| 转置、轴调整 | 视图 |
| `reshape()` | 尽量产生视图，必要时可能复制 |
| `ravel()` | 尽量产生视图，必要时可能复制 |
| `view()` | 视图 |
| 整数列表/数组索引 | 副本 |
| 布尔索引 | 副本 |
| `flatten()` | 副本 |
| `copy()` | 副本 |

## 6. 如何理解 `.base`

`.base` 表示当前数组的底层内存依赖于哪个对象，但不保证一定指向“操作的上一步”，也不保证任何场景下都以同一种方式指向最原始数组。

### 6.1 数组自己拥有数据

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.base)  # None
```

`arr.base is None` 通常说明 `arr` 自己拥有底层内存。

### 6.2 转置视图依赖原数组

```python
arr2 = arr.T

print(arr2.base is arr)  # True
print(arr2.base is arr.base)  # False
```

最后一个结果为 `False`，是因为：

```python
arr2.base is arr
arr.base is None
```

因此 `arr2.base is arr.base` 实际是在判断：

```python
arr is None  # False
```

### 6.3 `reshape()` 产生的中间视图

```python
original = np.arange(6)
arr = original.reshape(2, 3)
arr2 = arr.T
```

这里真正拥有数据的是 `original`。`arr` 和 `arr2` 都可能依赖更底层的数组对象，因此不能把 `.base` 简单理解为“它直接由哪个变量创建”。

> [!tip] 最可靠的方法
> 想判断两个数组是否共享底层数据，优先使用 `np.shares_memory()`：
>
> ```python
> print(np.shares_memory(arr, arr2))
> ```

## 7. 为什么同时打印 `.data` 和分别打印看起来不同

```python
a = np.array([1, 2, 3])
b = a[:]
c = np.asarray(a)

print(a.data, b.data, c.data)
```

`.data` 返回的是一个临时的 `memoryview` 包装对象。打印结果中看到的地址通常是这个包装对象的地址，而不一定是底层数组数据的地址。

同时打印时，Python 会同时保留三个不同的临时 `memoryview` 对象，所以显示的地址可能不同：

```python
print(a.data, b.data, c.data)
```

分别打印时，前一个临时对象在打印后可能被释放，后一个临时对象可能复用同一块对象内存，因此显示的地址可能看起来相同：

```python
print(a.data)
print(b.data)
print(c.data)
```

这不能用于判断数组是否共享数据。

如果想查看数组数据的起始内存地址，可以使用：

```python
print(a.ctypes.data)
print(b.ctypes.data)
print(c.ctypes.data)
```

但切片可能从原数组的不同位置开始，因此起始地址不同也不一定代表完全没有共享内存。最终仍应使用：

```python
np.shares_memory(a, b)
```

## 8. `strides` 与转置视图

`strides` 表示沿着每个轴移动一个位置时，需要跨过多少个字节。

```python
arr = np.arange(6).reshape(2, 3)

print(arr)
print(arr.strides)

arr2 = arr.T
print(arr2.strides)
```

假设数组元素的数据类型为 `int64`，每个元素占 8 字节，常见结果是：

```text
arr.strides  = (24, 8)
arr2.strides = (8, 24)
```

解释：

- `arr` 每行有 3 个元素，移动到下一行需要跨过 `3 × 8 = 24` 字节。
- `arr` 在同一行移动到下一列，只需跨过 8 字节。
- 转置后通常不需要重新排列或复制数据，只需交换形状和步长信息。

这也是 `arr.T` 通常能够成为视图的原因。

## 9. `is`、`.base` 与共享内存的区别

这三个判断回答的是不同问题：

```python
a is b
b.base is a
np.shares_memory(a, b)
```

| 写法                       | 回答的问题                      |
| ------------------------ | -------------------------- |
| `a is b`                 | `a` 和 `b` 是否为同一个 Python 对象 |
| `b.base is a`            | `b.base` 当前是否恰好指向 `a`      |
| `np.shares_memory(a, b)` | 两个数组是否共享底层内存               |

示例：

```python
a = np.array([1, 2, 3])
b = a[:]
c = np.asarray(a)

print(a is b)                  # False
print(a is c)                  # True
print(np.shares_memory(a, b))  # True
print(np.shares_memory(a, c))  # True
```

## 10. bit 和 Byte

正确的换算是：

```text
1 Byte（字节）= 8 bit（比特/位）
```

- `bit` 是最小的数据单位，只能表示 `0` 或 `1`。
- `Byte` 由 8 个 bit 组成。
- 小写 `b` 通常表示 bit。
- 大写 `B` 通常表示 Byte。

常见换算：

```text
1 Byte = 8 bit
1 KB = 1024 Byte
1 MB = 1024 KB
1 GB = 1024 MB
```

例如，网络带宽 `100 Mbps` 表示每秒 100 兆比特，理论下载速度约为：

```text
100 ÷ 8 = 12.5 MB/s
```

`strides` 中的数字以字节为单位，因此一个 `int64` 元素通常占：

```text
64 bit ÷ 8 = 8 Byte
```

## 11. 最终记忆清单

> [!success] 核心结论
> - `numpy` 是包，`np` 是它的别名。
> - `np.array()` 是函数，返回 `np.ndarray` 对象。
> - `np.array()` 默认倾向于创建独立数组；`np.asarray()` 尽量避免不必要的复制。
> - 普通切片、转置和许多形状调整操作通常产生视图。
> - 视图是不同的数组对象，但可能共享同一块底层内存。
> - 整数数组索引和布尔索引通常产生副本。
> - `.base is None` 通常表示数组自己拥有数据，但 `.base` 不适合单独作为共享内存的最终判断依据。
> - `.data` 返回的是 `memoryview` 包装对象，打印结果不能直接证明是否共享底层内存。
> - 判断是否为同一对象：使用 `is`。
> - 判断是否共享内存：使用 `np.shares_memory()`。
> - `1 Byte = 8 bit`，不是 `1 bit = 8 Byte`。

## 12. 综合验证代码

```python
import numpy as np

# 1. 创建数组
a = np.array([1, 2, 3, 4, 5, 6])

# 2. 整体切片：新对象，但共享内存
b = a[:]

# 3. asarray：条件符合时直接返回 a
c = np.asarray(a)

# 4. array：默认创建独立数组
d = np.array(a)

print("对象身份：")
print(a is b)  # False
print(a is c)  # True
print(a is d)  # False

print("是否共享内存：")
print(np.shares_memory(a, b))  # True
print(np.shares_memory(a, c))  # True
print(np.shares_memory(a, d))  # False

print("base：")
print(a.base)       # None
print(b.base is a)  # True

print("数据起始地址：")
print(a.ctypes.data)
print(b.ctypes.data)
print(c.ctypes.data)
print(d.ctypes.data)

# 5. 转置视图与 strides
matrix = a.reshape(2, 3)
transposed = matrix.T

print(matrix.strides)
print(transposed.strides)
print(np.shares_memory(matrix, transposed))  # True
```
