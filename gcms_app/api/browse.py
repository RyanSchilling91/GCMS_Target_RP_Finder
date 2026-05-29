from __future__ import annotations

import threading
from uuid import uuid4

from fastapi import APIRouter, HTTPException

from gcms_app.services.browse_service import _browse_folder_worker, _browse_lock, _browse_results

router = APIRouter(prefix="/api/browse", tags=["browse"])


@router.post("/open")
def open_browser():
    request_id = str(uuid4())
    with _browse_lock:
        _browse_results[request_id] = "__pending__"
    thread = threading.Thread(target=_browse_folder_worker, args=(request_id,), daemon=True)
    thread.start()
    return {"request_id": request_id}


@router.get("/{request_id}")
def poll_browser(request_id: str):
    with _browse_lock:
        value = _browse_results.get(request_id)
    if value is None:
        raise HTTPException(status_code=404, detail="Unknown request_id")
    if value == "__pending__":
        return {"status": "pending"}
    return {"status": "ready", "path": value or ""}
