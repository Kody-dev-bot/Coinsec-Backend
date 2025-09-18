import pytest
from unittest.mock import Mock
from sqlmodel import Session
from datetime import datetime

from app.crud.keyword import KeywordCRUD
from app.models.keyword import Keyword


class TestKeywordCRUD:
    """KeywordCRUD 类的测试"""

    @pytest.fixture
    def mock_session(self):
        """创建模拟数据库会话"""
        return Mock(spec=Session)

    @pytest.fixture
    def sample_keyword(self):
        """创建示例关键词对象"""
        return Keyword(
            id=1,
            category_id=1,
            word="餐饮",
            type="category",
            deleted=0,
            create_time=datetime.now(),
            update_time=datetime.now()
        )

    def test_create_keyword(self, mock_session, sample_keyword):
        """测试创建关键词"""
        # 设置模拟行为
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # 调用方法
        result = KeywordCRUD.create_keyword(mock_session, sample_keyword)
        
        # 验证调用
        mock_session.add.assert_called_once_with(sample_keyword)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_keyword)
        assert result == sample_keyword

    def test_get_keyword_exists(self, mock_session, sample_keyword):
        """测试获取存在的关键词"""
        # 设置模拟行为
        mock_session.get.return_value = sample_keyword
        
        # 调用方法
        result = KeywordCRUD.get_keyword(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Keyword, 1)
        assert result == sample_keyword

    def test_get_keyword_not_exists(self, mock_session):
        """测试获取不存在的关键词"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = KeywordCRUD.get_keyword(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Keyword, 999)
        assert result is None

    def test_get_keywords(self, mock_session):
        """测试获取关键词列表"""
        # 创建示例数据
        keywords = [
            Keyword(id=1, category_id=1, word="餐饮", type="category", deleted=0,
                    create_time=datetime.now(), update_time=datetime.now()),
            Keyword(id=2, category_id=1, word="吃饭", type="category", deleted=0,
                    create_time=datetime.now(), update_time=datetime.now())
        ]
        
        # 设置模拟行为
        mock_exec = Mock()
        mock_exec.all.return_value = keywords
        mock_session.exec.return_value = mock_exec
        
        # 调用方法
        result = KeywordCRUD.get_keywords(mock_session, word="餐", category_id=1)
        
        # 验证调用和结果
        assert len(result) == 2
        assert result[0].word == "餐饮"
        assert result[1].word == "吃饭"

    def test_update_keyword_success(self, mock_session, sample_keyword):
        """测试成功更新关键词"""
        # 设置模拟行为
        mock_session.get.return_value = sample_keyword
        
        # 调用方法
        update_data = {"word": "新关键词", "type": "amount"}
        result = KeywordCRUD.update_keyword(mock_session, 1, update_data)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Keyword, 1)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_keyword)
        assert result.word == "新关键词"
        assert result.type == "amount"

    def test_update_keyword_not_exists(self, mock_session):
        """测试更新不存在的关键词"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = KeywordCRUD.update_keyword(mock_session, 999, {"word": "新关键词"})
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Keyword, 999)
        assert result is None

    def test_delete_keyword_success(self, mock_session, sample_keyword):
        """测试成功删除关键词"""
        # 设置模拟行为
        mock_session.get.return_value = sample_keyword
        
        # 调用方法
        result = KeywordCRUD.delete_keyword(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Keyword, 1)
        mock_session.commit.assert_called_once()
        assert result is True
        assert sample_keyword.deleted == 1

    def test_delete_keyword_not_exists(self, mock_session):
        """测试删除不存在的关键词"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = KeywordCRUD.delete_keyword(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Keyword, 999)
        assert result is False