from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

# 1: Bảng quản trị viên / admin
class User(Base):
    __tablename__ =  "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
# 2: Bảng dự án
class Project(Base):
    __tablename__ =  "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    

# 3: Bảng kỹ năng
class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False,) # ví dụ: backend, ai/ml, devops
    proficiency_level = Column(Float, default=1.0,) # Đánh giá từ 1.0 đến 5.0 do MLP dự đoán
    
    evidences = relationship("SkillEvidence", back_populates="skill")
    
    
    
# 4: Bảng báo cáo được nộp vào
class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    file_type = Column(String(20), nullable=True) # "markdown", "pdf", "docx"
    raw_content = Column(Text, nullable=False) # Nội dung được trích xuất từ file
    created_at = Column(DateTime, default=datetime.utcnow)
    
    evidences = relationship("SkillEvidence", back_populates="report")
    
    
    
# 5: Bảng chứng chỉ kĩ năng - phục vụ cho rag và chatbot đối chiếu
class SkillEvidence(Base):
    __tablename__ = "skill_evidences"
    id = Column(Integer, primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=True)
    context_snippet = Column(Text, nullable=False) # Đoạn trích chứng minh đã làm
    created_at = Column(DateTime, default=datetime.utcnow)




# 6: Bảng tin nhắn liên hệ từ khách
class ContactMessage(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String(100), nullable=False)
    sender_mail = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)