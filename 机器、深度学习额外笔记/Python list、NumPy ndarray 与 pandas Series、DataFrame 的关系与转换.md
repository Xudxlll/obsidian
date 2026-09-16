---
title: Python list、NumPy ndarray 与 pandas Series、DataFrame 的关系与转换
date: 2026-09-16
tags:
  - Python
  - NumPy
  - pandas
  - 数据结构
---

# Python list、NumPy ndarray 与 pandas Series、DataFrame 的关系与转换

> [!abstract] 本文主线
> - `list` 是 Python 通用容器，元素可以是不同类型。
> - `ndarray` 是 NumPy 的多维数组，通常使用统一的数据类型，适合高效数值运算。
> - `Series` 是带 `index` 的一维数据结构，可以理解为“数据值 + 行标签”。
> - `DataFrame` 是带行、列标签的二维表格，可以理解为多个 Series 按列组合而成。
> - 结构转换时，要特别留意维度、标签、数据类型以及是否复制数据。

## 1. 四种数据结构之间的关系

可以先用下面这条主线理解它们：

```text
Python list
    ↓ 增强数值计算能力，通常统一元素类型
NumPy ndarray
    ↓ 增加 index 标签
pandas Series
    ↓ 多个 Series 按列组成表格
pandas DataFrame
```

这只是帮助理解的主线，并不表示它们内部完全等价。尤其是 pandas 还支持自己的扩展数据类型，DataFrame 也不一定只是一个普通二维 `ndarray`。

| 数据结构 | 常见维度 | 是否有标签 | 数据类型 | 典型用途 |
| --- | ---: | --- | --- | --- |
| `list` | 一维，也可嵌套 | 无 | 可以混合 | 普通 Python 数据存储 |
| `ndarray` | 任意维度 | 无 | 通常统一 | 向量、矩阵和高效数值计算 |
| `Series` | 一维 | 有 `index` | 一列通常一种类型 | 带标签的一列数据 |
| `DataFrame` | 二维 | 有 `index` 和 `columns` | 不同列可以不同 | 表格数据分析 |

## 2. Python `list`：通用容器

```python
data = [10, 20, 30]
```

列表可以存放不同类型的对象：

```python
data = [10, "张三", True]
```

但是列表本身不进行向量化数值运算：

```python
data = [1, 2, 3]

print(data * 2)
# [1, 2, 3, 1, 2, 3]
```

这里的 `* 2` 是把列表重复两遍，而不是让每个元素乘以 2。

## 3. NumPy `ndarray`：高效多维数组

```python
import numpy as np

arr = np.array([1, 2, 3])

print(arr * 2)
# [2 4 6]
```

NumPy 数组支持向量化运算。它还可以是二维或更高维：

```python
arr2 = np.array([
    [90, 80],
    [85, 70],
    [95, 88]
])

print(arr2.shape)
# (3, 2)
```

二维 `ndarray` 可以理解为“没有行名和列名的矩阵”。为保证高效计算，一个数组通常使用统一的 `dtype`。

## 4. pandas `Series`：带标签的一维数据

```python
import pandas as pd

s = pd.Series(
    [90, 85, 95],
    index=["张三", "李四", "王五"],
    name="数学成绩"
)
```

一个 Series 主要包含：

```text
数据值 values + 索引 index + 名称 name
```

既可以按位置访问，也可以按标签访问：

```python
s.iloc[0]       # 按位置访问，得到 90
s.loc["张三"]  # 按标签访问，得到 90
```

### 4.1 Series 会按照标签对齐

```python
s1 = pd.Series([10, 20], index=["a", "b"])
s2 = pd.Series([1, 2], index=["b", "a"])

print(s1 + s2)
```

结果为：

```text
a    12
b    21
```

计算过程是：

```text
a：10 + 2 = 12
b：20 + 1 = 21
```

NumPy 数组通常按照位置计算，而 Series 在运算前通常会按照索引标签对齐。

## 5. pandas `DataFrame`：带行列标签的二维表格

```python
df = pd.DataFrame({
    "姓名": ["张三", "李四", "王五"],
    "数学": [90, 85, 95],
    "英语": [80, 70, 88]
})
```

DataFrame 具有：

- 行索引：`df.index`
- 列标签：`df.columns`
- 每一列可以有自己的数据类型

可以把 DataFrame 理解为多个 Series 按列组合：

```text
DataFrame
├── 姓名列：Series
├── 数学列：Series
└── 英语列：Series
```

取出一列后通常得到 Series：

```python
s = df["数学"]

print(type(s))
# <class 'pandas.core.series.Series'>
```

## 6. 转换方法总览

