---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## sn 原始分区的共同作用

每个文件保存**一个期货合约月份在某个年月**的期权行，而不是一个文件保存整个品种的完整曲面。路径`archive/交易所/underlying/options/年/月/options_年月.parquet`编码了分区边界。把同一时刻的多个月份按显式键对齐，才能得到期限轴。

本页共55个有效Parquet，页脚行数合计1,332,443。各文件的读取者是`catalog.py`与`io.py`；清洗节点进入`features.py`和`surfaces.py`。不同时再读合并总表。

|文件路径（点击原文件）|行数|该文件作用|
|---|---:|---|
|[archive/SF/sn2412/options/2024/08/options_202408.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2412/options/2024/08/options_202408.parquet>)|396|sn2412于2024-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2412/options/2024/09/options_202409.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2412/options/2024/09/options_202409.parquet>)|27,794|sn2412于2024-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2412/options/2024/10/options_202410.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2412/options/2024/10/options_202410.parquet>)|27,920|sn2412于2024-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2412/options/2024/11/options_202411.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2412/options/2024/11/options_202411.parquet>)|26,844|sn2412于2024-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2501/options/2024/08/options_202408.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2501/options/2024/08/options_202408.parquet>)|396|sn2501于2024-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2501/options/2024/09/options_202409.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2501/options/2024/09/options_202409.parquet>)|27,794|sn2501于2024-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2501/options/2024/10/options_202410.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2501/options/2024/10/options_202410.parquet>)|27,920|sn2501于2024-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2501/options/2024/11/options_202411.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2501/options/2024/11/options_202411.parquet>)|34,254|sn2501于2024-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2501/options/2024/12/options_202412.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2501/options/2024/12/options_202412.parquet>)|31,440|sn2501于2024-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2502/options/2024/11/options_202411.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2502/options/2024/11/options_202411.parquet>)|5,354|sn2502于2024-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2502/options/2024/12/options_202412.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2502/options/2024/12/options_202412.parquet>)|31,790|sn2502于2024-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2502/options/2025/01/options_202501.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2502/options/2025/01/options_202501.parquet>)|20,280|sn2502于2025-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2503/options/2024/12/options_202412.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2503/options/2024/12/options_202412.parquet>)|9,106|sn2503于2024-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2503/options/2025/01/options_202501.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2503/options/2025/01/options_202501.parquet>)|24,900|sn2503于2025-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2503/options/2025/02/options_202502.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2503/options/2025/02/options_202502.parquet>)|22,752|sn2503于2025-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2504/options/2025/01/options_202501.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2504/options/2025/01/options_202501.parquet>)|5,886|sn2504于2025-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2504/options/2025/02/options_202502.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2504/options/2025/02/options_202502.parquet>)|30,384|sn2504于2025-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2504/options/2025/03/options_202503.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2504/options/2025/03/options_202503.parquet>)|31,736|sn2504于2025-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2505/options/2025/02/options_202502.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2505/options/2025/02/options_202502.parquet>)|14,130|sn2505于2025-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2505/options/2025/03/options_202503.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2505/options/2025/03/options_202503.parquet>)|34,424|sn2505于2025-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2505/options/2025/04/options_202504.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2505/options/2025/04/options_202504.parquet>)|32,624|sn2505于2025-04的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2506/options/2025/03/options_202503.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2506/options/2025/03/options_202503.parquet>)|13,486|sn2506于2025-03的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2506/options/2025/04/options_202504.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2506/options/2025/04/options_202504.parquet>)|39,944|sn2506于2025-04的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2506/options/2025/05/options_202505.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2506/options/2025/05/options_202505.parquet>)|29,376|sn2506于2025-05的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2507/options/2025/04/options_202504.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2507/options/2025/04/options_202504.parquet>)|5,938|sn2507于2025-04的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2507/options/2025/05/options_202505.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2507/options/2025/05/options_202505.parquet>)|29,526|sn2507于2025-05的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2507/options/2025/06/options_202506.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2507/options/2025/06/options_202506.parquet>)|24,402|sn2507于2025-06的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2508/options/2025/05/options_202505.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2508/options/2025/05/options_202505.parquet>)|6,064|sn2508于2025-05的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2508/options/2025/06/options_202506.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2508/options/2025/06/options_202506.parquet>)|31,154|sn2508于2025-06的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2508/options/2025/07/options_202507.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2508/options/2025/07/options_202507.parquet>)|30,448|sn2508于2025-07的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2509/options/2025/06/options_202506.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2509/options/2025/06/options_202506.parquet>)|5,894|sn2509于2025-06的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2509/options/2025/07/options_202507.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2509/options/2025/07/options_202507.parquet>)|33,122|sn2509于2025-07的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2509/options/2025/08/options_202508.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2509/options/2025/08/options_202508.parquet>)|25,956|sn2509于2025-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2510/options/2025/07/options_202507.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2510/options/2025/07/options_202507.parquet>)|5,968|sn2510于2025-07的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2510/options/2025/08/options_202508.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2510/options/2025/08/options_202508.parquet>)|31,050|sn2510于2025-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2510/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2510/options/2025/09/options_202509.parquet>)|27,510|sn2510于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2511/options/2025/08/options_202508.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2511/options/2025/08/options_202508.parquet>)|6,064|sn2511于2025-08的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2511/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2511/options/2025/09/options_202509.parquet>)|32,752|sn2511于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2511/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2511/options/2025/10/options_202510.parquet>)|3,404|sn2511于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2512/options/2025/09/options_202509.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2512/options/2025/09/options_202509.parquet>)|6,182|sn2512于2025-09的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2512/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2512/options/2025/10/options_202510.parquet>)|3,404|sn2512于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2601/options/2025/10/options_202510.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2601/options/2025/10/options_202510.parquet>)|710|sn2601于2025-10的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2601/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2601/options/2025/11/options_202511.parquet>)|4,802|sn2601于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2601/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2601/options/2025/12/options_202512.parquet>)|14,246|sn2601于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2602/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2602/options/2025/11/options_202511.parquet>)|21,012|sn2602于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2602/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2602/options/2025/12/options_202512.parquet>)|44,450|sn2602于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2602/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2602/options/2026/01/options_202601.parquet>)|49,312|sn2602于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2603/options/2025/11/options_202511.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2603/options/2025/11/options_202511.parquet>)|2,816|sn2603于2025-11的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2603/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2603/options/2025/12/options_202512.parquet>)|39,344|sn2603于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2603/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2603/options/2026/01/options_202601.parquet>)|63,272|sn2603于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2603/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2603/options/2026/02/options_202602.parquet>)|38,054|sn2603于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2604/options/2025/12/options_202512.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2604/options/2025/12/options_202512.parquet>)|20,686|sn2604于2025-12的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2604/options/2026/01/options_202601.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2604/options/2026/01/options_202601.parquet>)|56,438|sn2604于2026-01的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2604/options/2026/02/options_202602.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2604/options/2026/02/options_202602.parquet>)|51,282|sn2604于2026-02的全部期权报价，提供同月份执行价截面与时间序列|
|[archive/SF/sn2604/options/2026/03/options_202603.parquet](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/11-基于期权波动率曲面与智能体的量化风控预警系统/期权课题数据集/archive/SF/sn2604/options/2026/03/options_202603.parquet>)|66,251|sn2604于2026-03的全部期权报价，提供同月份执行价截面与时间序列|
