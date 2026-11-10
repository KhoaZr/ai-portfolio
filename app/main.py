from fastapi import FastAPI, Depends

from app.database import engine, Base
from app.routers import auth
from app.core.deps import get_current_admin
from app.models.models import User


# Khởi tạo các bảng trong Database
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI Portfolio API"
)


# Đăng ký router xác thực
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {
        "message": "AI Portfolio Backend is running!"
    }


# Tuyến đường thử nghiệm yêu cầu đăng nhập Admin
@app.get("/api/admin/me")
def read_admin_profile(
    current_admin: User = Depends(get_current_admin)
):
    return {
        "status": "success",
        "message": f"Xin chào Admin {current_admin.username}!",
        "user_id": current_admin.id
    }