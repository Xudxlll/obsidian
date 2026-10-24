---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

检查Agent输入输出合同、品种、时点与完整载荷。

用临时Parquet制造可控源，确认返回曲面、证据、状态、时间轴等字段，并拒绝不合法请求。通过合同只说明结构与行为符合预期，不说明预警有预测能力。

源文件：[test_agent_contracts.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有6个test函数。

## 逐项合同索引

### `test_agent_result_to_dict_serializes_nested_market_data`

[定位第24行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py:24>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
payload['timestamp'] == '2025-04-07T10:15:00'
payload['risk_score'] == 0.98
payload['data_quality']['clean_rate'] == 0.99
payload['surfaces']['iv']['values'][1][1] is None
```

### `test_agent_result_from_dict_accepts_legacy_payload_without_policy_identity`

[定位第92行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py:92>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
restored.policy_version is None
restored.policy_parameter_hash is None
restored.transition_reason is None
restored.alert_emitted is False
```

### `test_knowledge_graph_result_round_trips_inside_agent_result`

[定位第118行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py:118>)。

Catches graph records being lost or made non-JSON-safe in agent cache payloads.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
payload['knowledge_graph']['timestamp'] == '2025-04-07T10:15:00'
payload['knowledge_graph']['active_paths'][0]['edge_ids'] == ['edge_evidence_anomaly', 'edge_anomaly_mechanism', 'edge_mechanism_consequence']
AgentResult.from_dict(payload).to_dict() == payload
payload['knowledge_graph']['error_type'] is None
```

### `test_knowledge_graph_result_accepts_legacy_error_payload_and_round_trips_type`

[定位第181行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py:181>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
restored_legacy.error_type is None
restored_legacy.error_message == 'legacy graph failure'
structured.to_dict()['error_type'] == 'KnowledgeGraphValidationError'
KnowledgeGraphResult.from_dict(structured.to_dict()) == structured
```

### `test_graph_record_contracts_round_trip_json_safe_nested_values`

[定位第204行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py:204>)。

Catches nested node and edge metadata escaping graph serialization.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
GraphNodeRecord.from_dict(node.to_dict()).to_dict() == {'node_id': 'evidence_atm_iv', 'node_type': 'Evidence', 'label': 'ATM隐含波动率', 'properties': {'observed_at': '2025-04-07T10:15:00', 'weights': [0.2, 0.8]}}
GraphEdgeRecord.from_dict(edge.to_dict()).to_dict() == {'edge_id': 'edge_evidence_anomaly', 'source_node_id': 'evidence_atm_iv', 'target_node_id': 'anomaly_atm_iv', 'relation_type': 'EXCEEDS', 'properties': {'pressure': 1.2}}
```

### `test_agent_config_resolves_and_creates_runtime_directories`

[定位第238行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_agent_contracts.py:238>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
config.data_source == (tmp_path / 'data').resolve()
config.cache_dir.is_dir()
config.output_dir.is_dir()
config.pipeline_config('CU').product == 'cu'
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[曲面观策项目学习与面试/04-面试与验证/05-本轮验证记录.md|05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
