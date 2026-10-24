---
类型: 源码教学
模块: 核心链路
源文件: "src/option_risk/interactive.py"
依据: 最终提交项目静态源码
---

> [!abstract] 一句话定位
> **将Agent契约转换成交互Plotly图形**。图层消费结果并允许旋转、悬停、查看历史，不替代分析与决策。

源文件：[src/option_risk/interactive.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:1>)。本文解释实际实现；逐字源码请结合知识库的源码档案阅读。

## 输入、输出与上下游

输入SurfacePayload（期限用年）或timeline，输出Plotly Figure交Streamlit展示。它不访问原始数据、不训练、不修改告警级别。与Matplotlib离线图不同，3D纵轴用T年而非DTE天。

## 逐个理解核心对象与函数

### `_title`（24—28 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:24>)

统一标题为指标、品种、时间，并明确横轴ln(K/F)、纵轴T=dte/365。标题本身不检查数据经济坐标是否正确，应由上游契约保证。

### `_layout`（31—42 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:31>)

统一白色主题、字体、边距、高度和水平图例并返回同一个figure，减少不同图视觉语义不一致。

### `iv_surface_figure`（45—68 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:45>)

用SurfacePayload的k与T建mesh，Plotly Surface画IV，connectgaps=False保留无支持区域，hover显示坐标与IV；设置scene轴名和高度610。

### `surface_heatmap_figure`（71—86 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:71>)

用原始k/T轴和values画Heatmap，明确connectgaps=False，色条取指标名，显示悬停数值；不对缺失节点补值。

### `greeks_figure`（89—126 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:89>)

2×2子图遍历四Greeks，Delta/Theta用RdBu并zmid=0，Gamma/Vega用Viridis，分别放置色条；标题声称与IV使用同一网格，但本函数只消费传入payload，不检查各网格一致性。应以每个payload实际坐标及上游构建方式为准。

### `term_curves_figure`（129—152 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:129>)

逐期限行取有限values，只画该期限支持的k位置，用不同线型与点型区分，name展示DTE与T；曲线横轴仍是k，因此实际为“各期限微笑曲线”，不是固定k下横轴T的期限结构曲线。

### `timeline_figure`（155—222 行）

[定位源码](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/interactive.py:155>)

把timeline截到selected_timestamp及以前，画core_risk_pressure、dynamic_boundary、danger_core_boundary，再按0—3级画不同颜色/符号状态点。图例0.98与1.50文字硬编码，纵轴值来自列；若政策变化，文字有漂移风险。只负责展示上游已算时间轴，并不独立保证特征无未来。

## 关键推导、具体例子与真实边界

悬停中IV=0.25表示年化波动率25%，不能读成0.25%；T=0.0822约30天，不是0.0822天。不同指标有不同单位，Delta可正可负、Theta可能负，颜色应按相同指标内部比较。

`term_curves_figure`名字容易误导：$T$固定、$k$变化的是微笑；$k$固定、$T$变化才是期限结构。图层从同一SurfacePayload读取，不保证Greeks是从正式IV曲面重新求导得到；上游实际上是聚合/插值原Greeks列。

## 面试怎么讲，追问怎么答

**问：显示“不显示未来”是否能证明无泄漏？** 它只证明这张图截去了未来行；还要检查原特征的rolling/shift、Agent读取截止、模型训练边界等。

**问：交互图缺一块是bug吗？** 可能是数据无支持/拟合不可用，应先看质量与fit_diagnostics，再判断展示问题。

## 下一步学习

[[曲面观策项目学习与面试/02-循序学习/核心02-同一时间怎样从微笑走到曲面.md|核心02-同一时间怎样从微笑走到曲面]]
