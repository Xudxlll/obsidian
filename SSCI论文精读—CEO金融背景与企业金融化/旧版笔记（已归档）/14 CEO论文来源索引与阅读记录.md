---
created: 2026-10-25
tags: [论文精读, 来源, 版本记录]
---

# 来源索引与阅读记录

返回：[[00 CEO论文阅读导航与核心结论]]

## 一、本次完整精读的主要来源

用户文件：`/Users/xuji/Documents/简历/SSCI2区 第二作者.pdf`。

保留副本：[[CEO金融背景与企业金融化—用户提供投稿稿.pdf]]，共20页；首两页为投稿系统封面及作者页，p.3开始匿名正文，p.18—20为参考文献。页码均指PDF物理页号，不把它与正式期刊页码混用。

全文图片与折叠文本：[[15 CEO论文原文逐页对照]]。数值和版面冲突时，以原PDF页面为准；规范公式与中文解释见各专题笔记。

| PDF页 | 内容 | 主要阅读入口 |
| --- | --- | --- |
| 1—2 | 稿号、作者顺序、通讯作者、投稿版本 | 00、02、11 |
| 3—4 | 摘要、引言、贡献、理论开头 | 01、02 |
| 5—7 | 理论与H1—H3，模型设定开头 | 02、03、05 |
| 7—9 | 式(1)—(5)、变量定义、原表4-2、样本 | 03、05、07、08 |
| 10 | 数据处理、描述统计表2、VIF表3开头 | 04、08 |
| 11—12 | VIF续、基准表4、稳健表5开头 | 05、06、08 |
| 13—14 | 表5续、机制表6、产权解释 | 06、07、08、09 |
| 15—16 | 现金流解释、表7、结论 | 08、09、10 |
| 17 | 管理与政策讨论 | 09 |
| 18—20 | 参考文献 | 本篇与原文对照 |

## 二、正式发表记录与个人贡献

正式题名：*CEO financial background and corporate financialization*。

作者：Dan Kang、Jiahao Xu、Qiye Tong、Jiayan Li。期刊：*Finance Research Letters*，71，106382，正式卷期2025年1月。

来源：[出版社页面](https://www.sciencedirect.com/science/article/pii/S1544612324014119)｜[DOI入口](https://doi.org/10.1016/j.frl.2024.106382)｜[Crossref登记](https://api.crossref.org/works/10.1016/j.frl.2024.106382)。登记原始响应已保存于附件，便于区分正式出版日期与DOI创建时间。

发表版CRediT把Jiahao Xu列入Data curation、Formal analysis、Methodology、Validation、Writing – review & editing；用途仅是确认贡献类别，不将其扩展为全部操作独立完成。

查阅时间：2026-10-25。可见页面包含摘要、部分正文和贡献声明，本次未取得正式版完整PDF。所有原表精确数字以用户上传稿为来源；未核验特定年份SSCI／JCR或中科院分区。

## 三、用于解释方法的外部资料

| 来源 | 本次用途 | 边界 |
| --- | --- | --- |
| [Stata：xtreg](https://www.stata.com/manuals/xtxtreg.pdf) | 固定效应与面板推断的基本区分 | 不据此声称原研究使用某个具体命令 |
| [Stata：teffects psmatch](https://www.stata.com/manuals/causalteffectspsmatch.pdf) | 匹配与可观测选择的基本含义 | 不证明原稿已完成平衡或DID |
| [Stata：mediate](https://www.stata.com/manuals/causalmediate.pdf) | 区分路径回归与因果中介 | 不把当前工具当作当年已采用的方法 |
| [Hadlock与Pierce：New Evidence on Measuring Financial Constraints](https://doi.org/10.1093/rfs/hhq009) | SA指标由规模年龄信息构造的原始方法背景 | 未从当前投稿稿恢复实际SA代码 |
| [Monetary Policy, Corporate Finance, and Investment](https://academic.oup.com/jeea/article/21/6/2586/7080145) | 补充SA公式和资产单位／截断的重要性 | 是另一研究的具体应用，不代替本文构造说明 |

外部资料只辅助解释统计概念，原论文结果、引用和工作贡献仍分别以相应原始来源为准。

## 四、原稿中值得回读的参考文献

以下来自用户PDF的参考文献表，**本次没有逐篇精读全部文献**。除了上表已查阅的特定方法资料，其余仅列作后续阅读线索，不声称已验证其中每项方法和结论。

- Hambrick与Mason(1984)：高阶梯队理论。原稿正文写2004，与参考表1984不同，后续应核对引用。
- Marquis与Tilcsik(2013)：Imprinting: towards a multilevel theory。帮助厘清“烙印”而非“污名／品牌”。
- Baron与Kenny(1986)：中介与调节变量区别，原稿三步法来源。
- Hadlock与Pierce(2010)：金融约束测量，SA指标背景。
- Kramer与Liao(2016)：The spillover effects of management overconfidence on analyst forecasts。原稿将其作为OC构造依据之一，具体是否支持该残差构造需回读原文。
- Lun(2022)：CEO金融背景、公司绩效与实体企业金融化。适合评估本研究相对既有文献的增量。
- Oradi等(2020)：CEO金融背景与内部控制缺陷。适合比较金融背景的定义与履历测量。
- Liu等(2020)：金融背景高管与创新投入、产出的挤出效应。应区分其研究对象与本文CEO／金融化设定。

稿件参考表有Jiang等(2022)条目重复，正文有书签错误及部分年份不一致。这些保留在原页，不据此猜测其他文献内容。

## 五、本次实际完成的精读过程

1. 提取20页文本并渲染为逐页图像，对照全页总览及关键模型、变量、结果页。
2. 按问题、理论、设计、测量、结果、机制与结论建立阅读路线。
3. 拆解双向固定效应、系数单位、三步中介、PSM与DID、组间差检验。
4. 将变量表和数值表完整转录，保留原t值、星号、N与R²；将160个非空回归系数和t值逐一与来源页文本核对。
5. 区分投稿稿与发表页可见内容，按CRediT还原第二作者贡献范围。
6. 建立复现路线、待确认清单、复述提纲和24道自测题。
7. 检查16篇笔记的102处内部链接、34个展示公式、20页附件图像及PDF副本完整性；在Obsidian中抽查数学、表格和流程图，修正星号被Markdown误解析的显示问题。

上述转录和教学计算不等于取得原始样本后的回归复现。未完成的原始数据、代码与正式全文核对，已在相关笔记明确列出。
