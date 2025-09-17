from typing import Optional, List
from sqlmodel import Session, select

from app.models.user import User


class UserCRUD:
    """User 模型的 CRUD 操作类"""

    @staticmethod
    def create_user(session: Session, user: User) -> User:
        """
        创建用户

        Args:
            session: 数据库会话
            user: User 对象

        Returns:
            User: 创建的 User 对象
        """
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def get_user(session: Session, user_id: int) -> type[User] | None:
        """
        根据 ID 获取用户

        Args:
            session: 数据库会话
            user_id: 用户 ID

        Returns:
            Optional[User]: User 对象或 None
        """
        db_user = session.get(User, user_id)
        if db_user is None or db_user.deleted == 1:
            return None
        return db_user

    @staticmethod
    def get_user_by_name(session: Session, user_name: str) -> Optional[User]:
        """
        根据用户名获取用户

        Args:
            session: 数据库会话
            user_name: 用户名

        Returns:
            Optional[User]: User 对象或 None
        """
        statement = select(User).where(User.user_name == user_name).where(User.deleted == 0)
        return session.exec(statement).first()

    @staticmethod
    def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        获取用户列表

        Args:
            session: 数据库会话
            skip: 跳过的记录数
            limit: 返回的记录数

        Returns:
            List[User]: User 对象列表
        """
        statement = select(User).where(User.deleted == 0).offset(skip).limit(limit)
        result = session.exec(statement).all()
        return list(result)

    @staticmethod
    def update_user(session: Session, user_id: int, user_update: dict) -> type[User] | None:
        """
        更新用户

        Args:
            session: 数据库会话
            user_id: 用户 ID
            user_update: 更新的字段字典

        Returns:
            Optional[User]: 更新后的 User 对象或 None
        """
        db_user = session.get(User, user_id)
        if not db_user:
            return None

        if db_user.deleted == 1:
            return None

        for key, value in user_update.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)

        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(session: Session, user_id: int) -> bool:
        """
        删除用户（软删除）

        Args:
            session: 数据库会话
            user_id: 用户 ID

        Returns:
            bool: 是否删除成功
        """
        db_user = session.get(User, user_id)
        if not db_user:
            return False

        db_user.deleted = 1
        session.commit()
        return True