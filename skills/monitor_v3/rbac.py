#!/usr/bin/env python3
"""
RBAC 權限管理 - Agent Monitor v3

功能：
- 角色權限控制
- 用戶認證
- 權限檢查
"""

import hashlib
import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class Role(Enum):
    """角色"""
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    GUEST = "guest"


class Action(Enum):
    """操作"""
    # 讀取
    READ_LOGS = "read:logs"
    READ_TRACES = "read:traces"
    READ_METRICS = "read:metrics"
    READ_ALERTS = "read:alerts"
    READ_SESSIONS = "read:sessions"
    READ_CONFIG = "read:config"
    
    # 寫入
    WRITE_LOGS = "write:logs"
    WRITE_TRACES = "write:traces"
    WRITE_ALERTS = "write:alerts"
    WRITE_CONFIG = "write:config"
    
    # 管理
    MANAGE_USERS = "manage:users"
    MANAGE_ROLES = "manage:roles"
    MANAGE_ALERTS = "manage:alerts"
    MANAGE_SYSTEM = "manage:system"
    
    # 全部
    ALL = "*"


# 角色權限映射
ROLE_PERMISSIONS = {
    Role.ADMIN: [Action.ALL],
    Role.EDITOR: [
        Action.READ_LOGS,
        Action.READ_TRACES,
        Action.READ_METRICS,
        Action.READ_ALERTS,
        Action.READ_SESSIONS,
        Action.WRITE_LOGS,
        Action.WRITE_TRACES,
        Action.WRITE_ALERTS,
    ],
    Role.VIEWER: [
        Action.READ_LOGS,
        Action.READ_TRACES,
        Action.READ_METRICS,
        Action.READ_ALERTS,
        Action.READ_SESSIONS,
    ],
    Role.GUEST: [
        Action.READ_LOGS,
    ],
}


@dataclass
class User:
    """用戶"""
    user_id: str
    username: str
    role: str
    email: str = None
    created_at: str = None
    last_login: str = None
    metadata: Dict = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}


class RBAC:
    """RBAC 權限管理"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.getenv(
            "RBAC_CONFIG_PATH",
            "./data/rbac.json"
        )
        self.users: Dict[str, User] = {}
        self._load()
    
    def _load(self):
        """從文件加載"""
        try:
            with open(self.config_path, "r") as f:
                data = json.load(f)
                
                # 加載用戶
                for user_data in data.get("users", []):
                    user = User(**user_data)
                    self.users[user.user_id] = user
        except FileNotFoundError:
            # 創建默認管理員
            self._create_default_admin()
    
    def _save(self):
        """保存到文件"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        
        data = {
            "users": [asdict(u) for u in self.users.values()]
        }
        
        with open(self.config_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def _create_default_admin(self):
        """創建默認管理員"""
        admin = User(
            user_id="admin",
            username="admin",
            role=Role.ADMIN.value,
            email="admin@localhost"
        )
        self.users["admin"] = admin
        self._save()
    
    def hash_password(self, password: str) -> str:
        """密碼哈希"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """驗證密碼"""
        return self.hash_password(password) == hashed
    
    # ============== 用戶管理 ==============
    
    def create_user(
        self,
        user_id: str,
        username: str,
        role: str = "viewer",
        email: str = None,
        password: str = None
    ) -> User:
        """創建用戶"""
        user = User(
            user_id=user_id,
            username=username,
            role=role,
            email=email
        )
        self.users[user_id] = user
        self._save()
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """獲取用戶"""
        return self.users.get(user_id)
    
    def list_users(self) -> List[User]:
        """列出所有用戶"""
        return list(self.users.values())
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """更新用戶"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self._save()
        return True
    
    def delete_user(self, user_id: str) -> bool:
        """刪除用戶"""
        if user_id in self.users:
            del self.users[user_id]
            self._save()
            return True
        return False
    
    # ============== 權限檢查 ==============
    
    def get_role_permissions(self, role: str) -> List[Action]:
        """獲取角色權限"""
        try:
            role_enum = Role(role)
            return ROLE_PERMISSIONS.get(role_enum, [])
        except ValueError:
            return []
    
    def check_permission(
        self,
        user_id: str,
        action: str,
        resource_id: str = None
    ) -> bool:
        """檢查權限"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        # 管理員擁有所有權限
        if user.role == Role.ADMIN.value:
            return True
        
        # 獲取權限列表
        permissions = self.get_role_permissions(user.role)
        
        # 檢查權限
        for perm in permissions:
            if perm == Action.ALL:
                return True
            
            if perm.value == action:
                return True
            
            # 前綴匹配
            if action.startswith(perm.value.split(":")[0]):
                return True
        
        # 資源級別檢查
        if resource_id and user.role in [Role.EDITOR.value, Role.VIEWER.value]:
            # 簡單的資源擁有者檢查
            if resource_id.startswith(user_id):
                return True
        
        return False
    
    def require_permission(self, user_id: str, action: str):
        """require decorator 裝飾器支持"""
        if not self.check_permission(user_id, action):
            raise PermissionError(f"Permission denied: {action}")
    
    # ============== 認證 ==============
    
    def authenticate(
        self,
        username: str,
        password: str,
        password_hash: str = None
    ) -> Optional[User]:
        """認證用戶"""
        for user in self.users.values():
            if user.username == username:
                # 如果提供密碼哈希，驗證
                if password_hash:
                    if self.verify_password(password, password_hash):
                        user.last_login = datetime.now().isoformat()
                        self._save()
                        return user
                else:
                    # 嘗試直接密碼（不推薦）
                    if password == "admin":  # 簡單默認密碼
                        user.last_login = datetime.now().isoformat()
                        self._save()
                        return user
        
        return None
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """登入"""
        user = self.authenticate(username, password)
        if user:
            return {
                "user_id": user.user_id,
                "username": user.username,
                "role": user.role,
                "token": self._generate_token(user.user_id)
            }
        return None
    
    def _generate_token(self, user_id: str) -> str:
        """生成 token"""
        import secrets
        return hashlib.sha256(
            f"{user_id}{datetime.now().isoformat()}{secrets.token_hex(16)}".encode()
        ).hexdigest()


# ============== 快捷函數 ==============

rbac = RBAC()


def check_permission(user_id: str, action: str) -> bool:
    """快捷權限檢查"""
    return rbac.check_permission(user_id, action)


def require(user_id: str, action: str):
    """快捷權限要求"""
    rbac.require_permission(user_id, action)


# ============== 主程式 ==============

if __name__ == "__main__":
    print("=" * 50)
    print("🔐 RBAC Test")
    print("=" * 50)
    
    # 測試權限
    print("\n📋 Role permissions:")
    for role in Role:
        perms = rbac.get_role_permissions(role.value)
        print(f"  {role.value}: {[p.value for p in perms[:3]]}...")
    
    # 測試權限檢查
    print("\n🔍 Permission checks:")
    print(f"  admin -> *: {rbac.check_permission('admin', 'read:logs')}")
    print(f"  editor -> *: {rbac.check_permission('editor', 'read:logs')}")
    print(f"  viewer -> write:logs: {rbac.check_permission('viewer', 'write:logs')}")
    
    # 列出用戶
    print("\n👥 Users:")
    for user in rbac.list_users():
        print(f"  {user.username}: {user.role}")
    
    print("\n✅ RBAC test complete!")
