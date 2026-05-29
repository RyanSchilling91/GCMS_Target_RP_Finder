from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

from gcms_app.services.batch_service import load_batch, validate_batch_folder

router = APIRouter()


class BatchLoadRequest(BaseModel):
    batch_path: str
    imported_by: str = "unknown"


class BatchValidateRequest(BaseModel):
    batch_path: str


@router.post("/batch/validate")
async def validate_batch(request: BatchValidateRequest):
    """
    Validate that a path looks like a ChemStation .B batch folder
    before committing to a full load. Returns folder metadata and
    a list of .D subfolders found.
    """
    path = Path(request.batch_path)

    if not path.exists():
        raise HTTPException(status_code=400, detail="Path does not exist.")

    # validate_batch_folder returns {"valid": bool, "error": str|None, "batch_path": str}
    validation = validate_batch_folder(str(path))

    if not validation["valid"]:
        raise HTTPException(status_code=400, detail=validation["error"])

    return {
        "valid": True,
        "batch_path": validation["batch_path"],
        "batch_folder_name": path.name,
    }


@router.post("/batch/load")
async def load_batch_endpoint(request: BatchLoadRequest):
    """
    Load a full .B batch folder — discover all .D sample subfolders,
    find target.rp in each, parse compound records, and return
    structured batch results ready for the workflow layer.
    """
    path = Path(request.batch_path)

    if not path.exists():
        raise HTTPException(status_code=400, detail="Path does not exist.")

    try:
        result = load_batch(
            batch_path=str(path),
            imported_by=request.imported_by
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch load failed: {str(e)}"
        )

    return result
