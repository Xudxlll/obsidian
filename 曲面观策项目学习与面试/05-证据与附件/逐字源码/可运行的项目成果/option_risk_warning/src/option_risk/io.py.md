---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/io.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/io.py>)

SHA-256：`70aaf30c6588f3e4c91b6a7b08570045c3f5be126279a6c96bdb8018b75f4511`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd
import pyarrow.parquet as pq


READ_COLUMNS = [
    "timestamp",
    "contract",
    "underlying",
    "option_type",
    "strike",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "amount",
    "open_interest",
    "settlement_price",
    "pre_close",
    "suspend_flag",
    "iv",
    "delta",
    "gamma",
    "theta",
    "vega",
    "dte",
    "moneyness",
    "moneyness_type",
    "date",
]


def discover_parquet_files(data_dir: str | Path) -> list[Path]:
    root = Path(data_dir)
    if root.is_file() and root.suffix.lower() == ".parquet":
        return [root]
    files = sorted(path for path in root.rglob("*.parquet") if not path.name.endswith(".bak"))
    if not files:
        raise FileNotFoundError(f"No .parquet files found under {root}")
    return files


def contract_product(series: pd.Series) -> pd.Series:
    return series.astype("string").str.extract(r"^([A-Za-z]+)", expand=False).str.lower()


def _available_columns(path: Path) -> set[str]:
    return set(pq.ParquetFile(path).schema_arrow.names)


def partition_product(path: Path) -> str | None:
    for part in reversed(path.parts):
        match = re.fullmatch(r"([A-Za-z]+)\d{3,4}", part)
        if match:
            return match.group(1).lower()
    return None


def read_option_files(
    files: Iterable[Path],
    product: str,
    start_date: str | None = None,
    end_date: str | None = None,
) -> tuple[pd.DataFrame, dict[str, object]]:
    """Read and product-filter files one at a time to contain polluted partitions."""

    product = product.lower()
    files = list(files)
    frames: list[pd.DataFrame] = []
    scanned_rows = 0
    skipped_files: list[str] = []
    schema_variants: dict[str, set[str]] = {}
    partition_skipped = 0
    files_read = 0

    for path in files:
        path_product = partition_product(path)
        if path_product is not None and path_product != product:
            partition_skipped += 1
            continue
        columns = _available_columns(path)
        missing = sorted(set(READ_COLUMNS) - columns)
        if missing:
            skipped_files.append(f"{path}: missing {missing}")
            continue

        table = pq.read_table(path, columns=READ_COLUMNS)
        files_read += 1
        frame = table.to_pandas()
        scanned_rows += len(frame)
        schema_key = ",".join(f"{field.name}:{field.type}" for field in table.schema)
        schema_variants.setdefault(schema_key, set()).add(str(path))

        frame["contract"] = frame["contract"].astype("string")
        frame["underlying"] = frame["underlying"].astype("string")
        frame["product"] = contract_product(frame["contract"])
        frame = frame.loc[frame["product"].eq(product)].copy()
        if frame.empty:
            continue

        frame["datetime"] = pd.to_datetime(
            frame["timestamp"].astype("string"), format="%Y%m%d%H%M%S", errors="coerce"
        )
        if start_date:
            frame = frame.loc[frame["datetime"] >= pd.Timestamp(start_date)]
        if end_date:
            end = pd.Timestamp(end_date) + pd.Timedelta(days=1)
            frame = frame.loc[frame["datetime"] < end]
        if not frame.empty:
            frame["source_file"] = str(path)
            frames.append(frame)

    if not frames:
        raise ValueError(f"No rows for product={product!r} after filtering")

    data = pd.concat(frames, ignore_index=True, sort=False)
    profile = {
        "files_discovered": len(files),
        "files_scanned": files_read,
        "files_skipped_by_partition_product": partition_skipped,
        "rows_scanned": int(scanned_rows),
        "rows_after_product_filter": int(len(data)),
        "skipped_files": skipped_files,
        "schema_variant_count": len(schema_variants),
        "schema_variants": [
            {"schema": schema, "file_count": len(paths), "example": sorted(paths)[0]}
            for schema, paths in schema_variants.items()
        ],
    }
    return data, profile
````

</details>
