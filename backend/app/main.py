from fastapi import FastAPI
from app.api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db
from app.db.seed import seed_default_categories
from app.db.session import SessionLocal
from app.config import settings

app = FastAPI(title="Notes API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=settings.cors_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()
    try:
        seed_default_categories(db)
    finally:
        db.close()
    
app.include_router(api_router, prefix="/api/v1")



@app.get("/")
def health():
    return {"status": "ok"}
