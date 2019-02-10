from app.models.user import UserModel
from tests.base_test import BaseTest


class UserTest(BaseTest):
    def test_create_user(self):
        user = UserModel('test', '123')
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, '123')
