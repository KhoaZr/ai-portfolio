from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ---  SCHEMAS CHO DỰ ÁN (PROJECTS) --- 
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    tech_stack: Optional[str] = None
    github_url: Optional[str] = None
    
class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True


# --- SCHEMA CHO KĨ NĂNG (SKILLs) ---

class SkillBase(BaseModel):
    name: str
    category: str
    proficiency_level: Optional[float] = 1.0


class SkillCreate(SkillBase):
    pass 


class SkillResponse(SkillBase):
    id: int
    class Config:
        from_attributes = True


# --- SCHEMA CHO BÁO CÁO (REPORTS) ---
class ReportResponse(BaseModel):
    id: int
    title: str
    file_type: str
    created_at: datetime
    class Config: 
        from_attributes = True


# --- SCHEMA CHO LIÊN HỆ (CONTACTS) ---
class ContactCreate(BaseModel):
    sender_name: str
    sender_email: EmailStr
    message: str
    
class ContactResponse(ContactCreate):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True