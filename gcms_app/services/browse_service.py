from __future__ import annotations
import threading

_browse_results: dict[str, str | None] = {}
_browse_lock = threading.Lock()


def _browse_folder_worker(request_id: str):
    """Run a native folder picker and store the selected path by request id."""
    selected: str | None = None
    try:
        from tkinter import Tk, filedialog
        root = Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        try:
            selected = filedialog.askdirectory()
        finally:
            root.destroy()
    except Exception:
        selected = None
    with _browse_lock:
        _browse_results[request_id] = selected or None
