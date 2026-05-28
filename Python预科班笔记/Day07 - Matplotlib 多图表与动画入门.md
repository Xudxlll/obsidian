## 今天学了什么

> [!info] 今天学了什么
> - 学习柱状图、散点图、折线图、箱线图、热力图和直方图的适用场景。
> - 使用 NumPy 生成随机数据，配合 Matplotlib 观察数据分布和关系。
> - 学习 `Figure/Axes` 对象和 `FuncAnimation()`，让图表按帧更新。

## 抓主线

> [!tip] 抓主线
> 1. 不同图表回答不同问题：比较、相关性、趋势、分布或异常值。
> 2. NumPy 负责生成或组织数据。
> 3. Matplotlib 负责把数据映射成图形。
> 4. 动画通过更新函数反复修改图形状态。

## 课堂代码合集

### day07/01_bar.py

```python
"""
柱状图(条状图)
"""
import matplotlib.pyplot as plt

values = [35, 20, 48, 70, 54, 60]
labels = ["C++", "PHP", "JS", "GO", "PYTHON", "C"]
colors = ["#1f77b4", "#ff7f0e", "#9468bd", "#2ca0f8", "#d62728", "green"]

# 标题
plt.title("My Bar")

# x,y数据标签
plt.xlabel("Programming Language")
plt.ylabel("Usage Percentage")

# 其实 bar方法有一个返回值,包含了图表了全部信息
bars = plt.bar(labels, values, color=colors)

for bar in bars:
    height = bar.get_height()
    print(bar.get_height())  # 其实就是数据
    print(bar.get_width())  # 柱状的宽度
    print(bar.get_x())  # 柱状左下角下标

    # 把数值显示在每个柱状的上方,且居中显示
    # bar.get_x() + bar.get_width() / 2 -0.4 + 0.4  0
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x坐标
        height + 1,  # y坐标
        height,  # 数值
        ha="center"  # 水平居中
    )

# 数据标签
plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：柱状图(条状图)；标题；x,y数据标签；其实 bar方法有一个返回值,包含了图表了全部信息。
> - 主要变量/数据名包括：`values`、`labels`、`colors`、`bars`、`height`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `return`：把函数处理结果返回给调用处，供后续代码继续使用。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 通过赋值语句保存中间结果，主要变量包括：`values`、`labels`、`colors`、`bars`、`height`。

> [!warning] 需要注意的点
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。

> [!success] 举一反三
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day07/02_scatter.py

```python
"""
散点图 数据的相关性
"""
import matplotlib.pyplot as plt
import numpy as np

# 生成
x = np.random.rand(200)
y = np.random.rand(200)
colors = np.random.rand(200)

# cmap 把数值映射成颜色 viridis默认的颜色映射的方案  plasma coolwarm tab10
plt.scatter(x, y, c=colors, cmap="coolwarm")

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：散点图 数据的相关性；生成；cmap 把数值映射成颜色 viridis默认的颜色映射的方案  plasma coolwarm tab10。
> - 主要变量/数据名包括：`x`、`y`、`colors`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import numpy as np`：用 `np` 这个常用别名调用 NumPy 的数组与随机数功能。
> - `np.random.rand()`：调用 `np.random` 中的 `rand` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.scatter()`：调用 `plt` 中的 `scatter` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 通过赋值语句保存中间结果，主要变量包括：`x`、`y`、`colors`。

> [!warning] 需要注意的点
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。
> - `is` 比较对象身份，`==` 比较值是否相等，不要混用。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day07/03_line.py

```python
"""
双折线图
"""
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [120, 150, 135, 160, 200, 180]
users = [80, 85, 90, 110, 125, 115]

plt.plot(months, sales, color="#2f66e5", marker="o", label="Sales")
plt.plot(months, users, color="#ff7fee", marker="s", linestyle="--", label="Users")

plt.title("Monthly Sales & User Growth")
plt.xlabel("Month")
plt.ylabel("Amount")
plt.grid(True, linestyle="--", alpha=0.8)
plt.legend()

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：双折线图。
> - 主要变量/数据名包括：`months`、`sales`、`users`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `plt.grid()`：调用 `plt` 中的 `grid` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 通过赋值语句保存中间结果，主要变量包括：`months`、`sales`、`users`。

> [!warning] 需要注意的点
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day07/04_boxplot.py

```python
"""
箱体图
"""
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ["SimHei"]
plt.rcParams['axes.unicode_minus'] = False

