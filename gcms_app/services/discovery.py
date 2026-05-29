from __future__ import annotations

from pathlib import Path
from typing import Any

from .folder_utils import normalize_folder_key

TARGET_REPORTS = ("target.rp",)


def discover_batch(folder: Path) -> dict[str, Any]:
    """Discover target.rp files in all .D subfolders of a .B batch folder."""
    if not folder.exists():
        raise FileNotFoundError(f"Selected path does not exist: {folder}")
    if not folder.is_dir():
        raise NotADirectoryError(f"Selected path is not a directory: {folder}")

    d_folders: list[dict[str, Any]] = []

    for child in sorted(folder.iterdir(), key=lambda p: p.name.lower()):
        if not child.is_dir() or child.suffix.lower() != ".d":
            continue
        target_rp_path = _find_file(child, "target.rp")
        d_folders.append({
            "folder_name": child.name,
            "folder_path": str(child.resolve()),
            "normalized_key": normalize_folder_key(child.name),
            "target_rp_path": target_rp_path,
            "has_target_rp": target_rp_path is not None,
        })

    with_target = sum(1 for d in d_folders if d["has_target_rp"])
    return {
        "selected_folder": str(folder.resolve()),
        "d_folders": d_folders,
        "total_d_folders": len(d_folders),
        "d_folders_with_target_rp": with_target,
        "d_folders_missing_target_rp": len(d_folders) - with_target,
    }


def _find_file(folder: Path, expected_name: str) -> str | None:
    """Return the resolved path to a file if it exists inside folder, else None."""
    expected_lower = expected_name.lower()
    for child in folder.iterdir():
        if child.is_file() and child.name.lower() == expected_lower:
            return str(child.resolve())
    return None


def format_discovery_result(result: dict[str, Any]) -> str:
    """Format a discovery result dict into a human-readable string summary."""
    lines = [
        f"Selected folder: {result['selected_folder']}",
        f"Total .D folders: {result['total_d_folders']}",
        f"With target.rp:   {result['d_folders_with_target_rp']}",
        f"Missing target.rp: {result['d_folders_missing_target_rp']}",
        "\n.D folder status:",
    ]
    for d in result["d_folders"]:
        status = "OK" if d["has_target_rp"] else "MISSING target.rp"
        lines.append(f"  {d['folder_name']} | {status}")
    return "\n".join(lines)
