## 今天学了什么

> [!info] 今天学了什么
> - 学习安装和导入 Matplotlib 可视化库。
> - 使用 `plt.plot()` 绘制折线图，使用 `plt.pie()` 绘制饼图。
> - 使用 `plt.bar()` 绘制柱状图，并给图表添加标题、坐标轴标签和数值标注。

## 抓主线

> [!tip] 抓主线
> 1. 先准备 x/y、标签、颜色等绘图数据。
> 2. 再调用 Matplotlib 的绘图函数生成图表。
> 3. 最后通过标题、标签、标注和 `plt.show()` 完成展示。

## 课堂代码合集

### day06/01_plot.py

```python
"""
matplotlib  可视化库
这是第三方组织在维护，不是python自带的，所以需要下载安装

下载的流程:windows
 1.win + r键 调出运行的窗口
 2.输入cmd，回车
 3.输入下方命令 并回车 注意空格和大小写
 pip install matplotlib
 如果下载成功 会出现 Successfully installed....

会遇到问题:
1.下载的时候总失败，更换网络多次尝试
2.提示 pip 不是内部或外部的命令... 百度一下:添加python解释器到环境变量 path
3.提示 Requirement already satisfied.... 代表你当前的环境中已经有这个三方库了,不需要重复下载
4.Error:Could not find a version ....检査python环境 + 网络 + 拼写
"""

# 折线图
# 引入可视化库中的pyplot模块  as 起了一个别名简化名称长度
# import 导入 引入
import matplotlib.pyplot as plt

# x,y轴数据
x = [1,2,3,4,5]
y = [1,9,15,25,8]

# 绘图
plt.plot(x, y,
         color="red", #线条颜色
         linewidth=5, #线宽
         linestyle="--", #线条风格
         marker="s", #标记点风格
         markersize="10", #标记点大小
         label="HAHA"
         )

# x,y轴数据标签
plt.xlabel("Time")
plt.ylabel("energy")

# 表的标题
plt.title("My Plot")

# 添加图例
# loc 图例的位置 左上角 lower right 右下角
# fontsize 字体大小
# framealpha 透明度
# plt.legend(loc="upper left", fontsize=10, framealpha=1)
plt.legend(
    loc='upper left',
    title='Data Series',
    ncol=2,
    frameon=True,
    shadow=True,
    fontsize=9
)

# 数据点标注
# xy注释坐标  xytext文本标签坐标
plt.annotate("HP",xy=(4,25),xytext=(3,20))

# 显示
plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：matplotlib  可视化库；这是第三方组织在维护，不是python自带的，所以需要下载安装；下载的流程:windows；1.win + r键 调出运行的窗口。
> - 主要变量/数据名包括：`x`、`y`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import matplotlib.pyplot as plt`：用 `plt` 这个常用别名创建图形、坐标轴和图表。
> - `plt.plot()`：调用 `plt` 中的 `plot` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.xlabel()`：调用 `plt` 中的 `xlabel` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.ylabel()`：调用 `plt` 中的 `ylabel` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.title()`：调用 `plt` 中的 `title` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.legend()`：调用 `plt` 中的 `legend` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.annotate()`：调用 `plt` 中的 `annotate` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.show()`：显示 Matplotlib 图形窗口。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。

> [!warning] 需要注意的点
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。

### day06/02_pie.py

```python
"""
饼状图
"""
import matplotlib.pyplot as plt

# 数据
sizes = [25, 30, 95, 10, 68]
# 标签
labels = ["c++", "go", "python", "php", "js"]
# 颜色
colors = ["gold", "green", "pink", "cyan", "purple"]
# 突出显示
explode = (0.5, 0, 0, 0, 0)
# 绘制饼图  关键字参数  labels参数要使用哪一个数据
plt.pie(sizes,
        labels=labels,
        colors=colors,
        explode=explode,
        autopct="%1.1f%%"
)
# 第一个%表示当前格式化的开始
# 1.1f 第一个1代表的是最小字段宽度(字符数),可以简单理解为
# 如果显示的数 数字不足1个字符,包括小数点,左侧用空格填充。
# .1 浮点数保留1位小数  f浮点数格式  %%把特殊的%转成普通的%

# 显示图表
plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：饼状图；数据；标签；颜色。
> - 主要变量/数据名包括：`sizes`、`labels`、`colors`、`explode`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `plt.pie()`：调用 `plt` 中的 `pie` 功能，结合本文件注释理解它在当前练习中的作用。

### day06/03_bar.py

```python
"""
柱状图（条状图）
"""
import matplotlib.pyplot as plt

values = [10, 20, 30, 20, 10]
labels = ["a", "b", "c", "d", "e"]

# 颜色
colors = ["gold", "green", "pink", "cyan", "purple"]

# 数据标签

# 标题
plt.title("AAA")

# x,y数据标签
plt.xlabel("A")
plt.ylabel("B")

# 其实bar方法有一个返回值,包含了图表的全部信息
bars = plt.bar(labels, values, color=colors)
for bar in bars:
    height = bar.get_height()
    print(bar.get_height())  # 数据
    print(bar.get_width())  # 柱状的宽度
    print(bar.get_x())  # 柱状左下角的下标

    # 并把数值显示在每个柱状的上方，且居中显示
    # bar.get_x() + bar.get_width() / 2   2-0.4+0.4
    plt.text(
        bar.get_x() + bar.get_width() / 2,  # x坐标
        height + 1,   # y坐标
        height,   # 数值
        ha = "center",   # 水平居中
    )

plt.show()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：柱状图（条状图）；颜色；数据标签；标题。
> - 主要变量/数据名包括：`values`、`labels`、`colors`、`bars`、`height`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `plt.bar()`：调用 `plt` 中的 `bar` 功能，结合本文件注释理解它在当前练习中的作用。
> - `.get_height()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.get_width()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.get_x()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `plt.text()`：调用 `plt` 中的 `text` 功能，结合本文件注释理解它在当前练习中的作用。
> - `return`：把函数处理结果返回给调用处，供后续代码继续使用。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习安装和导入 Matplotlib 可视化库。；使用 `plt.plot()` 绘制折线图，使用 `plt.pie()` 绘制饼图。；使用 `plt.bar()` 绘制柱状图，并给图表添加标题、坐标轴标签和数值标注。
> - **真实文件里的练习/主题**：matplotlib  可视化库；饼状图；柱状图（条状图）。
>
> **新学代码怎么理解**
> - `import matplotlib.pyplot as plt`：用 `plt` 这个常用别名创建图形、坐标轴和图表。
> - `plt.plot()`：调用 `plt` 中的 `plot` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.xlabel()`：调用 `plt` 中的 `xlabel` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.ylabel()`：调用 `plt` 中的 `ylabel` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.title()`：调用 `plt` 中的 `title` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.legend()`：调用 `plt` 中的 `legend` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.annotate()`：调用 `plt` 中的 `annotate` 功能，结合本文件注释理解它在当前练习中的作用。
> - `plt.show()`：显示 Matplotlib 图形窗口。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
