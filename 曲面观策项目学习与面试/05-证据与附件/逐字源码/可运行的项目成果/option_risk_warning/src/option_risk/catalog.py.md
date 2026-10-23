---
tags: [曲面观策, 项目复习]
核查日期: 2026-10-24
---

## 原始文件

[可运行的项目成果/option_risk_warning/src/option_risk/catalog.py](</Users/xuji/Documents/第五届中国研究生金融科技创新大赛/揭榜挂帅-11-曲面观策/可运行的项目成果/option_risk_warning/src/option_risk/catalog.py>)

SHA-256：`6dd174d40b676df187a1356008127a37c838adb8f9e3fd312fb54c7b0de7b5aa`。下方内容逐字保留；教学解释在逐文件笔记中。

<details>
<summary>展开原始全文（长文件建议按函数名搜索）</summary>

````python
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from .config import AgentConfig
from .contracts import ProductOption
from .errors import DataSourceUnavailableError, InvalidProductError
from .io import READ_COLUMNS, contract_product, partition_product


PRODUCT_LABELS = {
    "a": "豆一",
    "ag": "白银",
    "al": "铝",
    "ao": "氧化铝",
    "au": "黄金",
    "b": "豆二",
    "br": "丁二烯橡胶",
    "bu": "沥青",
    "c": "玉米",
    "cs": "玉米淀粉",
    "cu": "铜",
    "eb": "苯乙烯",
    "eg": "乙二醇",
    "fu": "燃料油",
    "i": "铁矿石",
    "jd": "鸡蛋",
    "l": "聚乙烯",
    "lc": "碳酸锂",
    "lh": "生猪",
    "m": "豆粕",
    "ni": "镍",
    "p": "棕榈油",
    "pb": "铅",
    "pg": "液化石油气",
    "pp": "聚丙烯",
    "ps": "多晶硅",
    "rb": "螺纹钢",
    "ru": "天然橡胶",
    "sc": "原油",
    "si": "工业硅",
    "sn": "锡",
    "sp": "纸浆",
    "v": "聚氯乙烯",
    "y": "豆油",
    "zn": "锌",
}

_ARCHIVE_MEMBER = re.compile(
    r"^(?:(?P<root>[^/]+)/)?(?P<archive_path>archive/[^/]+/"
    r"(?P<contract>[A-Za-z]+\d{3,4})/options/"
    r"(?P<year>\d{4})/(?P<month>\d{2})/options_\d{6}\.parquet)\Z"
)
_CONTRACT_PRODUCT = re.compile(r"^([A-Za-z]+)")
_WINDOWS_DRIVE = re.compile(r"^[A-Za-z]:")


def _decode_process_output(value: bytes) -> str:
    for encoding in ("utf-8", "gb18030"):
        try:
            return value.decode(encoding)
        except UnicodeDecodeError:
            continue
    return value.decode(errors="replace")


def _atomic_write_text(path: Path, value: str, *, encoding: str = "utf-8") -> None:
    """Publish a complete text cache without exposing a partially written file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}-",
        suffix=".tmp",
        dir=path.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        temporary.write_text(value, encoding=encoding)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _atomic_write_parquet(frame: pd.DataFrame, path: Path) -> None:
    """Publish a complete Parquet cache using a unique same-directory file."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}-",
        suffix=".parquet.tmp",
        dir=path.parent,
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        frame.to_parquet(temporary, index=False)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


