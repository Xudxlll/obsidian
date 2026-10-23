---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/pyproject.toml](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/pyproject.toml>)

SHA-256：`86fc3f892c717828d960dd0207308a5ecb654090f6d3bba332fd1c2f8b2fa4aa`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````toml
[build-system]
requires = ["setuptools>=75", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "option-risk-warning"
version = "0.2.0"
description = "Commodity option volatility-surface risk warning prototype"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
  "joblib>=1.4",
  "matplotlib>=3.9",
  "nbclient>=0.10",
  "nbformat>=5.10",
  "networkx>=3.4,<4",
  "numpy>=2.0",
  "pandas>=2.2",
  "plotly>=6.0",
  "pyarrow>=17",
  "scikit-learn>=1.5",
  "scipy>=1.14",
  "streamlit>=1.62,<1.63",
]

[project.optional-dependencies]
dev = ["ipykernel>=6.29", "jupyter>=1.1", "pytest>=8.3"]

[project.scripts]
option-risk = "option_risk.cli:main"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
````

</details>
