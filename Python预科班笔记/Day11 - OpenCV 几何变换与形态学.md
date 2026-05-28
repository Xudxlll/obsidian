## 今天学了什么

> [!info] 今天学了什么
> - 学习图像翻转、平移、旋转、缩放等几何变换。
> - 学习图像加法、减法和加权融合，理解像素级运算。
> - 学习腐蚀、膨胀、开运算、闭运算、形态学梯度、顶帽和黑帽。

## 抓主线

> [!tip] 抓主线
> 1. 几何变换改变像素的位置。
> 2. 像素运算改变像素值之间的关系。
> 3. 形态学操作根据结构元素改变前景区域形状。
> 4. 不同形态操作服务于去噪、连接、填洞、提边或提取局部差异。

## 课堂代码合集

### day11/01_cv_flip.py

```python
"""
形态操作
   仿射转换(平移 镜像 旋转) 透视转换
   缩放 
   图像加法减法
   腐蚀和膨胀
   开闭运算 形态学梯度 礼帽运算 黑帽运算

图像翻转 ==> 镜像
本质上是 坐标转换
"""
import cv2

im = cv2.imread("../img_data/Linus.png")
cv2.imshow("im", im)

# 垂直镜像 沿着x轴上下颠倒
# 第0行和最后1行交换,第1行和倒数第2行交换，以此类推
im_flip1 = cv2.flip(im, 0)
cv2.imshow("im_flip1", im_flip1)

# 水平 沿着y轴左右
# 第0列和最后1列交换,第1列和倒数第2列交换，以此类推
im_flip2 = cv2.flip(im, 1)
cv2.imshow("im_flip2", im_flip2)

# 同时进行水平镜像和垂直镜像
im_flip3 = cv2.flip(im, -1)
cv2.imshow("im_flip3", im_flip3)

cv2.waitKey()
cv2.destroyAllWindows()


# **核心主题：如何通过数学运算和结构操作来改变图像的形状、位置、大小、结构以及像素值关系。**
#
# **一、几何变换 (Geometric Transformations)**
# 这类操作改变的是图像中像素的**空间位置关系**，需要知道变换后每个像素的新位置在哪里。
#
# 1.  **仿射变换 (Affine Transformation):**
#     *   **本质：** 是一种**线性变换**（直线变换后还是直线，平行线变换后依然平行）加上**平移**。可以用一个 **2x3 的变换矩阵** `M` 来表示。
#     *   **通用公式 (OpenCV 中使用)：**
#         `dst(x, y) = src(M₁₁ * x + M₁₂ * y + M₁₃, M₂₁ * x + M₂₂ * y + M₂₃)`
#     *   **包含的具体操作：**
#         *   **平移 (Translation):** 将图像沿着X轴和Y轴移动指定的像素距离 (`tx`, `ty`)。变换矩阵很简单：
#             ```
#             M = [ 1  0  tx ]
#                 [ 0  1  ty ]
#             ```
#             *   *效果：* 图像整体移动，移出画布的部分会丢失，新出现的区域通常填充黑色或指定的颜色。
#         *   **缩放 (Scaling):** 改变图像的宽度和高度。`(sx, sy)` 分别是 X 轴和 Y 轴的缩放因子。
#             ```
#             M = [ sx  0   0  ]
#                 [ 0   sy  0  ]
#             ```
#             *   *效果：*
#                 *   `sx/sy > 1`：放大图像。放大后像素信息不会增加，会变得模糊（需要插值）。
#                 *   `0 < sx/sy < 1`：缩小图像。丢弃部分像素信息。
#                 *   `sx/sy < 0`：除了缩放，还会进行镜像（见下）。
#         *   **镜像 (Reflection / Flipping):** 沿着某个轴翻转图像。这就是你笔记和代码中重点提到的部分！
#             *   **水平镜像 (沿垂直轴/Y轴)：** 就像照镜子，左右互换。`sx = -1, sy = 1, tx = width` (或特定调整)。
#                 *   `cv2.flip(img, 1)` 或 `cv2.flip(img, flipCode=1)`。如你代码中的 `im_flip2`。
#                 *   *数学本质：* `x' = width - 1 - x` (原点在左上角)。
#             *   **垂直镜像 (沿水平轴/X轴)：** 上下颠倒。`sx = 1, sy = -1, ty = height` (或特定调整)。
#                 *   `cv2.flip(img, 0)` 或 `cv2.flip(img, flipCode=0)`。如你代码中的 `im_flip1`。
#                 *   *数学本质：* `y' = height - 1 - y`。
#             *   **双向镜像 (沿两个轴)：** 先水平再垂直，或者先垂直再水平，效果一样：旋转180度。
#                 *   `cv2.flip(img, -1)` 或 `cv2.flip(img, flipCode=-1)`。如你代码中的 `im_flip3`。
#                 *   *数学本质：* `x' = width - 1 - x`, `y' = height - 1 - y`。
#             *   **为什么叫“仿射”中的镜像？** 因为镜像可以用缩放因子为负的缩放变换矩阵来表示（通常还需要配合平移来保证图像还在画布内）。
#         *   **旋转 (Rotation):** 围绕一个点（通常是图像中心）旋转图像一个角度 θ (theta)。
#             ```
#             M = [ cosθ   -sinθ   (1-cosθ)*center_x + sinθ*center_y ]
#                 [ sinθ    cosθ   -sinθ*center_x + (1-cosθ)*center_y ]
#             ```
#             *   `cv2.getRotationMatrix2D(center, angle, scale)` 计算矩阵。
#             *   `cv2.warpAffine(img, M, (width, height))` 应用变换。
#             *   *效果：* 图像旋转，角落部分可能移出画布，新区域填充背景色。旋转也会导致部分像素信息损失或需要插值。
#     *   **共同特点：** 都需要一个变换矩阵 `M`，最终都通过 `cv2.warpAffine()` 函数来实现变换（除了镜像有专门的 `flip` 函数）。
#
# 2.  **透视变换 (Perspective Transformation):**
#     *   **本质：** 比仿射变换更通用的一种**投影变换**。它不再保持平行性（平行线变换后可能相交）。用于模拟视角变化，比如把一张倾斜拍摄的名片“拉正”成矩形俯视图。
#     *   **原理：** 需要图像上的 **4 个点** (通常是源图像中的一个四边形的4个角点) 和它们变换后对应的 **4 个目标点**。
#     *   **计算：** `cv2.getPerspectiveTransform(src_points, dst_points)` 计算得到一个 **3x3 的变换矩阵** `M_persp`。
#     *   **应用：** `cv2.warpPerspective(img, M_persp, (width, height))`。
#     *   **与仿射的区别：** 仿射是3自由度(平移tx,ty, 旋转θ, 缩放sx,sy)，透视是8自由度。仿射保持平行线，透视不保持。
#
# **二、像素运算 (Pixel-wise Operations)**
# 这类操作直接对图像的**像素值**进行数学运算，不改变像素的位置。
#
# 1.  **图像加法 (Image Addition):**
#     *   **目的：** 叠加两幅图像（如叠加水印）、降低噪声（多幅图像平均）。
#     *   **操作：** `cv2.add(img1, img2)` 或 `numpy` 加法 `img1 + img2`。
#     *   **关键区别：**
#         *   `cv2.add()`: **饱和运算**。结果超出255 (对于8位图像) 会被截断到255。`150 + 150 = 255`。
#         *   `numpy +`: **模运算**。结果超出255会取模。`150 + 150 = 300 % 256 = 44` (通常不是想要的效果)。
#     *   **加权加法 (图像混合)：** `cv2.addWeighted(img1, alpha, img2, beta, gamma)`。效果：`dst = alpha * img1 + beta * img2 + gamma`。
#
# 2.  **图像减法 (Image Subtraction):**
#     *   **目的：** 检测变化（监控中运动物体检测）、去除背景、比较差异。
#     *   **操作：** `cv2.subtract(img1, img2)` 或 `numpy` 减法 `img1 - img2`。
#     *   **关键区别：**
#         *   `cv2.subtract()`: **饱和运算**。结果小于0会被截断到0。`50 - 100 = 0`。
#         *   `numpy -`: **模运算**。结果小于0会取模。`50 - 100 = -50 % 256 = 206` (通常不是想要的效果)。
#     *   **绝对差 (Absolute Difference):** 更常用！`cv2.absdiff(img1, img2)`。计算 `|img1 - img2|`。结果总是非负的，直接显示出差异区域。是运动检测的基础。
#
# **三、形态学操作 (Morphological Operations)**
# 这类操作基于**形状**，使用一个称为**结构元素 (Structuring Element)** 的小模板（如小矩形、十字形、圆形）在图像上滑动，根据邻域像素和结构元素的形状关系来修改图像（主要是二值图像，有时也用于灰度图像）。核心目标是**改变物体的形状、连接性、去除噪声**。
#
# 1.  **基础操作：**
#     *   **腐蚀 (Erosion):**
#         *   **操作：** 结构元素在图像上滑动。只有当结构元素**完全覆盖**的区域都是前景(白色)时，中心点才保留为前景；否则变为背景(黑色)。
#         *   **效果：** 前景物体**变小、变瘦**。细小的前景物体（噪声点）会被**消除**，断开的前景物体可能被**分离**。`cv2.erode(img, kernel, iterations)`
#     *   **膨胀 (Dilation):**
#         *   **操作：** 结构元素在图像上滑动。只要结构元素覆盖的区域**包含至少一个**前景像素，中心点就置为前景。
#         *   **效果：** 前景物体**变大、变粗**。细小的**孔洞**会被**填充**，断开的前景物体可能被**连接**。`cv2.dilate(img, kernel, iterations)`
#     *   **关键参数：**
#         *   `kernel`: 结构元素。大小和形状（`cv2.getStructuringElement(shape, size)`）直接影响效果。矩形`MORPH_RECT`、十字形`MORPH_CROSS`、椭圆形`MORPH_ELLIPSE`。
#         *   `iterations`: 执行操作的次数。次数越多，效果越强。
#
# 2.  **组合操作 (基于腐蚀和膨胀)：**
#     *   **开运算 (Opening):**
#         *   **操作：** **先腐蚀，后膨胀**。`opening = cv2.dilate(cv2.erode(img, kernel), kernel)`
#         *   **效果：** **消除小的前景噪点（“胡椒盐”噪声中的盐粒/白点），平滑物体轮廓，断开细小的连接。** 能基本保持物体原有大小。
#         *   **记忆口诀：** “开”门 - 先腐蚀（消除门口小障碍），再膨胀（恢复门的大小）。
#     *   **闭运算 (Closing):**
#         *   **操作：** **先膨胀，后腐蚀**。`closing = cv2.erode(cv2.dilate(img, kernel), kernel)`
#         *   **效果：** **填充前景物体内部小的孔洞和裂缝，连接邻近的物体，平滑轮廓。** 能基本保持物体原有大小。
#         *   **记忆口诀：** “关”门 - 先膨胀（堵住门缝/孔洞），再腐蚀（恢复门的大小）。
#     *   **形态学梯度 (Morphological Gradient):**
#         *   **操作：** **膨胀图减去腐蚀图**。`gradient = cv2.dilate(img, kernel) - cv2.erode(img, kernel)` 或 `cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)`
#         *   **效果：** 得到物体**边缘轮廓**。看起来像图像的边缘。
#     *   **礼帽/顶帽运算 (Top Hat):**
#         *   **操作：** **原图减去开运算图**。`tophat = img - opening` 或 `cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)`
#         *   **效果：** 突出原图中比周围区域**亮**的**小细节**或**噪点**（这些细节在开运算中被去掉了）。常用于在**不均匀光照**背景下提取亮的小物体。
#     *   **黑帽运算 (Black Hat):**
#         *   **操作：** **闭运算图减去原图**。`blackhat = closing - img` 或 `cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)`
#         *   **效果：** 突出原图中比周围区域**暗**的**小细节**或**孔洞**（这些细节在闭运算中被填充了）。常用于检测暗的小物体或孔洞。
#
# **总结回顾：**
#
# 1.  **几何变换 (改位置/形状):**
#     *   **仿射 (`warpAffine`)：** 平移、缩放(含负缩放即镜像)、旋转。保持平行线。
#     *   **镜像 (`flip`)：** 水平(`1`)、垂直(`0`)、双向(`-1`)。坐标变换本质。
#     *   **透视 (`warpPerspective`)：** 视角校正。需要4对点。不保持平行线。
# 2.  **像素运算 (改像素值):**
#     *   **加法 (`add/addWeighted`)：** 叠加、混合。注意饱和 vs 模运算。
#     *   **减法 (`subtract/absdiff`)：** 找变化、去背景。`absdiff` 最常用（取绝对值）。
# 3.  **形态学操作 (改形状/结构)：**
#     *   **基础：** 腐蚀(瘦身/去小点)、膨胀(增肥/补小洞)。核心是`kernel`。
#     *   **组合：**
#         *   **开运算：** 去亮噪点 (先腐后膨)。
#         *   **闭运算：** 补暗小洞 (先膨后腐)。
#         *   **形态学梯度：** 求边缘 (膨 - 腐)。
#         *   **礼帽：** 提亮细节 (原 - 开)。
#         *   **黑帽：** 提暗细节 (闭 - 原)。
#
# **关键理解点：**
#
# *   **坐标 vs 像素值：** 几何变换改变像素坐标位置；像素运算和形态学操作改变的是像素位置上的灰度值或二值。
# *   **结构元素 (Kernel) 的重要性：** 在形态学中，`kernel` 的大小和形状决定了操作的力度和效果。就像你用不同大小和形状的“刷子”去修改图像的结构。
# *   **开闭运算的互补性：** 开去小亮点，闭补小黑洞。它们是处理二值图像噪声和连接性的利器。
# *   **礼帽/黑帽的应用场景：** 它们特别擅长在复杂背景下提取特定的小特征（亮或暗）。
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/Linus.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：形态操作；仿射转换(平移 镜像 旋转) 透视转换；缩放；图像加法减法。
> - 主要变量/数据名包括：`im`、`im_flip1`、`im_flip2`、`im_flip3`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.flip()`：按水平、垂直或双方向翻转图像。

### day11/02_cv_warp.py

```python
"""
仿射变换: 平移 镜像 旋转
图像平移

"""
import cv2
import numpy as np

