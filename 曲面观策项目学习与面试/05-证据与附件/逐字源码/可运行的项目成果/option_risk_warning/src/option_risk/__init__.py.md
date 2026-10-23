---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/__init__.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/__init__.py>)

SHA-256：`33aadb0c6a4963e0331455d738094a58af145f33e0c92617fadf95dd11a83941`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
"""Single-Agent volatility-surface risk warning prototype."""

from .agent import OptionRiskAgent
from .config import AgentConfig, PipelineConfig
from .pipeline import run_pipeline

__all__ = ["AgentConfig", "OptionRiskAgent", "PipelineConfig", "run_pipeline"]
__version__ = "0.2.0"
````

</details>
