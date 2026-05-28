## 今天学了什么

> [!info] 今天学了什么
> - 学习使用 python-docx 创建 Word 文档、标题、段落、换页和表格。
> - 把 Excel 表格内容读取出来，再写入 Word 表格。
> - 初步学习 OpenCV：读取图像、查看数组形状、显示图像窗口。

## 抓主线

> [!tip] 抓主线
> 1. Word 自动化先创建文档对象，再添加内容，最后保存文件。
> 2. Excel 转 Word 的关键是把表格行列映射到 Word 表格单元格。
> 3. OpenCV 把图像读成 NumPy 数组，再通过窗口显示出来。

## 课堂代码合集

### day09/01_docx.py

```python
"""
docx
pip install python-docx

标题
段落等级
段落
表格
图片
换页符
...
"""

import docx

# 初始化文档对象
word = docx.Document()

article_dict = {
    "title": "见与不见",
    "content": ["你见，或者不见我", "我就在那里", "不悲 不喜",
                "你跟，或者不跟我", "我的手就在你手里", "不舍 不弃!"]
}

# 添加标题
word.add_heading(article_dict["title"], level=0)

# 添加段落内容
for item in article_dict["content"]:
    word.add_paragraph(item)

# 保存文档
word.save("见与不见.docx")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：docx；pip install python-docx；标题；段落等级。
> - 主要变量/数据名包括：`word`、`article_dict`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import docx`：导入 python-docx，用来创建和编辑 Word 文档。
> - `docx.Document()`：调用 `docx` 中的 `Document` 功能，结合本文件注释理解它在当前练习中的作用。
> - `.add_heading()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.add_paragraph()`：向 Word 文档添加段落。

> [!abstract] 代码逻辑怎么走
> - 先创建 Word 文档对象，再添加标题、段落或表格，最后保存文档。

> [!warning] 需要注意的点
> - Word 表格写入时要确认行数、列数和源数据一致，避免单元格索引越界。

> [!success] 举一反三
> - 可以把 Excel 统计结果自动写进 Word，形成一键生成报告的流程。

### day09/02_docx.py

```python
"""
追加表格
"""
import math
from docx import Document

word = Document("见与不见.docx")

# 换页符
word.add_page_break()

# 创建表格对象
# table = word.add_table(5, 2)
# table.cell(0, 0).text = "仓央嘉措"

# 新需求把下列内容写到docx的文档的表格中
info = [
    ["中文名", "仓央嘉措"],
    ["籍贯", "中国西藏"],
    ["民族", "门巴族"],
    ["职业", "第六世dalai"]
]

# 创建表格对象  len()求长度（其实就是元素的个数）
rows = len(info)
cols = len(info[0])
table = word.add_table(rows, cols)

for row in range(rows):
    print("row:",row)
    for col in range(cols):
        print("col:",col)
        table.cell(row, col).text = info[row][col]
        print(info[row][col])

# table = word.add_table(len(info), len(info[0]))
# print(len(info))
# print(len(info[0]))
#
# a = 0
# x = 0
#
# for item in info:
#     b = int(abs(math.sin(x)))
#     table.cell(a, b).text = item[b]
#     x += math.pi / 2
#     b = int(abs(math.sin(x)))
#     table.cell(a, b).text = item[b]
#     a += 1
#     x += math.pi / 2

# table.cell(1, 0).text = "中文名"
# table.cell(1, 1).text = "仓央嘉措"
# table.cell(2, 0).text = "籍贯"
# table.cell(2, 1).text = "中国西藏"
# table.cell(3, 0).text = "民族"
# table.cell(3, 1).text = "门巴族"
# table.cell(4, 0).text = "职业"
# table.cell(4, 1).text = "第六世dalai"

word.save("带表格的见与不见.docx")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：追加表格；换页符；创建表格对象；table = word.add_table(5, 2)。
> - 主要变量/数据名包括：`word`、`info`、`rows`、`cols`、`table`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import math`：导入 `math` 模块，为本文件后续调用它的功能做准备。
> - `Document()`：创建或打开 Word 文档对象。
> - `.add_page_break()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.add_table()`：向 Word 文档插入表格。

