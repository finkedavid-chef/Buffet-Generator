from unittest import result
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import traceback

app = FastAPI()
import buffet

app = FastAPI(title="Buffet Generator", version="1.0.0")
app.mount("/Static", StaticFiles(directory="Static"), name="Static")

class Rules(BaseModel):
    forbidden_tags: List[str] = buffet.DEFAULT_Rules["forbidden_tags"]
    max_tags_counts: dict = buffet.DEFAULT_Rules["max_tags_counts"]
    unique_main: bool = buffet.DEFAULT_Rules["unique_main"]

@app.get("/")
def home():
    return FileResponse("Static/index.html")
 
class GenerateRequest(BaseModel):
    required_tags: List[str]
    forbidden_tags: List[str]

def norm(tags: List[str]) -> List[str]:
    return [t.strip().lower() for t in tags]

@app.post("/api/generate_buffet")
def api_generate_buffet(req: GenerateRequest):
    result = buffet.generate_Buffet(
        required_tags=norm(req.required_tags),
        forbidden_tags=norm(req.forbidden_tags)
    )
    if not result:
        return {
        "ok": False,
        "message": "Buffet nicht gefunden.",
        "buffet": []
        }
    return {
        "ok": True, 
        "buffet": result
    }


     