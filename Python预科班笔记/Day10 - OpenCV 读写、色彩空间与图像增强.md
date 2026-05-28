## 今天学了什么

> [!info] 今天学了什么
> - 学习 OpenCV 图像读取、显示、保存，以及灰度和彩色读取方式。
> - 学习 BGR、RGB、GRAY、HSV、YUV 等色彩空间转换。
> - 学习二值化、直方图均衡化、通道拆分和 NumPy 数组切片。
> - 使用 HSV 范围、掩膜和按位与从图像中提取指定颜色。

## 抓主线

> [!tip] 抓主线
> 1. 图像先被读成数组。
> 2. 色彩空间转换让不同任务更容易处理。
> 3. 二值化和掩膜把目标区域从背景中分离出来。
> 4. 通道与切片让我们能直接操作像素矩阵。

## 课堂代码合集

### day10/01_cv_read.py

```python
"""
读取灰度图像并保存
"""

import cv2

# 读取图片  ./同级目录    ../父级目录
im = cv2.imread("../img_data/Linus.png", 0)

cv2.imshow("bak", im)

# 图像路径，图像信息
cv2.imwrite("Linus_new.png", im)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/Linus.png]]
> ![[附件/Python预科班/day10/Linus_new.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：读取灰度图像并保存；读取图片  ./同级目录    ../父级目录；图像路径，图像信息。
> - 主要变量/数据名包括：`im`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.imread()`：按路径读取图像，第二个参数常用来控制彩色或灰度读取。
> - `cv2.imwrite()`：把处理后的图像保存到指定路径。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day10/02_cv_color.py

```python
"""
色彩空间
信号灯识别,肤色检测 ==> HSV HLS  分离颜色和亮度
灰度化 ==> 边缘检测 二值化   减少数据的维度
模拟光照 ==> Lab
通道分离和合并 ==> 提取特定的通道特征
"""
import cv2

im = cv2.imread("../img_data/Linus.png", 1)
cv2.imshow("BGR", im)

# 颜色空间转换的一个函数
# 彩色图转RGB
im_rgb = cv2.cvtColor(im,cv2.COLOR_BGR2RGB)
cv2.imshow("RGB", im_rgb)

# 彩色图转灰度图
im_gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
cv2.imshow("GRAY", im_gray)

# 彩色图转HSV   色相0~360 饱和度0~1 亮度0~1
im_hsv = cv2.cvtColor(im,cv2.COLOR_BGR2HSV)
cv2.imshow("HSV", im_hsv)

# 彩色图转YUV  亮度信号+2个色差信号只有Y没有UV 图像就是灰度图
im_yuv = cv2.cvtColor(im,cv2.COLOR_BGR2YUV)
cv2.imshow("YUV", im_yuv)

# # 灰度图转彩色图
# im_bgr = cv2.cvtColor(im_gray,cv2.COLOR_GRAY2BGR)
# cv2.imshow("bgr", im_bgr)


cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/Linus.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：色彩空间；信号灯识别,肤色检测 ==> HSV HLS  分离颜色和亮度；灰度化 ==> 边缘检测 二值化   减少数据的维度；模拟光照 ==> Lab。
> - 主要变量/数据名包括：`im`、`im_rgb`、`im_gray`、`im_hsv`、`im_yuv`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.cvtColor()`：转换图像颜色空间，例如 BGR、RGB、GRAY、HSV。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`im_rgb`、`im_gray`、`im_hsv`、`im_yuv`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。
> - OpenCV 默认读入 BGR，不是常见的 RGB；做颜色判断前要先确认色彩空间。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day10/03_cv_binary.py

