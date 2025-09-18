import pytest
from unittest.mock import Mock
from sqlmodel import Session
from datetime import datetime
from decimal import Decimal

from app.crud.record import RecordCRUD
from app.models.record import Record


class TestRecordCRUD:
    """RecordCRUD 类的测试"""

    @pytest.fixture
    def mock_session(self):
        """创建模拟数据库会话"""
        return Mock(spec=Session)

    @pytest.fixture
    def sample_record(self):
        """创建示例记账记录对象"""
        return Record(
            id=1,
            user_id=1,
            original_text="餐饮消费",
            amount=Decimal('100.00'),
            type="expense",
            category_id=1,
            record_time=datetime.now(),
            deleted=0
        )

    def test_create_record(self, mock_session, sample_record):
        """测试创建记账记录"""
        # 设置模拟行为
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # 调用方法
        result = RecordCRUD.create_record(mock_session, sample_record)
        
        # 验证调用
        mock_session.add.assert_called_once_with(sample_record)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_record)
        assert result == sample_record

    def test_get_record_exists(self, mock_session, sample_record):
        """测试获取存在的记账记录"""
        # 设置模拟行为
        mock_session.get.return_value = sample_record
        
        # 调用方法
        result = RecordCRUD.get_record(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Record, 1)
        assert result == sample_record

    def test_get_record_not_exists(self, mock_session):
        """测试获取不存在的记账记录"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = RecordCRUD.get_record(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Record, 999)
        assert result is None

    def test_get_records(self, mock_session):
        """测试获取记账记录列表"""
        # 创建示例数据
        records = [
            Record(id=1, user_id=1, original_text="餐饮消费", amount=Decimal('100.00'), 
                   type="expense", category_id=1, record_time=datetime.now(), deleted=0),
            Record(id=2, user_id=1, original_text="交通费用", amount=Decimal('50.00'), 
                   type="expense", category_id=2, record_time=datetime.now(), deleted=0)
        ]
        
        # 设置模拟行为
        mock_exec = Mock()
        mock_exec.all.return_value = records
        mock_session.exec.return_value = mock_exec
        
        # 调用方法
        result = RecordCRUD.get_records(mock_session, user_id=1, record_type="expense")
        
        # 验证调用和结果
        assert len(result) == 2
        assert result[0].original_text == "餐饮消费"
        assert result[1].original_text == "交通费用"

    def test_update_record_success(self, mock_session, sample_record):
        """测试成功更新记账记录"""
        # 设置模拟行为
        mock_session.get.return_value = sample_record
        
        # 调用方法
        update_data = {"amount": Decimal('150.00'), "original_text": "新描述"}
        result = RecordCRUD.update_record(mock_session, 1, update_data)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Record, 1)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_record)
        assert result.amount == Decimal('150.00')
        assert result.original_text == "新描述"

    def test_update_record_not_exists(self, mock_session):
        """测试更新不存在的记账记录"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = RecordCRUD.update_record(mock_session, 999, {"amount": Decimal('200.00')})
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Record, 999)
        assert result is None

    def test_delete_record_success(self, mock_session, sample_record):
        """测试成功删除记账记录"""
        # 设置模拟行为
        mock_session.get.return_value = sample_record
        
        # 调用方法
        result = RecordCRUD.delete_record(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Record, 1)
        mock_session.commit.assert_called_once()
        assert result is True
        assert sample_record.deleted == 1

    def test_delete_record_not_exists(self, mock_session):
        """测试删除不存在的记账记录"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = RecordCRUD.delete_record(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Record, 999)
        assert result is False