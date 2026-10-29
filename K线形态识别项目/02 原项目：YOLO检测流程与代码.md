# 原项目：YOLO检测流程与代码

返回 [[00 项目总览与学习路线]]。

## 1. 模型到底做什么？

普通图片分类给整张图一个类别；目标检测同时输出**类别、位置框和置信度**，一张图可以有多个框，也可能没有框。YOLO属于目标检测方法；CNN等网络层可从图像中提取局部空间特征，但模型是否可靠要靠实际测试，不能由架构名称保证。

相关基础：[[AMA564 DEEP LEARNING/Lecture 04 - Computer Vision、Convolution 与 CNN 基础|卷积与CNN]]、[[Python、数据分析与人工智能/深度学习/08_目标检测_笔记|目标检测与YOLO]]。

GitHub仓库是 [candlestick-pattern-yolo](https://github.com/ayhannbozkurt/candlestick-pattern-yolo)，我们加载的是它所使用的 [FODUU YOLOv8 权重](https://huggingface.co/foduucom/stockmarket-pattern-detection-yolov8)。仓库代码、模型权重、原训练数据是不同东西：我们已经保存并运行代码和权重，但不能据此说掌握了原作者完整训练集或它的全部标注规范。

## 2. 模型输出的六类

| 类别 | 直观理解 |
|---|---|
| M_Head | M形／双顶 |
| W_Bottom | W形／双底 |
| Head and shoulders top | 头肩顶 |
| Head and shoulders bottom | 头肩底 |
| Triangle | 三角形整理 |
| StockLine | 原模型类别名；本次没有足够清楚的标注定义 |

图形名称只是形态类别，不应直接等同买入、卖出或未来方向。不同人对局部小形态和大形态的框法可能不同。

## 3. 代码如何串起来？

`outputs/original-yolo-run/upstream/src/model/pattern_detector.py` 定义 `PatternDetector` 类。类可以理解为一个工具的设计图，实例是具体工具；相关基础见 [[Python、数据分析与人工智能/Python基础/07-面向对象编程基础|Python类与实例]]。

实际批处理封装在 `outputs/original-yolo-run/run_images.py`。核心两句如下（节选；这两句不能脱离上下文单独运行）：

```python
detections = detector.detect_patterns(image, conf_threshold=conf)
annotated = detector.draw_detections(image, detections)
```

第一句接收图像并返回检测列表；每项包含 `pattern`、`confidence` 和 `bbox`。第二句把框和标签画在图片副本上。`bbox` 是 `[x1, y1, x2, y2]`：左上角与右下角像素坐标。置信度是模型输出分数，**不是经过验证的真实正确概率**。

我们保留了未修改的检测类，但为运行修正了加载器等兼容问题并增加批处理入口；细节见原项目运行目录的 README 和 `compatibility.patch`。运行时没有重新训练FODUU权重。

## 4. 已经跑过什么？

对全部117张图运行，69张有输出、48张无输出，共104个检测框。**104是输出个数，不是正确个数**。大量滑窗重叠，相同历史形态也会重复出现。无输出只表示该设置下未超过输出阈值，不证明图片没有形态。

后续单独对12张不重叠图片做了视觉标签评估，详见 [[04 如何判断模型效果与下一步]]。要看输出，可打开 `outputs/original-yolo-run/results/` 的图片和 `predictions.json`。
