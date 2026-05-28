## 今天学了什么

> [!info] 今天学了什么
> - 学习均值滤波、中值滤波和高斯滤波，比较它们的去噪效果。
> - 学习用卷积核做图像锐化，增强边缘和纹理。
> - 学习 Canny、Sobel 等边缘检测思路。
> - 学习二值化后查找轮廓，并绘制轮廓或外接矩形。

## 抓主线

> [!tip] 抓主线
> 1. 滤波先处理噪声和平滑问题。
> 2. 锐化和边缘检测强调灰度变化明显的位置。
> 3. 轮廓查找通常依赖二值图。
> 4. 绘制结果帮助检查检测是否正确。

## 课堂代码合集

### day12/01_cv_blur.py

```python
"""
图像梯度:
   计算的是图像变化的速度  图像边缘信息
   描述了图像中像素值变化的速度和方向,向量
   通过模板运算(卷积)在图像上滑动
   边缘部分 灰度值变化比较大 梯度较大
   平滑部分 灰度值变化比较小 梯度较小

均值滤波指模板权重都为1的滤波器。==> n*n的矩阵  ==> 核 ==> (3,3) (5,5) (7,7)
原始图像: 假设中间像素是噪声  把噪声转换成合理值
[
  10 20  30
  40 150 60
  70 80  90
]

邻域选择: [10 20 30 40 150 60 70 80 90]
计算均值: (10+20+30+40+150+60+70+80+90) / 9 = 550 / 9 = 61
替换中间像素: 把150 替换成 61
替换策略:所有的中心元素 不管你是不是噪声
效果:噪声==>均值被抑制 非噪声 均值改变原像素值,可能会丢失细节和边缘

均值滤波可以起到图像平滑的效果，可以去除噪声，但随着模板尺寸的增加图像会变得更为模糊,可能会丢失细节

均值滤波通过邻域平均值替换中心像素,实现噪声抑制

"""
import cv2

im = cv2.imread("../img_data/lena.jpg", 0)
cv2.imshow("im", im)

# 第二参数是滤波器大小
im_mean_blur1 = cv2.blur(im, (3, 3))
im_mean_blur2 = cv2.blur(im, (7, 7))
cv2.imshow("im_mean_blur1", im_mean_blur1)
cv2.imshow("im_mean_blur2", im_mean_blur2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/lena.jpg]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像梯度:；计算的是图像变化的速度  图像边缘信息；描述了图像中像素值变化的速度和方向,向量；通过模板运算(卷积)在图像上滑动。
> - 主要变量/数据名包括：`im`、`im_mean_blur1`、`im_mean_blur2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.blur()`：均值滤波，让图像变平滑。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`im_mean_blur1`、`im_mean_blur2`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day12/02_cv_medianblur.py

```python
"""
中值滤波

中值滤波基于排序统计
将邻域内像素排序后,取中位数值代替原像素值
去噪 + 保留原始图像锐度 + 不修改原始图像灰度值
对椒盐噪声(黑白噪点)抑制效果明显
中值滤波是一种非线性变化，可能会破坏图像中线性关系，对于点、线等细节较多的图像和高精度的图像处理任务中并不太合适。

[
  3 2 1
  6 101 9
  4 5 7
]
邻域像素值: [1 2 3 4 5 6 7 9 101]
取中值:窗口3*3(9) 中值为5
替换原始像素值: 101 替换为 5

噪声特征: 在图像中表现为极值(极大,极小)
替换策略:所有的中心元素 不管你是不是噪声
效果:噪声==>中心值替代噪声值,噪声抑制 非噪声 中间值接近原值 变化不大(细节保留)

"""
import cv2

im = cv2.imread("../img_data/lena_noise.png", 0)
cv2.imshow("im", im)
print(im)
# 滤波器必须是大于1的奇数
im_median_blur1 = cv2.medianBlur(im, 3)
im_median_blur2 = cv2.medianBlur(im, 7)
im_mean_blur1 = cv2.blur(im, (3, 3))
im_mean_blur2 = cv2.blur(im, (7, 7))
cv2.imshow("im_median_blur1", im_median_blur1)
cv2.imshow("im_median_blur2", im_median_blur2)
cv2.imshow("im_mean_blur1", im_mean_blur1)
cv2.imshow("im_mean_blur2", im_mean_blur2)
print(im_median_blur1)
print(im_mean_blur1)
cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/lena_noise.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：中值滤波；中值滤波基于排序统计；将邻域内像素排序后,取中位数值代替原像素值；去噪 + 保留原始图像锐度 + 不修改原始图像灰度值。
> - 主要变量/数据名包括：`im`、`im_median_blur1`、`im_median_blur2`、`im_mean_blur1`、`im_mean_blur2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.medianBlur()`：中值滤波，常用于去除椒盐噪声。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`im_median_blur1`、`im_median_blur2`、`im_mean_blur1`、`im_mean_blur2`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day12/03_cv_gaussblur.py

