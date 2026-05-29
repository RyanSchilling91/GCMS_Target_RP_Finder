from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from Trinity.services.parsing.text_cleaning import strip_escape_sequences
from Trinity.services.parsing.target_parser import parse_target_rp_text
from .discovery import discover_batch

logger = logging.getLogger(__name__)


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


def get_batch_display_name(batch_path: str) -> str:
    """Return the folder name component of a batch path for use as a display label."""
    return Path(batch_path).name if batch_path else ""


def load_batch(batch_path: str, imported_by: str) -> dict[str, Any]:
    """Walk a .B batch folder, parse target.rp from each .D subfolder, return structured result."""
    discovery = discover_batch(Path(batch_path))

    samples: dict[str, Any] = {}
    warnings: list[str] = []
    parse_errors: list[dict[str, str]] = []
    parsed_count = 0

    for d in discovery["d_folders"]:
        folder_name = d["folder_name"]
        normalized_key = d["normalized_key"]

        if not d["has_target_rp"]:
            warnings.append(folder_name)
            logger.warning("No target.rp found in %s", folder_name)
            continue

        try:
            raw_text = Path(d["target_rp_path"]).read_text(encoding="utf-8", errors="ignore")
            cleaned_text = strip_escape_sequences(raw_text)
            parsed = parse_target_rp_text(cleaned_text)
            samples[normalized_key] = {
                "folder_path": d["folder_path"],
                "normalized_key": normalized_key,
                "target_rp_path": d["target_rp_path"],
                "compounds": parsed["compounds"],
                "metadata": parsed["metadata"],
            }
            parsed_count += 1
        except Exception as exc:
            logger.error("Failed to parse target.rp in %s: %s", folder_name, exc)
            parse_errors.append({"folder": folder_name, "error": str(exc)})

    return {
        "batch_path": str(Path(batch_path).resolve()),
        "batch_folder_name": get_batch_display_name(batch_path),
        "sample_count": discovery["total_d_folders"],
        "parsed_count": parsed_count,
        "warning_count": len(warnings),
        "parse_errors": parse_errors,
        "warnings": warnings,
        "samples": samples,
    }
