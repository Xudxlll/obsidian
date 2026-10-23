---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## pb 原始分区的共同作用

每个文件保存**一个期货合约月份在某个年月**的期权行，而不是一个文件保存整个品种的完整曲面。路径`archive/交易所/underlying/options/年/月/options_年月.parquet`编码了分区边界。把同一时刻的多个月份按显式键对齐，才能得到期限轴。

本页共53个有效Parquet，页脚行数合计1,311,080。各文件的读取者是`catalog.py`与`io.py`；清洗节点进入`features.py`和`surfaces.py`。不同时再读合并总表。

|文件路径（点击原文件）|行数|该文件作用|
|---|---:|---|
|[archive/SF/pb2412/options/2024/08/options_202408.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2412/options/2024/08/options_202408.parquet>)|440|pb2412于2024-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2412/options/2024/09/options_202409.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2412/options/2024/09/options_202409.parquet>)|32,574|pb2412于2024-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2412/options/2024/10/options_202410.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2412/options/2024/10/options_202410.parquet>)|31,968|pb2412于2024-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2412/options/2024/11/options_202411.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2412/options/2024/11/options_202411.parquet>)|29,664|pb2412于2024-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2501/options/2024/08/options_202408.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2501/options/2024/08/options_202408.parquet>)|440|pb2501于2024-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2501/options/2024/09/options_202409.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2501/options/2024/09/options_202409.parquet>)|31,220|pb2501于2024-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2501/options/2024/10/options_202410.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2501/options/2024/10/options_202410.parquet>)|31,946|pb2501于2024-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2501/options/2024/11/options_202411.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2501/options/2024/11/options_202411.parquet>)|37,296|pb2501于2024-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2501/options/2024/12/options_202412.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2501/options/2024/12/options_202412.parquet>)|34,844|pb2501于2024-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2502/options/2024/11/options_202411.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2502/options/2024/11/options_202411.parquet>)|6,552|pb2502于2024-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2502/options/2024/12/options_202412.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2502/options/2024/12/options_202412.parquet>)|37,414|pb2502于2024-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2502/options/2025/01/options_202501.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2502/options/2025/01/options_202501.parquet>)|25,742|pb2502于2025-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2503/options/2024/12/options_202412.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2503/options/2024/12/options_202412.parquet>)|15,328|pb2503于2024-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2503/options/2025/01/options_202501.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2503/options/2025/01/options_202501.parquet>)|34,202|pb2503于2025-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2503/options/2025/02/options_202502.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2503/options/2025/02/options_202502.parquet>)|29,384|pb2503于2025-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2504/options/2025/01/options_202501.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2504/options/2025/01/options_202501.parquet>)|8,512|pb2504于2025-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2504/options/2025/02/options_202502.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2504/options/2025/02/options_202502.parquet>)|37,274|pb2504于2025-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2504/options/2025/03/options_202503.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2504/options/2025/03/options_202503.parquet>)|35,200|pb2504于2025-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2505/options/2025/02/options_202502.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2505/options/2025/02/options_202502.parquet>)|9,320|pb2505于2025-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2505/options/2025/03/options_202503.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2505/options/2025/03/options_202503.parquet>)|34,772|pb2505于2025-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2505/options/2025/04/options_202504.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2505/options/2025/04/options_202504.parquet>)|31,166|pb2505于2025-04的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2506/options/2025/03/options_202503.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2506/options/2025/03/options_202503.parquet>)|14,470|pb2506于2025-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2506/options/2025/04/options_202504.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2506/options/2025/04/options_202504.parquet>)|39,190|pb2506于2025-04的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2506/options/2025/05/options_202505.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2506/options/2025/05/options_202505.parquet>)|29,354|pb2506于2025-05的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2507/options/2025/04/options_202504.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2507/options/2025/04/options_202504.parquet>)|10,740|pb2507于2025-04的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2507/options/2025/05/options_202505.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2507/options/2025/05/options_202505.parquet>)|35,128|pb2507于2025-05的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2507/options/2025/06/options_202506.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2507/options/2025/06/options_202506.parquet>)|29,050|pb2507于2025-06的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2508/options/2025/05/options_202505.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2508/options/2025/05/options_202505.parquet>)|9,024|pb2508于2025-05的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2508/options/2025/06/options_202506.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2508/options/2025/06/options_202506.parquet>)|31,072|pb2508于2025-06的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2508/options/2025/07/options_202507.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2508/options/2025/07/options_202507.parquet>)|31,832|pb2508于2025-07的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2509/options/2025/06/options_202506.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2509/options/2025/06/options_202506.parquet>)|9,734|pb2509于2025-06的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2509/options/2025/07/options_202507.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2509/options/2025/07/options_202507.parquet>)|37,444|pb2509于2025-07的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2509/options/2025/08/options_202508.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2509/options/2025/08/options_202508.parquet>)|28,376|pb2509于2025-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2510/options/2025/07/options_202507.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2510/options/2025/07/options_202507.parquet>)|9,320|pb2510于2025-07的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2510/options/2025/08/options_202508.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2510/options/2025/08/options_202508.parquet>)|32,582|pb2510于2025-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2510/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2510/options/2025/09/options_202509.parquet>)|28,028|pb2510于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2511/options/2025/08/options_202508.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2511/options/2025/08/options_202508.parquet>)|6,360|pb2511于2025-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2511/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2511/options/2025/09/options_202509.parquet>)|33,780|pb2511于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2511/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2511/options/2025/10/options_202510.parquet>)|3,700|pb2511于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2512/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2512/options/2025/09/options_202509.parquet>)|9,800|pb2512于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2512/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2512/options/2025/10/options_202510.parquet>)|3,700|pb2512于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2601/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2601/options/2025/10/options_202510.parquet>)|11,658|pb2601于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2601/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2601/options/2025/11/options_202511.parquet>)|33,566|pb2601于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2601/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2601/options/2025/12/options_202512.parquet>)|33,216|pb2601于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2602/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2602/options/2025/11/options_202511.parquet>)|14,862|pb2602于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2602/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2602/options/2025/12/options_202512.parquet>)|39,146|pb2602于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2602/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2602/options/2026/01/options_202601.parquet>)|27,688|pb2602于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2603/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2603/options/2025/12/options_202512.parquet>)|21,004|pb2603于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2603/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2603/options/2026/01/options_202601.parquet>)|35,586|pb2603于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2603/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2603/options/2026/02/options_202602.parquet>)|20,222|pb2603于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2604/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2604/options/2026/01/options_202601.parquet>)|28,744|pb2604于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2604/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2604/options/2026/02/options_202602.parquet>)|31,596|pb2604于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/pb2604/options/2026/03/options_202603.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/pb2604/options/2026/03/options_202603.parquet>)|45,850|pb2604于2026-03的全部期权报价，提供同月份执行价截面与时间序列|