```python
"""
二值化和反二值化

作用:简化图像信息,突出关键特征 ==> 边缘检测，形状识别
"""
import cv2

im = cv2.imread("../img_data/Lena.jpg", 0)
print(im)

# 二值化 黑白图像 只有2个值
# 125 阈值 区分前景还是背景当像素值超出值后赋予新值255(白色)
# retval 实际返回的阈值   dst 单通道二值图像
retval1, dst1 = cv2.threshold(im, 125, 255, cv2.THRESH_BINARY)
cv2.imshow("dst1", dst1)

# 反二值化
retval2, dst2 = cv2.threshold(im, 125, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("dst2", dst2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/lena.jpg]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：二值化和反二值化；作用:简化图像信息,突出关键特征 ==> 边缘检测，形状识别；二值化 黑白图像 只有2个值；125 阈值 区分前景还是背景当像素值超出值后赋予新值255(白色)。
> - 主要变量/数据名包括：`im`、`retval1, dst1`、`retval2, dst2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.threshold()`：按阈值把灰度图转换成二值图或反二值图。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`retval1, dst1`、`retval2, dst2`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。
> - 阈值会直接影响二值图效果，后续轮廓、掩膜或形态学结果都依赖它。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day10/04_cv_hist.py

```python
"""
灰度图直方图均衡化
拉伸像素值的范围,让像素值在0~255 上分布更加均匀
全局操作，无法针对局域调整 cv2.createCLAHE() 自适应直方图均衡化
"""
import cv2
import matplotlib.pyplot as plt

# 灰度图
im = cv2.imread("../img_data/sunrise.jpg", 0)
cv2.imshow("bak", im)

# 直方图均衡化
im_equ = cv2.equalizeHist(im)
cv2.imshow("im_equ", im_equ)


# 绘制原始直方图
# hist需求一个一维数组 im.ravel()返回一个一维数组
plt.hist(im.ravel(), 256, range=[0, 256], label="bak")
plt.legend()

# 绘制均衡化直方图
plt.subplot(2, 1, 2)    # 行,列,第几个子图
plt.hist(im_equ.ravel(), 256, range=[0, 256], label="equalize")
plt.legend()
plt.show()

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/sunrise.jpg]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：灰度图直方图均衡化；拉伸像素值的范围,让像素值在0~255 上分布更加均匀；全局操作，无法针对局域调整 cv2.createCLAHE() 自适应直方图均衡化；灰度图。
> - 主要变量/数据名包括：`im`、`im_equ`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.equalizeHist()`：做直方图均衡化，增强灰度或亮度对比。
> - `.ravel()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `plt.subplot()`：调用 `plt` 中的 `subplot` 功能，结合本文件注释理解它在当前练习中的作用。

> [!abstract] 代码逻辑怎么走
> - 先准备图表数据、标签和颜色，再调用 Matplotlib 绘图函数，最后显示图表。
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`im_equ`。

> [!warning] 需要注意的点
> - 绘图时数据长度、标签数量和颜色数量要能对应上，否则图表含义会混乱。
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。
> - `is` 比较对象身份，`==` 比较值是否相等，不要混用。

> [!success] 举一反三
> - 可以换一组真实业务数据，尝试选择最适合表达比较、趋势或分布的图表。
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day10/05_cv_slice.py

```python
"""
通道操作
"""
import cv2

im = cv2.imread("../img_data/opencv.png")
cv2.imshow("bak",im)
print(im.shape)

# 所有行,所有列,索引为0的元素(第一个通道 Blue)
blue = im[:,:,0]
cv2.imshow("blue", blue)

# 所有行,所有列,索引为1的元素(第二个通道 green)
green = im[:,:,1]
cv2.imshow("green", green)

# 所有行,所有列,索引为2的元素(第三个通道 red)
red = im[:,:,2]
cv2.imshow("red", red)

# 去掉绿色通道
im[::1]=0
cv2.imshow("green", im)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/opencv.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：通道操作；所有行,所有列,索引为0的元素(第一个通道 Blue)；所有行,所有列,索引为1的元素(第二个通道 green)；所有行,所有列,索引为2的元素(第三个通道 red)。
> - 主要变量/数据名包括：`im`、`blue`、`green`、`red`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - 本文件主要是在复习或组合前面已经学过的写法，没有引入需要单独记忆的新函数/方法；重点看它如何把旧知识组合成当前题目。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`blue`、`green`、`red`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day10/06_np.py

```python
"""
数组切片
"""
import numpy as np

