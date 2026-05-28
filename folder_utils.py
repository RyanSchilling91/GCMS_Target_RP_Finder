from __future__ import annotations

import re


def normalize_folder_key(folder_name: str) -> str:
    """Strip leading injection-order prefix e.g. '03-' from folder name."""
    return re.sub(r"^\d+-", "", folder_name).lower()
