from typing import Optional, List
from sqlmodel import Session, select

from app.models import Keyword
from app.models.keyword import Keyword


class KeywordCRUD:
    """Keyword 模型的 CRUD 操作类"""

    @staticmethod
    def create_keyword(session: Session, keyword: Keyword) -> Keyword:
        """
        创建关键词

        Args:
            session: 数据库会话
            keyword: Keyword 对象

        Returns:
            Keyword: 创建的 Keyword 对象
        """
        session.add(keyword)
        session.commit()
        session.refresh(keyword)
        return keyword

    @staticmethod
    def get_keyword(session: Session, keyword_id: int) -> Optional[Keyword]:
        """
        根据 ID 获取关键词

        Args:
            session: 数据库会话
            keyword_id: 关键词 ID

        Returns:
            Optional[Keyword]: Keyword 对象或 None
        """
        return session.get(Keyword, keyword_id)

    @staticmethod
    def get_keywords(session: Session, word: Optional[str] = None, keyword_type: Optional[str] = None,
                     user_id: Optional[int] = None, category_id: Optional[int] = None,
                     skip: int = 0, limit: int = 100) -> List[Keyword]:
        """
        获取关键词列表

        Args:
            session: 数据库会话
            word: 关键词内容（模糊匹配）
            keyword_type: 关键词类型
            user_id: 用户 ID
            category_id: 分类 ID
            skip: 跳过的记录数
            limit: 返回的记录数

        Returns:
            List[Keyword]: Keyword 对象列表
        """
        statement = select(Keyword).where(Keyword.deleted == 0)

        if word:
            statement = statement.where(Keyword.word.like(f"%{word}%"))

        if keyword_type:
            statement = statement.where(Keyword.type == keyword_type)

        if user_id is not None:
            statement = statement.where(Keyword.user_id == user_id)

        if category_id is not None:
            statement = statement.where(Keyword.category_id == category_id)

        statement = statement.offset(skip).limit(limit)
        result = session.exec(statement).all()
        return list(result)

    @staticmethod
    def update_keyword(session: Session, keyword_id: int, keyword_update: dict) -> type[Keyword] | None:
        """
        更新关键词

        Args:
            session: 数据库会话
            keyword_id: 关键词 ID
            keyword_update: 更新的字段字典

        Returns:
            Optional[Keyword]: 更新后的 Keyword 对象或 None
        """
        keyword = session.get(Keyword, keyword_id)
        if not keyword:
            return None

        for key, value in keyword_update.items():
            if hasattr(keyword, key):
                setattr(keyword, key, value)

        session.commit()
        session.refresh(keyword)
        return keyword

    @staticmethod
    def delete_keyword(session: Session, keyword_id: int) -> bool:
        """
        删除关键词（软删除）

        Args:
            session: 数据库会话
            keyword_id: 关键词 ID

        Returns:
            bool: 是否删除成功
        """
        keyword = session.get(Keyword, keyword_id)
        if not keyword:
            return False

        keyword.deleted = 1
        session.commit()
        return True