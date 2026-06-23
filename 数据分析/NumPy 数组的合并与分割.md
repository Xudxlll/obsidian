---
title: NumPy 数组的合并与分割
date: 2026-06-18
tags:
  - Python
  - NumPy
  - ndarray
  - 数据分析
source_note: "[[Clippings/2026-06-18-3-6 Numpy数组的合并与分割]]"
source_url: https://www.bilibili.com/video/BV1T2X8YBEMK/
---


> [!abstract] 本文主线
> - `np.concatenate()` 可以沿指定轴拼接多个同维数组。
> - `np.vstack()` 主要用于上下堆叠，`np.hstack()` 主要用于左右堆叠。
> - `np.stack()` 会创建一个新轴，用来保留“第几个数组”这一层结构。
> - 合并前必须检查数组的维度和形状是否匹配。
> - `np.split()` 可以按分割点或等份数量拆分数组。
> - `np.vsplit()` 用于上下分割，`np.hsplit()` 用于左右分割。
> - 在机器学习中，数组分割常用于把特征矩阵 `X` 和目标值 `y` 分开。

# 1. 准备示例数组

```python
import numpy as np

x = np.array([1, 2, 3])
y = np.array([4, 5, 6])
z = np.array([6, 6, 6])

A = np.array([
    [1, 2, 3],
    [4, 5, 6]
])
```

这些数组的形状分别是：

```python
print(x.shape)  # (3,)
print(A.shape)  # (2, 3)
```

- `x` 是包含 3 个元素的一维数组。
- `A` 是 2 行 3 列的二维数组。
- 如果把 `A` 看成数据集，可以理解为“2 个样本，每个样本有 3 个特征”。

# 2. `np.concatenate()`：沿指定轴合并数组

## 2.1 合并一维数组

```python
result = np.concatenate([x, y])

print(result)
# [1 2 3 4 5 6]

print(result.shape)
# (6,)
```

`np.concatenate()` 的第一个参数是由待合并数组组成的序列，可以一次传入两个或更多数组：

```python
result = np.concatenate([x, y, z])

print(result)
# [1 2 3 4 5 6 6 6 6]
```

## 2.2 合并二维数组

```python
result = np.concatenate([A, A])

print(result)
# [[1 2 3]
#  [4 5 6]
#  [1 2 3]
#  [4 5 6]]

print(result.shape)
# (4, 3)
```

`axis` 的默认值为 `0`，所以这里沿第 0 轴合并，行数从 2 增加到 4。

从数据集角度理解：

```text
原数据：2个样本 × 3个特征
新数据：2个样本 × 3个特征
合并后：4个样本 × 3个特征
```

# 3. 如何理解 `axis`

对于形状为 `(行数, 列数)` 的二维数组：

| `axis` | 合并方向 | 变化的部分 | 数据含义 |
| --- | --- | --- | --- |
| `axis=0` | 上下合并 | 行数增加 | 增加样本 |
| `axis=1` | 左右合并 | 列数增加 | 增加特征 |


![539](assets/NumPy%20数组的合并与分割/数组的轴2.png)

![](assets/NumPy%20数组的合并与分割/数组的轴1.png)

## 3.1 `axis=0`：增加行

```python
result = np.concatenate([A, A], axis=0)

print(result.shape)
# (4, 3)
```

## 3.2 `axis=1`：增加列

```python
result = np.concatenate([A, A], axis=1)

print(result)
# [[1 2 3 1 2 3]
#  [4 5 6 4 5 6]]

print(result.shape)
# (2, 6)
```

从数据集角度理解：

```text
原数据：2个样本 × 3个特征
新增：相同2个样本的另外3个特征
合并后：2个样本 × 6个特征
```

> [!tip] 判断方法
> `axis` 表示“沿着哪个轴进行操作”，也就是结果中哪个轴的长度会发生变化。

# 4. 合并数组时的形状要求

`np.concatenate()` 要求：

