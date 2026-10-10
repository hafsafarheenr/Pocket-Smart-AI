from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.db import init_db
from app.routes import auth, planners, pages

@asynccontextmanager
async def lifespan(app:FastAPI):
    init_db()
    yield

init_db()
app=FastAPI(title=settings.app_name,version="1.0.0",description="Budget-aware GenAI recommendation assistant",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static",StaticFiles(directory=BASE_DIR / "static"),name="static")
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)

@app.get("/health")
def health(): return {"status":"ok","app":settings.app_name,"gemini_configured":bool(settings.gemini_api_key),"model":settings.gemini_model}

if __name__=="__main__":
    import uvicorn
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
