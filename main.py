# main.py
from fastapi import FastAPI
from src.config.db import engine, Base
from src.routes.chat_router import router as ChatRouter
from src.schemas.schema import User, ChatSession, Message 
Base.metadata.create_all(bind=engine)

from src.routes.ai_router import router as aiRouter
from src.routes.userRoute import router as UserRouter

app = FastAPI(title="Ai learning")

routes = [aiRouter, UserRouter,ChatRouter]
for r in routes:
    app.include_router(r)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)          
    