```text
list
 ├─ np.array(lst) ───────────→ ndarray
 ├─ pd.Series(lst) ──────────→ Series
 └─ pd.DataFrame(data) ──────→ DataFrame

ndarray
 ├─ arr.tolist() ────────────→ list
 ├─ pd.Series(arr) ──────────→ Series（通常要求一维）
 └─ pd.DataFrame(arr) ───────→ DataFrame

Series
 ├─ s.tolist() ──────────────→ list
 ├─ s.to_numpy() ────────────→ ndarray
 └─ s.to_frame() ────────────→ DataFrame

DataFrame
 ├─ df.to_numpy().tolist() ──→ 嵌套 list
 ├─ df.to_numpy() ───────────→ ndarray
 ├─ df["列名"] ──────────────→ Series
 └─ df.squeeze("columns") ───→ Series（仅一列时）
```

## 7. `list` 与 `ndarray` 互相转换

### 7.1 `list` 转 `ndarray`

```python
lst = [10, 20, 30]
arr = np.array(lst)
```

嵌套列表可以转换成二维数组：

```python
lst2 = [
    [1, 2],
    [3, 4]
]

arr2 = np.array(lst2)
```

### 7.2 `ndarray` 转 `list`

```python
lst = arr.tolist()
```

`tolist()` 会根据数组维度递归生成嵌套列表：

```python
arr2.tolist()
# [[1, 2], [3, 4]]
```

## 8. `list` 与 `Series` 互相转换

### 8.1 `list` 转 `Series`

```python
lst = [90, 85, 95]

s = pd.Series(
    lst,
    index=["张三", "李四", "王五"],
    name="数学成绩"
)
```

如果不指定 `index`，默认使用从 0 开始的整数索引。

### 8.2 `Series` 转 `list`

```python
lst = s.tolist()
# [90, 85, 95]
```

转换为列表后，Series 的 `index` 和 `name` 会丢失。如果希望保留“标签—数据”的对应关系，可以转成字典：

```python
s.to_dict()
# {'张三': 90, '李四': 85, '王五': 95}
```

## 9. `ndarray` 与 `Series` 互相转换

### 9.1 一维 `ndarray` 转 `Series`

```python
arr = np.array([90, 85, 95])

s = pd.Series(
    arr,
    index=["张三", "李四", "王五"],
    name="数学成绩"
)
```

Series 是一维数据结构，普通二维数组不能直接转换成一个 Series：

```python
arr2 = np.array([
    [1, 2],
    [3, 4]
])

# pd.Series(arr2)
# ValueError: Data must be 1-dimensional
```

二维数组通常应转换成 DataFrame。

### 9.2 `Series` 转 `ndarray`

推荐使用：

```python
arr = s.to_numpy()
```

也可以使用：

```python
arr = s.values
```

新代码通常优先使用 `.to_numpy()`，因为它明确表达了“转换成 NumPy 数组”的目的。转换后不会保留 Series 的 `index` 和 `name`。

## 10. `list` 与 `DataFrame` 互相转换

### 10.1 二维 `list` 转 `DataFrame`

```python
data = [
    ["张三", 90, 80],
    ["李四", 85, 70],
    ["王五", 95, 88]
]

df = pd.DataFrame(
    data,
    columns=["姓名", "数学", "英语"]
)
```

这里每个内层列表表示一行。

### 10.2 “字典中的列表”转 `DataFrame`

```python
data = {
    "姓名": ["张三", "李四", "王五"],
    "数学": [90, 85, 95],
    "英语": [80, 70, 88]
}

df = pd.DataFrame(data)
```

这里每个字典键成为列名，对应的列表成为一列。

### 10.3 `DataFrame` 转二维 `list`

```python
data = df.to_numpy().tolist()
```

结果类似：

```python
[
    ["张三", 90, 80],
    ["李四", 85, 70],
    ["王五", 95, 88]
]
```

这种转换会丢失行索引和列名。如果希望每一行都保留列名，适合转换成“字典列表”：

```python
records = df.to_dict(orient="records")
```

结果类似：

```python
[
    {"姓名": "张三", "数学": 90, "英语": 80},
    {"姓名": "李四", "数学": 85, "英语": 70},
    {"姓名": "王五", "数学": 95, "英语": 88}
]
```

## 11. `ndarray` 与 `DataFrame` 互相转换

### 11.1 二维 `ndarray` 转 `DataFrame`

```python
arr = np.array([
    [90, 80],
    [85, 70],
    [95, 88]
])

df = pd.DataFrame(
    arr,
    index=["张三", "李四", "王五"],
    columns=["数学", "英语"]
)
```

这相当于给原本没有标签的数组增加行索引和列标签。

### 11.2 `DataFrame` 转 `ndarray`

推荐使用：

```python
arr = df.to_numpy()
```

也可以使用：

```python
arr = df.values
```

转换时需要注意：

1. 行索引和列名会丢失。
2. 如果不同列的数据类型不同，NumPy 为了使用统一 `dtype`，可能会进行类型转换。
3. 混合字符串和数字的 DataFrame 转为数组后，数组的 `dtype` 可能是 `object`。

