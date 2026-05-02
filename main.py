from fastapi import FastAPI
from src.routes.ai_router import router as aiRouter
from src.routes.userRoute import router as UserRouter

# cool and clean
app = FastAPI(title="Ai learning")

routes = [aiRouter,UserRouter]

for r in routes:
    app.include_router(r)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)