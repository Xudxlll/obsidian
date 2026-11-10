# 量化交易入门指南：第12天 - 价值因子与动量因子的本质逻辑

**学习时间：60分钟**

> 本文为量化交易学习系列第12天内容，深度剖析低市盈率（价值因子）和动量因子的长期有效性、背后逻辑、实证研究与实战应用，帮助你理解现代多因子投资的核心。

---

## 一、为什么低市盈率（PE）的股票长期表现更好？——价值因子的本质逻辑

### 1. 从实证数据来看：价值因子是有效的

- 学术研究（如 Fama-French 三因子模型）和实践经验都发现：
    

- 低 PE（或低 PB、低EV/EBITDA） 的股票，在长期内平均收益率高于高估值股票。
    
- 这构成了"价值因子"（Value Factor）策略的核心：买入低估值、卖出高估值的股票组合，获取超额收益。
    

> **但关键问题是——为什么会这样？**

---

### 2. 三种主流解释

#### 1 风险补偿理论（Risk-Based View）

- 代表人：Fama-French
    
- "价值股"其实风险更高，所以投资者需要获得更高的预期收益作为补偿。
    
- 低 PE 的股票通常处于困境、行业周期底部、或财务恶化状态，未来不确定性大，市场给出低估值。
    
- 长期来看，这些股票平均会给出更高的收益，作为承担更高风险的补偿。
    

**举例：**煤炭股在行业周期底部时，PE 可能只有 3~5 倍，但如果周期反转，利润暴涨，股价上涨可翻倍。

#### 2 行为偏差理论（Behavioral View）

- 代表人：Lakonishok, Shleifer, Vishny 等
    
- 市场存在系统性错误定价，投资者的"行为偏差"造成了价值股被低估。
    
- 投资者倾向于追捧"故事股"、成长股，低 PE 的股票往往"不性感"，被市场忽视，导致低估。
    
- 聪明的价值投资者通过"逆向操作"获取超额收益。
    

**举例：**很多人喜欢买新能源、科技、AI，但不屑于钢铁、水泥、银行等"低 PE 候选"，造成定价偏差。

#### 3 坏消息过度反应 + 坏消息均值回归

- 当公司出现坏消息（盈利下滑、丑闻等）时，PE 会很低，投资者往往反应过度，导致价格过度下跌。
    
- 但很多公司经营稳健，有一定的恢复力，一旦恢复盈利，估值回升，股价上涨。
    

**举例：**某公司今年利润断崖式下跌，PE 变得很低，但如果只是暂时因素（如疫情、原材料暴涨），明年恢复盈利就可能股价翻倍。

---

### 3. 现实中你该怎么用价值因子？

- 单独看 PE 不够，要结合多维因子选股：
    

- 综合使用 PE、PB、EV/EBITDA、股息率等构建"价值得分"；
    
- 排除掉"伪价值股"（坏账、高负债、僵尸企业）；
    
- 与"质量因子"搭配（选低估 + 高质量）；
    
- 长期持有 + 分散组合 → 获得更稳健的超额收益。
    

---

### 4. 小结：价值因子的三大解释

|理论视角|解释为什么低 PE 股票表现更好|
|---|---|
|风险补偿理论|价值股风险更高，收益也更高（是应得的）|
|行为偏差理论|市场错误定价 + 投资者偏好成长，低估价值股|
|情绪均值回归|坏消息后股价过度反应，后续均值回归反弹|

> 这些理论可以互补解释低 PE 有效性的现象。

---

## 二、动量因子（Momentum Factor）：强者恒强的市场逻辑

### 1. 动量因子的基本定义

- 动量因子：过去表现好的股票未来一段时间内往往还会继续上涨，反之亦然。
    
- 常见定义：过去 3~12个月的收益率（常用过去12个月剔除最近1个月）；选取收益率排名靠前的一组股票（如前20%）构建"动量组合"。
    
- 实证研究发现：无论在美股、A股、欧洲、日本等市场，动量因子都显著存在，是多因子模型（如 Carhart 四因子模型）中的核心因子之一。
    

---

### 2. 为什么动量有效？（动量因子的本质逻辑）

#### 1 行为金融学解释（最主流）

- 动量是市场参与者的非理性行为导致的价格惯性。
    
- 主要包括两类心理偏差：
    

- **信息反应不足（Underreaction）**：投资者对利好消息反应缓慢，价格会缓慢上涨一段时间，形成"上涨的惯性"。
    
- **羊群效应（Herding）与趋势跟随**：投资者喜欢追涨杀跌，技术派交易员根据趋势建仓，趋势形成后吸引更多人跟进，趋势被自我强化。
    

