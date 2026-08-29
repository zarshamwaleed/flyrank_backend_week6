from fastapi import FastAPI
from src.routes import classify

app = FastAPI(title="LLM Classifier API")
app.include_router(classify.router)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "LLM Classifier API", "endpoint": "POST /classify/"}