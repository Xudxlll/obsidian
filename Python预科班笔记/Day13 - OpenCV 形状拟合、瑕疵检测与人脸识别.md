## 今天学了什么

> [!info] 今天学了什么
> - 学习最小包围圆、拟合椭圆和多边形近似等形状分析方法。
> - 通过 CPU 镀盘瑕疵检测练习灰度化、二值化、轮廓、掩膜、形态学和面积筛选。
> - 通过硬币计数综合使用模糊、OTSU 二值化、轮廓查找和绘制。
> - 使用 Haar 级联分类器完成基础人脸检测。

## 抓主线

> [!tip] 抓主线
> 1. 形状拟合把轮廓转换成更容易理解的几何描述。
> 2. 综合检测任务通常先预处理，再分割，再找轮廓，最后按条件筛选。
> 3. 分类器检测依赖训练好的模型文件。
> 4. 结果绘制是验证识别效果的重要一步。

## 课堂代码合集

### day13/01_cv_circle.py

```python
"""
最小包围圆
"""
import cv2

im = cv2.imread("../img_data/cloud.png", 0)
cv2.imshow("im", im)

ret, binary = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)

contours, hie = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# 圆心,半径
(x, y), radius = cv2.minEnclosingCircle(contours[0])

# 绘制圆
cv2.circle(im, (int(x), int(y)), int(radius), (255, 255, 255), 2)

cv2.imshow("circle",im)
cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/cloud.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：最小包围圆；圆心,半径；绘制圆。
> - 主要变量/数据名包括：`im`、`ret, binary`、`contours, hie`、`x, y, radius`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.minEnclosingCircle()`：计算包住目标轮廓的最小圆。
> - `cv2.circle()`：在图像上绘制圆形。

### day13/02_cv_ellipse.py

```python
"""
最优拟合椭圆
"""
import cv2
im = cv2.imread("../img_data/cloud.png")
cv2.imshow("im", im)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hie = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

ellipse = cv2.fitEllipse(contours[0])
print(ellipse)
# 绘制椭圆
cv2.ellipse(im, ellipse, (0, 0, 255), 2)

cv2.imshow("circle", im)
cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/cloud.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：最优拟合椭圆；绘制椭圆。
> - 主要变量/数据名包括：`im`、`gray`、`ret, binary`、`contours, hie`、`ellipse`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.fitEllipse()`：调用 `cv2` 中的 `fitEllipse` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.ellipse()`：在图像上绘制或拟合椭圆。

### day13/03_cv_arc.py

```python
"""
逼近多边形
"""
import cv2

im = cv2.imread("../img_data/cloud.png")
cv2.imshow("im", im)

gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hie = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# 周长
epslion = 0.005 * cv2.arcLength(contours[0], True)

# 用多边形近似轮廓
# 返回值多边形的顶点坐标列表
adp = cv2.approxPolyDP(contours[0], epslion, True)
print(adp)

# 绘制多边形
im_adp = cv2.drawContours(im, [adp], 0, (0, 0, 255), 2)
cv2.imshow("im_adp", im_adp)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/cloud.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：逼近多边形；周长；用多边形近似轮廓；返回值多边形的顶点坐标列表。
> - 主要变量/数据名包括：`im`、`gray`、`ret, binary`、`contours, hie`、`epslion`、`adp`、`im_adp`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.findContours()`：查找图像中的轮廓。
> - `cv2.arcLength()`：计算轮廓周长。
> - `cv2.approxPolyDP()`：把轮廓近似成多边形，便于识别形状。
> - `cv2.drawContours()`：把检测到的轮廓画回图像上。
> - 列表 `[]`：保存一组有顺序、可修改的数据。
> - `return`：把函数处理结果返回给调用处，供后续代码继续使用。

### day13/04_CPU.py

```python
"""
综合案例 CPU镀盘瑕疵检测
"""
import cv2
import numpy as np

im = cv2.imread("../img_data/CPU.png")
# cv2.imshow("im", im)

# 灰度化
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cv2.imshow("im_gray", im_gray)

# 二值化
t, binary = cv2.threshold(im_gray, 160, 255, cv2.THRESH_BINARY)
cv2.imshow("binary", binary)

# 找轮廓点
contours, hie = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 生成掩膜图像
mask = np.zeros_like(binary)

# 把镀盘填充画在掩膜图像上， 最后一个-1 填充轮廓
im_fill = cv2.drawContours(mask, contours, -1, 255, -1)
cv2.imshow("im_fill", im_fill)

# 图像减法
im_sub = cv2.subtract(im_fill, binary)
cv2.imshow("im_sub", im_sub)

# 收缩离散点
im_close = cv2.morphologyEx(im_sub, cv2.MORPH_CLOSE, (3, 3), iterations=3)
cv2.imshow("im_close", im_close)