data = [np.random.normal(0, std, 100) for std in range(1, 4)]

plt.boxplot(data, patch_artist=True)
plt.xticks([1, 2, 3], ["组1", "组2", "组3"])

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：箱体图。
> - 主要变量/数据名包括：`data`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 列表推导式：把“遍历 + 条件 + 生成新元素”压缩成一行。
> - `np.random.normal()`：调用 `np.random` 中的 `normal` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.boxplot()`：调用 `plt` 中的 `boxplot` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.xticks()`：调用 `plt` 中的 `xticks` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 通过赋值语句保存中间结果，主要变量包括：`data`。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写循环边界时要特别小心。
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day07/05_colorbar.py

```python
"""
热力图
"""
import matplotlib.pyplot as plt
import numpy as np

# 5行5列的二维数组 [0,1)
data = np.random.rand(20,20)

# 把二维数组转成图像
plt.imshow(data)

plt.colorbar()

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：热力图；5行5列的二维数组 [0,1)；把二维数组转成图像。
> - 主要变量/数据名包括：`data`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `plt.imshow()`：调用 `plt` 中的 `imshow` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.colorbar()`：调用 `plt` 中的 `colorbar` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 通过赋值语句保存中间结果，主要变量包括：`data`。

> [!warning] 需要注意的点
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day07/06_hist.py

```python
"""
直方图
"""
import matplotlib.pyplot as plt
import numpy as np

data = np.random.randn(1000)

# 分25个区间
plt.hist(data, bins=25, color="purple",edgecolor="black")

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：直方图；分25个区间。
> - 主要变量/数据名包括：`data`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `np.random.randn()`：调用 `np.random` 中的 `randn` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.hist()`：调用 `plt` 中的 `hist` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 通过赋值语句保存中间结果，主要变量包括：`data`。

> [!warning] 需要注意的点
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day07/07_fig.py

```python
"""
利用图形对象创建图表
"""
import matplotlib.pyplot as plt
import numpy as np

# 随机生成5个整数
data = np.random.randint(1, 10, 5)
labels = [f"Item{i + 1}" for i in range(5)]

# 图形  Figure 其实就是画布 尺寸 图形的标题...
# 控制图形的绘制 Axes 图形(折线,柱状) 标签 网格线...
# subplots()函数返回一个元组 (图形对象Figure , 控制图形绘制对象Axes)
fig, ax = plt.subplots()

# 绘制
ax.bar(labels, data)

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：利用图形对象创建图表；随机生成5个整数；图形  Figure 其实就是画布 尺寸 图形的标题...；控制图形的绘制 Axes 图形(折线,柱状) 标签 网格线...。
> - 主要变量/数据名包括：`data`、`labels`、`fig, ax`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `np.random.randint()`：生成指定范围内的随机整数。
> - 元组 `()`：保存不可变序列。
> - `plt.subplots()`：创建图形和坐标轴对象，是 Matplotlib 绘图的常用入口。
> - `.bar()`：绘制柱状图。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 通过赋值语句保存中间结果，主要变量包括：`data`、`labels`、`fig, ax`。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写循环边界时要特别小心。
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day07/08_animation.py

```python
"""
基础的动态柱状图
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

data = np.random.randint(1, 10, 5)
labels = [f"Item{i + 1}" for i in range(5)]

fig, ax = plt.subplots()
# 绘制
ax.bar(labels, data)

# 更新函数
# 如果参数出现灰色,代表当前的代码中没有显式使用,此处frame参数不需要显式的使用(会自动调用)
def update(frame):
    global data  # 函数内修改全局的data变量的值
    data = np.random.randint(1, 10, 5)
    # 清空坐标轴,把原来的图表删除掉
    ax.clear()
    # 绘制新图
    ax.bar(labels, data)

# fig 图形 update更新函数(内部修改图形) frames 帧数  interval更新时间 毫秒
# 内部不断的调用(自动 不需要开发者管) update 更新函数,来实现动态
animation = FuncAnimation(fig, update, frames=10, interval=500)

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：基础的动态柱状图；绘制；更新函数；如果参数出现灰色,代表当前的代码中没有显式使用,此处frame参数不需要显式的使用(会自动调用)。
> - 文件中定义了函数：`update(frame)`。
> - 主要变量/数据名包括：`data`、`labels`、`fig, ax`、`animation`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import matplotlib`：导入 Matplotlib 相关能力，用来绘图或制作动画。
> - `global`：在函数内声明使用全局变量。
> - `.clear()`：清空坐标轴内容，常用于动画逐帧重绘。
> - `FuncAnimation()`：让 Matplotlib 按帧反复调用更新函数，生成动画。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把独立功能封装起来；后面通过函数调用复用这些功能。
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 先定义更新函数，再让 `FuncAnimation()` 按帧调用它刷新图表。
> - 通过赋值语句保存中间结果，主要变量包括：`data`、`labels`、`fig, ax`、`animation`。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写循环边界时要特别小心。
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。
> - 动画更新函数要返回或修改正确的图形对象，坐标轴范围变化过大时画面会跳动。

> [!success] 举一反三
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。
> - 可以把随机数据换成实时数据或文件数据，观察动画更新逻辑是否仍然成立。

### day07/08_animation_dove.py

```python
"""
丝滑的动态柱状图
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

