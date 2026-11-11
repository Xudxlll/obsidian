# 量化交易进阶:第45天 - 因子数据库设计(Factor Database Design)

原创 逻辑与流 逻辑与流 2025年11月4日 21:03 北京 标题已修改 1人

数据结构决定策略效率 因子计算完成后,如何存储 索引 查询直接影响整个回测与生产系统的性能本文系统讲解因子数据库设计思路,从三层架构(原始行情库 因子库 回测数据集)出发,详细解析因子表的核心字段设计 主键与索引策略 外键关系 对比SQLite与MySQL的适用场景,通过SQLAlchemy ORM框架完整演示因子数据库的建模 连接 写入 查询操作,提供可直接运行的完整示例代码 揭示因子数据库在量化系统中的核心作用——让因子计算与回测模块完全解耦,支持多进程与历史数据复用,大幅提升系统效率,为量化策略的工程化奠定坚实基础

## 学习时间

理论学习: 15分钟

代码实践: 20分钟

案例分析: 10分钟

总计: 45分钟

我们正式进入量化课程 Day 45：因子数据库设计

今天这一讲非常关键，因为——“数据结构决定策略效率”

因子计算完以后，如果你存储 索引 查询都设计得好，整个回测与生产系统会快好几倍

## 一 因子数据库设计思路

在一个完整的量化系统中，我们通常有如下三个层次的数据库结构：

<table><tr><td>模块</td><td>作用</td><td>示例表</td></tr><tr><td>原始行情库</td><td>存储原始行情数据(开高低收、成交量等)</td><td>price_daily</td></tr><tr><td>因子库</td><td>存储各种计算后的因子结果</td><td>factor_value</td></tr><tr><td>回测数据集</td><td>用于回测或实盘信号</td><td>backtest_signal</td></tr></table>

今天我们主要关注因子库设计

## 因子表的核心字段设计

<table><tr><td>字段名</td><td>类型</td><td>含义</td><td>备注</td></tr><tr><td>id</td><td>INTEGER / BIGINT</td><td>自增主键</td><td>唯一标识</td></tr><tr><td>factor_id</td><td>VARCHAR(64)</td><td>因子名或因子标识</td><td>例如 "PE", "PB", "ROE_5D"</td></tr><tr><td>stock_code</td><td>VARCHAR(16)</td><td>股票代码</td><td>e.g. "000001.SZ"</td></tr><tr><td>trade_date</td><td>DATE</td><td>交易日期</td><td>通常按日为主键部分</td></tr><tr><td>factor_value</td><td>FLOAT / DOUBLE</td><td>因子值</td><td>可以为 NULL</td></tr><tr><td>update_time</td><td>DATETIME</td><td>数据更新时间</td><td>自动维护</td></tr></table>

主键与索引设计

通常我们希望唯一确定一条因子记录的键是：

PRIMARY KEY (factor\_id, stock\_code, trade\_date)

这样可以保证每个因子 每支股票 每个交易日的记录唯一

此外，为加快查询：

创建索引：

(trade\_date) → 快速获取某 日所有股票的因子

(stock\_code) → 快速获取某支股票的时间序列

(factor\_id) → 快速获取某个因子全样本

## 外键关系

可选，但推荐在工程化系统中加入：

stock\_code 可关联到股票主表 stock\_basic(code, name, industry, status)

factor\_id 可关联到因子定义表 factor\_meta(factor\_id, description, update\_freq, author)

这让系统更具可扩展性

## 二<sub>、</sub>SQLite 与 MySQL 对比

结论：

学习<sub>、</sub>研究<sub>、</sub>开发阶段 → SQLite

回测平台 因子共享服务 → MySQL

SQLite 是最佳入门方案：易用 便携 无依赖

## 三 用 SQLAlchemy 建模与操作因子表

SQLAlchemy 是 Python 的 ORM 框架，可以兼容 SQLite MySQL PostgreSQL 等

下面我们从零构建一个完整的因子数据库模块

1 建立模型类（ORM 映射）

from sqlalchemy import create\_engine, Column, Integer, String, Float, Date, DateTime, Prima

from sqlalchemy.orm import declarative\_base, sessionmaker

from datetime import datetime

Base = declarative\_base()

class FactorValue(Base):

## \_\_tablename\_\_ = 'factor\_value'

$$
\text { factor\_id } = \text { Column(String(64),   nullable = False) }
$$

$$
\text { stock\_code } = \text { Column(String(16),   nullable = False) }
$$

