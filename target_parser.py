"""Parse target.rp files produced by the HP ChemStation instrument software.

Column positions confirmed against fixture files input data/target.rp
(13-10cs-4440.D, level 10) and input data/target.rp_low_level
(03-o02cs-4440.D, level 1):
  - Compound prefix + number: line[0:5]  (prefix in [0], number right-justified in [1:5])
  - Compound name:            line[6:40].strip()
  - RESPONSE:                 line[77:85].strip()  (right-justified integer, ends at col 84)
"""
from __future__ import annotations

import re
from typing import Any

from .text_cleaning import strip_escape_sequences

_DATA_FILE_RE = re.compile(r"^Data file\s*:\s*(.+)$", re.IGNORECASE)
_REPORT_DATE_RE = re.compile(r"^Report Date\s*:\s*(.+)$", re.IGNORECASE)
_QUANT_TYPE_RE = re.compile(r"Quant\s+Type\s*:\s*(\S+)", re.IGNORECASE)

# Fixed column positions (confirmed by char-by-char inspection of fixture files)
_NAME_START = 6
_NAME_END = 40
_RESP_START = 77
_RESP_END = 85

_NOT_DETECTED = "Compound Not Detected"


def parse_target_rp_text(text: str) -> dict[str, Any]:
    """Parse target.rp text into compound areas and report metadata.

    Returns:
        {
            "compounds": [
                {
                    "compound_number": int,
                    "compound_name":   str,
                    "area":            float | None,
                    "is_istd":         bool,
                    "is_surrogate":    bool,
                    "detected":        bool,
                }
            ],
            "metadata": {
                "data_file":   str,
                "report_date": str,
                "quant_type":  str,
            }
        }
    """
    cleaned = strip_escape_sequences(text)
    lines = cleaned.splitlines()

    metadata: dict[str, str] = {"data_file": "", "report_date": "", "quant_type": ""}
    compounds: list[dict[str, Any]] = []
    seen: set[int] = set()

    for line in lines:
        _update_metadata(line, metadata)
        row = _parse_compound_line(line)
        if row is None:
            continue
        num = row["compound_number"]
        if num in seen:
            continue  # header column repeats across pages; skip duplicates
        seen.add(num)
        compounds.append(row)

    return {"compounds": compounds, "metadata": metadata}


def _update_metadata(line: str, meta: dict[str, str]) -> None:
    m = _DATA_FILE_RE.match(line.strip())
    if m and not meta["data_file"]:
        meta["data_file"] = m.group(1).strip()
        return
    m = _REPORT_DATE_RE.match(line.strip())
    if m and not meta["report_date"]:
        meta["report_date"] = m.group(1).strip()
        return
    m = _QUANT_TYPE_RE.search(line)
    if m and not meta["quant_type"]:
        meta["quant_type"] = m.group(1).strip()


def _parse_compound_line(line: str) -> dict[str, Any] | None:
    """Return a compound dict for a valid compound data line, or None."""
    if len(line) < 6:
        return None

    prefix = line[0]
    if prefix not in (" ", "*", "$"):
        return None

    num_str = line[0:5].lstrip("*$ ")
    if not num_str.isdigit():
        return None

    # Separator between number field and name must be a space
    if line[5] != " ":
        return None

    compound_number = int(num_str)
    is_istd = prefix == "*"
    is_surrogate = prefix == "$"
    compound_name = line[_NAME_START:_NAME_END].strip()

    if not compound_name:
        return None

    if _NOT_DETECTED in line:
        return {
            "compound_number": compound_number,
            "compound_name": compound_name,
            "area": None,
            "is_istd": is_istd,
            "is_surrogate": is_surrogate,
            "detected": False,
        }

    if len(line) <= _RESP_START:
        return None

    resp_str = line[_RESP_START:_RESP_END].strip()
    if not resp_str or not resp_str.isdigit():
        return None

    return {
        "compound_number": compound_number,
        "compound_name": compound_name,
        "area": float(resp_str),
        "is_istd": is_istd,
        "is_surrogate": is_surrogate,
        "detected": True,
    }
