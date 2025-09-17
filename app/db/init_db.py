from sqlmodel import SQLModel
from app.db.session import engine


def init_db():
    """
    初始化数据库，创建所有表
    """
    # 创建所有表
    SQLModel.metadata.create_all(bind=engine)


def drop_db():
    """
    删除所有表（谨慎使用）
    """
    SQLModel.metadata.drop_all(bind=engine)