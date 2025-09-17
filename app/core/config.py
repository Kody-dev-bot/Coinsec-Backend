import os
from typing import Optional


class DatabaseConfig:
    # 数据库配置
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: int = int(os.environ.get("DB_PORT", 3306))
    DB_USER: str = os.environ.get("DB_USER", "root")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")
    DB_NAME: str = os.environ.get("DB_NAME", "coinsec")
    DB_CHARSET: str = os.environ.get("DB_CHARSET", "utf8mb4")
    
    # 数据库连接池配置
    DB_POOL_SIZE: int = int(os.environ.get("DB_POOL_SIZE", 10))
    DB_MAX_OVERFLOW: int = int(os.environ.get("DB_MAX_OVERFLOW", 20))
    DB_POOL_TIMEOUT: int = int(os.environ.get("DB_POOL_TIMEOUT", 30))
    DB_POOL_RECYCLE: int = int(os.environ.get("DB_POOL_RECYCLE", 3600))
    
    @classmethod
    def get_database_url(cls) -> str:
        """生成数据库连接URL"""
        if cls.DB_PASSWORD:
            return f"mysql+pymysql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}?charset={cls.DB_CHARSET}"
        else:
            return f"mysql+pymysql://{cls.DB_USER}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}?charset={cls.DB_CHARSET}"