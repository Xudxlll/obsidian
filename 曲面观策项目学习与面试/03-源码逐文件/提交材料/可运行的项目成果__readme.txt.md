---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 目录说明文件

它解释本目录对应比赛哪一项提交、有哪些材料与操作要求；不参与训练、曲面计算或预警。

源文件：[readme.txt](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/readme.txt>)。

## 逐字原文

```text
文件夹作用：存放初赛提交材料②“可运行的项目成果”。

文件说明：
1. option_risk_warning_submission.zip
   曲面观策团队开发的 OptionRiskAgent 完整提交包。系统使用一个业务Agent完成问题一与问题二：读取指定品种和有效时间点，构造总方差IV曲面及Delta、Gamma、Vega、Theta曲面，提取12项风险证据，输出0—3级动态预警，并通过NetworkX四层知识图谱提供固定查询和可追溯解释。

运行环境：
- Windows 10/11或macOS；
- Python >= 3.12；
- 首次安装依赖通常需要网络，安装完成后可使用本地数据离线运行；
- 依赖在压缩包内的pyproject.toml中声明，主要包括pandas、NumPy、SciPy、PyArrow、NetworkX、Plotly、Matplotlib、scikit-learn和Streamlit。

安装步骤：
1. 解压 option_risk_warning_submission.zip；
2. 进入解压后的 option_risk_warning 目录；
3. 创建环境：python -m venv .venv
4. Windows安装：.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
5. macOS安装：./.venv/bin/python -m pip install -e '.[dev]'


启动后访问：http://127.0.0.1:8501

用户操作：从下拉框选择真实品种，再选择该品种可用时间点，点击“开始风险分析”。

数据说明：提交包不重复携带大赛提供的大体量原始数据。评委运行时请自行使用大赛数据。详细命令、跨平台说明、测试与验收证据见压缩包内README.md。


```

## 怎样使用

把它作为材料导航，再转到对应源码、技术文档、画布或声明；其中的运行与验证说法需按当前环境和轻量包实际内容核查。
