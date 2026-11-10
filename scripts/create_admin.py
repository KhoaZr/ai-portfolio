
import sys
import os
from getpass import getpass

# Thêm đường dẫn gốc vào sys.path để import được app
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from app.database import SessionLocal
from app.models.models import User
from app.core.security import get_password_hash


def init_admin():
    db = SessionLocal()

    try:
        username = input("Nhập username Admin [admin]: ").strip() or "admin"

        # Kiểm tra tài khoản đã tồn tại
        existing_user = db.query(User).filter(
            User.username == username
        ).first()

        if existing_user:
            print(f"Tài khoản '{username}' đã tồn tại!")
            return

        # Nhập mật khẩu an toàn
        password = getpass("Nhập mật khẩu Admin: ")
        confirm_password = getpass("Xác nhận mật khẩu: ")

        # Kiểm tra mật khẩu
        if not password:
            print("Mật khẩu không được để trống!")
            return

        if password != confirm_password:
            print("Mật khẩu xác nhận không khớp!")
            return

        if len(password.encode("utf-8")) > 72:
            print("Mật khẩu không được vượt quá 72 bytes!")
            return

        # Tạo tài khoản Admin
        admin_user = User(
            username=username,
            hashed_password=get_password_hash(password)
        )

        db.add(admin_user)
        db.commit()

        print("Tạo tài khoản Admin thành công!")
        print(f"Username: {username}")

    except Exception as e:
        db.rollback()
        print(f"Lỗi khi tạo tài khoản Admin: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    init_admin()
