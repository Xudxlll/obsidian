---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/errors.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/errors.py>)

SHA-256：`d54e1192ece3ae228797861ae6996c3efdf1897e02aa6de883e97e9ddbd4fffb`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
"""Explicit errors raised by the single option risk Agent."""


class OptionRiskAgentError(RuntimeError):
    """Base class for user-facing Agent failures."""


class DataSourceUnavailableError(OptionRiskAgentError):
    """The configured market-data source cannot be read."""


class InvalidProductError(OptionRiskAgentError):
    """The requested product is not present in the catalog."""


class InvalidTimestampError(OptionRiskAgentError):
    """The requested timestamp is not valid for the selected product."""


class InsufficientHistoryError(OptionRiskAgentError):
    """There is not enough past data to make a dynamic decision."""


class SurfaceNotReadyError(OptionRiskAgentError):
    """The selected snapshot cannot form a reliable surface."""


class EvaluationUnavailableError(OptionRiskAgentError):
    """No competition-format offline evaluation is available."""
````

</details>
