import os
from PIL import Image
from pypdf import PdfReader
from docx import Document
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Khởi tạo client Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ai_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def extract_text_from_pdf(file_path: str) -> str:
    """Trích xuất văn bản từ PDF kỹ thuật số"""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    
    return text.strip()

def extract_text_from_docx(file_path: str) -> str:
    """Trích xuất văn bản từ file word"""
    doc = Document(file_path)
    text = [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
    return "\n".join(text).strip()

def extract_with_llm_vision(image_path: str) -> str:
    """Bóc tách chữ viết tay/ ảnh scan bằng Gemini 1.5 flash vision"""
    if not ai_client:
        raise ValueError(
            "Chưa cấu hình GEMINI_API_KEY trong file env. Hãy kiểm tra lại"
        )
        
    # Mở file bằng Pillow
    img = Image.open(image_path)
    system_prompt = """
    Bạn là chuyên gia phân tích và trích xuất nội dung tài liệu kỹ thuật (Technical Document Parser & OCR Specialist).

    NHIỆM VỤ:
    Phân tích hình ảnh được cung cấp và trích xuất toàn bộ nội dung văn bản có trong hình ảnh. Bao gồm:
    - Văn bản in.
    - Chữ viết tay.
    - Tiêu đề và tiêu đề phụ.
    - Danh sách đánh số và danh sách gạch đầu dòng.
    - Bảng biểu và dữ liệu trong bảng.
    - Ghi chú, chú thích và nội dung bên lề.
    - Công thức, ký hiệu và đoạn mã lập trình (nếu có).

    YÊU CẦU XỬ LÝ:

    1. ĐỘ CHÍNH XÁC
    - Trích xuất đầy đủ nội dung, không tự ý lược bỏ hoặc tóm tắt.
    - Giữ nguyên ý nghĩa và thứ tự xuất hiện của nội dung trong ảnh.
    - Giữ chính xác các thuật ngữ chuyên ngành, thuật ngữ công nghệ và tên thư viện.
    - Ví dụ: Python, FastAPI, React, Docker, PostgreSQL, SQLAlchemy, Machine Learning, API, JWT,...
    - Không tự ý dịch thuật ngữ tiếng Anh sang tiếng Việt.
    - Không tự suy diễn hoặc bổ sung nội dung không xuất hiện trong ảnh.
    - Nếu không thể đọc được một đoạn văn bản, đánh dấu [Không đọc được] thay vì tự phỏng đoán.

    2. CẤU TRÚC VÀ ĐỊNH DẠNG
    - Chuyển đổi nội dung sang định dạng Markdown chuẩn.
    - Sử dụng #, ##, ### để phân cấp tiêu đề.
    - Sử dụng - cho danh sách gạch đầu dòng.
    - Sử dụng 1., 2., 3. cho danh sách đánh số.
    - Sử dụng bảng Markdown để trình bày dữ liệu dạng bảng.
    - Sử dụng dấu ` để định dạng thuật ngữ, tên biến, hàm và lệnh code.
    - Sử dụng khối code với ngôn ngữ tương ứng nếu hình ảnh chứa mã nguồn.
    - Giữ nguyên cấu trúc phân cấp và mối quan hệ giữa các phần nội dung.

    3. XỬ LÝ NỘI DUNG ĐẶC BIỆT
    - Với chữ viết tay: cố gắng nhận diện chính xác nội dung.
    - Với bảng biểu: bảo toàn hàng, cột và dữ liệu tương ứng.
    - Với công thức toán học: giữ nguyên ký hiệu và biểu thức.
    - Với mã nguồn: bảo toàn cú pháp, tên biến, tên hàm và cấu trúc code.
    - Với sơ đồ có chú thích: trích xuất các nhãn và nội dung văn bản có thể đọc được.

    4. QUY TẮC ĐẦU RA
    - Chỉ trả về nội dung đã trích xuất dưới định dạng Markdown.
    - Không viết lời mở đầu hoặc lời dẫn như "Đây là kết quả trích xuất".
    - Không đưa ra nhận xét, đánh giá hoặc giải thích ngoài nội dung hình ảnh.
    - Không thêm kết luận hoặc thông tin không có trong tài liệu.
    - Đảm bảo Markdown có cấu trúc rõ ràng, dễ đọc và thuận tiện để lưu thành file .md.

    MỤC TIÊU CUỐI CÙNG:
    Tạo ra một bản Markdown phản ánh trung thực, đầy đủ và có cấu trúc của tài liệu gốc, có thể sử dụng trực tiếp để lưu trữ trong Knowledge Base hoặc làm tài liệu học tập.
    """
    response = ai_client.models.generate_content(
        model="gemini-3.8-flash", contents=[img,system_prompt]
    )
    
    # Lấy nội dung văn bản từ Gemini
    extrac_markdown = response.text
    if not extrac_markdown:
        raise ValueError("Gemini không trả về nội dung văn bản")
    return extrac_markdown


def process_report_with_llm(file_path: str, file_type: str) -> str:
    """Bộ điều phối trích xuất chính bằng LLM"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File không tồn tại: {file_path}")
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "docx":
        return extract_text_from_docx(file_path)
    elif file_type == "scan_image":
        return extract_with_llm_vision(file_path)
    elif file_type == "markdown":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"Định dạng file {file_path} chưa được hỗ trợ!")