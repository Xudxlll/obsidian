---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/visualization.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **把既有分析结果导出为离线图像和网格**。绘图不训练模型，也不负责校验最终经济有效性。

源文件：[src/option_risk/visualization.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/visualization.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入SurfaceGrid或nodes/alerts，输出PNG和NPZ路径。Matplotlib使用Agg无界面后端，适合批处理。pipeline负责提前创建figures目录；绘图函数自身不总是mkdir。

## 逐个理解核心对象与函数

### `_formal_timeline_pressure`（21—27 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/visualization.py:21>)

强制要求core_risk_pressure列，转换为数值并返回中文标签；缺列抛异常，防止用risk_probability或总体质量压力替代正式驱动轴。

### `plot_surface_3d`（30—44 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/visualization.py:30>)

meshgrid将k/DTE变二维坐标，mask无效values，用plot_surface生成3D图，标注ln(K/F)、天数和指标，固定视角保存160dpi后关闭figure释放资源。

### `plot_greeks_heatmaps`（47—68 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/visualization.py:47>)

2×2展示Delta/Gamma/Vega/Theta，每项调用surface_grid；Delta/Theta用发散色，其余Viridis。imshow extent把最小最大DTE映到像素边界，期限实际不等距时视觉可能近似均匀，不应据像素距离读取精确期限间隔。

### `plot_alert_timeline`（71—129 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/visualization.py:71>)

优先只画test，空则tail1000。上图ATM IV并按alert_level着色，下图严格画core_risk_pressure和DecisionPolicy固定警告/危险核心阈值。标的是持续状态而非只画通知；图标题固定写连续三个月，需要数据覆盖与实际配置相符。

### `save_snapshot_grids`（132—143 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/visualization.py:132>)

依次构建五个metric的grid，用每个metric独立的values/x/dte键保存压缩NPZ，加timestamp字符串。每项保存独立横轴，不能预设IV专用拟合网格和Greeks33点完全同轴；消费方应按各自键读取。

## 关键推导、具体例子与真实边界

一个表中的NaN节点在3D图里是信息缺口，不是0；把NaN填0会制造虚假的低波动山谷。单快照图只说明截面形状，时间轴才反映动态压力；两者需要同时解释。

代码给图设中文字体候选，但实际机器若缺字体仍可能乱码；仅静态读源码不等于已经渲染验证。此学习整理没有运行原项目全量作图，不能声称所有PNG已重新生成无误。

## 面试怎么讲，追问怎么答

**问：Greeks热图表示组合风险吗？** 展示节点聚合Greeks，没结合投资者实际多空头寸和合约乘数，不能当个人组合净风险。

**问：时间轴散点就是发送通知吗？** 本图按alert_level画持续状态，通知应另看alert_emitted列。

## 下一步学习

[[02-循序学习/核心08-离线Pipeline与单时点Agent的完整关系]]