#### 2 风险补偿理论（较弱的解释）

- 动量股票可能存在某种未被观测到的风险敞口，长期收益高是对特定风险的补偿。
    
- 但这种解释经常难以成立，因为动量组合的夏普比率很高，波动率不高。
    

#### 3 市场结构机制（交易摩擦 + 投资限制）

- 某些大机构因合规限制、持仓限制、再平衡机制无法立刻调整，信息影响在价格中"延迟显现"，造成动量效应。
    

---

### 3. 动量策略如何构建？

- 典型动量选股流程：
    

1. 对所有股票计算过去12个月收益率（剔除最近1个月）；
    
2. 按收益率从高到低排序，选前20%股票为"高动量组合"；
    
3. 每月或每季度进行再平衡；
    
4. 对组合进行等权/市值权重投资；
    

- 动量还可以分为：
    

- **绝对动量**：某资产自己过去涨 → 未来可能还涨；
    
- **相对动量**：资产A涨得比资产B多 → 未来更可能继续强势。
    

---

### 4. 动量策略的风险与陷阱

|风险|说明|
|---|---|
|反转效应|短期动量可能遭遇突发事件而迅速反转|
|回撤较大|动量策略在"市场风格突变"时会遭遇集体性失效|
|高换手、高交易成本|频繁调仓造成滑点和交易费用|
|与价值因子冲突|高动量股票往往估值也高，和价值因子"天然对立"|

---

### 5. 动量因子的现实应用

- AQR、Two Sigma、Renaissance 等量化基金，都大量使用动量因子，但通常会：
    

- 将动量因子与价值、质量、波动率等多因子结合；
    
- 优化组合风险、提升稳定性；
    
- 控制换手率、降低交易成本。
    

---

### 6. 小结：动量因子的核心特性

|特性|动量因子|
|---|---|
|定义|过去表现好的股票未来更容易继续表现好|
|理论解释|投资者行为偏差 + 信息反应延迟|
|策略方向|顺势而为、买强卖弱|
|风险|短期反转、高换手、风格切换回撤|
|应用方式|常与其他因子组合构建稳健策略|

---

---

## 三、补充：PCA主成分分析的详细计算过程

在上一篇文章中，我们介绍了主成分分析（PCA）作为多因子降维的重要工具，但由于篇幅限制，没有给出详细的计算过程。今天我们来补充这部分内容，帮助大家更好地理解PCA的数学原理和实际应用。

### 1. PCA基本概念回顾

**主成分分析（Principal Component Analysis, PCA）**是一种统计降维技术，其核心思想是：

- 将多个相关的变量（因子）转换为少数几个不相关的主成分
    
- 每个主成分都是原始变量的线性组合
    
- 主成分按照解释方差的大小排序，第一个主成分解释最多的方差
    

**在量化投资中的应用价值：**

- 解决因子冗余问题：PE、PB、EV/EBITDA等估值因子高度相关
    
- 降维简化模型：从20+个原始因子提取3-5个主成分
    
- 识别独立风险源：避免虚假分散化，构建更稳健的投资组合
    

---

### 2. PCA详细计算过程：4只股票的3因子分析

让我们通过一个具体的例子来详细讲解PCA的每一步计算。假设我们有4只股票，每只股票有3个因子暴露：市盈率（PE）、净资产收益率（ROE）和动量因子（Momentum）。

#### 第一步：原始数据准备

|股票|PE ()|ROE () %|Momentum ()|
|---|---|---|---|
|股票A|10|15|0.5|
|股票B|12|20|0.7|
|股票C|15|10|-0.2|
|股票D|20|12|0.1|

**目标**：将这三个相关性较高的因子 () 降维融合成1个或2个不相关的综合因子 ()。

#### 第二步：数据标准化

由于三个因子的量纲和尺度完全不同（PE是倍数，ROE是百分比，Momentum是收益率），必须进行标准化。

**公式：**

其中 是均值，是标准差。

**计算各因子的均值和标准差：**

|因子|(均值)|(标准差)|
|---|---|---|
|PE ()|(10+12+15+20)/4 = 14.25|4.03|
|ROE ()|(15+20+10+12)/4 = 14.25|4.03|
|Momentum ()|(0.5+0.7-0.2+0.1)/4 = 0.275|0.35|

**标准化后的数据矩阵 Z：**

例如，股票A的PE标准化：

以此类推，我们得到标准化后的矩阵 Z：

|股票|(PE)|(ROE)|(Momentum)|
|---|---|---|---|
|股票A|-1.055|0.186|0.643|
|股票B|-0.558|1.427|1.214|
|股票C|0.186|-1.055|-1.357|
|股票D|1.427|-0.558|-0.500|

