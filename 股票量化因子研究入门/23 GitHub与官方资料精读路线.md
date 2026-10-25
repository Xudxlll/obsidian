---
title: GitHub与官方资料精读路线
type: 资料精读
tags: [因子研究, GitHub, 官方文档]
status: 未学习
created: 2026-10-26
---

[[00 从这里开始 - 因子研究学习地图]] → 本篇 → [[25 研究模板与一对一提问卡]]

## 用一个问题读一小段代码

你的目标是掌握研究流程，不是把仓库全部跑完。每次只带一个问题进入源码，例如“这个因子何时可见”“收益从哪个价格开始”“样本为什么消失”。读完要留下自己的小复现和边界说明。以下链接已于 **2026-10-26** 核验；链接存在不代表所有环境都能运行，更不代表适用于真实 A 股或能盈利。

## 第一站：先学因子，再学组合

先读官方 ML4T 的 [04_alpha_factor_research](https://github.com/stefan-jansen/machine-learning-for-trading/tree/second-edition/04_alpha_factor_research) README，再定位 pandas 构造因子及 Alphalens 评价的例子；摘录“数据→信号→评价”的输入输出，与你的五日反转比较。之后读 [05_strategy_evaluation](https://github.com/stefan-jansen/machine-learning-for-trading/tree/second-edition/05_strategy_evaluation)，先抓收益、风险与基准，不急着复现组合优化。

**版本陷阱**：上述目录属于 `second-edition`，核验时该分支指向 `f652d79ab2f137d75d554af2cc437a5512b16069`；当前 `main` 已采用第三版章节布局。旧教程的“第4章”不能直接对应当前 main。第二版也含历史平台和旧依赖，阅读思路与直接安装必须分开；不要为运行旧平台交出真实账户密钥。

## 第二站：看清评价器到底收到什么

阅读 [Alphalens-reloaded overview.ipynb](https://github.com/stefan-jansen/alphalens-reloaded/blob/main/src/alphalens/examples/overview.ipynb)。先找因子 Series 的日期与股票双层索引，再找价格矩阵与 forward returns，最后看分组、IC 与换手。它是评价工具，不会替你决定正确成交时间。例子的数据源和下载方法可能随服务变化，先使用本课程已保存样本，不以下载失败否定方法。

做一个对照：课程信号在 t 收盘后、t+1 开盘入场；若评价器把同一日期的收盘价当收益起点，问题已经变了。先手算一只股票的 H=5 标签，再检查工具输出是否一致。不要直接贴一张漂亮 tear sheet 就结束。[项目说明与依赖](https://github.com/stefan-jansen/alphalens-reloaded/blob/main/README.md)

## 第三站：后学 Qlib 的工程组织

先读 [workflow 官方说明](https://qlib.readthedocs.io/en/latest/component/workflow.html)，辨认数据、训练、推断、评价和记录；再读 [handler.py](https://github.com/microsoft/qlib/blob/main/qlib/contrib/data/handler.py) 与 [loader.py](https://github.com/microsoft/qlib/blob/main/qlib/contrib/data/loader.py) 的 Alpha158、Alpha360。它们是特征集合，不是保证有效的“158/360个独立 alpha”。只挑一条表达式翻译成人话并手算。

检查默认标签与本课 H=5 是否一致，再检查训练拟合区间；配置文件存在不会自动保证无泄漏。最后读 [PIT 文档](https://qlib.readthedocs.io/en/latest/advanced/PIT.html) 及 [PIT 采集说明](https://github.com/microsoft/qlib/blob/main/scripts/data_collector/pit/README.md)：工具支持 PIT，不等于输入数据天然有正确历史版本。官方采集说明也提醒其数据可能不完善。

## 第四站：知道为什么需要保留失败实验

先读 Harvey、Liu、Zhu 的 [因子多重检验论文摘要与引言](https://people.duke.edu/~charvey/Research/Published_Papers/P118_and_the_cross.PDF)，理解“试过很多因子后只报告赢家”的问题；再读 Bailey、López de Prado 的 [Deflated Sharpe Ratio](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)，理解筛选会抬高看见的最佳表现。不要把某个 t 值阈值当成所有市场、所有样本的通行证。

## 练习与验收

任选一个例子，用六行笔记写：问题、输入、可见时间、公式、收益起点、尚未核实处。问题：代码能运行，能否证明回测无泄漏？

> [!answer]- 展开参考答案
> 不能。运行只说明这组输入和环境完成了计算。还需核对历史股票池、复权与财报版本、标签时点、训练切分及交易约束；这些常常由使用者负责。

- [ ] 手算并复现一条公式，能解释每个 `shift/Ref` 的方向。
- [ ] 保存分支或提交编号，不依赖会变化的默认首页。
- [ ] 安装前查看依赖和许可，记录未核实项；详见 [[27 来源索引与核验记录]]。
