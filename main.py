from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.config import settings
from app.routes import leads


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings.validate()   # fail fast if any required env var is missing
    yield


app = FastAPI(title="AI Lead Qualifier", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(leads.router, prefix="/leads", tags=["leads"])


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("static/form.html")


@app.get("/health")
async def health():
    return {"status": "ok"}