```python
"""
高斯滤波
"""
import cv2

im = cv2.imread("../img_data/lena.jpg", 0)
cv2.imshow("im", im)

# 第三个参数是 高斯核在 x方向的标准差
im_gaussian_blur1 = cv2.GaussianBlur(im, (3, 3), 1)
im_gaussian_blur2 = cv2.GaussianBlur(im, (5, 5), 1)
cv2.imshow("im_gaussian_blur1", im_gaussian_blur1)
cv2.imshow("im_gaussian_blur2", im_gaussian_blur2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/lena.jpg]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：高斯滤波；第三个参数是 高斯核在 x方向的标准差。
> - 主要变量/数据名包括：`im`、`im_gaussian_blur1`、`im_gaussian_blur2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.GaussianBlur()`：高斯滤波，用带权重的邻域平均平滑图像。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`im_gaussian_blur1`、`im_gaussian_blur2`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day12/04_cv_sharpen.py

```python
"""
图像锐化
增加图像细节边缘和轮廓
通过增强图像中的高频成分(边缘,纹理)
将求取的边缘按照一定系数比例叠加到原始图像上，即可实现对图像的锐化操作

"""

import cv2
import numpy as np

im = cv2.imread("../img_data/lena.jpg", 0)
cv2.imshow("im", im)

# 图像源,图像深度 -1 输入和输入深度一致, 锐化算子(卷积核)
# 中心像素权重为9, 周围像素为-1 中心像素更加突出(过冲)
# 如果算子的权重和为1,锐化后的图像整体亮度不变(仅突出细节),可能导致边缘出现噪点
sharpen1 = np.array([
    [-1, -1, -1],
    [-1, 9, -1],
    [-1, -1, -1]
])
im_sharpen1 = cv2.filter2D(im, -1, sharpen1)
cv2.imshow("im_sharpen1", im_sharpen1)

sharpen2 = np.array([
    [0, -1, 0],
    [-1, 8, -1],
    [0, 1, 0]
]) / 4.0

im_sharpen2 = cv2.filter2D(im, -1, sharpen2)
cv2.imshow("im_sharpen2", im_sharpen2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/lena.jpg]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像锐化；增加图像细节边缘和轮廓；通过增强图像中的高频成分(边缘,纹理)；将求取的边缘按照一定系数比例叠加到原始图像上，即可实现对图像的锐化操作。
> - 主要变量/数据名包括：`im`、`sharpen1`、`im_sharpen1`、`sharpen2`、`im_sharpen2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.filter2D()`：用自定义卷积核处理图像，例如锐化。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`sharpen1`、`im_sharpen1`、`sharpen2`、`im_sharpen2`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day12/05_cv_edge.py

