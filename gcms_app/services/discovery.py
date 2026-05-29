from __future__ import annotations

import json
from pathlib import Path

from .folder_utils import normalize_folder_key
from typing import Iterable

TARGET_REPORTS = ("spike.rp", "initcal.rp")
_MAP_PATH = Path(__file__).resolve().parents[2] / "Json" / "calibration_point_file_map.json"


def _load_calibration_suffixes() -> set[str]:
    """Load the set of valid calibration .D suffixes from the JSON map file."""
    data = json.loads(_MAP_PATH.read_text(encoding="utf-8"))
    return {entry["data_file_key"].lower() for entry in data.get("calibration_points", [])}


def discover_report_files(folder: Path) -> dict[str, object]:
    """Discover spike.rp and initcal.rp files in a .B batch folder and return counts and paths."""
    if not folder.exists():
        raise FileNotFoundError(f"Selected path does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Selected path is not a directory: {folder}")

    grouped: dict[str, list[str]] = {name: [] for name in TARGET_REPORTS}
    d_folder_statuses: list[dict[str, object]] = []
    cal_suffixes = _load_calibration_suffixes()

    for child in folder.iterdir():
        if not child.is_dir():
            continue

        suffix = child.suffix.lower()
        if suffix == ".d":
            is_cal = normalize_folder_key(child.name) in cal_suffixes
            has_spike = _collect_if_exists(child, "spike.rp", grouped) if is_cal else False
            d_folder_statuses.append({"folder_name": child.name, "is_calibration": is_cal, "spike": has_spike})
        elif suffix == ".m":
            _collect_if_exists(child, "initcal.rp", grouped)

    for name in TARGET_REPORTS:
        grouped[name].sort()

    counts = {name: len(grouped[name]) for name in TARGET_REPORTS}
    total = sum(counts.values())
    d_completeness = _build_d_folder_completeness_summary(d_folder_statuses)
    return {"selected_folder": str(folder.resolve()), "counts": counts, "total": total, "files": grouped, "d_folder_completeness": d_completeness}


def _collect_if_exists(folder: Path, expected_name: str, grouped: dict[str, list[str]]) -> bool:
    """Append a file path to a list if the file exists at the given location."""
    expected_lower = expected_name.lower()
    for child in folder.iterdir():
        if child.is_file() and child.name.lower() == expected_lower:
            grouped[expected_lower].append(str(child.resolve()))
            return True
    return False


def _build_d_folder_completeness_summary(d_folder_statuses: list[dict[str, object]]) -> dict[str, object]:
    """Build a per-.D folder report of which required files are present or missing."""
    sorted_statuses = sorted(d_folder_statuses, key=lambda s: str(s["folder_name"]).lower())
    cal_statuses = [s for s in sorted_statuses if s["is_calibration"]]
    return {
        "total_d_folders_scanned": len(sorted_statuses),
        "calibration_d_folders": len(cal_statuses),
        "non_calibration_d_folders": len(sorted_statuses) - len(cal_statuses),
        "missing_spike": sum(1 for status in cal_statuses if not status["spike"]),
        "statuses": sorted_statuses,
    }


def format_discovery_result(result: dict[str, object]) -> str:
    """Format a discovery result dict into a human-readable string summary."""
    lines = [f"Selected folder: {result['selected_folder']}"]
    counts = result["counts"]
    assert isinstance(counts, dict)
    for report_name in TARGET_REPORTS:
        lines.append(f"{report_name}: {counts[report_name]}")
    lines.append(f"total report files found: {result['total']}")

    d_summary = result["d_folder_completeness"]
    assert isinstance(d_summary, dict)
    lines.append("\nD folder completeness:")
    lines.append(f"total .D folders scanned: {d_summary['total_d_folders_scanned']}")
    lines.append(f"calibration .D folders: {d_summary['calibration_d_folders']}")
    lines.append(f"non-calibration .D folders: {d_summary['non_calibration_d_folders']}")
    lines.append(f"missing spike.rp in calibration .D folders: {d_summary['missing_spike']}")
    lines.append("\n.D folder report status:")
    statuses = d_summary["statuses"]
    assert isinstance(statuses, list)
    if not statuses:
        lines.append("  (none)")
    else:
        for status in statuses:
            lines.append(f"  {status['folder_name']} | calibration: {'yes' if status['is_calibration'] else 'no'} | spike: {'yes' if status['spike'] else 'no'}")

    files = result["files"]
    assert isinstance(files, dict)
    for report_name in TARGET_REPORTS:
        lines.append(f"\n{report_name} files:")
        paths: Iterable[str] = files[report_name]
        paths_list = list(paths)
        if not paths_list:
            lines.append("  (none)")
            continue
        for file_path in paths_list:
            lines.append(f"  {file_path}")
    return "\n".join(lines)
