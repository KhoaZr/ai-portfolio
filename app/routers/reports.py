import os
import shutil

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Report, User
from app.schemas.portfolio import ReportResponse
from app.core.deps import get_current_admin


router = APIRouter(
    prefix="/api/reports",
    tags=["Report Ingestion"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".png",
    ".jpg",
    ".jpeg",
    ".md"
}


@router.post(
    "/upload",
    response_model=ReportResponse,
    status_code=status.HTTP_201_CREATED
)
async def upload_report(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """API Admin: Upload file báo cáo hoặc ảnh scan để chuẩn bị bóc tách AI"""

    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Định dạng file không được hỗ trợ. "
                f"Chỉ chấp nhận: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        )

    # Lưu file vào thư mục đệm uploads/
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Xác định loại file
    if file_ext in [".jpg", ".jpeg", ".png"]:
        file_type = "scan_image"
    elif file_ext == ".pdf":
        file_type = "pdf"
    elif file_ext == ".docx":
        file_type = "docx"
    else:
        file_type = "markdown"

    # Ghi nhận bản ghi Report
    # Tạm thời raw_content lưu đường dẫn file.
    # Giai đoạn 3, AI sẽ bóc tách nội dung văn bản.
    new_report = Report(
        title=file.filename,
        file_type=file_type,
        raw_content=f"[FILE_PATH]: {file_path}"
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report