class OptionDataCatalog:
    """Discover products and valid point-in-time snapshots without loading all columns."""

    MANIFEST_VERSION = "v2-safe-posix"
    COMPLETION_MARKER_VERSION = 2
    TIMESTAMP_INDEX_VERSION = "v3-windowed-prior-history"

    def __init__(self, config: AgentConfig):
        self.config = config
        self.config.ensure_directories()
        self._fingerprint: str | None = None
        self._manifest: list[str] | None = None
        self._products: list[ProductOption] | None = None

    @property
    def source_fingerprint(self) -> str:
        if self._fingerprint is not None:
            return self._fingerprint
        hasher = hashlib.sha256()
        archive = self.config.archive_path
        if archive is not None and archive.is_file():
            stat = archive.stat()
            hasher.update(f"{archive.resolve()}|{stat.st_size}|{stat.st_mtime_ns}".encode("utf-8"))
        else:
            root = self.config.data_source
            if not root.exists():
                raise DataSourceUnavailableError(f"数据源不存在：{root}")
            files = sorted(root.rglob("*.parquet")) if root.is_dir() else [root]
            if not files:
                raise DataSourceUnavailableError(f"数据源中未发现Parquet文件：{root}")
            for path in files:
                stat = path.stat()
                hasher.update(
                    f"{path.relative_to(root) if root.is_dir() else path.name}|"
                    f"{stat.st_size}|{stat.st_mtime_ns}".encode("utf-8")
                )
        hasher.update(self.config.config_version.encode("utf-8"))
        self._fingerprint = hasher.hexdigest()[:16]
        return self._fingerprint

    def _directory_files(self) -> list[Path]:
        root = self.config.data_source
        if root.is_file() and root.suffix.lower() == ".parquet":
            return [root]
        if root.is_dir():
            return sorted(path for path in root.rglob("*.parquet") if not path.name.endswith(".bak"))
        return []

    @staticmethod
    def _validate_archive_path(member: str) -> PurePosixPath:
        if not member or "\\" in member or "\x00" in member:
            raise DataSourceUnavailableError(f"压缩包包含不安全路径：{member}")
        if _WINDOWS_DRIVE.match(member) or member.startswith("//"):
            raise DataSourceUnavailableError(f"压缩包包含不安全路径：{member}")
        parts = member.split("/")
        if any(part in {"", ".", ".."} or ":" in part for part in parts):
            raise DataSourceUnavailableError(f"压缩包包含不安全路径：{member}")
        path = PurePosixPath(member)
        if path.is_absolute() or path.as_posix() != member:
            raise DataSourceUnavailableError(f"压缩包包含不安全路径：{member}")
        return path

    @classmethod
    def _validated_archive_member(cls, member: str) -> tuple[PurePosixPath, re.Match[str]]:
        path = cls._validate_archive_path(member)
        match = _ARCHIVE_MEMBER.fullmatch(member)
        if match is None:
            raise DataSourceUnavailableError(f"压缩包包含不安全路径：{member}")
        return path, match

    def _archive_members(self) -> list[str]:
        if self._manifest is not None:
            return self._manifest
        archive = self.config.archive_path
        if archive is None or not archive.is_file():
            self._manifest = []
            return self._manifest
        manifest_dir = self.config.cache_dir / "catalog" / self.source_fingerprint
        manifest_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = manifest_dir / f"archive_members_{self.MANIFEST_VERSION}.json"
        if manifest_path.exists():
            try:
                payload = json.loads(manifest_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                manifest_path.unlink(missing_ok=True)
            else:
                if not isinstance(payload, list) or not all(
                    isinstance(item, str) for item in payload
                ):
                    manifest_path.unlink(missing_ok=True)
                else:
                    for member in payload:
                        self._validated_archive_member(member)
                    self._manifest = sorted(set(payload))
                    return self._manifest
        try:
            completed = subprocess.run(
                ["tar", "-tf", str(archive)],
                check=True,
                capture_output=True,
            )
        except (FileNotFoundError, subprocess.CalledProcessError) as exc:
            raise DataSourceUnavailableError(f"无法读取数据压缩包：{archive}") from exc
        members = []
        for member in _decode_process_output(completed.stdout).splitlines():
            candidate = member[:-1] if member.endswith("/") else member
            self._validate_archive_path(candidate)
            if member.endswith("/"):
                continue
            if _ARCHIVE_MEMBER.fullmatch(member):
                members.append(member)
        self._manifest = sorted(set(members))
        _atomic_write_text(
            manifest_path,
            json.dumps(self._manifest, ensure_ascii=False, indent=2),
        )
        return self._manifest

    @staticmethod
    def _member_product(member: str) -> str | None:
        match = _ARCHIVE_MEMBER.fullmatch(member)
        if match is None:
            return None
        product = _CONTRACT_PRODUCT.match(match.group("contract"))
        return product.group(1).lower() if product else None

    def list_products(self) -> list[ProductOption]:
        if self._products is not None:
            return list(self._products)
        coverage: dict[str, list[pd.Timestamp]] = {}
        for path in self._directory_files():
            product = partition_product(path)
            if product:
                coverage.setdefault(product, [])
                month_match = re.search(r"[\\/](\d{4})[\\/](\d{2})[\\/]", str(path))
                if month_match:
                    coverage[product].append(
                        pd.Timestamp(f"{month_match.group(1)}-{month_match.group(2)}-01")
                    )
        for member in self._archive_members():
            product = self._member_product(member)
            match = _ARCHIVE_MEMBER.fullmatch(member)
            if product and match:
                coverage.setdefault(product, []).append(
                    pd.Timestamp(f"{match.group('year')}-{match.group('month')}-01")
                )
        if not coverage:
            raise DataSourceUnavailableError("数据源中未识别到任何期权品种")
        self._products = [
            ProductOption(
                code=product,
                label=f"{product} {PRODUCT_LABELS.get(product, product.upper())}",
                start=min(months) if months else None,
                end=max(months) if months else None,
            )
            for product, months in sorted(coverage.items())
        ]
        return list(self._products)

    def _validate_product(self, product: str) -> str:
        normalized = product.lower().strip()
        available = {item.code for item in self.list_products()}
        if normalized not in available:
            raise InvalidProductError(
                f"品种 {product!r} 不存在；可用品种：{', '.join(sorted(available))}"
            )
        return normalized

    @staticmethod
    def _completion_marker(root: Path, product: str) -> Path:
        return root / ".complete" / f"{product}.json"

    @classmethod
    def _expected_archive_paths(cls, members: list[str], base: Path) -> list[Path]:
        paths = []
        for member in members:
            archive_path, _ = cls._validated_archive_member(member)
            paths.append(base.joinpath(*archive_path.parts))
        return paths

    @classmethod
    def _completed_product_files(
        cls,
        root: Path,
        product: str,
        members: list[str],
    ) -> list[Path]:
        marker = cls._completion_marker(root, product)
        if marker.is_symlink() or not marker.is_file():
            return []
        try:
            payload = json.loads(marker.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return []
        if not isinstance(payload, dict):
            return []
        records = payload.get("members")
        if payload.get("version") != cls.COMPLETION_MARKER_VERSION:
            return []
        if not isinstance(records, list) or len(records) != len(members):
            return []
        root_resolved = root.resolve()
        files = cls._expected_archive_paths(members, root)
        for member, record, path in zip(members, records, files, strict=True):
            if not isinstance(record, dict) or set(record) != {"path", "size"}:
                return []
            size = record.get("size")
            if record.get("path") != member or type(size) is not int or size < 0:
                return []
            if path.is_symlink() or not path.is_file():
                return []
            if not path.resolve().is_relative_to(root_resolved):
                return []
            try:
                if path.stat().st_size != size:
                    return []
                pq.ParquetFile(path).metadata
            except Exception:
                return []
        return sorted(files)

    @classmethod
    def _write_completion_marker(
        cls,
        root: Path,
        product: str,
        members: list[str],
    ) -> None:
        marker = cls._completion_marker(root, product)
        marker.parent.mkdir(parents=True, exist_ok=True)
        files = cls._expected_archive_paths(members, root)
        records = [
            {"path": member, "size": path.stat().st_size}
            for member, path in zip(members, files, strict=True)
        ]
        _atomic_write_text(
            marker,
            json.dumps(
                {"version": cls.COMPLETION_MARKER_VERSION, "members": records},
                ensure_ascii=False,
                indent=2,
            ),
        )

    @classmethod
    def _migrate_legacy_product_cache(
        cls,
        root: Path,
        product: str,
        members: list[str],
    ) -> list[Path]:
        if not root.is_dir():
            return []
        expected = set(members)
        existing = [
            path
            for path in root.rglob("*.parquet")
            if partition_product(path) == product
        ]
        actual = {path.relative_to(root).as_posix() for path in existing}
        if actual != expected:
            return []
        root_resolved = root.resolve()
        for path in existing:
            if path.is_symlink() or not path.is_file():
                return []
            if not path.resolve().is_relative_to(root_resolved):
                return []
            try:
                pq.ParquetFile(path).metadata
            except Exception:
                # A legacy cache is optional; any unreadable footer makes it a miss.
                return []
        cls._write_completion_marker(root, product, members)
        return cls._completed_product_files(root, product, members)

    @staticmethod
    def _selection_patterns(members: list[str]) -> list[str]:
        patterns: list[str] = []
        for member in members:
            match = _ARCHIVE_MEMBER.fullmatch(member)
            assert match is not None
            suffix = match.group("archive_path")
            if not suffix.isascii():
                raise DataSourceUnavailableError(f"压缩包成员的选择路径非ASCII：{member}")
            patterns.append(f"*/{suffix}" if match.group("root") else suffix)
        return list(dict.fromkeys(patterns))

    @classmethod
    def _validate_staged_files(cls, staging: Path, members: list[str]) -> list[Path]:
        expected = set(members)
        staged = sorted(staging.rglob("*.parquet"))
        actual = {path.relative_to(staging).as_posix() for path in staged}
        if actual != expected:
            missing = sorted(expected - actual)
            unexpected = sorted(actual - expected)
            raise DataSourceUnavailableError(
                f"压缩包提取结果与精确清单不一致："
                f"missing={missing}, unexpected={unexpected}"
            )
        staging_resolved = staging.resolve()
        for path in staged:
            if path.is_symlink() or not path.is_file():
                raise DataSourceUnavailableError(f"压缩包提取产生不安全文件：{path}")
            if not path.resolve().is_relative_to(staging_resolved):
                raise DataSourceUnavailableError(f"压缩包提取产生越界文件：{path}")
            try:
                pq.ParquetFile(path).metadata
            except Exception as exc:
                raise DataSourceUnavailableError(
                    f"压缩包提取产生不可读Parquet文件：{path}"
                ) from exc
        return staged

    @classmethod
    def _publish_staged_product(
        cls,
        staging: Path,
        root: Path,
        product: str,
        members: list[str],
    ) -> list[Path]:
        staged = cls._validate_staged_files(staging, members)
        root.mkdir(parents=True, exist_ok=True)
        root_resolved = root.resolve()
        for source in staged:
            relative = source.relative_to(staging)
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.parent.resolve().is_relative_to(root_resolved):
                raise DataSourceUnavailableError(f"压缩包发布路径越界：{target}")
            os.replace(source, target)

        cls._write_completion_marker(root, product, members)
        completed = cls._completed_product_files(root, product, members)
        if not completed:
            raise DataSourceUnavailableError(f"品种 {product} 提取结果无法通过完成校验")
        return completed

    def _ensure_product_extracted(self, product: str) -> list[Path]:
        archive = self.config.archive_path
        if archive is None or not archive.is_file():
            return []
        root = self.config.cache_dir / "extracted" / self.source_fingerprint
        manifest = self._archive_members()
        for member in manifest:
            self._validated_archive_member(member)
        members = sorted(
            member for member in manifest if self._member_product(member) == product
        )
        if not members:
            return []
        marker = self._completion_marker(root, product)
        marker_existed = marker.is_file() or marker.is_symlink()
        completed = self._completed_product_files(root, product, members)
        if completed:
            return completed
        marker.unlink(missing_ok=True)
        if not marker_existed:
            migrated = self._migrate_legacy_product_cache(root, product, members)
            if migrated:
                return migrated

        root.mkdir(parents=True, exist_ok=True)
        staging_parent = root / ".staging"
        staging_parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=f"{product}-", dir=staging_parent))
        selection_path = staging / ".members.txt"
        selection_path.write_text(
            "\n".join(self._selection_patterns(members)) + "\n",
            encoding="ascii",
        )
        try:
            subprocess.run(
                [
                    "tar",
                    "-xf",
                    str(archive),
                    "-C",
                    str(staging),
                    "-T",
                    str(selection_path),
                ],
                check=True,
                capture_output=True,
            )
        except FileNotFoundError as exc:
            raise DataSourceUnavailableError("系统未找到可读取RAR的tar/bsdtar命令") from exc
        except subprocess.CalledProcessError as exc:
            detail = _decode_process_output(exc.stderr).strip() if exc.stderr else ""
            suffix = f"：{detail}" if detail else ""
            raise DataSourceUnavailableError(
                f"无法为品种 {product} 提取Parquet数据{suffix}"
            ) from exc
        else:
            return self._publish_staged_product(staging, root, product, members)
        finally:
            shutil.rmtree(staging, ignore_errors=True)

    def product_files(
        self,
        product: str,
        start: pd.Timestamp | None = None,
        end: pd.Timestamp | None = None,
    ) -> list[Path]:
        product = self._validate_product(product)
        files = [path for path in self._directory_files() if partition_product(path) == product]
        if not files:
            files = self._ensure_product_extracted(product)
        if start is None and end is None:
            return sorted(files)
        selected: list[Path] = []
        for path in files:
            match = re.search(r"[\\/](\d{4})[\\/](\d{2})[\\/]", str(path))
            if match is None:
                selected.append(path)
                continue
            month_start = pd.Timestamp(f"{match.group(1)}-{match.group(2)}-01")
            month_end = month_start + pd.offsets.MonthEnd(1) + pd.Timedelta(days=1)
            if start is not None and month_end <= pd.Timestamp(start):
                continue
            if end is not None and month_start > pd.Timestamp(end):
                continue
            selected.append(path)
        return sorted(selected)

    def _timestamp_cache_path(self, product: str) -> Path:
        path = self.config.cache_dir / "catalog" / self.source_fingerprint
        path.mkdir(parents=True, exist_ok=True)
        signature = {
            "lookback_calendar_days": self.config.lookback_calendar_days,
            "pipeline_config": self.config.pipeline_config(product).to_dict(),
        }
        digest = hashlib.sha256(
            json.dumps(signature, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()[:16]
        return path / (
            f"{product}_timestamps_{self.TIMESTAMP_INDEX_VERSION}_{digest}.parquet"
        )

    def _build_timestamp_index(self, product: str) -> pd.DataFrame:
        config = self.config.pipeline_config(product)
        node_parts: list[pd.DataFrame] = []
        catalog_columns = [
            "timestamp",
            "contract",
            "underlying",
            "option_type",
            "strike",
            "open",
            "high",
            "low",
            "close",
            "open_interest",
            "suspend_flag",
            "iv",
            "delta",
            "gamma",
            "theta",
            "vega",
            "dte",
            "moneyness",
        ]
        numeric_columns = [
            "strike",
            "open",
            "high",
            "low",
            "close",
            "open_interest",
            "suspend_flag",
            "iv",
            "delta",
            "gamma",
            "theta",
            "vega",
            "dte",
            "moneyness",
        ]
        for path in self.product_files(product):
            schema = set(pq.ParquetFile(path).schema_arrow.names)
            # ``read_option_files`` rejects a partition missing any production
            # column, so the UI catalog must reject it too.
            if not set(READ_COLUMNS).issubset(schema):
                continue
            frame = pq.ParquetFile(path).read(columns=catalog_columns).to_pandas()
            frame["datetime"] = pd.to_datetime(
                frame["timestamp"].astype("string"), format="%Y%m%d%H%M%S", errors="coerce"
            )
            for column in numeric_columns:
                frame[column] = pd.to_numeric(frame[column], errors="coerce")
            frame["option_type"] = frame["option_type"].astype("string").str.lower()
            valid = frame[[
                "datetime",
                "contract",
                "underlying",
                "option_type",
                *numeric_columns,
            ]].notna().all(axis=1)
            valid &= contract_product(frame["contract"]).eq(product)
            valid &= frame["option_type"].isin(["call", "put"])
            valid &= frame["suspend_flag"].eq(0)
            valid &= (
                frame["strike"].gt(0)
                & frame["close"].ge(0)
                & frame["high"].ge(frame["low"])
                & frame["open"].between(frame["low"], frame["high"], inclusive="both")
                & frame["close"].between(frame["low"], frame["high"], inclusive="both")
            )
            valid &= frame["iv"].between(config.iv_min, config.iv_max, inclusive="both")
            valid &= frame["delta"].between(-1.0001, 1.0001, inclusive="both")
            valid &= frame["gamma"].ge(0) & frame["vega"].ge(0)
            valid &= frame["dte"].between(config.min_dte, config.max_dte, inclusive="both")
            valid &= frame["moneyness"].between(
                config.min_moneyness, config.max_moneyness, inclusive="both"
            )
            valid &= ~np.isclose(
                frame["iv"],
                config.iv_solver_floor,
                atol=config.iv_floor_tolerance,
                rtol=0,
            )
            log_moneyness = np.log(frame["moneyness"].clip(lower=1e-9))
            is_atm = log_moneyness.abs().le(config.atm_log_band)
            surface_eligible = (
                is_atm
                | ((log_moneyness < -config.atm_log_band) & frame["option_type"].eq("put"))
                | ((log_moneyness > config.atm_log_band) & frame["option_type"].eq("call"))
            )
            valid_frame = frame.loc[valid & surface_eligible].copy()
            if valid_frame.empty:
                continue
            valid_frame["is_atm"] = is_atm.loc[valid_frame.index].to_numpy()
            nodes = (
                valid_frame.groupby(
                    ["datetime", "underlying", "dte", "strike"],
                    observed=True,
                    as_index=False,
                )["is_atm"]
                .max()
            )
            node_parts.append(nodes)
        if not node_parts:
            return pd.DataFrame(columns=["datetime", "quote_count", "expiry_count"])
        nodes = (
            pd.concat(node_parts, ignore_index=True)
            .groupby(
                ["datetime", "underlying", "dte", "strike"],
                observed=True,
                as_index=False,
            )["is_atm"]
            .max()
        )
        per_expiry = (
            nodes.groupby(["datetime", "dte"], observed=True)
            .size()
            .rename("node_count")
            .reset_index()
        )
        usable_expiries = per_expiry.loc[per_expiry["node_count"].ge(3), ["datetime", "dte"]]
        usable_nodes = nodes.merge(usable_expiries, on=["datetime", "dte"], how="inner")
        summary = usable_nodes.groupby("datetime", observed=True).agg(
            quote_count=("strike", "size"),
            expiry_count=("dte", "nunique"),
            atm_node_count=("is_atm", "sum"),
        )
        summary = summary.loc[
            summary["quote_count"].ge(config.min_quotes_per_snapshot)
            & summary["expiry_count"].ge(config.min_expiries_per_snapshot)
            & summary["atm_node_count"].ge(1)
        ].sort_index()
        if summary.empty:
            return pd.DataFrame(columns=["datetime", "quote_count", "expiry_count"])
        timestamps = pd.DatetimeIndex(summary.index)
        window_start = timestamps - pd.Timedelta(days=self.config.lookback_calendar_days)
        first_in_window = np.searchsorted(
            timestamps.asi8,
            window_start.asi8,
            side="left",
        )
        strictly_earlier_count = np.arange(len(timestamps)) - first_in_window
        eligible = strictly_earlier_count >= config.min_history_bars
        return summary.loc[eligible].reset_index(names="datetime")

    def list_timestamps(self, product: str) -> pd.DatetimeIndex:
        product = self._validate_product(product)
        if self.config.archive_path is not None and self.config.archive_path.is_file():
            # A timestamp index is derived from the extracted product cache.  A
            # valid derived index must not hide later corruption of its source.
            self.product_files(product)
        cache_path = self._timestamp_cache_path(product)
        if cache_path.exists():
            try:
                summary = pd.read_parquet(cache_path)
                required = {"datetime", "quote_count", "expiry_count"}
                if not required.issubset(summary.columns):
                    raise ValueError("timestamp cache schema is incomplete")
            except Exception:
                # The directory is derived data. A partial/corrupt cache is a
                # miss and must never make a valid product unusable.
                cache_path.unlink(missing_ok=True)
                summary = self._build_timestamp_index(product)
                _atomic_write_parquet(summary, cache_path)
        else:
            summary = self._build_timestamp_index(product)
            _atomic_write_parquet(summary, cache_path)
        if summary.empty:
            return pd.DatetimeIndex([], name="datetime")
        timestamps = pd.to_datetime(summary["datetime"], errors="coerce").dropna().sort_values()
        return pd.DatetimeIndex(timestamps.unique(), name="datetime")
````

</details>
