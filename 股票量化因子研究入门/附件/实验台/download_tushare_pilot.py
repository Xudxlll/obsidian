"""获取固定小样本教学数据；不读取、记录或展示账户密钥内容。"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

HERE = Path(__file__).resolve().parent
CONFIG = {
    "purpose": "固定20只股票教学样本；事后人工选样，存在选择和幸存者偏差，不能代表历史A股股票池",
    "start_date": "20230101",
    "end_date": "20251231",
    "assets": ["000001.SZ", "000063.SZ", "000333.SZ", "000651.SZ", "000858.SZ", "002415.SZ", "002594.SZ", "600000.SH", "600009.SH", "600030.SH", "600036.SH", "600104.SH", "600276.SH", "600309.SH", "600519.SH", "600887.SH", "601166.SH", "601318.SH", "601398.SH", "601857.SH"],
    "factor": "-(adjusted_close / adjusted_close.shift(5) - 1)",
    "label": "adjusted_open.shift(-6) / adjusted_open.shift(-1) - 1",
    "train": ["2023-01-01", "2023-12-31"],
    "validation": ["2024-01-01", "2024-12-31"],
    "test": ["2025-01-01", "2025-12-31"],
    "execution": "signal at close; next session open; idealized fills; no historical tradability engine",
    "neutralization": "未获取历史行业与市值，真实小样本不做行业市值中性化",
    "amount_unit": "CNY，daily.amount千元乘1000转换；不是复权金额",
    "signal_direction": "预设反转：数值越大越看好；不得查看测试结果后改向",
    "research_status": "教学试验；非有效Alpha认定、非可交易业绩、非实盘成果",
}


def get_token(env_file: Path | None) -> str:
    token = os.getenv("TUSHARE_TOKEN", "").strip()
    if not token and env_file:
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                if key.strip() == "TUSHARE_TOKEN":
                    token = value.strip().strip("\"").strip("'")
                    break
    if not token:
        raise RuntimeError("未配置 TUSHARE_TOKEN。请使用环境变量，或 --env-file 指向已有本机配置；不要把密钥写进笔记。")
    return token


def fetch(token: str, api: str, params: dict, fields: str, out: Path, records: list) -> pd.DataFrame:
    key = hashlib.sha256(json.dumps([api, params, fields], sort_keys=True).encode()).hexdigest()[:16]
    cache = out / "raw" / f"{api}_{key}.csv"
    meta_path = cache.with_suffix(".metadata.json")
    if cache.exists():
        content_sha = hashlib.sha256(cache.read_bytes()).hexdigest()
        if meta_path.exists():
            cache_meta = json.loads(meta_path.read_text())
            if cache_meta["content_sha256"] != content_sha:
                raise RuntimeError(f"{cache.name} 与缓存元信息哈希不同，请另建快照，不覆盖旧研究。")
        else:
            # 首次版本的旧缓存没有精确请求完成日志，不把读取时间冒充取得时间。
            cache_meta = {"content_sha256": content_sha, "fetched_at": None,
                          "cache_file_written_at": datetime.fromtimestamp(cache.stat().st_mtime, ZoneInfo("Asia/Shanghai")).isoformat(),
                          "time_provenance": "旧缓存缺精确接收日志；文件mtime仅作本地写入时间参考"}
            meta_path.write_text(json.dumps(cache_meta, ensure_ascii=False, indent=2), encoding="utf-8")
        table = pd.read_csv(cache, dtype={"trade_date": str, "cal_date": str, "ts_code": str})
        records.append({"api": api, "params": params, "fields": fields, "rows": len(table), "file": str(cache.relative_to(out)), "cache": True, **cache_meta})
        return table
    payload = {"api_name": api, "token": token, "params": params, "fields": fields}
    for attempt in range(3):
        try:
            req = urllib.request.Request("https://api.tushare.pro", data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=35) as response:
                result = json.load(response)
            break
        except (TimeoutError, urllib.error.URLError):
            if attempt == 2:
                raise RuntimeError(f"{api} 网络请求失败；已成功分段保存在raw，可重跑续传。") from None
            time.sleep(2 * (attempt + 1))
    if result.get("code") != 0:
        # 不回显响应原文，避免服务端错误内容意外带入认证信息。
        raise RuntimeError(f"{api} 返回错误码 {result.get('code')}。请检查官方权限与限频说明；未对权限错误重复请求。")
    data = result.get("data") or {}
    table = pd.DataFrame(data.get("items", []), columns=data.get("fields", []))
    if table.empty:
        raise RuntimeError(f"{api} 返回空表：{params}。停止导出，防止把不完整数据当完整面板。")
    if len(table) >= 6000:
        raise RuntimeError(f"{api} 可能达到行数上限，需要更细分段后再运行。")
    table.to_csv(cache, index=False)
    cache_meta = {"content_sha256": hashlib.sha256(cache.read_bytes()).hexdigest(),
                  "fetched_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
                  "time_provenance": "接口响应完成并写入本地后的日志时间"}
    meta_path.write_text(json.dumps(cache_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    records.append({"api": api, "params": params, "fields": fields, "rows": len(table), "file": str(cache.relative_to(out)), "cache": False, **cache_meta})
    time.sleep(1.35)
    return table


def main() -> None:
    parser = argparse.ArgumentParser(description="获取Tushare固定小样本教学面板，不是历史全市场股票池")
    parser.add_argument("--env-file", type=Path, help="已有本机.env位置，仅用于内存读取密钥")
    parser.add_argument("--output", type=Path, default=HERE / "real_data")
    args = parser.parse_args()
    out = args.output.resolve()
    (out / "raw").mkdir(parents=True, exist_ok=True)
    config_path = out / "pilot_protocol.json"
    if config_path.exists() and json.loads(config_path.read_text()) != CONFIG:
        raise RuntimeError("已有研究协议与当前配置不同。请用新输出目录保存新实验，避免覆盖研究历史。")
    config_path.write_text(json.dumps(CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")
    token = get_token(args.env_file)
    records = []
    now = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat()
    previous = {}
    if (out / "manifest.json").exists():
        previous = json.loads((out / "manifest.json").read_text())
        archive_dir = out / "manifest_history"
        archive_dir.mkdir(exist_ok=True)
        archive_dir.joinpath(now.replace(":", "-") + ".json").write_text(json.dumps(previous, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {"complete": False,
                "first_retrieval_started_at": previous.get("first_retrieval_started_at", previous.get("retrieved_at", now)),
                "run_started_at": now, "protocol": CONFIG, "requests": records,
                "filename_hash_rule": "raw文件名为请求参数哈希；内容SHA256另见每条请求记录",
                "sources": ["https://tushare.pro/document/2?doc_id=27", "https://tushare.pro/document/2?doc_id=28", "https://tushare.pro/document/2?doc_id=26"]}
    try:
        cal = fetch(token, "trade_cal", {"exchange": "SSE", "start_date": CONFIG["start_date"], "end_date": CONFIG["end_date"]}, "exchange,cal_date,is_open", out, records)
        sessions = pd.DataFrame({"date": pd.to_datetime(cal.loc[cal["is_open"].astype(int).eq(1), "cal_date"], format="%Y%m%d").sort_values().dt.strftime("%Y-%m-%d")})
        sessions.to_csv(out / "sessions.csv", index=False)
        parts, adjs = [], []
        for year in range(2023, 2026):
            params = {"ts_code": ",".join(CONFIG["assets"]), "start_date": f"{year}0101", "end_date": f"{year}1231"}
            parts.append(fetch(token, "daily", params, "ts_code,trade_date,open,high,low,close,vol,amount", out, records))
            for number, asset in enumerate(CONFIG["assets"], start=1):
                adjs.append(fetch(token, "adj_factor", {"ts_code": asset, "start_date": f"{year}0101", "end_date": f"{year}1231"}, "ts_code,trade_date,adj_factor", out, records))
                if number % 5 == 0:
                    print(f"{year}年复权因子已取得 {number}/{len(CONFIG['assets'])} 个样本", flush=True)
        daily, adj = pd.concat(parts, ignore_index=True), pd.concat(adjs, ignore_index=True)
        keys = ["trade_date", "ts_code"]
        if daily.duplicated(keys).any() or adj.duplicated(keys).any():
            raise RuntimeError("原始数据有重复主键，需检查，未静默去重。")
        panel = daily.merge(adj, on=keys, how="left", validate="one_to_one")
        if panel["adj_factor"].isna().any():
            raise RuntimeError("有行情缺少当日复权因子，未生成不完整面板。")
        if set(panel["ts_code"]) != set(CONFIG["assets"]):
            raise RuntimeError("返回股票集合不完整，检查接口多代码参数与权限。")
        panel["date"] = pd.to_datetime(panel["trade_date"], format="%Y%m%d").dt.strftime("%Y-%m-%d")
        panel["amount"] = panel["amount"].astype(float) * 1000
        panel["volume_shares"] = panel["vol"].astype(float) * 100
        panel = panel.rename(columns={"ts_code": "asset"})
        panel = panel[["date", "asset", "open", "high", "low", "close", "adj_factor", "amount", "volume_shares"]].sort_values(["date", "asset"])
        if (panel[["open", "close", "adj_factor"]] <= 0).any().any():
            raise RuntimeError("发现非正价格或复权因子，请先检查数据质量。")
        panel.to_csv(out / "panel.csv", index=False)
        expected = len(sessions) * len(CONFIG["assets"])
        manifest.update({"complete": True, "rows": len(panel), "assets": panel.asset.nunique(), "sessions": len(sessions), "missing_grid_cells": expected - len(panel), "panel_sha256": hashlib.sha256((out / "panel.csv").read_bytes()).hexdigest(), "sessions_sha256": hashlib.sha256((out / "sessions.csv").read_bytes()).hexdigest()})
        print(json.dumps({k: manifest[k] for k in ["complete", "rows", "assets", "sessions", "missing_grid_cells"]}, ensure_ascii=False))
    except Exception as exc:
        manifest["failure"] = str(exc)
        raise
    finally:
        (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
