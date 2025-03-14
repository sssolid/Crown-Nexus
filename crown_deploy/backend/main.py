from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Crown Nexus API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