# 1维数组 [开始:结束:步长]
# 2维数组 [行，列]
# 3维数组 [页切片,行切片,列切片]

arr = np.arange(1, 28)
arr.resize(3, 3, 3)   # 改变数据的维度
print(arr)

# # 切出第一页
# print(arr[0])
# print(arr[0,:,:])
#
# # 切出所有页的第一行
# print(arr[:,0,:])
#
# # 切出第2页的第1行第1列
# print(arr[1,0,0])

# # 切出所有的行，不要最后一列
# print(arr[:, :, 0:2])
# print(arr[:, :, :arr.shape[2]-1])
# print(arr[:, :, :-1].shape)

arr[0, :, :] = 0
print(arr)
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：数组切片；1维数组 [开始:结束:步长]；2维数组 [行，列]；3维数组 [页切片,行切片,列切片]。
> - 主要变量/数据名包括：`arr`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `np.arange()`：调用 `np` 中的 `arange` 功能，结合本文件注释理解它在当前练习中的作用。
> - `.resize()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。

> [!abstract] 代码逻辑怎么走
> - 通过赋值语句保存中间结果，主要变量包括：`arr`。

> [!warning] 需要注意的点
> - 读这份代码时，先看变量如何变化，再看最终输出。

> [!success] 举一反三
> - 可以修改示例数据重新运行，观察输出如何变化。

### day10/07_cv_color.py

```python
"""
从图片中提取特定的颜色  ==> 分割
"""
import cv2
import numpy as np

# 转换色彩空间
im = cv2.imread("../img_data/opencv.png")
hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
cv2.imshow("im", im)
cv2.imshow("hsv", hsv)


# 提取蓝色 定义颜色范围
# 蓝色 H通道 120上下浮动10
# 备注:标准HSV色彩空间H是360  opencv中的H是标准H的一半
# SV通道 50~255 饱和度太低,色调太暗计算出的颜色会不准确
minb = np.array([110,50,50])
maxb = np.array([130,255,255])


# 生成掩膜  二值图像(黑白图) 用于标记图像中要处理的区域
# 白色是要保留的区域，黑色是背景不用保留
# 会检查每个像素的HSV值是否在定义的颜色范围
# 110 <= H <= 130  50 <= S <= 255  50 <= V <= 255  ==>  白色
mask = cv2.inRange(hsv, minb, maxb)
cv2.imshow("mask", mask)

# 并计算提取目标区域  按位与 运算
blue = cv2.bitwise_and(im, im, mask=mask)
cv2.imshow("blue", blue)

# 提取红色
minr = np.array([0,50,50])
maxr = np.array([10,255,255])

mask = cv2.inRange(hsv, minr, maxr)
cv2.imshow("mask", mask)

red = cv2.bitwise_and(im, im, mask=mask)
cv2.imshow("red", red)

# 提取绿色
ming = np.array([35,50,50])
maxg = np.array([85,255,255])

mask = cv2.inRange(hsv, ming, maxg)
cv2.imshow("mask", mask)

green = cv2.bitwise_and(im, im, mask=mask)
cv2.imshow("green", green)


cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/opencv.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：从图片中提取特定的颜色  ==> 分割；转换色彩空间；提取蓝色 定义颜色范围；蓝色 H通道 120上下浮动10。
> - 主要变量/数据名包括：`im`、`hsv`、`minb`、`maxb`、`mask`、`blue`、`minr`、`maxr`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.cvtColor()`：转换图像颜色空间，例如 BGR、RGB、GRAY、HSV。
> - `np.array()`：创建 NumPy 数组，是图像和矩阵计算的基础结构。
> - `cv2.inRange()`：按颜色或数值范围生成掩膜，用来筛选目标区域。
> - `cv2.bitwise_and()`：结合掩膜保留图像中的指定区域。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`hsv`、`minb`、`maxb`、`mask`、`blue`、`minr`、`maxr`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。
> - OpenCV 默认读入 BGR，不是常见的 RGB；做颜色判断前要先确认色彩空间。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

### day10/1111111.py

```python
import cv2
import numpy as np