### day09/03_docx_excel.py

```python
"""
读取Excel表中的内容，写入到word文档的表格中
"""

from openpyxl import load_workbook
from docx import Document

# list1 = ["C", "C++", "PHP", "JS", "Python"]
# for item in list1:
#     print(item)
#
# for i in range(len(list1)):
#     print(i, list1[i])
#
# for i, item in enumerate(list1):
#     print(i, item)

# 读取文件
wb = load_workbook("带人口统计的表.xlsx")
ws = wb.active

# 创建文档对象
word = Document()
table = word.add_table(ws.max_row, ws.max_column)

for row_idx, row in enumerate(ws.iter_rows(values_only=True)):
    for col_idx, cell_val in enumerate(row):
        table.cell(row_idx, col_idx).text = str(cell_val)

word.save("带表格全国人口.docx")
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：读取Excel表中的内容，写入到word文档的表格中；list1 = ["C", "C++", "PHP", "JS", "Python"]；for item in list1:；print(item)。
> - 主要变量/数据名包括：`wb`、`ws`、`word`、`table`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `Document()`：创建或打开 Word 文档对象。
> - `.iter_rows()`：按行遍历 Excel 工作表数据。
> - `str()`：把数据转换为字符串。

### day09/04_opencv.py

```python
"""
opencv

pip install opencv-python==4.5.5.64 -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 300

pip install opencv-contrib-python==4.5.5.64 -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 300

读取图像  保存图像
"""
import cv2

# 读取图片 0单通道灰度 1 3通道
im = cv2.imread("img_data/Linus.png", 1)

# print(im)  # 颜色数字的显示范围 (255,255,255)  (0,0,0)  0~ 255
print(type(im), im.shape)  # <class 'numpy.ndarray'> (216, 160, 3)  高，宽，BGR3通道

cv2.imshow("test", im)  # 在窗口中读取图像
cv2.waitKey()   # 等待用户按键反馈
cv2.destroyAllWindows()  # 销毁窗口
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/day09/img_data/Linus.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：opencv；pip install opencv-python==4.5.5.64 -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 300；pip install opencv-contrib-python==4.5.5.64 -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 300；读取图像  保存图像。
> - 主要变量/数据名包括：`im`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `import cv2`：导入 OpenCV，用来读取、显示、处理和保存图像。
> - `cv2.imread()`：按路径读取图像，第二个参数常用来控制彩色或灰度读取。
> - `type()`：查看数据类型。
> - `cv2.imshow()`：弹出窗口显示图像，常和 `waitKey()` 配合观察处理结果。
> - `cv2.waitKey()`：等待键盘输入，避免图像窗口一闪而过。
> - `cv2.destroyAllWindows()`：关闭 OpenCV 打开的所有图像窗口。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习使用 python-docx 创建 Word 文档、标题、段落、换页和表格。；把 Excel 表格内容读取出来，再写入 Word 表格。；初步学习 OpenCV：读取图像、查看数组形状、显示图像窗口。
> - **真实文件里的练习/主题**：docx；追加表格；读取Excel表中的内容，写入到word文档的表格中；opencv。
>
> **新学代码怎么理解**
> - `import docx`：导入 python-docx，用来创建和编辑 Word 文档。
> - `docx.Document()`：调用 `docx` 中的 `Document` 功能，结合本文件注释理解它在当前练习中的作用。
> - `.add_heading()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.add_paragraph()`：向 Word 文档添加段落。
> - `import math`：导入 `math` 模块，为本文件后续调用它的功能做准备。
> - `Document()`：创建或打开 Word 文档对象。
> - `.add_page_break()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `.add_table()`：向 Word 文档插入表格。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
