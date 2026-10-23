---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## bu 原始分区的共同作用

每个文件保存**一个期货合约月份在某个年月**的期权行，而不是一个文件保存整个品种的完整曲面。路径`archive/交易所/underlying/options/年/月/options_年月.parquet`编码了分区边界。把同一时刻的多个月份按显式键对齐，才能得到期限轴。

本页共18个有效Parquet，页脚行数合计296,928。各文件的读取者是`catalog.py`与`io.py`；清洗节点进入`features.py`和`surfaces.py`。不同时再读合并总表。

|文件路径（点击原文件）|行数|该文件作用|
|---|---:|---|
|[archive/SF/bu2512/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2512/options/2025/09/options_202509.parquet>)|24,496|bu2512于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2512/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2512/options/2025/10/options_202510.parquet>)|3,996|bu2512于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2601/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2601/options/2025/09/options_202509.parquet>)|12,174|bu2601于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2601/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2601/options/2025/10/options_202510.parquet>)|1,998|bu2601于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2601/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2601/options/2025/11/options_202511.parquet>)|2,212|bu2601于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2601/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2601/options/2025/12/options_202512.parquet>)|5,410|bu2601于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2602/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2602/options/2025/10/options_202510.parquet>)|1,790|bu2602于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2602/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2602/options/2025/11/options_202511.parquet>)|8,132|bu2602于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2602/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2602/options/2025/12/options_202512.parquet>)|13,490|bu2602于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2602/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2602/options/2026/01/options_202601.parquet>)|9,296|bu2602于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2603/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2603/options/2025/11/options_202511.parquet>)|1,824|bu2603于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2603/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2603/options/2025/12/options_202512.parquet>)|33,914|bu2603于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2603/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2603/options/2026/01/options_202601.parquet>)|31,678|bu2603于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2603/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2603/options/2026/02/options_202602.parquet>)|19,386|bu2603于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2604/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2604/options/2025/12/options_202512.parquet>)|12,066|bu2604于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2604/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2604/options/2026/01/options_202601.parquet>)|30,242|bu2604于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2604/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2604/options/2026/02/options_202602.parquet>)|28,112|bu2604于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/bu2604/options/2026/03/options_202603.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/bu2604/options/2026/03/options_202603.parquet>)|56,712|bu2604于2026-03的全部期权报价，提供同月份执行价截面与时间序列|