# 寻找瑕疵轮廓
contours, hie = cv2.findContours(im_close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 对瑕疵面积排序,取最大的瑕疵
contours = sorted(contours, key=cv2.contourArea, reverse=True)
# 计算最大的瑕疵面积
area = cv2.contourArea(contours[0])

if area > 10:
    # 拟合瑕疵的最小外接圆 原始图像画出
    (x, y), radius = cv2.minEnclosingCircle(contours[0])
    cv2.circle(im, (int(x), int(y)), int(radius), (0, 0, 255), 2)
    cv2.imshow("im", im)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：综合案例 CPU镀盘瑕疵检测；cv2.imshow("im", im)；灰度化；二值化。
> - 主要变量/数据名包括：`im`、`im_gray`、`t, binary`、`contours, hie`、`mask`、`im_fill`、`im_sub`、`im_close`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.cvtColor()`：转换图像颜色空间，例如 BGR、RGB、GRAY、HSV。
> - `cv2.threshold()`：按阈值把灰度图转换成二值图或反二值图。
> - `cv2.findContours()`：查找图像中的轮廓。
> - `np.zeros_like()`：调用 `np` 中的 `zeros_like` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.drawContours()`：把检测到的轮廓画回图像上。
> - `cv2.subtract()`：对图像像素做饱和减法，常用于比较或削弱亮度。
> - `cv2.contourArea()`：调用 `cv2` 中的 `contourArea` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.circle()`：在图像上绘制圆形。

### day13/05_COIN.py

```python
"""
综合案例 标记图中硬币的轮廓并计算数量
"""
import cv2

im = cv2.imread("../img_data/coin.png")
# 灰度化
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# 高斯模糊 抑制噪声
im_blur = cv2.GaussianBlur(im_gray, (11, 11), 0)
# 二值化 OTSU 自动计算最佳全局阈值
t, binary = cv2.threshold(im_blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imshow("binary", binary)

# 查找轮廓
contours, hie = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# 绘制轮廓
cv2.drawContours(im, contours, -1, (0, 0, 255), 2)
cv2.imshow("im", im)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/coin.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：综合案例 标记图中硬币的轮廓并计算数量；灰度化；高斯模糊 抑制噪声；二值化 OTSU 自动计算最佳全局阈值。
> - 主要变量/数据名包括：`im`、`im_gray`、`im_blur`、`t, binary`、`contours, hie`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.cvtColor()`：转换图像颜色空间，例如 BGR、RGB、GRAY、HSV。
> - `cv2.threshold()`：按阈值把灰度图转换成二值图或反二值图。
> - `cv2.findContours()`：查找图像中的轮廓。
> - `cv2.drawContours()`：把检测到的轮廓画回图像上。

### day13/06_FACE.py

```python
"""
利用opencv提供的Haar级联分类器完成人脸识别
Haar级联分类器(预训练模型)基于Haar特征

"""
import cv2

# 加载分类器
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
im = cv2.imread("1.png")

im_gary = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

# 返回图像中
faces = face_cascade.detectMultiScale(im_gary, 1.3, 5)
print(faces)  # [[84 129 226 226]]  x,y,w,h

# 标记人脸
for x, y, w, h in faces:
    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow("face", im)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/day13/1.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：利用opencv提供的Haar级联分类器完成人脸识别；Haar级联分类器(预训练模型)基于Haar特征；加载分类器；返回图像中。
> - 主要变量/数据名包括：`face_cascade`、`im`、`im_gary`、`faces`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.CascadeClassifier()`：加载 Haar 级联分类器，常用于人脸检测。
> - `.detectMultiScale()`：在图像中检测目标区域，例如人脸框。
> - `cv2.rectangle()`：在图像上绘制矩形框。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习最小包围圆、拟合椭圆和多边形近似等形状分析方法。；通过 CPU 镀盘瑕疵检测练习灰度化、二值化、轮廓、掩膜、形态学和面积筛选。；通过硬币计数综合使用模糊、OTSU 二值化、轮廓查找和绘制。
> - **真实文件里的练习/主题**：最小包围圆；最优拟合椭圆；逼近多边形；综合案例 CPU镀盘瑕疵检测；综合案例 标记图中硬币的轮廓并计算数量；利用opencv提供的Haar级联分类器完成人脸识别。
>
> **新学代码怎么理解**
> - `cv2.minEnclosingCircle()`：计算包住目标轮廓的最小圆。
> - `cv2.circle()`：在图像上绘制圆形。
> - `cv2.fitEllipse()`：调用 `cv2` 中的 `fitEllipse` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.ellipse()`：在图像上绘制或拟合椭圆。
> - `cv2.findContours()`：查找图像中的轮廓。
> - `cv2.arcLength()`：计算轮廓周长。
> - `cv2.approxPolyDP()`：把轮廓近似成多边形，便于识别形状。
> - `cv2.drawContours()`：把检测到的轮廓画回图像上。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