1. 待合并数组的维度数必须相同。
2. 除了合并轴之外，其他轴的长度必须相同。

例如，`A` 是二维数组，`z` 是一维数组：

```python
print(A.shape)  # (2, 3)
print(z.shape)  # (3,)

# np.concatenate([A, z], axis=0)
# ValueError：两个数组的维度数不同
```

如果想把 `z` 作为一个新样本添加到 `A` 中，需要先把它变成 1 行 3 列的二维数组：

```python
z_2d = z.reshape(1, -1)

result = np.concatenate([A, z_2d], axis=0)

print(result)
# [[1 2 3]
#  [4 5 6]
#  [6 6 6]]

print(result.shape)
# (3, 3)
```

这里：

```text
z.shape      → (3,)
z_2d.shape   → (1, 3)
```

`-1` 表示让 NumPy 根据元素总数自动计算这一维的长度。

# 5. 合并操作不会修改原数组

```python
A2 = np.concatenate([A, z.reshape(1, -1)], axis=0)

print(A.shape)   # (2, 3)
print(A2.shape)  # (3, 3)
```

`np.concatenate()` 返回一个新的数组结果，不会直接修改 `A`。

如果需要保存合并结果，必须赋值给变量：

```python
A = np.concatenate([A, z.reshape(1, -1)], axis=0)
```

# 6. `np.vstack()`：上下堆叠

`vstack` 中的 `v` 是 `vertical`，表示垂直堆叠。对于二维数据，可以把它理解为增加行。

```python
result = np.vstack([A, z])

print(result)
# [[1 2 3]
#  [4 5 6]
#  [6 6 6]]

print(result.shape)
# (3, 3)
```

虽然 `A` 是二维数组、`z` 是一维数组，但 `vstack()` 会把一维数组按一行处理，因此这里不需要手动执行 `reshape()`。

对于本例，下面两种写法结果相同：

```python
np.concatenate([A, z.reshape(1, -1)], axis=0)
np.vstack([A, z])
```

> [!warning] `vstack()` 不是无条件合并
> 上下堆叠时，各数组的列数必须相同。

# 7. `np.hstack()`：左右堆叠

`hstack` 中的 `h` 是 `horizontal`，表示水平堆叠。对于二维数据，可以把它理解为增加列。

```python
B = np.full((2, 2), 100)

result = np.hstack([A, B])

print(result)
# [[  1   2   3 100 100]
#  [  4   5   6 100 100]]

print(result.shape)
# (2, 5)
```

形状变化为：

```text
A：(2, 3)
B：(2, 2)
结果：(2, 5)
```

左右堆叠时，两个数组的行数必须相同。

因此下面的代码会报错：

```python
# A.shape为(2, 3)，z.shape为(3,)
# np.hstack([A, z])
```

如果要把一列数据添加到 `A` 的右侧，需要让新数据具有 2 行：

```python
new_feature = np.array([10, 20]).reshape(-1, 1)
result = np.hstack([A, new_feature])

print(result)
# [[ 1  2  3 10]
#  [ 4  5  6 20]]
```

# 8. `np.stack()`：创建新轴后堆叠

前面的 `concatenate()`、`vstack()` 和 `hstack()` 都是在已有轴上连接数据。`np.stack()` 的关键区别是：

> `np.stack()` 会先创建一个新轴，再沿这个新轴排列多个数组。

## 8.1 把两个二维数组看成两个平面

```python
a = np.arange(1, 7).reshape(2, 3)
b = np.arange(7, 13).reshape(2, 3)

print(a)
# [[1 2 3]
#  [4 5 6]]

print(b)
# [[ 7  8  9]
#  [10 11 12]]
```

如果希望保留 `a`、`b` 两个完整平面，可以沿新建的第 0 轴堆叠：

```python
result = np.stack((a, b), axis=0)

print(result)
# [[[ 1  2  3]
#   [ 4  5  6]]
#
#  [[ 7  8  9]
#   [10 11 12]]]

print(result.shape)
# (2, 2, 3)
```