trade\_date = Column(Date, nullable=False)

factor\_value = Column(Float)

update\_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

\_table\_args\_\_ = (

$$
\text { PrimaryKeyConstraint('factor\_id', 'stock\_code', 'trade\_date'), }
$$

## 2 创建数据库连接与表结构

#SQLite

$$
\text { engine } = \text { create\_engine('sqlite:   //factor\_db.sqlite',   echo = False) }
$$

#MySQL（可扩展)

\# engine = create\_engine('mysql+pymysql://user:password@localhost/factor\_db?charset=utf8mb4

Base.metadata.create\_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

## 3 写入数据

import pandas as pd

#示例数据

data = [

$$
\{\text { 'factor\_id': 'PE', 'stock\_code': '000001.SZ', 'trade\_date': '2025 - 11 - 01', 'factor\_value }
$$

{'factor\_id': 'PE', 'stock\_code': '000002.SZ', 'trade\_date': '2025-11-01', 'factor\_value

{'factor\_id': 'PB', 'stock\_code': '000001.SZ', 'trade\_date': '2025-11-01', 'factor\_value

#批量写入

$$
\text { records } = [ \text { FactorValue } (* * d) \text {   for   } d \text {   in   data } ]
$$

session.add\_all(records)

session.commit()

## 4 查询数据

查询某日的 PE因子

res = session.query(FactorValue).filter(

FactorValue.factor\_id == 'PE',

FactorValue.trade\_date == '2025-11-01'

5 pandas 一键写入（适合大批量）

df = pd.DataFrame(data) df.to\_sql('factor\_value', engine, if\_exists='append', index=False)

## 四 完整可运行示例（SQLite）

整合上面内容，以下代码可直接运行：

lass FactorValue(Base): tablename\_\_ = 'factor\_value' factor\_id = Column(String(64), nullable=False) stock\_code = Column(String(16), nullable=False) trade\_date = Column(Date, nullable=False) factor\_value = Column(Float) update\_time = Column(DateTime, default=datetime.now, onupdate=datetime.now) table\_args\_\_ = ( PrimaryKeyConstraint('factor\_id', 'stock\_code', 'trade\_date'),

for r in res:

print(f"{r.stock\_code}: {r.factor\_value}")

## 输出：

000001.SZ: 12.3

000002.SZ: 15.6

## 五 扩展到 MySQL（只需两步）

## 1 修改连接字符串：

engine = create\_engine('mysql+pymysql://user:password@localhost/factor\_db?charset=utf8mb4')

2 在 MySQL 中提前建库：

CREATE DATABASE factor\_db CHARACTER SET utf8mb4 COLLATE utf8mb4\_unicode\_ci;

六 与"因子计算 → 存储 → 回测"流程衔接

整个流程如下：

## 1 计算阶段

在 Python 中根据行情数据计算因子值（如 PE ROE 动量等）

2 存储阶段（今日主题）

将因子结果以 factor\_id, stock\_code, trade\_date 三元组存入数据库

## 3 回测阶段

从数据库中读取所需因子数据 → 合并行情数据 → 排序/分组构建多空组合 → 计算收益

数据库在此扮演中枢角色：

它让"计算模块"和"回测模块"完全解耦，支持多进程与历史数据复用

总结

<table><tr><td>模块</td><td>要点</td></tr><tr><td>表结构</td><td>factor_id + stock_code + trade_date 三元主键</td></tr><tr><td>索引</td><td>按因子、股票、日期建索引加速查询</td></tr><tr><td>SQLite</td><td>本地研究型数据库,零配置</td></tr></table>

![](附件/MinerU图片/第45天/8a186f3e1757e4ba4cd11091e240607ed1c151cd885e551403bf81ee089d0137.jpg)  
阅读 144 修改于2025年11月 4 日

<table><tr><td>模块</td><td>要点</td></tr><tr><td>MySQL</td><td>生产与团队协作首选</td></tr><tr><td>ORM层</td><td>使用SQLAlchemy,兼容多数据库</td></tr><tr><td>工程化意义</td><td>因子复用、高效存储、快速查询、回测无缝衔接</td></tr></table>

## 结论

因子数据库设计是量化系统工程化的关键环节 通过合理的数据结构设计 索引策略和ORM框架应用我们实现了因子计算与回测模块的完全解耦,大幅提升了系统的可扩展性和执行效率 掌握SQLite与MySQL的适用场景,熟练使用SQLAlchemy进行数据库操作,为量化策略的工程化部署奠定了坚实基础
