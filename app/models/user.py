from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="用户ID")
    user_name: str = Field(max_length=50, description="用户名", sa_column_kwargs={"comment": "用户名"})
    password: str = Field(max_length=255, description="密码", sa_column_kwargs={"comment": "密码"})
    secret_key: str = Field(max_length=255, description="密码盐值,用于解密密码", sa_column_kwargs={"comment": "密码盐值,用于解密密码"})
    email: Optional[str] = Field(default=None, max_length=255, description="邮箱", sa_column_kwargs={"comment": "邮箱"})
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间", sa_column_kwargs={"comment": "创建时间"})
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间", sa_column_kwargs={"comment": "更新时间"})
    deleted: int = Field(default=0, description="是否删除（1=是/0=否）", sa_column_kwargs={"comment": "是否删除（1=是/0=否）"})
    
    __tablename__ = "user"
    
    class Config:
        table_args = {"comment": "系统用户表"}