形状可以读成：

```text
(2, 2, 3)
 ↑  ↑  ↑
平面 行 列
```

因此：

```python
print(result[0])  # 第一个完整平面a
print(result[1])  # 第二个完整平面b
```

数组结构为：

```text
result
├── result[0]：平面a，shape=(2,3)
└── result[1]：平面b，shape=(2,3)
```

## 8.2 `axis` 决定新轴插入在哪里

假设输入数组形状都是：

```text
a.shape = b.shape = (2, 3)
```

堆叠两个数组时，新轴的长度为 2。`axis` 决定这个新轴插入 `shape` 的哪个位置：

| 写法 | 新轴位置 | 结果形状 | 可理解为 |
| --- | --- | --- | --- |
| `np.stack((a,b), axis=0)` | 最前面 | `(2,2,3)` | 数组来源 × 行 × 列 |
| `np.stack((a,b), axis=1)` | 中间 | `(2,2,3)` | 行 × 数组来源 × 列 |
| `np.stack((a,b), axis=2)` | 最后面 | `(2,3,2)` | 行 × 列 × 数组来源 |
| `np.stack((a,b), axis=-1)` | 最后面 | `(2,3,2)` | 与 `axis=2` 相同 |

这里 `axis=0` 和 `axis=1` 碰巧都得到 `(2,2,3)`，是因为“数组数量”和原数组的行数刚好都是 2；虽然形状相同，内部元素的组织顺序并不相同。

可以使用下面的通用规则判断结果形状：

```text
输入形状：(d0, d1, ..., dn)
数组数量：k

axis=0  → (k, d0, d1, ..., dn)
axis=1  → (d0, k, d1, ..., dn)
axis=-1 → (d0, d1, ..., dn, k)
```

## 8.3 `stack()` 和 `concatenate()` 的区别

```python
joined = np.concatenate((a, b), axis=0)
stacked = np.stack((a, b), axis=0)

print(joined.shape)   # (4, 3)
print(stacked.shape)  # (2, 2, 3)
```

`concatenate()` 沿已有的行轴连接：

```text
两张2行3列的表 → 一张4行3列的表
```

`stack()` 创建新的数组来源轴：

```text
两张2行3列的表 → 2个平面，每个平面都是2行3列
```

对应关系是：

```text
concatenate(axis=0)：result[行, 列]
stack(axis=0)：      result[平面编号, 行, 列]
```

`stack(axis=0)` 也可以理解为先给每个数组增加一个轴，再执行连接：

```python
np.stack((a, b), axis=0)

# 大致等价于
np.concatenate((a[None, :, :], b[None, :, :]), axis=0)
```

## 8.4 `stack()` 和 `dstack()` 的关系

`dstack` 是 `depth stack` 的缩写，表示沿深度轴堆叠。它也可以把 `a`、`b` 看成两个完整平面，但它把“平面编号”放在最后一个轴 `axis=2`。

```python
a = np.arange(1, 7).reshape(2, 3)
b = np.arange(7, 13).reshape(2, 3)

result = np.dstack((a, b))

print(result)
# [[[ 1  7]
#   [ 2  8]
#   [ 3  9]]
#
#  [[ 4 10]
#   [ 5 11]
#   [ 6 12]]]

print(result.shape)
# (2, 3, 2)
```

它的形状应当读成：

```text
(2, 3, 2)
 ↑  ↑  ↑
行 列 深度/平面编号
```

### 8.4.1 `dstack()` 内部做了什么

对于二维数组，`dstack()` 可以理解为先给每个数组增加一个深度轴：

```python
print(a[:, :, None].shape)  # (2,3,1)
print(b[:, :, None].shape)  # (2,3,1)
# 此时还是按照标准顺序来看这个表，2是深度，3是行，1是列
```

`a` 大致由：

```text
[[1, 2, 3],
 [4, 5, 6]]
```

变成：

```text
[[[1],
  [2],
  [3]],

 [[4],
  [5],
  [6]]]
```

