---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/dashboard.py>)

SHA-256：`b95e1244d7b3521f05aec00a7617f6291298520fb3afe5b248049b1c9b488f43`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path

import pandas as pd
import streamlit as st

from option_risk.agent import OptionRiskAgent
from option_risk.config import AgentConfig
from option_risk.contracts import AgentResult
from option_risk.errors import OptionRiskAgentError
from option_risk.graph_queries import GraphQueryService, UnknownGraphNodeError
from option_risk.graph_visualization import knowledge_graph_figure
from option_risk.graph_explanation import render_graph_explanation
from option_risk.knowledge_graph import KnowledgeGraphError, graph_from_node_link
from option_risk.knowledge_schema import NodeType
from option_risk.interactive import (
    greeks_figure,
    iv_surface_figure,
    surface_heatmap_figure,
    term_curves_figure,
    timeline_figure,
)


LEVEL_COLORS = {0: "#2E7D32", 1: "#B28704", 2: "#D76500", 3: "#B71C1C"}
PRESET_GRAPH_QUERIES = (
    "为什么是当前预警等级？",
    "最主要的三项直接数据根因是什么？",
    "风险可能如何传导？",
    "可能影响哪些风险维度？",
    "当前结论的数据可信度如何？",
    "查看全部证据路径",
)


@st.cache_resource(show_spinner=False, scope="session")
def _agent_from_environment(
    data_source: str,
    cache_dir: str,
    output_dir: str,
    archive_path: str,
) -> OptionRiskAgent:
    return OptionRiskAgent(
        AgentConfig(
            data_source=Path(data_source),
            cache_dir=Path(cache_dir),
            output_dir=Path(output_dir),
            archive_path=Path(archive_path) if archive_path else None,
        )
    )


def _runtime_paths() -> tuple[str, str, str, str]:
    project_root = Path(__file__).resolve().parents[2]
    return (
        os.environ.get("OPTION_RISK_DATA_SOURCE", str(project_root / "data" / "demo")),
        os.environ.get("OPTION_RISK_CACHE_DIR", str(project_root / "data" / "agent_cache")),
        os.environ.get("OPTION_RISK_OUTPUT_DIR", str(project_root / "outputs" / "demo")),
        os.environ.get("OPTION_RISK_ARCHIVE_PATH", ""),
    )


