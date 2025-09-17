from typing import Optional, List
from sqlmodel import Session, select

from app.models.record import Record


class RecordCRUD:
    """Record 模型的 CRUD 操作类"""

    @staticmethod
    def create_record(session: Session, record: Record) -> Record:
        """
        创建记账记录

        Args:
            session: 数据库会话
            record: Record 对象

        Returns:
            Record: 创建的 Record 对象
        """
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

    @staticmethod
    def get_record(session: Session, record_id: int) -> Optional[Record]:
        """
        根据 ID 获取记账记录

        Args:
            session: 数据库会话
            record_id: 记录 ID

        Returns:
            Optional[Record]: Record 对象或 None
        """
        return session.get(Record, record_id)

    @staticmethod
    def get_records(session: Session, user_id: int, record_type: Optional[str] = None,
                    category_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[Record]:
        """
        获取记账记录列表

        Args:
            session: 数据库会话
            user_id: 用户 ID
            record_type: 记录类型 (expense/income)
            category_id: 分类 ID
            skip: 跳过的记录数
            limit: 返回的记录数

        Returns:
            List[Record]: Record 对象列表
        """
        statement = select(Record).where(Record.deleted == 0).where(Record.user_id == user_id)

        if record_type:
            statement = statement.where(Record.type == record_type)

        if category_id is not None:
            statement = statement.where(Record.category_id == category_id)

        statement = statement.offset(skip).limit(limit)
        result = session.exec(statement).all()
        return list(result)

    @staticmethod
    def update_record(session: Session, record_id: int, record_update: dict) -> type[Record] | None:
        """
        更新记账记录

        Args:
            session: 数据库会话
            record_id: 记录 ID
            record_update: 更新的字段字典

        Returns:
            Optional[Record]: 更新后的 Record 对象或 None
        """
        record = session.get(Record, record_id)
        if not record:
            return None

        for key, value in record_update.items():
            if hasattr(record, key):
                setattr(record, key, value)

        session.commit()
        session.refresh(record)
        return record

    @staticmethod
    def delete_record(session: Session, record_id: int) -> bool:
        """
        删除记账记录（软删除）

        Args:
            session: 数据库会话
            record_id: 记录 ID

        Returns:
            bool: 是否删除成功
        """
        record = session.get(Record, record_id)
        if not record:
            return False

        record.deleted = 1
        session.commit()
        return True