`b`也一样

```text
[[[ 7],
  [ 8],
  [ 9]],

 [[10],
  [11],
  [12]]]
```

然后 NumPy 沿最后一个轴，把相同行列位置的小列表合并：

```text
[1]和[7]  → [1,7]
[2]和[8]  → [2,8]
[3]和[9]  → [3,9]
```

因此相同行列位置的元素会被放到一起：

```text
a[0,0]=1，b[0,0]=7  → result[0,0]=[1,7]
a[0,1]=2，b[0,1]=8  → result[0,1]=[2,8]
```

### 8.4.2 如何取回两个完整平面

虽然打印结果看起来像把数字两两放在一起，但两个完整平面仍然存在。因为平面编号位于 `axis=2`，所以要用第三个索引选择平面：

```python
print(result[:, :, 0])
# [[1 2 3]
#  [4 5 6]]

print(result[:, :, 1])
# [[ 7  8  9]
#  [10 11 12]]
```

可以验证：

```python
print(np.array_equal(result[:, :, 0], a))  # True
print(np.array_equal(result[:, :, 1], b))  # True
```

所以 `dstack()` 的索引顺序是：

```python
result[行, 列, 平面编号]
```

### 8.4.3 与 `stack(axis=0)` 的区别

```python
c1 = np.stack((a, b), axis=0)
c2 = np.dstack((a, b))
```

它们都可以表示两个平面，区别只是“平面编号轴”放在哪里：

```text
stack(axis=0)：(平面编号, 行, 列) → shape=(2,2,3)
dstack()：     (行, 列, 平面编号) → shape=(2,3,2)
```

因此取出完整平面的写法不同：

```python
c1[0, :, :]  # 从stack(axis=0)的结果中取出a
c1[1, :, :]  # 从stack(axis=0)的结果中取出b

c2[:, :, 0]  # 从dstack()的结果中取出a
c2[:, :, 1]  # 从dstack()的结果中取出b
```

对于形状相同的二维数组，下面两种写法结果相同：

```python
np.dstack((a, b))
np.stack((a, b), axis=2)
```

也可以理解为：

```python
np.dstack((a, b))

# 对二维数组而言，大致等价于
np.concatenate((a[:, :, None], b[:, :, None]), axis=2)
```

> [!tip] 核心理解
> `dstack()` 也在堆平面，只是把“第几个平面”放在最后一个轴。因此要使用 `result[:, :, 0]`、`result[:, :, 1]` 取出各个平面。

## 8.5 `stack()` 的形状要求

`np.stack()` 要求所有输入数组的形状完全相同：

```python
a = np.ones((2, 3))
b = np.zeros((2, 3))

result = np.stack((a, b), axis=0)  # 可以
```

下面的形状不同，不能直接堆叠：

```python
a = np.ones((2, 3))
b = np.zeros((1, 3))

# np.stack((a, b), axis=0)
# ValueError：所有输入数组必须具有相同形状
```

这与 `concatenate()` 不同：`concatenate()` 只要求除合并轴以外的其他轴长度相同；`stack()` 因为保留每个完整输入数组，所以要求所有输入形状完全一致。

## 8.6 五种合并方式的对比

| 方法 | 是否创建新轴 | 二维数组中的常见效果 |
| --- | --- | --- |
| `np.concatenate(..., axis=0)` | 否 | 在已有第 0 轴上连接，增加行 |
| `np.concatenate(..., axis=1)` | 否 | 在已有第 1 轴上连接，增加列 |
| `np.vstack(...)` | 否 | 上下堆叠，通常增加行 |
| `np.hstack(...)` | 否 | 左右堆叠，通常增加列 |
| `np.stack(..., axis=...)` | 是 | 创建新轴，保留每个输入数组的完整结构 |

日常使用时：

- 想在已有轴上明确连接，使用 `np.concatenate()`。
- 想直观表达二维数组的上下堆叠，使用 `np.vstack()`。
- 想直观表达二维数组的左右堆叠，使用 `np.hstack()`。
- 想增加“批次、平面、时间或数组来源”等新维度，使用 `np.stack()`。