```python
"""
边缘检测
通过梯度计算可以获取图像中细节的边缘。
锐化边缘的同时减少噪声的影响，发展出了不同的边缘检测算子:
一阶梯度：
    计算图像灰度的一阶导数(梯度)
    Prewitt梯度算子、Sobel梯度算子
    低噪声 计算复杂度,需要实时处理
二阶梯度：
    计算图像灰度的二阶导数(梯度)
    Laplacian梯度算子
    高噪声 较高,需要额外平滑操作


"""
import cv2

im = cv2.imread("../img_data/lily.png", 0)
cv2.imshow("im", im)

# Canny算子
# im图像源是灰度的
# 第一个阈值 低阈值 梯度值低于此阈值会被排除 初步筛选边缘点
# 第二个阈值 高阈值 确定强边缘

# 核心步骤:
# 5*5高斯滤波 --> 用Sobel算子计算梯度(水平,垂直) --> NMS(非极大值抑制) --> 双阈值检测与边缘链接
# 梯度值 >= 240 直接保留
# 梯度值 [50,240) 之间,仅与强边缘链接时保留

# im_canny1 = cv2.Canny(im, 50, 170)
# cv2.imshow("im_canny1", im_canny1)
# im_canny2 = cv2.Canny(im, 180, 240)
# cv2.imshow("im_canny2", im_canny2)

# sobel算子
# 灰度图,输出图像的深度(数据类型),CV_8U(-1) 负值会截断为0,导致信息消失
# dx,dy(控制梯度方向): 1,0(水平梯度,垂直边缘)
# ksize 核大小 必须是奇数 大于1时 先进行高斯模糊,再计算梯度
im_hsobel = cv2.Sobel(im, cv2.CV_64F, 1, 0, ksize=1)
cv2.imshow("im_hsobel", im_hsobel)
# 0,1(垂直梯度,水平边缘)
im_vsobel = cv2.Sobel(im, cv2.CV_64F, 0, 1, ksize=5)
cv2.imshow("im_vsobel", im_vsobel)
# 1,1(2个方向梯度,2个方向边缘)
im_sobel = cv2.Sobel(im, cv2.CV_64F, 1, 1, ksize=5)
cv2.imshow("im_sobel", im_sobel)

im_1 = cv2.Sobel(im, cv2.CV_64F, 1, 0, ksize=1)
im_2 = cv2.Sobel(im_1, cv2.CV_64F, 0, 1, ksize=1)
im_3 = cv2.Sobel(im_2, cv2.CV_64F, 1, 1, ksize=1)
cv2.imshow("im_3", im_3)


# laplacian算子
im_laplacian = cv2.Laplacian(im, cv2.CV_64F)
cv2.imshow("im_laplacian", im_laplacian)



cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/lily.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：边缘检测；通过梯度计算可以获取图像中细节的边缘。；锐化边缘的同时减少噪声的影响，发展出了不同的边缘检测算子:；一阶梯度：。
> - 主要变量/数据名包括：`im`、`im_hsobel`、`im_vsobel`、`im_sobel`、`im_1`、`im_2`、`im_3`、`im_laplacian`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.Sobel()`：调用 `cv2` 中的 `Sobel` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.Laplacian()`：调用 `cv2` 中的 `Laplacian` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`im_hsobel`、`im_vsobel`、`im_sobel`、`im_1`、`im_2`、`im_3`、`im_laplacian`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day12/06_cv_find_draw.py

```python
"""
图像轮廓
"""
import cv2

im = cv2.imread("../img_data/3.png")
cv2.imshow("im", im)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
print(ret)
print(binary)
cv2.imshow("binary", binary)

# 查找图像的边缘
contours, hei = cv2.findContours(
    binary,  # 二值化后的图像
    cv2.RETR_EXTERNAL,  # 只检查外轮廓
    cv2.CHAIN_APPROX_NONE  # 存储所有的点
)
print(contours)
print(hei)
# 轮廓的层次关系信息（实际应为hierarchy）,
# 打印轮廓的层次信息（通常为4列的Numpy数组，描述轮廓间父子关系）
# [Next, Previous, First_Child, Parent]
# 每个轮廓对应这样一个四元组，四个值的含义如下：
# Next：同一层级中的下一个轮廓索引
# （比如：轮廓A→轮廓B→轮廓C形成一个链条）
# Previous：同一层级中的前一个轮廓索引
# （比如：轮廓C的前一个是轮廓B）
# First_Child：当前轮廓的第一个子轮廓索引
# （比如：大轮廓内部的小轮廓）
# Parent：当前轮廓的父轮廓索引
# （比如：小轮廓的外部轮廓）

# 只检测最外层轮廓（没有父轮廓）
# 所有轮廓的Parent = -1（表示无父轮廓）
# 所有轮廓的First_Child = -1（表示无子轮廓）
# 轮廓之间只有横向关系（通过Next/Previous连接）

# [[[ 1 -1 -1 -1]   轮廓0：下一个是1，无前一个，无子，无父
# [ 2  0 -1 -1]     轮廓1：下一个是2，前一个是0，无子，无父
# [ 3  1 -1 -1]     轮廓2：下一个是3，前一个是1，无子，无父
# [-1  2 -1 -1]]]   轮廓3：无下一个，前一个是2，无子，无父

"""
(1,N,4) N轮廓的数量 
4每个轮廓的层级信息 (Next,Previous,Firsrt_Child,Parent)
(下一个轮廓索引,前一个轮廓索引,第一个子轮廓索引,父轮廓索引) 如果没有就是-1
[[[ 1 -1 -1 -1]
  [ 2  0 -1 -1]
  [ 3  1 -1 -1]
  [-1  2 -1 -1]]]
"""

for i, contour in enumerate(contours):
    # (257, 1, 2) 257个轮廓点 1行2列
    print(f"{i:}shape:{contour.shape}")

