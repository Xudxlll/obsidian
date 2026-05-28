## 今天学了什么

> [!info] 今天学了什么
> - 优化 Matplotlib 动画，使用固定坐标轴、线性插值和对象更新减少跳动。
> - 学习 `openpyxl` 读取、创建、写入和保存 Excel 工作簿。
> - 用表格数据结构统计人口信息，并生成新的 Excel 结果表。
> - 使用 pandas 批量读取并合并目录下的 Excel 文件。

## 抓主线

> [!tip] 抓主线
> 1. 动画优化关注每一帧如何更新得更平滑。
> 2. `openpyxl` 适合逐单元格读写 Excel。
> 3. 统计任务先读表，再组织中间数据结构，最后写回新表。
> 4. pandas 更适合批量读取和合并表格。

## 课堂代码合集

### day08/01_animation.py

```python
"""
丝滑的动态柱状图
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

data = np.random.randint(1, 10, 5)
labels = [f"Item{i+1}" for i in range(5)]

fig, ax = plt.subplots()

ax.set_ylim(0, 10)  # 设置固定的y轴范围，避免跳动

# 保存柱状图对象
bars = ax.bar(labels, data)

# 更新函数
# 如果参数出现灰色，代表当前的代码中没有显式使用,此处frame不需要显式的使用(会自动调用)
def update(frame):
    new_data = np.random.randint(1, 10, 5)

    global data  # 函数内修改全局的data变量的值
    # 线性插值法
    # data逐渐向new_data移动  每次移动10%的距离
    data = np.clip(data + (new_data - data) * 0.1, 0, 10)

    ax.clear()
    ax.bar(labels, data)
    ax.set_ylim(0, 10)  # 设置固定的y轴范围，避免跳动

# fig 图形 update更新函数(内部修改图形) frames 帧数 interval 更新时间 毫秒
# 内部不断的调用(自动 不需要开发者管) update 更新函数,来实现动态
animation = FuncAnimation(fig, update, frames=2000, interval=100)

# 保存为mp4
# animation.save("dove.mp4",fps=120,dpi=300,writer="pillow")

# 保存为动图
# animation.save("dove.gif",fps=30,dpi=300,writer="pillow")

plt.show()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/day08/dove.gif]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：丝滑的动态柱状图；设置固定的y轴范围，避免跳动；保存柱状图对象；更新函数。
> - 文件中定义了函数：`update(frame)`。
> - 主要变量/数据名包括：`data`、`labels`、`fig, ax`、`bars`、`new_data`、`animation`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `.set_ylim()`：设置 y 轴显示范围。
> - `np.clip()`：把数组数值限制在指定范围内。
> - `FuncAnimation()`：让 Matplotlib 按帧反复调用更新函数，生成动画。

### day08/02_animation.py

```python
"""
更加丝滑的动态柱状图
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

data = np.random.randint(1, 10, 5)
labels = [f"Item{i+1}" for i in range(5)]

fig, ax = plt.subplots()

ax.set_ylim(0, 10)  # 设置固定的y轴范围，避免跳动

# 保存柱状图对象
bars = ax.bar(labels, data)

# 更新函数
# 如果参数出现灰色，代表当前的代码中没有显式使用,此处frame不需要显式的使用(会自动调用)
def update(frame):
    new_data = np.random.randint(1, 10, 5)

    global data  # 函数内修改全局的data变量的值
    # 线性插值法
    # data逐渐向new_data移动  每次移动10%的距离
    data = np.clip(data + (new_data - data) * 0.1, 0, 10)

    ax.set_ylim(0, 10)  # 设置固定的y轴范围，避免跳动

    # zip 把bars，data的元素一一组合起来  [1,2,3] [4,5,6] ==>[(1,4)(2,5)(3,6)]
    for bar, height in zip(bars, data):
        bar.set_height(height)

    return bars


# fig 图形 update更新函数(内部修改图形) frames 帧数 interval 更新时间 毫秒
# 内部不断的调用(自动 不需要开发者管) update 更新函数,来实现动态

animation = FuncAnimation(fig, update, frames=2000, interval=100, blit=True, cache_frame_data=False)

# 保存为mp4
# animation.save("dove.mp4",fps=120,dpi=300,writer="pillow")

# 保存为动图
# animation.save("dove.gif",fps=30,dpi=300,writer="pillow")

plt.show()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/day08/dove.gif]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：更加丝滑的动态柱状图；设置固定的y轴范围，避免跳动；保存柱状图对象；更新函数。
> - 文件中定义了函数：`update(frame)`。
> - 主要变量/数据名包括：`data`、`labels`、`fig, ax`、`bars`、`new_data`、`animation`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `FuncAnimation()`：让 Matplotlib 按帧反复调用更新函数，生成动画。

### day08/03_openpyxl_copy.py

```python
"""
openpyxl 拷贝操作
pip install openpyxl
"""
# 1.引入模块
import openpyxl

# 2.加载表
# wb其实就是工作簿(一个Excel表就是一个工作簿)
wb = openpyxl.load_workbook("全国人口统计表.xlsx")

# 3.保存
wb.save("新-全国人口统计表.xlsx")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：openpyxl 拷贝操作；pip install openpyxl；1.引入模块；2.加载表。
> - 主要变量/数据名包括：`wb`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import openpyxl`：导入 openpyxl，用来读写 Excel 工作簿。
> - `openpyxl.load_workbook()`：打开已有 Excel 工作簿。
> - `.save()`：把动画、图片或文档保存到文件。

> [!abstract] 代码逻辑怎么走
> - 先打开或创建工作簿，再定位工作表和单元格，最后保存 Excel 文件。

> [!warning] 需要注意的点
> - Excel 行列下标和单元格坐标要对齐；写完后记得保存到新文件，避免覆盖原始数据。

> [!success] 举一反三
> - 可以把同样流程改成读取成绩表、库存表或人口表，练习批量生成报表。

### day08/04_openpyxl_write.py

```python
"""
openpyxl 写入数据
"""
# 1.引入模块
import openpyxl

# 2.生成一个workbook对象
wb = openpyxl.Workbook()
# 获取活跃的工资表
ws = wb.active    # ws 可以简单理解成sheet
ws.title = "省会城市"

# 3.写入数据
ws['A1'] = "城市"
ws['B1'] = "省会"

city_dict = {
    "河北": "石家庄",
    "山西": "太原",
    "海南": "海口",
    "甘肃": "兰州",
    "宁夏": "银川"
}

row_num = 2
for province, capital in city_dict.items():
    # 把省份写在A列 column = 1
    ws.cell(row=row_num, column=1, value=province)
    # 把省会写在B列 column = 2
    ws.cell(row=row_num, column=2, value=capital)
    # 行号递增
    row_num += 1

# 列表形式怎么办？
city_list=[
    ["河北", "石家庄"],
    ["山西", "太原"],
    ["海南", "海口"],
    ["甘肃", "兰州"],
    ["宁夏", "银川"]
]
for i in city_list:
    ws.append(i)

# 4.保存
wb.save("全国城市省会表.xlsx")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：openpyxl 写入数据；1.引入模块；2.生成一个workbook对象；获取活跃的工资表。
> - 主要变量/数据名包括：`wb`、`ws`、`city_dict`、`row_num`、`city_list`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `openpyxl.Workbook()`：新建 Excel 工作簿。
> - `.cell()`：按行列位置访问 Excel 单元格。
> - 列表 `[]`：保存一组有顺序、可修改的数据。

### day08/05_openpyxl_count.py

```python
"""
人口统计分析
1.根据表分析每个省市县的内容 重复的只算一个 例如:北京市 东城区 出现了4次，只算1次
2.计算城市的区域数量  例如:北京市东城区出现了 4次，就算区域数量为 4
3.计算每个区域多少人   12345
区域数量 人口数量市区
北京市    东城区    3     12345
北京市    西城区    6     123000
广东省    白云区    1     6263
思路：
加载原表 ==〉 读数据 ==〉 造数据结构 ==〉创建新表对象 ==〉编辑表头 ==> 插入数据 ==> 保存
"""
import openpyxl

wb = openpyxl.load_workbook("全国人口统计表.xlsx")
ws = wb.active

population_total = {}

# 获取表中的最大行
for row in range(2, ws.max_row + 1):
    print(row)
    # 获取城市名称
    city = ws[f'A{row}'].value
    # 获取区域名称
    area = ws[f'B{row}'].value
    # 获取人口数
    population = ws[f'C{row}'].value

    # # 写入城市名 + 区域名 + 人口数
    # if city not in population_total:
    #     population_total[city] = {}
    # if area not in population_total[city]:
    #     population_total[city][area] = 0
    # population_total[city][area] += population

    # 写入城市名 + 区域名 + 区域数量 + 人口数
    population_total.setdefault(city, {})
    population_total[city].setdefault(area, {"区域数量": 0, "人口总数": 0})
    # if city not in population_total:
    #     population_total[city] = {}
    # if area not in population_total[city]:
    #     population_total[city][area] = {"区域数量": 0, "人口总数": 0}

    population_total[city][area]["区域数量"] += 1
    population_total[city][area]["人口总数"] += population

print(population_total)

# 创建新的工作簿并写入结果
wb_new = openpyxl.Workbook()
ws_new = wb_new.active
ws_new.title = "人口统计结果"

# 写入表头
ws_new.append(["市", "区", "区域数量", "人口总数"])

for city in population_total:
    print(city)  # 每个城市名称 其实就是字典的键
    print(population_total[city])  # 每个城市对应的区域,是一个字典
    for area in sorted(population_total[city]):
        print(area)  # 每个城市的每个区域名称,其实就是字典的键
        data = population_total[city][area]
        print(data)  # 其实是每个城市的区域的区域数量+人口总数

        ws_new.append([city, area, data["区域数量"], data["人口总数"]])


wb_new.save("带人口统计的表.xlsx")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：人口统计分析；1.根据表分析每个省市县的内容 重复的只算一个 例如:北京市 东城区 出现了4次，只算1次；2.计算城市的区域数量  例如:北京市东城区出现了 4次，就算区域数量为 4；3.计算每个区域多少人   12345。
> - 主要变量/数据名包括：`wb`、`ws`、`population_total`、`city`、`area`、`population`、`wb_new`、`ws_new`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 字典 `{key: value}`：用键值对描述结构化数据。
> - `.setdefault()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。

### day08/06_pandas_merge.py

```python
"""
pandas
pip install pandas
合并一个目录下的所有表内容
"""
import os
import pandas

# 指定文件位置
path = "MeageData"

# 有多少文件
file_list = os.listdir(path)

# 遍历文件，逐个读取，逐个写数据
merge_data = pandas.DataFrame()
for file in file_list:
    print(file)
    excel_data = pandas.read_excel(f"{path}/{file}")
    print(excel_data)
    merge_data = pandas.concat([merge_data, excel_data])

# 保存文件
merge_data.to_excel("合并后的个人信息.xlsx")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：pandas；pip install pandas；合并一个目录下的所有表内容；指定文件位置。
> - 主要变量/数据名包括：`path`、`file_list`、`merge_data`、`excel_data`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import os`：导入系统路径与文件操作相关功能。
> - `import pandas`：导入 pandas，用表格数据结构处理 Excel/CSV 等数据。
> - `os.listdir()`：调用 `os` 中的 `listdir` 功能，结合本文件注释理解它在当前练习中的作用。
> - `pandas.DataFrame()`：调用 `pandas` 中的 `DataFrame` 功能，结合本文件注释理解它在当前练习中的作用。
> - `pandas.read_excel()`：调用 `pandas` 中的 `read_excel` 功能，结合本文件注释理解它在当前练习中的作用。
> - `pandas.concat()`：调用 `pandas` 中的 `concat` 功能，结合本文件注释理解它在当前练习中的作用。
> - `.to_excel()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。

> [!abstract] 代码逻辑怎么走
> - 先遍历文件并读取表格，再把数据合并到同一个 DataFrame，最后导出结果。

> [!warning] 需要注意的点
> - 批量合并表格时要留意列名是否一致，以及目录中是否混入非目标文件。

> [!success] 举一反三
> - 可以在合并后继续做去重、排序、筛选或分组统计。

## 总结

> [!summary] 总结
> - **今天的核心任务**：优化 Matplotlib 动画，使用固定坐标轴、线性插值和对象更新减少跳动。；学习 `openpyxl` 读取、创建、写入和保存 Excel 工作簿。；用表格数据结构统计人口信息，并生成新的 Excel 结果表。
> - **真实文件里的练习/主题**：丝滑的动态柱状图；更加丝滑的动态柱状图；openpyxl 拷贝操作；openpyxl 写入数据；人口统计分析；pandas。
>
> **新学代码怎么理解**
> - `.set_ylim()`：设置 y 轴显示范围。
> - `np.clip()`：把数组数值限制在指定范围内。
> - `FuncAnimation()`：让 Matplotlib 按帧反复调用更新函数，生成动画。
> - `import openpyxl`：导入 openpyxl，用来读写 Excel 工作簿。
> - `openpyxl.load_workbook()`：打开已有 Excel 工作簿。
> - `.save()`：把动画、图片或文档保存到文件。
> - `openpyxl.Workbook()`：新建 Excel 工作簿。
> - `.cell()`：按行列位置访问 Excel 单元格。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