# 9. `np.split()`：按位置分割数组

## 9.1 分割一维数组

```python
x = np.arange(10)

x1, x2, x3 = np.split(x, [3, 7])

print(x1)  # [0 1 2]
print(x2)  # [3 4 5 6]
print(x3)  # [7 8 9]
```

分割点 `[3, 7]` 的含义与切片边界一致：

```text
x1 = x[:3]
x2 = x[3:7]
x3 = x[7:]
```

分割点位置本身属于后面一段。

规律是：

```text
n个分割点 → 最多得到n+1段
```

如果只传入一个分割点：

```python
x1, x2 = np.split(x, [5])

print(x1)  # [0 1 2 3 4]
print(x2)  # [5 6 7 8 9]
```

## 9.2 按等份数量分割

第二个参数也可以直接写成整数，表示把数组平均分成多少份：

```python
x1, x2 = np.split(x, 2)
```

这种写法要求数组能够被平均分割，否则会报错：

```python
# np.split(np.arange(10), 3)
# ValueError：10个元素不能平均分成3份
```

如果允许各段长度不完全相等，可以使用：

```python
np.array_split(np.arange(10), 3)
```

# 10. 分割二维数组

```python
A = np.arange(16).reshape(4, 4)

print(A)
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]
#  [12 13 14 15]]
```

## 10.1 `axis=0`：上下分割

```python
A1, A2 = np.split(A, [2], axis=0)

print(A1)
# [[0 1 2 3]
#  [4 5 6 7]]

print(A2)
# [[ 8  9 10 11]
#  [12 13 14 15]]
```

第 0 轴对应行，因此结果是上半部分和下半部分。

## 10.2 `axis=1`：左右分割

```python
A1, A2 = np.split(A, [2], axis=1)

print(A1)
# [[ 0  1]
#  [ 4  5]
#  [ 8  9]
#  [12 13]]

print(A2)
# [[ 2  3]
#  [ 6  7]
#  [10 11]
#  [14 15]]
```

第 1 轴对应列，因此结果是左半部分和右半部分。

# 11. `np.vsplit()` 和 `np.hsplit()`

## 11.1 `np.vsplit()`：上下分割

```python
upper, lower = np.vsplit(A, [2])
```

对于二维数组，它相当于：

```python
upper, lower = np.split(A, [2], axis=0)
```

## 11.2 `np.hsplit()`：左右分割

```python
left, right = np.hsplit(A, [2])
```

对于二维数组，它相当于：

```python
left, right = np.split(A, [2], axis=1)
```

## 11.3 分割方法速查

| 方法                      | 二维数组中的分割方式 | 常见结果   |
| ----------------------- | ---------- | ------ |
| `np.split(..., axis=0)` | 沿第 0 轴分割   | 上、下两部分 |
| `np.split(..., axis=1)` | 沿第 1 轴分割   | 左、右两部分 |
| `np.vsplit(...)`        | 上下分割       | 上、下两部分 |
| `np.hsplit(...)`        | 左右分割       | 左、右两部分 |
| `np.vsplit(A, 2)`       | 如果是不加中括号的话 | 代表平分数组 |


# 12. 机器学习中的典型场景：分离特征和目标值

假设每一行代表一个样本，前三列是特征，最后一列是目标值：

```python
data = np.array([
    [1.2, 3.4, 5.6, 0],
    [2.3, 4.5, 6.7, 1],
    [3.4, 5.6, 7.8, 0],
    [4.5, 6.7, 8.9, 1]
])
```

可以在最后一列之前进行水平分割：

```python
X, y_2d = np.hsplit(data, [-1])

print(X.shape)     # (4, 3)
print(y_2d.shape)  # (4, 1)
```

其中：

- `X` 是特征矩阵，包含 4 个样本、每个样本 3 个特征。
- `y_2d` 是目标值组成的二维单列数组。