im = cv2.imread("../img_data/Linus.png")
cv2.imshow("im", im)

# 获取原图的宽高
h, w = im.shape[:2]

# M 2 x 3仿射变换矩阵
# 左上 2 * 2 控制旋转 缩放 剪切 最后1列控制平移
# M = [
#     [a,b,c],
#     [d,e,f]
# ]
# a = 1 x轴缩放+旋转系数
# b = 0 xy轴的剪切系数
# d = 0 yx轴的剪切系数
# e = 1 y轴缩放+旋转系数
# c = tx x轴的平移量
# f = ty y轴的平移量

# (w,h)需要知道宽高,输出图像和原图大小一致

tx = 80  # 平移的x坐标
ty = 100  # 平移的y坐标
M = np.float32([[1, 0, tx], [0, 1, ty]])
# 向右移动80像素,向下移动100像素
im_translated = cv2.warpAffine(im, M, (w, h))
cv2.imshow("im_translated", im_translated)

# 向下移动50像素
M = np.float32([[1, 0, 0], [0, 1, 50]])
im_translated2 = cv2.warpAffine(im, M, (w, h))
cv2.imshow("im_translated2", im_translated2)

# 向左移动40像素,向下移动40个像素
M = np.float32([[1, 0, -40], [0, 1, 40]])
im_translated3 = cv2.warpAffine(im, M, (w, h))
cv2.imshow("im_translated3", im_translated3)

