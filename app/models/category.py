from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="分类ID")
    user_id: int = Field(description="所属用户ID（0表示系统默认分类）")
    name: str = Field(max_length=50, description="分类名称（如餐饮、交通）")
    type: str = Field(max_length=20, description="类型（expense=支出/income=收入）")
    sort: int = Field(default=0, description="排序权重（越大越靠前）")
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")
    deleted: int = Field(default=0, description="是否删除（1=是/0=否）")

    __tablename__ = "category"
    
    class Config:
        table_args = {"comment": "记账分类表"}