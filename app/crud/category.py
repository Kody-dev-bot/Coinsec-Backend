from typing import Optional, List
from sqlmodel import Session, select

from app.models.category import Category


class CategoryCRUD:
    """Category 模型的 CRUD 操作类"""

    @staticmethod
    def create_category(session: Session, category: Category) -> Category:
        """
        创建分类

        Args:
            session: 数据库会话
            category: Category 对象

        Returns:
            Category: 创建的 Category 对象
        """
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    @staticmethod
    def get_category(session: Session, category_id: int) -> type[Category] | None:
        """
        根据 ID 获取分类

        Args:
            session: 数据库会话
            category_id: 分类 ID

        Returns:
            Optional[Category]: Category 对象或 None
        """
        db_category = session.get(Category, category_id)
        if db_category is None or db_category.deleted == 1:
            return None
        return db_category

    @staticmethod
    def get_categories(session: Session, user_id: int = 0, category_type: Optional[str] = None,
                       skip: int = 0, limit: int = 100) -> List[Category]:
        """
        获取分类列表

        Args:
            session: 数据库会话
            user_id: 用户 ID，0 表示系统默认分类
            category_type: 分类类型 (expense/income)
            skip: 跳过的记录数
            limit: 返回的记录数

        Returns:
            List[Category]: Category 对象列表
        """
        statement = select(Category).where(Category.deleted == 0)
        
        if user_id is not None:
            statement = statement.where(Category.user_id == user_id)
            
        if category_type:
            statement = statement.where(Category.type == category_type)
            
        statement = statement.offset(skip).limit(limit)
        result = session.exec(statement).all()
        return list(result)

    @staticmethod
    def update_category(session: Session, category_id: int,
                        category_update: dict) -> type[Category] | None:
        """
        更新分类

        Args:
            session: 数据库会话
            category_id: 分类 ID
            category_update: 更新的字段字典

        Returns:
            Optional[Category]: 更新后的 Category 对象或 None
        """
        db_category = session.get(Category, category_id)
        if not db_category:
            return None

        if db_category.deleted == 1:
            return None
            
        for key, value in category_update.items():
            if hasattr(db_category, key):
                setattr(db_category, key, value)
                
        session.commit()
        session.refresh(db_category)
        return db_category

    @staticmethod
    def delete_category(session: Session, category_id: int) -> bool:
        """
        删除分类（软删除）

        Args:
            session: 数据库会话
            category_id: 分类 ID

        Returns:
            bool: 是否删除成功
        """
        db_category = session.get(Category, category_id)
        if not db_category:
            return False

        if db_category.deleted == 1:
            return False
            
        db_category.deleted = 1
        session.commit()
        return True