例如：

```python
df = pd.DataFrame({
    "姓名": ["张三", "李四"],
    "成绩": [90, 85]
})

arr = df.to_numpy()
print(arr.dtype)
# object
```

## 12. `Series` 与 `DataFrame` 互相转换

### 12.1 `Series` 转 `DataFrame`

```python
s = pd.Series(
    [90, 85, 95],
    index=["张三", "李四", "王五"],
    name="数学"
)

df = s.to_frame()
```

如果 Series 没有名称，可以在转换时指定列名：

```python
df = s.to_frame(name="数学")
```

### 12.2 `DataFrame` 取一列得到 `Series`

```python
s = df["数学"]
```

单层方括号和双层方括号的结果不同：

```python
df["数学"]       # Series，一维
df[["数学"]]     # DataFrame，二维
```

可以记成：

```text
单括号取一列   → Series
双括号取列集合 → DataFrame
```

### 12.3 使用 `squeeze()` 压缩单列 DataFrame

当 DataFrame 只有一列时，可以把长度为 1 的列维度压缩掉：

```python
df = pd.DataFrame({
    "成绩": [90, 85, 95]
})

s = df.squeeze("columns")

print(type(s))
# <class 'pandas.core.series.Series'>
```

形状变化为：

```text
DataFrame：(3, 1)
     ↓ df.squeeze("columns")
Series：(3,)
```

也可以写成：

```python
df.squeeze(axis="columns")
df.squeeze(axis=1)
```

建议明确指定列方向。如果直接调用 `df.squeeze()`，它会压缩所有长度为 1 的维度：

| 原 DataFrame 形状 | `df.squeeze()` 的结果 |
| --- | --- |
| `(3, 1)` | Series |
| `(1, 3)` | Series |
| `(1, 1)` | 标量 |
| `(3, 2)` | 仍然是 DataFrame |

如果已经知道列名，直接选择一列通常更直观：

```python
s = df["成绩"]
```

### 12.4 DataFrame 取一行通常也得到 `Series`

```python
df = pd.DataFrame(
    {
        "数学": [90, 85],
        "英语": [80, 70]
    },
    index=["张三", "李四"]
)

row = df.loc["张三"]       # Series
row_df = df.loc[["张三"]]  # DataFrame
```

单标签得到一维 Series；把标签放进列表中，则保留二维 DataFrame。

## 13. 用同一份数据串联四种结构

```python
import numpy as np
import pandas as pd

# 1. list：普通 Python 数据
scores_list = [90, 85, 95]

# 2. ndarray：适合数值运算
scores_array = np.array(scores_list)

# 3. Series：数组数据加学生姓名标签
scores_series = pd.Series(
    scores_array,
    index=["张三", "李四", "王五"],
    name="数学"
)

# 4. DataFrame：多列数据组成表格
df = pd.DataFrame({
    "数学": scores_series,
    "英语": [80, 70, 88]
})
```

可以把这个过程概括为：

```text
list
只有数据
    ↓
ndarray
数据 + 高效数值运算
    ↓
Series
数据 + 数值运算 + 行标签
    ↓
DataFrame
多列数据 + 行标签 + 列标签
```

## 14. 转换时最容易忽略的问题

### 14.1 标签是否会保留

```python
s.to_numpy()
df.to_numpy()
s.tolist()
df.to_numpy().tolist()
```

这些转换主要保留数据值，通常不会保留 pandas 的 `index`、`columns` 和 `name`。

### 14.2 数据类型是否会改变

NumPy 数组通常要求统一的 `dtype`。混合类型的 DataFrame 转成数组时，可能被统一为 `object`，也可能发生数值类型提升。

### 14.3 一维和二维不要混淆

```python
df["数学"].shape      # (n,)：Series
df[["数学"]].shape    # (n, 1)：DataFrame
```

虽然它们看起来都只有一列，但维度并不相同。这会影响机器学习模型、矩阵运算和函数参数的要求。

### 14.4 转换不一定总是复制数据

某些 NumPy 和 pandas 转换可能共享底层数据，也可能因为数据类型、内存布局等原因创建副本。如果后续代码会修改数据，不应仅凭转换函数名称假定是否复制；需要独立数据时应显式使用 `.copy()`。

## 15. 实际使用时如何选择

| 需求 | 推荐结构 |
| --- | --- |
| 临时保存一组普通 Python 对象 | `list` |
| 进行向量、矩阵和大量数值运算 | `ndarray` |
| 表示带索引的一列数据 | `Series` |
| 处理 CSV、Excel、数据库式表格 | `DataFrame` |

> [!summary] 一句话总结
> `Series` 像“带行标签的一维数组”，DataFrame 像“由多列 Series 组成的带行、列标签表格”；在它们与 list、ndarray 互相转换时，重点检查维度、标签、数据类型和复制关系。