data = np.random.randint(1, 10, 5)
labels = [f"Item{i + 1}" for i in range(5)]

fig, ax = plt.subplots()
# 保存柱状图对象
bars = ax.bar(labels, data)


# 更新函数
def update(frame):
    global data
    data = np.random.randint(1, 10, 5)

    # zip 把bars, data的元素一一组合起来
    # [1,2,3]  [4,5,6]  ==> [(1,4),(2,5),(3,6)]
    for bar, height in zip(bars, data):
        bar.set_height(height)

    return bars


# blit 是否启用Blitting优化 仅仅重绘变化的部分 要求update函数返回 重绘对象
# cache_frame_data 是否缓存帧的数据
animation = FuncAnimation(fig, update, frames=1000, interval=100, blit=True, cache_frame_data=False)

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：丝滑的动态柱状图；保存柱状图对象；更新函数；zip 把bars, data的元素一一组合起来。
> - 文件中定义了函数：`update(frame)`。
> - 主要变量/数据名包括：`data`、`labels`、`fig, ax`、`bars`、`animation`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `.set_height()`：修改柱子的高度，常用于动态图表更新。
> - `return`：结束函数并把结果返回给调用处。
> - `FuncAnimation()`：让 Matplotlib 按帧反复调用更新函数，生成动画。

> [!abstract] 代码逻辑怎么走
> - 先定义函数，把独立功能封装起来；后面通过函数调用复用这些功能。
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 先定义更新函数，再让 `FuncAnimation()` 按帧调用它刷新图表。
> - 通过赋值语句保存中间结果，主要变量包括：`data`、`labels`、`fig, ax`、`bars`、`animation`。

> [!warning] 需要注意的点
> - `range()` 的结束值取不到，写循环边界时要特别小心。
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。
> - 动画更新函数要返回或修改正确的图形对象，坐标轴范围变化过大时画面会跳动。

> [!success] 举一反三
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以继续把重复逻辑拆成函数，让主流程只负责调用。
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习柱状图、散点图、折线图、箱线图、热力图和直方图的适用场景。；使用 NumPy 生成随机数据，配合 Matplotlib 观察数据分布和关系。；学习 `Figure/Axes` 对象和 `FuncAnimation()`，让图表按帧更新。
> - **真实文件里的练习/主题**：柱状图(条状图)；散点图 数据的相关性；双折线图；箱体图；热力图；直方图；利用图形对象创建图表；基础的动态柱状图。
>
> **新学代码怎么理解**
> - `return`：把函数处理结果返回给调用处，供后续代码继续使用。
> - `import numpy as np`：用 `np` 这个常用别名调用 NumPy 的数组与随机数功能。
> - `np.random.rand()`：调用 `np.random` 中的 `rand` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.scatter()`：调用 `plt` 中的 `scatter` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.grid()`：调用 `plt` 中的 `grid` 功能，结合本文件注释理解它在当前练习中的作用。
> - 列表推导式：把“遍历 + 条件 + 生成新元素”压缩成一行。
> - `np.random.normal()`：调用 `np.random` 中的 `normal` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.boxplot()`：调用 `plt` 中的 `boxplot` 功能，结合本文件注释理解它在当前练习中的作用。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
