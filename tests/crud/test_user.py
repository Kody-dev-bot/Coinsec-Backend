import pytest
from unittest.mock import Mock
from sqlmodel import Session

from app.crud.user import UserCRUD
from app.models.user import User


class TestUserCRUD:
    """UserCRUD 类的测试"""

    @pytest.fixture
    def mock_session(self):
        """创建模拟数据库会话"""
        return Mock(spec=Session)

    @pytest.fixture
    def sample_user(self):
        """创建示例用户对象"""
        return User(
            id=1,
            user_name="testuser",
            email="test@example.com",
            deleted=0
        )

    def test_create_user(self, mock_session, sample_user):
        """测试创建用户"""
        # 设置模拟行为
        mock_session.add = Mock()
        mock_session.commit = Mock()
        mock_session.refresh = Mock()
        
        # 调用方法
        result = UserCRUD.create_user(mock_session, sample_user)
        
        # 验证调用
        mock_session.add.assert_called_once_with(sample_user)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_user)
        assert result == sample_user

    def test_get_user_exists(self, mock_session, sample_user):
        """测试获取存在的用户"""
        # 设置模拟行为
        mock_session.get.return_value = sample_user
        
        # 调用方法
        result = UserCRUD.get_user(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 1)
        assert result == sample_user

    def test_get_user_not_exists(self, mock_session):
        """测试获取不存在的用户"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = UserCRUD.get_user(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 999)
        assert result is None

    def test_get_user_deleted(self, mock_session):
        """测试获取已删除的用户"""
        deleted_user = User(
            id=1,
            user_name="testuser",
            email="test@example.com",
            deleted=1
        )
        
        # 设置模拟行为
        mock_session.get.return_value = deleted_user
        
        # 调用方法
        result = UserCRUD.get_user(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 1)
        assert result is None

    def test_get_user_by_name_exists(self, mock_session, sample_user):
        """测试根据用户名获取存在的用户"""
        # 设置模拟行为
        mock_exec = Mock()
        mock_exec.first.return_value = sample_user
        mock_session.exec.return_value = mock_exec
        
        # 调用方法
        result = UserCRUD.get_user_by_name(mock_session, "testuser")
        
        # 验证调用和结果
        assert result == sample_user

    def test_get_user_by_name_not_exists(self, mock_session):
        """测试根据用户名获取不存在的用户"""
        # 设置模拟行为
        mock_exec = Mock()
        mock_exec.first.return_value = None
        mock_session.exec.return_value = mock_exec
        
        # 调用方法
        result = UserCRUD.get_user_by_name(mock_session, "nonexistent")
        
        # 验证调用和结果
        assert result is None

    def test_get_users(self, mock_session):
        """测试获取用户列表"""
        # 创建示例数据
        users = [
            User(id=1, user_name="testuser1", email="test1@example.com", deleted=0),
            User(id=2, user_name="testuser2", email="test2@example.com", deleted=0)
        ]
        
        # 设置模拟行为
        mock_exec = Mock()
        mock_exec.all.return_value = users
        mock_session.exec.return_value = mock_exec
        
        # 调用方法
        result = UserCRUD.get_users(mock_session)
        
        # 验证调用和结果
        assert len(result) == 2
        assert result[0].user_name == "testuser1"
        assert result[1].user_name == "testuser2"

    def test_update_user_success(self, mock_session, sample_user):
        """测试成功更新用户"""
        # 设置模拟行为
        mock_session.get.return_value = sample_user
        
        # 调用方法
        update_data = {"user_name": "newusername", "email": "new@example.com"}
        result = UserCRUD.update_user(mock_session, 1, update_data)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 1)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(sample_user)
        assert result.user_name == "newusername"
        assert result.email == "new@example.com"

    def test_update_user_not_exists(self, mock_session):
        """测试更新不存在的用户"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = UserCRUD.update_user(mock_session, 999, {"user_name": "newuser"})
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 999)
        assert result is None

    def test_update_user_deleted(self, mock_session):
        """测试更新已删除的用户"""
        deleted_user = User(
            id=1,
            user_name="testuser",
            email="test@example.com",
            deleted=1
        )
        
        # 设置模拟行为
        mock_session.get.return_value = deleted_user
        
        # 调用方法
        result = UserCRUD.update_user(mock_session, 1, {"user_name": "newuser"})
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 1)
        assert result is None

    def test_delete_user_success(self, mock_session, sample_user):
        """测试成功删除用户"""
        # 设置模拟行为
        mock_session.get.return_value = sample_user
        
        # 调用方法
        result = UserCRUD.delete_user(mock_session, 1)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 1)
        mock_session.commit.assert_called_once()
        assert result is True
        assert sample_user.deleted == 1

    def test_delete_user_not_exists(self, mock_session):
        """测试删除不存在的用户"""
        # 设置模拟行为
        mock_session.get.return_value = None
        
        # 调用方法
        result = UserCRUD.delete_user(mock_session, 999)
        
        # 验证调用和结果
        mock_session.get.assert_called_once_with(User, 999)
        assert result is False