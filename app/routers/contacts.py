from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import ContactMessage, User
from app.schemas.portfolio import ContactCreate, ContactResponse
from app.core.deps import get_current_admin


router = APIRouter(
    prefix="/api/contacts",
    tags=["Contact Messages"]
)


@router.post(
    "",
    response_model=ContactResponse,
    status_code=status.HTTP_201_CREATED
)
def create_contact_message(
    message_data: ContactCreate,
    db: Session = Depends(get_db)
):
    """API Công khai: Khách/Recruiter gửi tin nhắn liên hệ"""

    new_message = ContactMessage(**message_data.model_dump())

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    return new_message


@router.get(
    "",
    response_model=List[ContactResponse]
)
def get_contact_messages(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    """API Admin: Xem toàn bộ tin nhắn liên hệ"""

    return db.query(ContactMessage).order_by(
        ContactMessage.created_at.desc()
    ).all()