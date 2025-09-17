from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime

class Keyword(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="关键词ID")
    word: str = Field(max_length=100, description="关键词内容")
    type: str = Field(max_length=50, description="关键词类型（如amount=金额/category=分类/type=收支类型）")
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", description="关联分类ID（可选）")
    user_id: Optional[int] = Field(default=None, description="所属用户ID（NULL表示系统关键词）")
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")
    deleted: int = Field(default=0, description="是否删除（1=是/0=否）")
    

    __tablename__ = "keyword"
    
    class Config:
        table_args = {"comment": "关键词表"}