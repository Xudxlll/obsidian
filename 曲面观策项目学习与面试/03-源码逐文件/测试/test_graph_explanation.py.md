---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

检验五段解释、路径引用与措辞边界。

向解释器输入可控图，检查每句能回指活动路径、质量限制和非方向性表达。内容安全正则/白名单只是工程护栏，不是数学上的永不误述证明。

源文件：[test_graph_explanation.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有19个test函数。

## 逐项合同索引

### `test_level_zero_without_active_paths_keeps_all_sections_nonempty_and_untraced`

[定位第84行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:84>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
paths == []
all((section.path_ids == () for section in sections))
'AG' in sections[0].content
'2025-04-07 10:15:00' in sections[0].content
```

### `test_near_threshold_watch_uses_dynamic_threshold_wording_and_values`

[定位第105行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:105>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
root.path_ids == (paths[0].path_id,)
root.content.startswith(f'[{paths[0].path_id}]')
'ATM隐含波动率' in root.content
'当前值 0.2' in root.content
```

### `test_watch_held_without_active_path_describes_persistence_not_current_anomaly`

[定位第128行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:128>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
paths == []
all((section.path_ids == () for section in sections))
'当前市场特征已回落' in text
'问题一持续性机制暂时保留' in text
```

### `test_watch_held_with_quality_only_path_still_describes_market_feature_fallback`

[定位第147行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:147>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
paths
all((path.conclusion_node_id.startswith('confidence:') for path in paths))
'当前市场特征已回落' in sections[0].content
'问题一持续性机制暂时保留' in sections[0].content
```

### `test_level_two_renders_three_unique_roots_and_relation_wording`

[定位第167行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:167>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
len(sections[1].path_ids) == 3
len(set(sections[1].path_ids)) == 3
text.count('当前值 0.2') == 3
'超过自身动态阈值' in text
```

### `test_level_three_core_plus_multiple_signals_preserves_formal_warning_state`

[定位第188行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:188>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
'0—3：危险' in sections[0].content
'danger_core_plus_multiple' in sections[0].content
'WarningState' in sections[0].content
'图谱不改变' in sections[0].content
```

### `test_quality_only_path_lowers_confidence_without_raising_market_alert`

[定位第210行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:210>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
'0—3：无预警' in sections[0].content
'降低当前分析置信度' in sections[2].content
'仅降低解释置信度' in sections[4].content
'不代表0—3市场预警等级上调' in sections[4].content
```

### `test_reconstructed_price_is_explicitly_limited_as_a_non_market_proxy`

[定位第227行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:227>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
'行权价/moneyness重构价格代理' in limitation
'不是真实期货市场数据' in limitation
'正式使用时应替换' in limitation
confidence == 'normal'
```

### `test_root_propagation_and_consequence_sentences_are_exactly_traceable`

[定位第243行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:243>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
set(section.path_ids).issubset({path.path_id for path in paths})
```

### `test_renderer_rejects_any_noncanonical_path_sequence`

[定位第263行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:263>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_renderer_validates_graph_before_rendering`

[定位第283行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:283>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(KnowledgeGraphValidationError)
```

### `test_renderer_is_deterministic_and_does_not_mutate_inputs`

[定位第291行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:291>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
first == second
list(graph.nodes(data=True)) == before_nodes
paths == before_paths
```

### `test_multi_quality_reason_order_survives_node_link_round_trip`

[定位第306行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:306>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
original == round_tripped
limitations.index('IV求解下限占比') < limitations.index('曲面节点覆盖缺口')
```

### `test_language_validator_rejects_unsupported_or_trading_language`

[定位第374行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:374>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(UnsafeGraphExplanationError)
```

### `test_language_validator_allows_approved_cautious_or_negative_wording`

[定位第411行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:411>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
validate_explanation_language(text) is None
```

### `test_language_validator_requires_a_string`

[定位第416行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:416>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(TypeError)
```

### `test_language_validator_rejects_uniformly_obfuscated_position_grammar`

[定位第424行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:424>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(UnsafeGraphExplanationError)
```

### `test_language_validator_rejects_positive_bare_action_after_english_negative`

[定位第439行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:439>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(UnsafeGraphExplanationError)
```

### `test_language_validator_rejects_positive_bare_action_after_chinese_negative`

[定位第452行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_graph_explanation.py:452>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(UnsafeGraphExplanationError)
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[曲面观策项目学习与面试/04-面试与验证/05-本轮验证记录.md|05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
