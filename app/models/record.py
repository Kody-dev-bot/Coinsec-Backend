from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from decimal import Decimal

class Record(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, description="记录ID")
    user_id: int = Field(description="用户ID")
    original_text: str = Field(max_length=500, description="用户原始对话文本（如\"今天吃饭花了50元\"）")
    amount: Decimal = Field(description="金额", max_digits=10, decimal_places=2)
    type: str = Field(max_length=20, description="类型（expense=支出/income=收入）")
    category_id: int = Field(description="分类ID（关联category表）")
    record_time: datetime = Field(description="记账发生时间（如2023-10-10 12:00:00）")
    note: Optional[str] = Field(default=None, max_length=500, description="备注（从文本中提取）")
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")
    deleted: int = Field(default=0, description="是否删除（1=是/0=否）")
    
    __tablename__ = "record"
    
    class Config:
        table_args = {"comment": "记账记录表"}