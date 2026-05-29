from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from gcms_app.api import browse, load

app = FastAPI(title="GCMS Target RP Discovery")

# Mount frontend static files
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "frontend")),
    name="static"
)

# browse.router already carries prefix="/api/browse" internally — include without extra prefix
app.include_router(browse.router)
# load.router uses bare route paths (/batch/validate, /batch/load) — add /api prefix here
app.include_router(load.router, prefix="/api")

# Serve index.html at root
@app.get("/")
async def root():
    return FileResponse(
        os.path.join(os.path.dirname(__file__), "frontend", "index.html")
    )
