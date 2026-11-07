from fastapi import FastAPI
from app.database import engine, Base
import app.models.models

# tự động tạo bảng nếu chưa tồn tại
Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI portfolio API")

@app.get("/")
def read_root():
    return {"message": "AI portfolio backend is running"}