如果希望目标值是形状为 `(4,)` 的一维数组，可以取出第 0 列：

```python
y = y_2d[:, 0]

print(y.shape)
# (4,)
```

也可以直接使用切片完成同样的任务：

```python
X = data[:, :-1]
y = data[:, -1]
```

在实际数据处理中，切片写法通常更加简洁；当需要把数组拆成多个连续区域时，`split()` 系列方法会更直观。

# 13. 常见错误

## 13.1 数组维度数不同

```python
A.shape  # (2, 3)
z.shape  # (3,)
```

二维数组和一维数组不能直接用 `concatenate()` 合并。应先使用 `reshape()` 统一维度，或选择适合的 `vstack()`。

## 13.2 非合并轴的长度不同

上下合并要求列数相同，左右合并要求行数相同。

```text
上下合并：(2, 3)和(1, 3)可以
左右合并：(2, 3)和(2, 2)可以
```

## 13.3 忘记保存合并结果

```python
np.concatenate([A, A])
```

这行代码虽然生成了新数组，但没有把结果保存下来。应写成：

```python
result = np.concatenate([A, A])
```

## 13.4 混淆分割点和分割份数

```python
np.split(x, [3, 7])  # 在索引3和7的位置切开
np.split(x, 2)       # 平均分成2份
```

列表表示分割点，整数表示等分数量。

# 14. 综合示例

```python
import numpy as np

# 两批样本，每个样本有3个特征
batch1 = np.array([
    [1, 2, 3],
    [4, 5, 6]
])

batch2 = np.array([
    [7, 8, 9],
    [10, 11, 12]
])

# 上下合并：增加样本
all_samples = np.vstack([batch1, batch2])

# 新增一列特征
new_feature = np.array([100, 200, 300, 400]).reshape(-1, 1)
dataset = np.hstack([all_samples, new_feature])

# 将前三列与最后一列分开
X, y_2d = np.hsplit(dataset, [-1])
y = y_2d[:, 0]

print(dataset)
print("X.shape =", X.shape)  # (4, 3)
print("y.shape =", y.shape)  # (4,)
```

# 15. 最终记忆清单

> [!success] 核心结论
> - `np.concatenate()` 可以合并多个数组，并通过 `axis` 指定合并轴。
> - 对二维数组来说，`axis=0` 通常表示增加行，`axis=1` 通常表示增加列。
> - `np.vstack()` 用于上下堆叠，`np.hstack()` 用于左右堆叠。
> - `np.stack()` 会创建新轴；`axis` 决定新轴插入结果形状的哪个位置。
> - `np.stack((a,b), axis=0)` 可以把两个二维数组保留为两个完整平面，结果形状为 `(数组数量, 行, 列)`。
> - `np.dstack((a,b))` 把平面编号放在最后一轴，结果按 `(行, 列, 平面编号)` 组织，可用 `result[:, :, 0]`、`result[:, :, 1]` 取回各平面。
> - `concatenate()` 在已有轴上连接，`stack()` 则创建新轴，并要求所有输入数组形状完全相同。
> - 合并数组时，维度数必须一致，并且除合并轴外的其他轴长度必须相同。
> - 合并函数返回新数组，不会直接修改原数组。
> - `np.split()` 中，列表表示分割点，整数表示平均分割的份数。
> - `np.vsplit()` 用于上下分割，`np.hsplit()` 用于左右分割。
> - `n` 个合法分割点最多把数组分成 `n+1` 段。
> - 机器学习中经常需要把数据表拆成特征矩阵 `X` 和目标值 `y`。
> - 如果目标值是 `(n, 1)` 的单列二维数组，可以使用 `y[:, 0]` 转成 `(n,)` 的一维数组。

# 来源说明

本文根据视频字幕重新整理，并对字幕中的函数名称、参数写法和示例代码进行了规范化。原始字幕见：[[Clippings/2026-06-18-3-6 Numpy数组的合并与分割]]。
