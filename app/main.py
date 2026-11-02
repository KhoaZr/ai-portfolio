from fastapi import FastAPI

app = FastAPI(title="AI portfolio API")

@app.get("/")
def read_root():
    return {"message": "AI portfolio backend is running"}