#### 第三步：计算协方差矩阵

对于标准化后的数据，其协方差矩阵 C 实际上就是相关系数矩阵。计算公式为：

因为数据已经标准化，均值为0，所以公式简化为：

其中 （样本数）。

**计算过程示例：**

- **(PE vs PE):**
    
- **(PE vs ROE):**
    
- **(PE vs Momentum):**
    

**最终协方差矩阵 C：**

#### 第四步：计算特征值和特征向量

我们需要解方程：，其中 是特征值，是特征向量。

**特征方程：**

**计算这个3×3矩阵的行列式（过程略，可通过SVD分解或使用计算器），我们得到三个特征值：**

按大小排序： 

将每个特征值 代入方程 ，求解向量 。

#### a) 对于 ：

解方程组：

化简为：

令 ，从前两个方程可以解出 , （过程略）。

得到向量 。

单位化（使其模长为1）：

单位化后的特征向量：

#### b) 对于 ：

同样方法，解得单位化后的特征向量约为：

#### c) 对于 ：

同样方法，解得单位化后的特征向量约为：

**对应的单位化特征向量：**

#### 第五步：主成分解释与选择

**方差解释率计算：**

总方差 = 

- PC1解释方差比例： 
    
- PC2解释方差比例： 
    
- PC3解释方差比例： 
    

前两个主成分（PC1 + PC2）共解释了约 83.3% 的方差，因此我们可以选择降维到2维。

**主成分的经济含义解释：**

**第一主成分 (PC1)：**

- PE (0.645) 有很高的正载荷
    
- ROE (-0.455) 和 Momentum (-0.613) 有较高的负载荷
    

**解释：**这个主成分代表了 "高估值、低质量、负动量" vs "低估值、高质量、正动量" 的风格暴露。PC1得分高的股票是"高估值、低质量、负动量"的股票。

**第二主成分 (PC2)：**

- ROE (-0.735) 和 PE (-0.583) 有很高的负载荷
    
- Momentum (0.347) 有正载荷
    

**解释：**这个主成分代表了 "低估值、高质量、正动量" vs "高估值、低质量、负动量"。PC2得分高的股票是"低估值、高质量、正动量"的优质股票。

#### 第六步：计算主成分得分

将标准化后的原始数据 Z 投影到选定的主成分方向上。

**投影矩阵 W：**

**主成分得分矩阵 Y = Z W**

### 计算股票A的得分：

**PC1得分：**

**PC2得分：**

同理计算所有股票，得到最终的2维主成分得分：

|股票|PC1 Score|PC2 Score|
|---|---|---|
|股票A|-1.159|0.701|
|股票B|-1.343|1.405|
|股票C|1.589|-0.469|
|股票D|0.913|-1.637|

**投资含义解读：**

- **股票B**：PC2得分最高(1.405)，代表"低估值、高质量、正动量"的优质股票
    
- **股票D**：PC2得分最低(-1.637)，代表"高估值、低质量、负动量"的股票
    
- **股票C**：PC1得分最高(1.589)，代表"高估值、低质量、负动量"风格
    
- **股票A**：PC1得分最低(-1.159)，代表"低估值、高质量、正动量"风格
    

---

### 3. PCA在量化投资中的实际应用价值

通过这个详细的PCA计算过程，我们可以看到：

1. **因子降维**：将3个相关因子压缩为2个独立的主成分，保留了83.3%的信息
    
2. **风险识别**：PC1代表"估值-质量-动量"综合风格，PC2代表"优质股票"特征
    
3. **投资决策**：股票B在PC2上得分最高，是典型的"低估值、高质量、正动量"优质股票
    
4. **模型简化**：从复杂的多因子分析简化为二维主成分分析
    

**实际投资中的应用场景：**

- **多因子选股**：从20+个原始因子中提取3-5个主成分进行选股
    
- **风险模型**：构建基于主成分的风险模型，更准确地估计投资组合风险
    
- **风格轮动**：基于主成分得分进行风格轮动策略
    
- **因子择时**：识别不同市场环境下主成分的有效性变化
    

## 总结

现在，你可以在二维平面上以PC1和PC2为轴，将4只股票绘制出来。股票B在PC2上得分最高，代表它是"低估值、高质量、正动量"的典型。股票D在PC2上得分最低，代表其风格相反。这为投资组合的构建和风格分析提供了极其有价值的信息。

通过Python代码实现，读者可以：

1. 验证手工计算的准确性
    
2. 理解每个步骤的具体实现
    
