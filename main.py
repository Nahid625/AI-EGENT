from fastapi import FastAPI
from src.routes.ai_router import router

# cool and clean
app = FastAPI(title="Ai learning")
app.include_router(router)