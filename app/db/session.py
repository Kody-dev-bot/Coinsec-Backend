from sqlmodel import create_engine, Session
from app.core.config import DatabaseConfig
from typing import Generator

# 创建数据库引擎
engine = create_engine(
    DatabaseConfig.get_database_url(),
    pool_size=DatabaseConfig.DB_POOL_SIZE,
    max_overflow=DatabaseConfig.DB_MAX_OVERFLOW,
    pool_timeout=DatabaseConfig.DB_POOL_TIMEOUT,
    pool_recycle=DatabaseConfig.DB_POOL_RECYCLE,
    echo=True # 生产环境中设为False，开发环境中可以设为True查看SQL语句
)


def get_session() -> Generator[Session, None, None]:
    """
    获取数据库会话
    
    Yields:
        Session: 数据库会话对象
    """
    with Session(engine) as session:
        yield session