# 向右移动40像素,向上移动40个像素
M = np.float32([[1, 0, 40], [0, 1, -40]])
im_translated4 = cv2.warpAffine(im, M, (w, h))
cv2.imshow("im_translated4", im_translated4)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/Linus.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：仿射变换: 平移 镜像 旋转；图像平移；获取原图的宽高；M 2 x 3仿射变换矩阵。
> - 主要变量/数据名包括：`im`、`h, w`、`tx`、`ty`、`M`、`im_translated`、`im_translated2`、`im_translated3`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `np.float32()`：调用 `np` 中的 `float32` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.warpAffine()`：执行仿射变换，用来平移、旋转或缩放图像。

### day11/03_cv_warp.py

```python
"""
仿射变换: 平移 镜像 旋转
图像旋转

"""
import cv2
import numpy as np

im = cv2.imread("../img_data/Linus.png")
cv2.imshow("im", im)

# 获取原图的宽高
h, w = im.shape[:2]

# 旋转矩阵 角度 旋转中心 缩放比例
center = (w / 2, h / 2)
angle = -45  # 数字为正 逆时针
scale = 0.5  # 缩放因子 1不缩放 <1 缩小 >1放大
M = cv2.getRotationMatrix2D(center, angle, scale)


im_rotated = cv2.warpAffine(im, M, (w, h))
cv2.imshow("im_rotated", im_rotated)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/Linus.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：仿射变换: 平移 镜像 旋转；图像旋转；获取原图的宽高；旋转矩阵 角度 旋转中心 缩放比例。
> - 主要变量/数据名包括：`im`、`h, w`、`center`、`angle`、`scale`、`M`、`im_rotated`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.getRotationMatrix2D()`：生成图像旋转所需的仿射矩阵。
> - `cv2.warpAffine()`：执行仿射变换，用来平移、旋转或缩放图像。

### day11/04_cv_resize.py

```python
"""
图像缩放
图像大小调整的过程
放大:插入元素 最邻近插值法 双线性插值法(2*2 加权平均)
缩小:删除矩阵中元素实现



"""
import cv2