3. 可视化PCA的结果
    
4. 在实际项目中应用这些方法
    

---

### 5. 小结：价值因子、动量因子与PCA的完美结合

通过今天的学习，我们不仅深入理解了价值因子和动量因子的本质逻辑，还通过详细的PCA计算过程，掌握了多因子分析的核心工具。

|分析层次|价值因子|动量因子|PCA主成分分析|
|---|---|---|---|
|**理论基础**|风险补偿/行为偏差|信息反应不足/羊群效应|线性代数/统计降维|
|**应用目标**|识别低估股票|捕捉趋势延续|多因子降维融合|
|**投资策略**|逆向投资|趋势跟随|综合因子投资|
|**风险特征**|长期均值回归|短期反转风险|系统性风险识别|

这三个工具的结合，为构建稳健的多因子投资策略奠定了坚实基础。下一讲我们将进入"因子组合与风格轮动"的世界，敬请期待！

  

暂无评论

**留言 15**

- ![](https://wx.qlogo.cn/mmopen/96oMn0arIyJQtvt8ic1M5ke5DvCkqCkPEkqW5thazQGfGznxsD08hbXxb7hknkQz3U9Gib5kSqiaXq7IdliacKhqn7X39g0GudiaRf33PLJaFZEaEw4kOznbPoe6SczId3uVs/64)
    
    Martin
    
    浙江7月22日
    
    12
    
- ![](https://wx.qlogo.cn/mmopen/N4HWkmwbSVT9VefZ1xUErHnToPibUicgMpib1F2VgiaI8TdH6iaXia6ibujZ6wRd6tlmWibE0OpXiczQ9dLyia60tRvibSX4LjYwpvlhH0pK83PbqmhjkRianjwNS1qBCqOibWsaWCw2k/64)
    
    Vision
    
    广东7月19日
    
    请问针对每一个股票的PCA值算出来以后还是很难配权重，比如我想要暴露特定的风格，但是PCA值代表了多个因子，这样就显得有点混杂，另外PCA1和PCA2有时又在一个股票上体现出矛盾，这个实际应用中，没太理解
    
    ![](https://wx.qlogo.cn/mmhead/N4HWkmwbSVRs6ksens5I0QuEB8zB7LcOkzhicHT8DyxsqhEDdCibGucuq074CPcvhMavhpia041YTo/64)
    
    逻辑与流
    
    作者7月20日
    
    你这个理解是对的。PCA 算出来的 PC1、PC2 本身并不等于“价值因子”“动量因子”这种清晰风格，它只是从一组原始因子里抽出来的统计方向。它的目标是解释方差、压缩信息、去冗余，不是天然帮我们生成一个可解释的投资风格。这也是我现在回头看这篇文章觉得需要修正的地方：当时把 PCA 的“降维能力”和“投资可解释性”说得有点靠近了，实际工程里两者要分开。PCA 可以帮我们理解因子结构，但真正配权还是要回到清晰的投资目标和约束上。
    
    展开
    
    ![](https://wx.qlogo.cn/mmopen/N4HWkmwbSVT9VefZ1xUErHnToPibUicgMpib1F2VgiaI8TdH6iaXia6ibujZ6wRd6tlmWibE0OpXiczQ9dLyia60tRvibSX4LjYwpvlhH0pK83PbqmhjkRianjwNS1qBCqOibWsaWCw2k/64)
    
    Vision
    
    广东7月20日
    
    回复 **逻辑与流**：发现真的是每天一篇，像你学习
    
- ![](https://wx.qlogo.cn/mmopen/CT9RPyOYiaXHBW3fnwadlmCXicOXswm75QdicSayqxiaKoGLIVxEm02nFUOcmiapxWPMA4dlP9tpribeHsUjbN6z4yBGqkJ7NeBdSB1HwdA6aHPvJDybHmLFIFmnwffCAU7RsT/64)
    
    陈康康
    
    福建6月6日
    
    另外一个想问的是，PC1,PC2的特征向量，以及计算出来的score应该不具有可解释性吧？如“股票B在PC2上得分最高，是典型的"低估值、高质量、正动量"优质股票”这个说法，没怎么明白呢
    
    ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    逻辑与流
    
    作者6月6日
    
    你很牛逼啊，指出的问题都非常专业。严格来说，PCA 计算出来的 PC1、PC2 本身只是数学上的主成分方向，以及样本在这些方向上的投影得分，并不天然具有经济含义。
    
    主成分的经济含义通常是研究者根据载荷（Loading）的结构进行人为解释的。例如如果一个主成分主要由 PE、PB 等估值因子构成，我们可能把它解释为“估值风格因子”；如果主要由 ROE、ROA 等质量指标构成，我们可能把它解释为“质量风格因子”。
    
    因此文中“股票B在PC2上得分最高，是典型的低估值、高质量、正动量股票”的表述确实有些过度解释。更严谨的说法应该是：
    
    股票B在第二主成分方向上的投影最大，而这个主成分是否代表‘优质股票’，还需要结合载荷结构和后续因子有效性检验（IC、回测等）来验证。
    
    感谢指出，这也是 PCA 在量化投资中最容易被误解的地方之一。
    
    展开
    
    ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    陈康康
    
    福建6月6日
    
    回复 **逻辑与流**：主要是来请教，感谢解答 ， 文章都写的非常好(ˊᗜˋ*)，正在跟着学习呢
    
    1条回复
    
- ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    陈康康
    
    福建6月6日
    
    ROE (-0.735) 和 PE (-0.583) 有很高的负载荷Momentum (0.347) 有正载荷解释：这个主成分代表了 "低估值、高质量、正动量" vs "高估值、低质量、负动量"。PC2得分高的股票是"低估值、高质量、正动量"的优质股票。
    
    ----------------
    
    这块是不是写错啦？ roe高的负载荷应该指低质量吧？ 还是我理解错了呢(๑•̌.•̑๑)ˀ̣ˀ̣
    
    ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    逻辑与流
    
    作者6月6日
    
    严格按照文中给出的载荷来看，ROE 的系数为 -0.735，因此 PC2 得分越高并不对应 ROE 越高，而是对应 ROE 越低。这里我在解释主成分经济含义时写得不够严谨。
    
    需要注意的是，PCA 特征向量的方向本身可以整体乘以 -1 而不改变结果，因此在实际分析中通常会根据经济含义调整方向后再解释。文章这里给出的载荷和后面的“高质量（高ROE）”解释没有完全对应上，感谢指出，我后续会修正这部分表述。
    
    展开
    
- ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    五更琉璃
    
    上海6月6日
    
    为什么协方差矩阵中自己和自己的相关系数不是1
    
    ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    逻辑与流
    
    作者6月6日
    
    你指出得很对。文章这里的计算口径不够严谨。理论上，如果数据已经标准化，并且标准化与协方差计算采用同一套分母口径，那么协方差矩阵的对角线应该是 1。文中之所以出现 1.165，是因为标准化时用了总体标准差口径，而计算协方差时用了样本协方差口径，导致结果不再严格等于 1。这里应该统一口径后修正为 1。
    
    ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    逻辑与流
    
    作者6月6日
    
    数学基础不错
    
- ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    工作版-罗德鑫-13989719294
    
    浙江2025年9月9日
    
    哭了，好难啊
    
    首评
    
    ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHZpZXdCb3g9IjAgMCA0MCA0MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBjbGlwLXBhdGg9InVybCgjY2xpcDBfNDIyMF8yNjc0KSI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTAgMGg0MHY0MEgweiIvPjxwYXRoIGZpbGw9IiNFREVERUQiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExLjUgMjlhMSAxIDAgMCAxLTEtMXYtLjY4NGMwLS42ODYuNDk4LTEuNDg0IDEuMTE0LTEuNzg1bDUuNjYtMi43NjJjLjgyMS0uNCAxLjAxMi0xLjI4OC40Mi0xLjk5bC0uMzYyLS40MjljLS43MzYtLjg3Mi0xLjMzMi0yLjUtMS4zMzItMy42NFYxNWMwLTIuMjEgMS43OTUtNCA0LTQgMi4yMSAwIDQgMS43OTMgNCA0djEuNzFjMCAxLjE0LS42IDIuNzczLTEuMzMyIDMuNjQybC0uMzYxLjQyOGMtLjU5LjY5OS0uNDA2IDEuNTg4LjQxOSAxLjk5bDUuNjYgMi43NjJjLjYxNS4zIDEuMTE0IDEuMDkzIDEuMTE0IDEuNzg0VjI4YTEgMSAwIDAgMS0xIDFoLTE3eiIgZmlsbD0iIzAwMCIgZmlsbC1vcGFjaXR5PSIuOSIgb3BhY2l0eT0iLjIiLz48L2c+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMF80MjIwXzI2NzQiPjxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik0wIDBoNDB2NDBIMHoiLz48L2NsaXBQYXRoPjwvZGVmcz48L3N2Zz4=)
    
    逻辑与流
    
    作者2025年9月9日
    
    了解个概念就行，很多干这个行业的人也看不懂这些公式
    

已无更多数据

写留言