
import os
import shutil

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status
)
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin
from app.database import get_db
from app.models.models import Report, User
from app.schemas.portfolio import ReportResponse
from app.services.extractor import process_report_with_llm


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


# ==========================================
# API 1: UPLOAD REPORT
# ==========================================

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
    """API Admin: Upload file báo cáo hoặc ảnh scan."""

    file_ext = os.path.splitext(file.filename)[1].lower()

    # Kiểm tra định dạng file
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Định dạng file không được hỗ trợ. "
                f"Chỉ chấp nhận: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        )

    # Lưu file vào thư mục uploads/
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lưu file: {str(e)}"
        )

    # Xác định loại file
    if file_ext in [".jpg", ".jpeg", ".png"]:
        file_type = "scan_image"
    elif file_ext == ".pdf":
        file_type = "pdf"
    elif file_ext == ".docx":
        file_type = "docx"
    else:
        file_type = "markdown"

    # Tạo bản ghi Report trong database
    new_report = Report(
        title=file.filename,
        file_type=file_type,
        raw_content=f"[FILE_PATH]: {file_path}"
    )

    try:
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return new_report

    except Exception as e:
        db.rollback()

        # Xóa file nếu không lưu được database
        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lưu thông tin báo cáo: {str(e)}"
        )


# ==========================================
# API 2: PROCESS REPORT WITH LLM VISION
# ==========================================

@router.post(
    "/{report_id}/process",
    response_model=ReportResponse
)
def trigger_llm_extraction(
    report_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """
    API Admin: Kích hoạt LLM Vision để bóc tách
    nội dung ảnh viết tay hoặc tài liệu và lưu Markdown vào DB.
    """

    # Tìm báo cáo trong database
    report = db.query(Report).filter(
        Report.id == report_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bản ghi báo cáo"
        )

    # Lấy đường dẫn file đã upload
    file_path = report.raw_content.replace(
        "[FILE_PATH]: ",
        "",
        1
    ).strip()

    # Kiểm tra file tồn tại
    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy file gốc trên hệ thống"
        )

    try:
        # Gửi file đến LLM để bóc tách nội dung
        extracted_markdown = process_report_with_llm(
            file_path,
            report.file_type
        )

        # Lưu nội dung Markdown vào database
        report.raw_content = extracted_markdown
        db.commit()
        db.refresh(report)

        return report

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi trong quá trình bóc tách LLM: {str(e)}"
        )