def _styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {max-width: 1480px; padding-top: 1.5rem; padding-bottom: 3rem;}
        .agent-banner {padding: 1rem 1.2rem; border-radius: 0.75rem; border: 1px solid #D8DEE8;
                       background: #F8FAFD; margin: 0.5rem 0 1rem 0;}
        .risk-card {padding: 1rem 1.2rem; border-radius: 0.75rem; color: white;
                    box-shadow: 0 2px 8px rgba(32,39,51,.12); margin-bottom: 1rem;}
        .reason-card {padding: .7rem .9rem; border-left: 4px solid #E87500;
                      background: #FFF8F0; margin: .45rem 0; border-radius: .25rem;}
        div[data-testid="stMetric"] {background: #F8FAFD; border: 1px solid #E2E7EF;
                                     padding: .7rem; border-radius: .65rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_summary(result: AgentResult) -> None:
    level_color = LEVEL_COLORS[result.alert_level]
    st.markdown(
        f"<div class='risk-card' style='background:{level_color}'>"
        f"<div style='font-size:.9rem;opacity:.9'>OptionRiskAgent 当前判断</div>"
        f"<div style='font-size:1.8rem;font-weight:700'>{result.alert_level}级 · {result.alert_name}</div>"
        f"<div>{result.product} ｜ {result.timestamp:%Y-%m-%d %H:%M:%S}</div></div>",
        unsafe_allow_html=True,
    )
    columns = st.columns(4)
    columns[0].metric("综合风险压力", f"{result.risk_score:.3f}" if result.risk_score is not None else "不可用")
    clean_rate = result.data_quality.get("clean_rate")
    columns[1].metric("清洗后有效率", f"{float(clean_rate):.1%}" if clean_rate is not None else "不可用")
    columns[2].metric("曲面期限数", int(len(result.surfaces["iv"].time_to_expiry)))
    columns[3].metric(
        "标的价格来源",
        "真实期货行情" if result.price_source == "real_futures" else "重构代理",
    )
    if result.price_source != "real_futures":
        st.warning("当前未配置真实期货行情，标的价格和CVaR使用 strike/moneyness 重构代理；代理结果仅用于探索性验证。")


def _render_decision(result: AgentResult) -> None:
    st.markdown(f"### Agent判断：{result.alert_level}级 {result.alert_name}")
    st.caption("原因由当前值、当前时点以前的滚动动态阈值和变化方向生成，不包含知识图谱或交易建议。")
    if result.policy_version:
        policy_hash = (result.policy_parameter_hash or "未记录")[:12]
        transition = result.transition_reason or "未记录"
        st.caption(
            f"决策审计：策略 {result.policy_version} / 参数 {policy_hash} / 状态转换 {transition}"
        )
    st.caption("本时点已新发风险通知" if result.alert_emitted else "当前风险状态延续，本时点未新发通知")
    for reason in result.trigger_reasons:
        st.markdown(f"<div class='reason-card'>{reason.message}</div>", unsafe_allow_html=True)
    with st.expander("数据质量与审计信息"):
        st.json(result.data_quality)


def _render_surfaces(result: AgentResult) -> None:
    st.plotly_chart(iv_surface_figure(result.surfaces["iv"], result.product), width="stretch")
    left, right = st.columns(2)
    with left:
        st.plotly_chart(surface_heatmap_figure(result.surfaces["iv"], result.product), width="stretch")
    with right:
        st.plotly_chart(term_curves_figure(result.surfaces["iv"], result.product), width="stretch")
    st.plotly_chart(greeks_figure(result.surfaces, result.product), width="stretch")


def _feature_column_config() -> dict[str, object]:
    return {
        "当前值": st.column_config.NumberColumn(format="%.6f"),
        "动态阈值": st.column_config.NumberColumn(format="%.6f"),
        "压力倍数": st.column_config.NumberColumn(format="%.3f"),
        "变化率": st.column_config.NumberColumn(format="percent"),
    }


def _render_features(result: AgentResult) -> None:
    records = [asdict(item) for item in result.feature_evidence]
    if not records:
        st.info("当前时点没有可展示的风险特征证据。")
        return
    frame = pd.DataFrame(records).rename(
        columns={
            "group": "特征组",
            "label": "风险特征",
            "current_value": "当前值",
            "reference_value": "动态阈值",
            "pressure_ratio": "压力倍数",
            "change_rate": "变化率",
            "status": "状态",
        }
    )
    frame = frame.sort_values("压力倍数", ascending=False, na_position="last")
    st.dataframe(
        frame[["特征组", "风险特征", "当前值", "动态阈值", "压力倍数", "变化率", "状态"]],
        hide_index=True,
        width="stretch",
        column_config=_feature_column_config(),
    )


def _render_evaluation(result: AgentResult) -> None:
    evaluation = result.evaluation
    if evaluation is None or not evaluation.available:
        st.info("该品种尚未生成连续不少于三个月的离线回测；当前时点分析不受影响。")
        return
    metrics = evaluation.metrics
    test = metrics.get("test_metrics") or {}
    cvar = metrics.get("cvar_backtest") or {}
    model = metrics.get("model") or {}
    config = metrics.get("config") or {}
    test_start = model.get("test_start")
    test_end = config.get("end_date")
    if test_start and test_end:
        st.caption(
            f"固定样本外测试期：{str(test_start)[:10]} 至 {str(test_end)[:10]}；"
            "正式主策略参数在代码中预注册固定；轻量ML对照仅使用测试期之前的训练/验证数据。"
        )
    columns = st.columns(4)
    columns[0].metric("预警精确率", f"{float(test.get('event_precision', 0)):.2%}")
    columns[1].metric("风险事件召回率", f"{float(test.get('event_recall', 0)):.2%}")
    lead = test.get("average_lead_minutes")
    columns[2].metric("平均提前时间", f"{float(lead):.1f}分钟" if lead is not None else "不可用")
    columns[3].metric("多空平均CVaR改善", f"{float(cvar.get('average_improvement_rate', 0)):.2%}")
    st.caption("CVaR为比赛规定的离线评价，不是Agent发出的减仓建议。")
    with st.expander("查看完整回测审计信息"):
        st.json(metrics)


def _preset_query_rows(
    service: GraphQueryService,
    graph_result,
    label: str,
) -> list[dict[str, object]]:
    """Return only one of the fixed, validated graph result views."""
    if label == PRESET_GRAPH_QUERIES[0]:
        return service.paths_to_alert()
    if label == PRESET_GRAPH_QUERIES[1]:
        return service.root_evidence(limit=3)
    if label == PRESET_GRAPH_QUERIES[2]:
        return [path.to_dict() for path in graph_result.active_paths[:3]]
    if label == PRESET_GRAPH_QUERIES[3]:
        return service.possible_consequences()
    if label == PRESET_GRAPH_QUERIES[4]:
        return service.quality_limitations()
    if label == PRESET_GRAPH_QUERIES[5]:
        return [path.to_dict() for path in graph_result.active_paths]
    raise ValueError("Unknown fixed graph query")


def _selected_node_detail(
    service: GraphQueryService, selected_node_id: object
) -> dict[str, object] | None:
    try:
        return service.inspect_node(selected_node_id)
    except UnknownGraphNodeError:
        return None


def _selection_node_id(selection: object) -> object:
    try:
        selection_data = (
            selection["selection"]
            if isinstance(selection, dict)
            else selection.selection
        )
        points = selection_data["points"]
        customdata = points[0]["customdata"] if points else ()
        return customdata[0] if customdata else None
    except (AttributeError, KeyError, IndexError, TypeError):
        return None


def _validated_graph_view(graph_result, result: AgentResult):
    """Validate every graph-owned display field before it reaches Streamlit."""
    service = GraphQueryService(graph_result)
    graph = graph_from_node_link(graph_result.graph_json)
    sections, explanation_text, confidence = render_graph_explanation(
        graph,
        graph_result.active_paths,
    )
    if (
        tuple(sections) != graph_result.explanation_sections
        or explanation_text != graph_result.explanation_text
        or confidence != graph_result.explanation_confidence
    ):
        raise KnowledgeGraphError("知识图谱解释不是当前图的规范渲染")
    warning_rows = [
        data
        for _, data in graph.nodes(data=True)
        if data["node_type"] == NodeType.WARNING_STATE.value
    ]
    if len(warning_rows) != 1:
        raise KnowledgeGraphError("知识图谱缺少唯一 WarningState")
    warning = warning_rows[0]
    if (
        result.product != graph_result.product
        or result.timestamp != graph_result.timestamp
        or result.alert_level != warning["alert_level"]
        or result.alert_name != warning["alert_name"]
        or result.alert_emitted != warning["alert_emitted"]
        or result.risk_score != warning["risk_score"]
        or result.transition_reason != warning["transition_reason"]
        or result.policy_parameter_hash != warning["policy_hash"]
    ):
        raise KnowledgeGraphError("问题一与知识图谱 WarningState 不一致")
    return service, tuple(sections), confidence, warning


def _render_knowledge_graph(result: AgentResult) -> None:
    graph_result = result.knowledge_graph
    if graph_result is None or graph_result.status != "ready":
        st.warning("风险知识图谱暂不可用；其余问题一结果仍可正常查看。")
        return
    try:
        service, sections, confidence, warning = _validated_graph_view(graph_result, result)
    except KnowledgeGraphError as error:
        st.warning(f"风险知识图谱校验未通过：{error}")
        return

    for section in sections:
        st.markdown(f"### {section.title}")
        st.write(section.content)
    graph_key = (
        f"graph_selection_{result.product}_{result.timestamp.strftime('%Y%m%dT%H%M%S')}"
    )
    selection = st.plotly_chart(
        knowledge_graph_figure(graph_result),
        width="stretch",
        on_select="rerun",
        selection_mode="points",
        key=graph_key,
    )
    selected_node_id = _selection_node_id(selection)
    if selected_node_id is not None:
        detail = _selected_node_detail(service, selected_node_id)
        if detail is None:
            st.info("该节点选择已过期，未显示旧事件数据。")
        else:
            st.markdown("#### 选中节点审计")
            st.json(detail)
            edge_audit = [
                edge
                for edge in graph_result.graph_json["edges"]
                if edge.get("source") == selected_node_id
                or edge.get("target") == selected_node_id
            ]
            if edge_audit:
                st.json(edge_audit)

    query_label = st.selectbox(
        "预设图谱查询",
        options=PRESET_GRAPH_QUERIES,
        key=f"graph_query_{result.product}_{result.timestamp.strftime('%Y%m%dT%H%M%S')}",
    )
    if query_label == PRESET_GRAPH_QUERIES[0]:
        st.caption(
            f"当前 WarningState：{warning['alert_level']}级 {warning['alert_name']}；"
            f"状态转换：{warning['transition_reason'] or '未记录'}"
        )
    if query_label == PRESET_GRAPH_QUERIES[4]:
        st.caption(f"当前解释置信度：{confidence}")
    st.json(_preset_query_rows(service, graph_result, query_label))
    with st.expander("完整路径审计"):
        st.json([path.to_dict() for path in graph_result.active_paths])
    with st.expander("全部节点审计"):
        st.json(graph_result.graph_json["nodes"])
    with st.expander("全部边审计"):
        st.json(graph_result.graph_json["edges"])
    with st.expander("缺失证据"):
        st.json(list(graph_result.missing_evidence))


def _render_result(result: AgentResult) -> None:
    _render_summary(result)
    tabs = st.tabs(
        [
            "Agent决策",
            "风险知识图谱",
            "IV与Greeks曲面",
            "风险特征",
            "预警时间轴",
            "离线回测验证",
        ]
    )
    with tabs[0]:
        _render_decision(result)
    with tabs[1]:
        _render_knowledge_graph(result)
    with tabs[2]:
        _render_surfaces(result)
    with tabs[3]:
        _render_features(result)
    with tabs[4]:
        st.plotly_chart(
            timeline_figure(result.timeline, result.timestamp, result.product),
            width="stretch",
        )
    with tabs[5]:
        _render_evaluation(result)


def render_dashboard(agent: OptionRiskAgent) -> None:
    _styles()
    st.title("期权波动率曲面风控智能体")
    st.markdown(
        "<div class='agent-banner'><b>唯一业务Agent：</b>OptionRiskAgent　｜　"
        "输入：品种 + 时间点　｜　输出：曲面、Greeks、风险特征、0—3级预警与原因</div>",
        unsafe_allow_html=True,
    )
    try:
        products = agent.list_products()
    except OptionRiskAgentError as exc:
        st.error(str(exc))
        return
    labels = {item.code: item.label for item in products}
    product = st.selectbox(
        "品种",
        options=[item.code for item in products],
        index=None,
        format_func=lambda value: labels[value],
        placeholder="请选择已有品种",
        accept_new_options=False,
        help="选项完全来自当前数据源，不能输入不存在的品种。",
        key="product_selection",
    )
    previous_product = st.session_state.get("_active_product")
    selection_generation = int(st.session_state.get("_selection_generation", 0))
    if product != previous_product:
        st.session_state["_active_product"] = product
        selection_generation += 1
        st.session_state["_selection_generation"] = selection_generation
        st.session_state.pop("agent_result", None)
        for key in list(st.session_state):
            if key.startswith("graph_selection_") or key.startswith("graph_query_"):
                st.session_state.pop(key, None)

    selected_time_text: str | None = None
    if product is not None:
        try:
            with st.spinner(f"正在读取 {labels[product]} 的有效时间点……"):
                timestamps = agent.list_timestamps(product)
        except OptionRiskAgentError as exc:
            st.error(str(exc))
            return
        options = [timestamp.strftime("%Y-%m-%d %H:%M:%S") for timestamp in timestamps]
        selected_time_text = st.selectbox(
            "时间点",
            options=options,
            index=None,
            placeholder="请选择该品种的有效时间点",
            accept_new_options=False,
            help="仅显示能够形成曲面且具备动态阈值历史的真实时间点。",
            key=f"timestamp_selection_{product}_{selection_generation}",
        )
        if not options:
            st.warning("该品种没有满足曲面与历史要求的可选时间点。")

    analyze_clicked = st.button(
        "开始风险分析",
        type="primary",
        disabled=product is None or selected_time_text is None,
        width="stretch",
    )
    if analyze_clicked and product is not None and selected_time_text is not None:
        try:
            with st.spinner("OptionRiskAgent正在构建曲面、提取特征并进行动态分级……"):
                st.session_state["agent_result"] = agent.analyze(
                    product,
                    pd.Timestamp(selected_time_text),
                )
        except OptionRiskAgentError as exc:
            st.error(str(exc))
            st.session_state.pop("agent_result", None)
    result = st.session_state.get("agent_result")
    if isinstance(result, AgentResult):
        _render_result(result)


def main() -> None:
    st.set_page_config(
        page_title="期权风控智能体",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    render_dashboard(_agent_from_environment(*_runtime_paths()))


if __name__ == "__main__":
    main()
````

</details>
