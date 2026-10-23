---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## fu 原始分区的共同作用

每个文件保存**一个期货合约月份在某个年月**的期权行，而不是一个文件保存整个品种的完整曲面。路径`archive/交易所/underlying/options/年/月/options_年月.parquet`编码了分区边界。把同一时刻的多个月份按显式键对齐，才能得到期限轴。

本页共24个有效Parquet，页脚行数合计414,302。各文件的读取者是`catalog.py`与`io.py`；清洗节点进入`features.py`和`surfaces.py`。不同时再读合并总表。

|文件路径（点击原文件）|行数|该文件作用|
|---|---:|---|
|[archive/SF/fu2601/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2601/options/2025/09/options_202509.parquet>)|21,692|fu2601于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2601/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2601/options/2025/10/options_202510.parquet>)|3,552|fu2601于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2602/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2602/options/2025/09/options_202509.parquet>)|21,078|fu2602于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2602/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2602/options/2025/10/options_202510.parquet>)|3,530|fu2602于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2602/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2602/options/2025/11/options_202511.parquet>)|1,250|fu2602于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2602/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2602/options/2025/12/options_202512.parquet>)|5,106|fu2602于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2602/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2602/options/2026/01/options_202601.parquet>)|2,376|fu2602于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2603/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2603/options/2025/10/options_202510.parquet>)|318|fu2603于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2603/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2603/options/2025/11/options_202511.parquet>)|2,656|fu2603于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2603/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2603/options/2025/12/options_202512.parquet>)|6,808|fu2603于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2603/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2603/options/2026/01/options_202601.parquet>)|5,920|fu2603于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2603/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2603/options/2026/02/options_202602.parquet>)|1,392|fu2603于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2604/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2604/options/2025/11/options_202511.parquet>)|27,324|fu2604于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2604/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2604/options/2025/12/options_202512.parquet>)|37,244|fu2604于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2604/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2604/options/2026/01/options_202601.parquet>)|32,582|fu2604于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2604/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2604/options/2026/02/options_202602.parquet>)|25,936|fu2604于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2604/options/2026/03/options_202603.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2604/options/2026/03/options_202603.parquet>)|56,882|fu2604于2026-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2605/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2605/options/2025/10/options_202510.parquet>)|1,250|fu2605于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2605/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2605/options/2025/11/options_202511.parquet>)|5,224|fu2605于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2605/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2605/options/2025/12/options_202512.parquet>)|8,510|fu2605于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2605/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2605/options/2026/01/options_202601.parquet>)|7,422|fu2605于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2605/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2605/options/2026/02/options_202602.parquet>)|8,324|fu2605于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2605/options/2026/03/options_202603.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2605/options/2026/03/options_202603.parquet>)|78,564|fu2605于2026-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/fu2605/options/2026/04/options_202604.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/fu2605/options/2026/04/options_202604.parquet>)|49,362|fu2605于2026-04的全部期权报价，提供同月份执行价截面与时间序列|
