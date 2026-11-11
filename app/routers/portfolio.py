from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Project, Skill, User
from app.schemas.portfolio import ProjectResponse, ProjectCreate, SkillCreate, SkillResponse
from app.core.deps import get_current_admin

router = APIRouter(prefix="/api/portfolio", tags=["Portfolio Management"])


# ---- API dự án (PROJECTS) ---
@router.get("/projects", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    """API Công Khai: Lấy danh sách dự án"""
    return db.query(Project).all()


@router.post("/projects", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """API Admin: Thêm dự án mới"""
    new_project = Project(**project_data.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

# --- API KỸ NĂNG (SKILLS) ---

@router.get("/skills", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    """API Công khai: Lấy danh sách kỹ năng"""
    return db.query(Skill).all()


@router.post(
    "/skills",
    response_model=SkillResponse,
    status_code=status.HTTP_201_CREATED
)
def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """API Admin: Thêm kỹ năng mới thủ công"""

    existing_skill = db.query(Skill).filter(
        Skill.name == skill_data.name
    ).first()

    if existing_skill:
        raise HTTPException(
            status_code=400,
            detail="Kỹ năng này đã tồn tại trong cơ sở dữ liệu"
        )

    new_skill = Skill(**skill_data.model_dump())

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill
    