# 读取彩色图像
im = cv2.imread("111.jpg", 1)
cv2.imshow("111", im)
resized_im = cv2.resize(im, None, fx=0.5, fy=0.5)  # 缩小到50%
cv2.imshow("222", resized_im)

# 1. 转换为HSV颜色空间
hsv = cv2.cvtColor(resized_im, cv2.COLOR_BGR2HSV)

# 2. 分离通道
h, s, v = cv2.split(hsv)

# 3. 仅对亮度通道(V)进行均衡化
v_eq = cv2.equalizeHist(v)

# 4. 合并通道
hsv_eq = cv2.merge([h, s, v_eq])

# 5. 转换回BGR
result = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)

# 保存结果
cv2.imwrite('output.jpg', result)
cv2.imshow("333", result)








cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/day10/111.jpg]]
> ![[附件/Python预科班/day10/output.jpg]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：读取彩色图像；缩小到50%；1. 转换为HSV颜色空间；2. 分离通道。
> - 主要变量/数据名包括：`im`、`resized_im`、`hsv`、`h, s, v`、`v_eq`、`hsv_eq`、`result`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.resize()`：缩放图像尺寸。
> - `cv2.cvtColor()`：转换图像颜色空间，例如 BGR、RGB、GRAY、HSV。
> - `cv2.split()`：把多通道图像拆成单独通道。
> - `cv2.equalizeHist()`：做直方图均衡化，增强灰度或亮度对比。
> - `cv2.merge()`：把多个单通道重新合并成多通道图像。
> - `cv2.imwrite()`：把处理后的图像保存到指定路径。

> [!abstract] 代码逻辑怎么走
> - 先读取图像，再按本节目标做色彩转换、阈值、形态学或轮廓处理，最后显示结果检查效果。
> - 通过赋值语句保存中间结果，主要变量包括：`im`、`resized_im`、`hsv`、`h, s, v`、`v_eq`、`hsv_eq`、`result`。

> [!warning] 需要注意的点
> - `cv2.imread()` 路径错误会返回 `None`，后续访问 `.shape` 或处理图像会报错。
> - OpenCV 默认读入 BGR，不是常见的 RGB；做颜色判断前要先确认色彩空间。

> [!success] 举一反三
> - 可以换一张图片重新调参数，观察读图、阈值、掩膜或轮廓结果如何变化。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习 OpenCV 图像读取、显示、保存，以及灰度和彩色读取方式。；学习 BGR、RGB、GRAY、HSV、YUV 等色彩空间转换。；学习二值化、直方图均衡化、通道拆分和 NumPy 数组切片。
> - **真实文件里的练习/主题**：读取灰度图像并保存；色彩空间；二值化和反二值化；灰度图直方图均衡化；通道操作；数组切片；从图片中提取特定的颜色  ==> 分割；读取彩色图像。
>
> **新学代码怎么理解**
> - `cv2.imread()`：按路径读取图像，第二个参数常用来控制彩色或灰度读取。
> - `cv2.imwrite()`：把处理后的图像保存到指定路径。
> - `cv2.cvtColor()`：转换图像颜色空间，例如 BGR、RGB、GRAY、HSV。
> - `cv2.threshold()`：按阈值把灰度图转换成二值图或反二值图。
> - `cv2.equalizeHist()`：做直方图均衡化，增强灰度或亮度对比。
> - `.ravel()`：调用对象自身的方法，重点看它修改了哪个对象或返回了什么结果。
> - `plt.subplot()`：调用 `plt` 中的 `subplot` 功能，结合本文件注释理解它在当前练习中的作用。
> - `np.arange()`：调用 `np` 中的 `arange` 功能，结合本文件注释理解它在当前练习中的作用。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
