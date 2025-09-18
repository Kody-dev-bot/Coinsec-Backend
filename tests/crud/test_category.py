import pytest
from unittest.mock import Mock, MagicMock
from sqlmodel import Session

from app.crud.category import CategoryCRUD
from app.models.category import Category


class TestCategoryCRUD:
    """CategoryCRUD 类的测试"""

    @pytest.fixture
    def mock_session(self):
        """创建模拟数据库会话"""
        return Mock(spec=Session)

    @pytest.fixture
    def sample_category(self):
        """创建示例分类对象"""
        return Category(
            id=1,
            user_id=0,
            name="餐饮",
            type="expense",
            sort=1,
            deleted=0
        )

    def test_create_category(self, mock_session, sample_category):
        """测试创建分类"""
        # 设置模拟行为
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # 调用方法
        result = CategoryCRUD.create_category(mock_session, sample_category)
        
        # 验证调用
        mock_session.add.assert_called_once_with(sample_category)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_category)
        assert result == sample_category

    def test_get_category_exists(self, mock_session, sample_category):
        """测试获取存在的分类"""
        # 设置模拟行为
        mock_session.get.return_value = sample_category
        
        # 调用方法
        result = CategoryCRUD.get_category(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Category, 1)
        assert result == sample_category

    def test_get_category_not_exists(self, mock_session):
        """测试获取不存在的分类"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = CategoryCRUD.get_category(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Category, 999)
        assert result is None

    def test_get_category_deleted(self, mock_session):
        """测试获取已删除的分类"""
        deleted_category = Category(
            id=1,
            user_id=0,
            name="餐饮",
            type="expense",
            sort=1,
            deleted=1
        )
        
        # 设置模拟行为
        mock_session.get.return_value = deleted_category
        
        # 调用方法
        result = CategoryCRUD.get_category(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Category, 1)
        assert result is None

    def test_get_categories(self, mock_session):
        """测试获取分类列表"""
        # 创建示例数据
        categories = [
            Category(id=1, user_id=0, name="餐饮", type="expense", sort=1, deleted=0),
            Category(id=2, user_id=0, name="交通", type="expense", sort=2, deleted=0)
        ]
        
        # 设置模拟行为
        mock_exec = Mock()
        mock_exec.all.return_value = categories
        mock_session.exec.return_value = mock_exec
        
        # 调用方法
        result = CategoryCRUD.get_categories(mock_session, user_id=0, category_type="expense")
        
        # 验证调用和结果
        assert len(result) == 2
        assert result[0].name == "餐饮"
        assert result[1].name == "交通"

    def test_update_category_success(self, mock_session, sample_category):
        """测试成功更新分类"""
        # 设置模拟行为
        mock_session.get.return_value = sample_category
        
        # 调用方法
        update_data = {"name": "新分类名称", "sort": 2}
        result = CategoryCRUD.update_category(mock_session, 1, update_data)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Category, 1)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_category)
        assert result.name == "新分类名称"
        assert result.sort == 2

    def test_update_category_not_exists(self, mock_session):
        """测试更新不存在的分类"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = CategoryCRUD.update_category(mock_session, 999, {"name": "新名称"})
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Category, 999)
        assert result is None

    def test_delete_category_success(self, mock_session, sample_category):
        """测试成功删除分类"""
        # 设置模拟行为
        mock_session.get.return_value = sample_category
        
        # 调用方法
        result = CategoryCRUD.delete_category(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Category, 1)
        mock_session.commit.assert_called_once()
        assert result is True
        assert sample_category.deleted == 1

    def test_delete_category_not_exists(self, mock_session):
        """测试删除不存在的分类"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = CategoryCRUD.delete_category(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(Category, 999)
        assert result is False