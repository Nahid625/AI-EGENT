from fastapi import FastAPI
from src.routes.ai_router import router

# cool and clean
app = FastAPI(title="Ai learning")
app.include_router(router)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)