# 绘制边缘
im_cnt = cv2.drawContours(im,  # 图像源
                          contours,  # 轮廓点列表
                          -1,  # 绘制全部轮廓
                          (0, 0, 255),  # 轮廓颜色
                          2  # 轮廓粗细
                          )
cv2.imshow("im_cnt", im_cnt)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/3.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像轮廓；(1,N,4) N轮廓的数量；4每个轮廓的层级信息 (Next,Previous,Firsrt_Child,Parent)；(下一个轮廓索引,前一个轮廓索引,第一个子轮廓索引,父轮廓索引) 如果没有就是-1。
> - 主要变量/数据名包括：`im`、`gray`、`ret, binary`、`contours, hei`、`im_cnt`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 元组 `()`：保存不可变序列。
> - `cv2.threshold()`：按阈值把灰度图转换成二值图或反二值图。
> - `cv2.findContours()`：查找图像中的轮廓。
> - `cv2.drawContours()`：把检测到的轮廓画回图像上。

> [!abstract] 代码逻辑怎么走
> - 使用 `for` 遍历序列或容器，对每个元素执行同样的处理。
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 轮廓类代码通常先得到二值图，再查找轮廓，最后把轮廓或拟合形状画回图像。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`gray`、`ret, binary`、`contours, hei`、`im_cnt`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。
> - OpenCV 默认读入 BGR，不是常见的 RGB；做颜色判断前要先确认色彩空间。
> - 阈值会直接影响二值图效果，后续轮廓、掩膜或形态学结果都依赖它。
> - 轮廓查找通常要基于二值图；输入灰度图或彩色图时结果容易不符合预期。

> [!success] 举一反三
> - 可以把循环和条件组合起来做筛选、统计、累加、菜单系统。
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day12/07_cv_rect.py

```python
"""
拟合矩形

"""
import cv2
import numpy as np

im = cv2.imread("../img_data/cloud.png")
cv2.imshow("im", im)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
print(ret)
print(binary)
contours, hie = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
print(contours)
print(hie)
# 计算并返回矩形的 x,y,w,h
x, y, w, h = cv2.boundingRect(contours[0])
print(x, y, w, h)

brcnt = np.array([[[x, y]], [[x + w, y]], [[x + w, y + h]], [[x, y + h]]])
print(brcnt)
print([brcnt])
im_cnt = cv2.drawContours(im, [brcnt], -1, (0, 0, 255), 2)
cv2.imshow("im_cnt", im_cnt)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/cloud.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：拟合矩形；计算并返回矩形的 x,y,w,h。
> - 主要变量/数据名包括：`im`、`gray`、`ret, binary`、`contours, hie`、`x, y, w, h`、`brcnt`、`im_cnt`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.boundingRect()`：调用 `cv2` 中的 `boundingRect` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 轮廓类代码通常先得到二值图，再查找轮廓，最后把轮廓或拟合形状画回图像。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`gray`、`ret, binary`、`contours, hie`、`x, y, w, h`、`brcnt`、`im_cnt`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。
> - OpenCV 默认读入 BGR，不是常见的 RGB；做颜色判断前要先确认色彩空间。
> - 阈值会直接影响二值图效果，后续轮廓、掩膜或形态学结果都依赖它。
> - 轮廓查找通常要基于二值图；输入灰度图或彩色图时结果容易不符合预期。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习均值滤波、中值滤波和高斯滤波，比较它们的去噪效果。；学习用卷积核做图像锐化，增强边缘和纹理。；学习 Canny、Sobel 等边缘检测思路。
> - **真实文件里的练习/主题**：图像梯度:；中值滤波；高斯滤波；图像锐化；边缘检测；图像轮廓；拟合矩形。
>
> **新学代码怎么理解**
> - `cv2.blur()`：均值滤波，让图像变平滑。
> - `cv2.medianBlur()`：中值滤波，常用于去除椒盐噪声。
> - `cv2.GaussianBlur()`：高斯滤波，用带权重的邻域平均平滑图像。
> - `cv2.filter2D()`：用自定义卷积核处理图像，例如锐化。
> - `cv2.Sobel()`：调用 `cv2` 中的 `Sobel` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.Laplacian()`：调用 `cv2` 中的 `Laplacian` 功能，结合本文件注释理解它在当前练习中的作用。
> - 元组 `()`：保存不可变序列。
> - `cv2.threshold()`：按阈值把灰度图转换成二值图或反二值图。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
