---
title: 从SQL到机器学习因子
type: 实操教程
tags: [因子研究, SQL, 机器学习, Ridge]
status: 未学习
created: 2026-10-26
---

[[00 从这里开始 - 因子研究学习地图]] → 本篇 → [[23 GitHub与官方资料精读路线]]

## 把已有机器学习知识接到股票面板上

一行是“某股票在某个信号日”。特征 $X_{i,t}$ 来自当时可见的信息；标签 $y_{i,t}$ 是之后五个开盘区间的收益；预测 $\hat y_{i,t}$ 可作选股分数。先用原始五日反转与负二十日波动两个特征，比较固定等权分数与 Ridge。线性模型便于检查符号、尺度和错位，深度学习不是入门门槛。

## 第一步：直接运行已有数据的桥接脚本

从 [sql_ml_bridge.py](附件/实验台/sql_ml_bridge.py) 开始，代码只用 NumPy、pandas 和 Python 自带 SQLite，不联网、不读取密钥。先确认 [[05 环境与实验台使用]] 的真实 CSV 已存在，再复制：

```bash
'/Users/xuji/.cache/factor-research-learning-venv/bin/python' '/Users/xuji/Documents/obsidian/股票量化因子研究入门/附件/实验台/sql_ml_bridge.py'
```

输出在 `附件/实验台/sql_ml_outputs/`：`predictions.csv` 是逐股票预测；`daily_ic.csv` 是分日期、分模型 IC；`diagnostics.csv` 是汇总；`coverage_and_boundaries.csv` 记录缺失与标签边界；`run_summary.json` 保存固定参数、训练处理值与局限。没有生成组合收益，不能把 IC 当作可交易业绩。

## 第二步：跟着字段走通 SQL

数据流是 `panel.csv + sessions.csv → load_panel → SQLite内存表 → 特征与标签 → 按日期分段 → 训练与评价`。字段对应如下：

|位置|日期/股票|收盘价|
|---|---|---|
|CSV|`date / asset`|原始 `close`，另有 `adj_factor`|
|`load_panel` 后|完整 `date×asset` 网格|`close` 已乘复权因子，缺价不填|
|SQLite表|`date / asset`|改名 `adj_close`，避免误认原价|

脚本把这张完整网格写入 `bars_calendar_aligned`，核心查询是：

```sql
WITH windows AS (
  SELECT date, asset, adj_close,
    LAG(adj_close, 5) OVER (
      PARTITION BY asset ORDER BY date) AS lag5,
    COUNT(adj_close) OVER (
      PARTITION BY asset ORDER BY date
      ROWS BETWEEN 5 PRECEDING AND CURRENT ROW) AS n_valid
  FROM bars_calendar_aligned
)
SELECT date, asset,
  CASE WHEN n_valid = 6 AND lag5 > 0
       THEN -(1.0 * adj_close / lag5 - 1.0)
       ELSE NULL END AS reversal_5d
FROM windows;
```

`LAG` 是同股往前五个日历格；`COUNT=6` 要求从 t−5 到 t 六个收盘价都存在，与实验台主线一致。只查两个端点会漏掉中间停牌。脚本用 `assert_allclose` 逐格核对 SQL 与 `lab.reversal_factor`，包含缺失位置。

## 第三步：只用过去构造两项特征

反转为 $-(C_t^{adj}/C_{t-5}^{adj}-1)$；低波为最近20个日收益的负样本标准差，使用 `ddof=1`，需要至少21个连续收盘价。不填补缺价，也不使用未来收益清洗特征。H=5 标签另由 `forward_returns` 计算 $O_{t+6}^{adj}/O_{t+1}^{adj}-1$，按相同日期和股票连接。

2023训练、2024验证、2025研究留出，每年先用 `sample_dates` 剔除跨年出口标签，再为统计拟合/评价取完整配对样本。同一信号日的股票全部进入同一段，禁止随机拆行。2024特征可使用2023已发生的历史价格。**2025已在课程中展示，不再是完全未见的独立证据。**

## 第四步：读懂固定 Ridge 的计算

脚本只在2023训练行拟合特征均值与总体标准差（`ddof=0`），之后原样转换2024、2025；没有重新拟合处理值、填补器或模型。低波特征自身的样本标准差与这里的训练尺度是两件事。

令训练标准化特征为 $Z$，训练标签均值为 $b$，固定 $\alpha=10$：

$$
\hat\beta=(Z^\top Z+10I)^{-1}Z^\top(y-b),\qquad
\hat y=b+Z\hat\beta.
$$

实际用 `numpy.linalg.solve`，不显式求逆。目标是残差平方和加 $10\|\beta\|^2$，截距不惩罚；这是求和口径，不与平均损失口径的同名 alpha 混同。没有搜索 alpha，也没有用验证年重训。等权基线取两列训练标准化特征的均值，仅用于同样本排序对照。[官方预处理泄漏说明](https://scikit-learn.org/stable/common_pitfalls.html)

## 练习与验收

运行后核对训练最后信号日与标签终点；再回答：窗口中间一天缺价、两端有价时，SQL 应输出什么？能把2025的正 IC 当作模型增量有效吗？

> [!answer]- 展开参考答案
> 完整窗口计数不足6，必须为缺失。2025已经展示，且这是事后固定20股、重叠标签的教学比较，没有中性化、显著性、成本或可交易性验证；正 IC 不能证明增量有效。下一步应冻结方案，用未参与选择的新数据或前瞻影子观测复核。

- [ ] 脚本成功运行，SQL与主线逐格核对通过。
- [ ] 能指出字段改名、两个标准差用途、训练参数与时间边界。
- [ ] 保存全部对照和负结果，不把诊断当收益；版本记录见 [[19 因子库数据管线与实验记录]]。
