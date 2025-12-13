# src/backend/app/main.py
from fastapi import FastAPI
from .routers import search, register, admin
from .services.db_service import create_tables
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",
    # "http://localhost:5174",
    "http://127.0.0.1:5173",
    # "http://127.0.0.1:5174",
    "https://darkanon1mous-reunite-ai.hf.space/",
    "https://reuniteai.netlify.app/"
]


app = FastAPI(title="ReUniteAI API")

app.include_router(search.router)
app.include_router(register.router)
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    await create_tables()
