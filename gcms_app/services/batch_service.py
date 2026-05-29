from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

from .initcal_parser import parse_initcal_text
from .spike_parser import parse_spike_text
from .target_parser import parse_target_rp_text
from .response_ratio_service import get_is_area, compute_response_ratio
from .folder_utils import normalize_folder_key
from .qc_service import get_qc_data

DEFAULT_CONCENTRATIONS = [0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 7.5, 10.0]
MAP_PATH = Path(__file__).resolve().parent / "Json" / "calibration_point_file_map.json"
logger = logging.getLogger(__name__)


class CalibrationFolderError(ValueError):
    """Raised when calibration level folders cannot be uniquely matched in the batch."""

    def __init__(self, missing: list[dict], duplicates: list[dict], found_folders: list[str]) -> None:
        self.missing = missing          # [{"level": int, "key": str}, ...]
        self.duplicates = duplicates    # [{"level": int, "key": str, "folders": [str]}, ...]
        self.found_folders = found_folders  # actual .D folder names present
        parts = []
        if missing:
            parts.append(f"{len(missing)} missing level(s): {[m['key'] for m in missing]}")
        if duplicates:
            parts.append(f"{len(duplicates)} ambiguous level(s): {[d['key'] for d in duplicates]}")
        super().__init__("; ".join(parts) if parts else "Calibration folder mismatch")


def validate_batch_folder(batch_path: str) -> dict[str, Any]:
    """Validate that path is a .B folder containing at least one .D and one .m subfolder."""
    path = Path(batch_path)
    if not path.exists() or not path.is_dir():
        return {"valid": False, "error": "Path does not exist or is not a directory."}
    if path.suffix.lower() != ".b":
        return {"valid": False, "error": "Folder must end with .B."}
    has_d = any(child.is_dir() and child.suffix.lower() == ".d" for child in path.iterdir())
    has_m = any(child.is_dir() and child.suffix.lower() == ".m" for child in path.iterdir())
    if not has_d or not has_m:
        return {"valid": False, "error": "Folder must contain at least one .D subfolder and one .m subfolder."}
    return {"valid": True, "error": None, "batch_path": str(path.resolve())}


def _norm(s: str) -> str:
    """Normalize a compound name for fuzzy comparison by lowercasing and stripping non-alphanumeric characters."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _names_match(name_a: str, name_b: str) -> bool:
    """Return True when normalized names are equal or one is a truncation prefix of the other."""
    a, b = _norm(name_a), _norm(name_b)
    return a == b or a.startswith(b) or b.startswith(a)


def get_calibration_data(batch_path: str) -> dict[str, Any]:
    """Load and join initcal and spike data from a batch folder into a structured compound list."""
    batch = Path(batch_path)
    method_folder = next(child for child in batch.iterdir() if child.is_dir() and child.suffix.lower() == ".m")
    initcal = parse_initcal_text((method_folder / "initcal.rp").read_text(encoding="utf-8", errors="ignore"))
    map_json = json.loads(MAP_PATH.read_text())
    level_to_key = {entry["calibration_point"]: entry["data_file_key"] for entry in map_json.get("calibration_points", [])}
    folders_by_key: dict[str, list[Path]] = {}
    for child in batch.iterdir():
        if child.is_dir() and child.suffix.lower() == ".d":
            folders_by_key.setdefault(normalize_folder_key(child.name), []).append(child)

    # Validate all calibration levels are uniquely matched before any assembly begins.
    # Partial loads silently using DEFAULT_CONCENTRATIONS are a data integrity failure —
    # the analyst must see a named error with what is missing and what was found.
    missing: list[dict] = []
    duplicates: list[dict] = []
    for level, key in level_to_key.items():
        matches = folders_by_key.get(key.lower(), [])
        if not matches:
            missing.append({"level": level, "key": key})
        elif len(matches) > 1:
            duplicates.append({"level": level, "key": key, "folders": [m.name for m in matches]})
    if missing or duplicates:
        found_folders = sorted(child.name for child in batch.iterdir() if child.is_dir() and child.suffix.lower() == ".d")
        raise CalibrationFolderError(missing, duplicates, found_folders)

    spike_by_level: dict[int, list[dict[str, Any]]] = {}
    target_compounds_by_level: dict[int, list[dict[str, Any]]] = {}
    for level, key in level_to_key.items():
        d = folders_by_key[key.lower()][0]  # unique match guaranteed by pre-validation above
        if (d / "spike.rp").exists():
            spike_by_level[level] = parse_spike_text((d / "spike.rp").read_text(encoding="utf-8", errors="ignore"))
        if (d / "target.rp").exists():
            target_compounds_by_level[level] = parse_target_rp_text(
                (d / "target.rp").read_text(encoding="utf-8", errors="ignore")
            )["compounds"]

    compounds: list[dict[str, Any]] = []
    for init_row in initcal["compound_level_areas"]:
        no = init_row["compound_number"]
        points = []
        for level in range(1, 11):
            lv = init_row["levels"][level]
            match = next((r for r in spike_by_level.get(level, []) if r["compound_number"] == no), None)
            if match and not _names_match(match["compound_name"], init_row["compound_name"]):
                logger.warning("compound name mismatch for #%s", no)
            if match is None:
                logger.warning("no spike match for compound #%s level %s", no, level)
            analyte_area = lv["area"]
            target_cpds = target_compounds_by_level.get(level, [])
            is_area = get_is_area(init_row["compound_name"], target_cpds)
            area_response = compute_response_ratio(analyte_area, is_area)
            if area_response is None:
                area_response = analyte_area  # fallback: target.rp absent or IS not detected
            points.append({
                "level": level,
                "concentration": match["amount_added"] if match else DEFAULT_CONCENTRATIONS[level - 1],
                "theoretical_concentration": match["amount_added"] if match else None,
                "limit_lower": match["limit_lower"] if match else None,
                "limit_upper": match["limit_upper"] if match else None,
                "area_response": area_response,
                "active": lv["active"],
            })
        # spike_limits uses points[0] (level 1). Confirmed by production data:
        # all 96 compounds share the same acceptance limits (80/120) across all levels.
        # If a future batch uses per-compound or per-level limits, revisit this.
        compounds.append({
            "compound_number": no,
            "compound_name": init_row["compound_name"],
            "points": points,
            "curve_type": init_row["curve_type"],
            "coefficients": {"b": init_row["b"], "m1": init_row["m1"], "m2": init_row["m2"]},
            "r2": init_row["r2"],
            "spike_limits": {"low": points[0]["limit_lower"], "high": points[0]["limit_upper"]},
            "spike_pass_fail": None,  # not evaluated at assembly time; set by qc_service
        })
    return {"batch_path": str(batch.resolve()), "compounds": compounds, "qc_samples": get_qc_data(str(batch), compounds)}


def get_batch_display_name(batch_path: str) -> str:
    """Return the folder name component of a batch path for use as a display label."""
    return Path(batch_path).name if batch_path else ""


def build_batch_store_payload(
    compounds: list[dict],
    qc_samples: list[dict],
    blank_results: list[dict],
) -> dict:
    """Assemble the canonical batch-store dict consumed by render_view and update_curve.

    Both load_batch and resume_run write to batch-store. This function is the
    single definition of that dict's shape so both paths stay in sync.
    Keys: compounds, qc_samples, blank_results.
    """
    return {"compounds": compounds, "qc_samples": qc_samples, "blank_results": blank_results}
