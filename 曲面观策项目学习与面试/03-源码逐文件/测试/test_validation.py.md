---
tags: [曲面观策, 逐文件]
核查日期: 2026-10-24
---

## 这份测试文件防什么错误

检查单Agent公开入口和问题一部署验收。

通过可控样本、替身或真实小文件核对品种目录、有效时点、完整五曲面与证据组，以及失败状态的显式呈现。

源文件：[test_validation.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py>)。

## 输入与输出

测试读取临时或明确指定的样本/结果，输出断言的通过或失败。下面列的是测试函数定义数，参数化会展开多个运行用例；不能把函数数当实际测试case数。此文件有11个test函数。

## 逐项合同索引

### `test_public_surface_exposes_exactly_one_business_agent`

[定位第101行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:101>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
summary['agent_classes'] == ['OptionRiskAgent']
summary['passed'] is True
```

### `test_result_validator_enforces_all_problem_one_outputs`

[定位第108行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:108>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
summary['surface_metrics'] == ['delta', 'gamma', 'iv', 'theta', 'vega']
set(summary['feature_groups']) == GROUPS
summary['alert_level'] == 0
summary['alert_emitted'] is False
```

### `test_result_validator_rejects_missing_fifth_feature_group`

[定位第120行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:120>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='质量与流动性')
```

### `test_result_validator_rejects_timeline_level_different_from_current_alert`

[定位第129行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:129>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='时间轴末行预警等级')
```

### `test_result_validator_rejects_timeline_emission_different_from_current_result`

[定位第142行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:142>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match='新发通知')
```

### `test_result_validator_rejects_timeline_identity_different_from_current`

[定位第163行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:163>)。

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
pytest.raises(AssertionError, match=message)
```

### `test_problem_one_validation_public_signatures_remain_exact`

[定位第207行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:207>)。

Catches Problem 2 weakening or renaming the existing Problem 1 API.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
str(inspect.signature(validate_agent_result)) == "(result: 'AgentResult', requested_product: 'str', requested_timestamp: 'pd.Timestamp') -> 'dict[str, Any]'"
str(inspect.signature(validate_deployment)) == "(agent: 'OptionRiskAgent', *, analyze: 'bool' = True, product_codes: 'list[str] | None' = None, progress: 'Callable[[str], None] | None' = None) -> 'dict[str, Any]'"
```

### `test_problem_one_result_summary_keys_and_values_remain_exact`

[定位第220行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:220>)。

Catches Problem 2 changing any established Problem 1 summary field.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
validate_agent_result(_result(), 'ag', pd.Timestamp('2025-04-30 15:00')) == _expected_problem_one_summary()
```

### `test_problem_one_result_identity_error_message_remains_exact`

[定位第229行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:229>)。

Catches Problem 2 changing the established identity failure semantics.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
str(captured.value) == "返回品种'ag'与请求'cu'不一致"
pytest.raises(AssertionError)
```

### `test_problem_one_deployment_report_contract_remains_exact`

[定位第258行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:258>)。

Catches the new deployment validator mutating the old report contract.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
set(report) == {'generated_at', 'mode', 'public_agent_surface', 'summary', 'products'}
pd.Timestamp(report['generated_at']).tzinfo is not None
report['mode'] == 'full'
report['public_agent_surface'] == {'agent_classes': ['OptionRiskAgent'], 'passed': True}
```

### `test_problem_one_deployment_unknown_product_error_remains_exact`

[定位第299行](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/tests/test_validation.py:299>)。

Catches Problem 2 changing old continuation rows or progress errors.

代表断言（代码表达测试合同，不表示本轮已通过）：

```python
report['products'] == [{'product': 'xx', 'status': 'failed', 'error_type': 'AssertionError', 'error': '数据目录不存在品种：xx'}]
report['summary'] == {'status': 'failed', 'product_count': 1, 'passed_products': 0, 'failed_products': 1}
agent.timestamp_calls == []
agent.analyze_calls == []
```

## 复习方法与实际执行状态

先说出该测试想防的错误，再改变一个输入，预测哪个断言会失败。所有当前运行记录集中在[[04-面试与验证/05-本轮验证记录]]；历史文档的751项不能替代本轮实际收集与执行数。