im = cv2.imread("../img_data/Linus.png")
cv2.imshow("im", im)

# 获取原图的宽高
h, w = im.shape[:2]

# 缩放到原来的一半
im_resized1 = cv2.resize(im, (w // 2, h // 2))
cv2.imshow("im_resized1", im_resized1)

# 缩放到指定大小
im_resized2 = cv2.resize(im, (200, 300))
cv2.imshow("im_resized2", im_resized2)

# 缩放到指定大小 最近邻插值
im_resized3 = cv2.resize(im, (600, 800), cv2.INTER_NEAREST)
cv2.imshow("im_resized3", im_resized3)

# 缩放到指定大小 双线性插值
im_resized4 = cv2.resize(im, (600, 800), cv2.INTER_LINEAR)
cv2.imshow("im_resized4", im_resized4)

# 缩放到指定大小
im_resized5 = cv2.resize(im, (600, 800), cv2.INTER_LANCZOS4)
cv2.imshow("im_resized5", im_resized5)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/Linus.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像缩放；图像大小调整的过程；放大:插入元素 最邻近插值法 双线性插值法(2*2 加权平均)；缩小:删除矩阵中元素实现。
> - 主要变量/数据名包括：`im`、`h, w`、`im_resized1`、`im_resized2`、`im_resized3`、`im_resized4`、`im_resized5`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.resize()`：缩放图像尺寸。

### day11/05_cv_add.py

```python
"""
图像加法  去噪声  水印
"""
import cv2

im1 = cv2.imread("../img_data/lena.jpg")
im2 = cv2.imread("../img_data/lily_square.png")

# 图片直接相加  过亮 过白  像素直接相加超出255截断为255
im_add1 = cv2.add(im1, im2)
cv2.imshow("im_add1", im_add1)

# 加权求和
im_add2 = cv2.addWeighted(im1, 0.7, im2, 0.3, 0)
cv2.imshow("im_add2", im_add2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/lena.jpg]]
> ![[附件/Python预科班/img_data/lily_square.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像加法  去噪声  水印；图片直接相加  过亮 过白  像素直接相加超出255截断为255；加权求和。
> - 主要变量/数据名包括：`im1`、`im2`、`im_add1`、`im_add2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.add()`：对图像像素做饱和加法，常用于图像叠加。
> - `cv2.addWeighted()`：调用 `cv2` 中的 `addWeighted` 功能，结合本文件注释理解它在当前练习中的作用。

### day11/06_cv_subtract.py

```python
"""
图像减法  图像的差异
"""
import cv2

im1 = cv2.imread("../img_data/bub.png")
im2 = cv2.imread("../img_data/bub2.png")

#
im_sub1 = cv2.subtract(im2, im1)
cv2.imshow("im_sub1", im_sub1)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/bub.png]]
> ![[附件/Python预科班/img_data/bub2.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像减法  图像的差异。
> - 主要变量/数据名包括：`im1`、`im2`、`im_sub1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.subtract()`：对图像像素做饱和减法，常用于比较或削弱亮度。

### day11/07_cv_erode.py

```python
"""
图像腐蚀
图像向内收缩 , 消除边界点 去除噪声,分离物体
"""
import cv2
import numpy as np

im = cv2.imread("../img_data/8.png")
cv2.imshow("im", im)

# 腐蚀
# 邻域最小值比较 滑动窗口机制 不是卷积
kernel = np.ones((3, 3), np.uint8)  # 腐蚀计算的腐蚀核
print(kernel)

# iterations 迭代次数为3 腐蚀操作重复3次 基于上一次结果继续腐蚀
im_erode = cv2.erode(im, kernel, iterations=3)
cv2.imshow("im_erode", im_erode)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/8.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像腐蚀；图像向内收缩 , 消除边界点 去除噪声,分离物体；腐蚀；邻域最小值比较 滑动窗口机制 不是卷积。
> - 主要变量/数据名包括：`im`、`kernel`、`im_erode`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `np.ones()`：创建全 1 数组，常用来构造卷积核或结构元素。
> - `cv2.erode()`：腐蚀白色区域，常用于去除小噪点。

### day11/08_cv_dilate.py

```python
"""
图像膨胀
图像向外扩充 链接图像 填充空洞
"""
import cv2
import numpy as np


im = cv2.imread("../img_data/6.png")
cv2.imshow("im", im)

kernel = np.ones((3, 3), np.uint8)  # 膨胀核
im_dilate = cv2.dilate(im, kernel, iterations=5)
cv2.imshow("im_dilate", im_dilate)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/6.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像膨胀；图像向外扩充 链接图像 填充空洞；膨胀核。
> - 主要变量/数据名包括：`im`、`kernel`、`im_dilate`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.dilate()`：膨胀白色区域，常用于填补断裂或扩张目标。

### day11/09_cv_open.py

```python
"""
图像开运算 先腐蚀后膨胀
"""
import cv2
import numpy as np

im1 = cv2.imread("../img_data/7.png")
im2 = cv2.imread("../img_data/8.png")
cv2.imshow("im1", im1)
cv2.imshow("im2", im2)

kernel = np.ones((10, 10), np.uint8)
o1 = cv2.morphologyEx(im1, cv2.MORPH_OPEN, kernel)
o2 = cv2.morphologyEx(im2, cv2.MORPH_OPEN, kernel)

cv2.imshow("o1", o1)
cv2.imshow("o2", o2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/7.png]]
> ![[附件/Python预科班/img_data/8.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像开运算 先腐蚀后膨胀。
> - 主要变量/数据名包括：`im1`、`im2`、`kernel`、`o1`、`o2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.morphologyEx()`：执行开运算、闭运算、梯度、顶帽、黑帽等形态学操作。

### day11/10_cv_close.py

```python
"""
图像闭运算 先膨胀后腐蚀
"""
import cv2
import numpy as np

im1 = cv2.imread("../img_data/9.png")
im2 = cv2.imread("../img_data/10.png")
cv2.imshow("im1", im1)
cv2.imshow("im2", im2)

kernel = np.ones((10, 10), np.uint8)
c1 = cv2.morphologyEx(im1, cv2.MORPH_CLOSE, kernel, iterations=2)
c2 = cv2.morphologyEx(im2, cv2.MORPH_CLOSE, kernel, iterations=2)

cv2.imshow("c1", c1)
cv2.imshow("c2", c2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/9.png]]
> ![[附件/Python预科班/img_data/10.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：图像闭运算 先膨胀后腐蚀。
> - 主要变量/数据名包括：`im1`、`im2`、`kernel`、`c1`、`c2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.morphologyEx()`：执行开运算、闭运算、梯度、顶帽、黑帽等形态学操作。

### day11/11_cv_gradient.py

```python
"""
形态学梯度

膨胀图像 - 腐蚀图像 原始图像中前景图像的边缘
"""
import cv2
import numpy as np

im1 = cv2.imread("../img_data/5.png")
cv2.imshow("im1", im1)

kernel = np.ones((3, 3), np.uint8)
o1 = cv2.morphologyEx(im1, cv2.MORPH_OPEN, kernel, iterations=3)
g1 = cv2.morphologyEx(o1, cv2.MORPH_GRADIENT, kernel)

cv2.imshow("g1", g1)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/5.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：形态学梯度；膨胀图像 - 腐蚀图像 原始图像中前景图像的边缘。
> - 主要变量/数据名包括：`im1`、`kernel`、`o1`、`g1`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.morphologyEx()`：执行开运算、闭运算、梯度、顶帽、黑帽等形态学操作。

### day11/12_cv_tophat.py

```python
"""
礼帽运算
原始图像减去开运算图像的操作 得到噪声信息
"""
import cv2
import numpy as np

im1 = cv2.imread("../img_data/5.png")
cv2.imshow("im1", im1)

kernel = np.ones((5, 5), np.uint8)
im_hat1 = cv2.morphologyEx(im1, cv2.MORPH_TOPHAT, kernel)
cv2.imshow("im_hat1", im_hat1)

# 手动实现礼帽运算
im_open = cv2.morphologyEx(im1, cv2.MORPH_OPEN, kernel)
im_hat2 = cv2.subtract(im1,im_open)
cv2.imshow("im_hat2", im_hat2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/5.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：礼帽运算；原始图像减去开运算图像的操作 得到噪声信息；手动实现礼帽运算。
> - 主要变量/数据名包括：`im1`、`kernel`、`im_hat1`、`im_open`、`im_hat2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.morphologyEx()`：执行开运算、闭运算、梯度、顶帽、黑帽等形态学操作。

### day11/13_cv_blackhat.py

```python
"""
黑帽运算
闭运算图像减去原始图像的操作
"""
import cv2
import numpy as np

im1 = cv2.imread("../img_data/9.png")
cv2.imshow("im1", im1)

kernel = np.ones((5, 5), np.uint8)
im_hat1 = cv2.morphologyEx(im1, cv2.MORPH_BLACKHAT, kernel)
cv2.imshow("im_hat1", im_hat1)

# 手动实现黑帽运算
im_colse = cv2.morphologyEx(im1, cv2.MORPH_CLOSE, kernel)
im_hat2 = cv2.subtract(im_colse, im1)
cv2.imshow("im_hat2", im_hat2)

cv2.waitKey()
cv2.destroyAllWindows()
```

> [!quote] 相关图示理解
> ![[附件/Python预科班/img_data/9.png]]

> [!note] 这份文件实际讲了什么
> - 文件说明/题目写的是：黑帽运算；闭运算图像减去原始图像的操作；手动实现黑帽运算。
> - 主要变量/数据名包括：`im1`、`kernel`、`im_hat1`、`im_colse`、`im_hat2`。

> [!example] 本文件出现的新代码 / 函数 / 方法
> - `cv2.morphologyEx()`：执行开运算、闭运算、梯度、顶帽、黑帽等形态学操作。

## 总结

> [!summary] 总结
> - **今天的核心任务**：学习图像翻转、平移、旋转、缩放等几何变换。；学习图像加法、减法和加权融合，理解像素级运算。；学习腐蚀、膨胀、开运算、闭运算、形态学梯度、顶帽和黑帽。
> - **真实文件里的练习/主题**：形态操作；仿射变换: 平移 镜像 旋转；仿射变换: 平移 镜像 旋转；图像缩放；图像加法  去噪声  水印；图像减法  图像的差异；图像腐蚀；图像膨胀。
>
> **新学代码怎么理解**
> - `cv2.flip()`：按水平、垂直或双方向翻转图像。
> - `np.float32()`：调用 `np` 中的 `float32` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.warpAffine()`：执行仿射变换，用来平移、旋转或缩放图像。
> - `cv2.getRotationMatrix2D()`：生成图像旋转所需的仿射矩阵。
> - `cv2.resize()`：缩放图像尺寸。
> - `cv2.add()`：对图像像素做饱和加法，常用于图像叠加。
> - `cv2.addWeighted()`：调用 `cv2` 中的 `addWeighted` 功能，结合本文件注释理解它在当前练习中的作用。
> - `cv2.subtract()`：对图像像素做饱和减法，常用于比较或削弱亮度。
>
> **复盘建议**
> - 先看文件说明，再看原代码，最后解释新函数/方法的输入、输出和用途。
