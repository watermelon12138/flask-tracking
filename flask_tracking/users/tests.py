from flask import url_for
from flask.ext.login import current_user

from flask_tracking.test_base import BaseTestCase
from .models import User


class UserViewsTests(BaseTestCase):
    def test_users_can_login(self):
        User.create(name="Joe", email="joe@joes.com", password="12345")

        with self.client:  # self.client = self.app.test_client()
            response = self.client.post(url_for("users.login"),
                                        data={"email": "joe@joes.com",
                                              "password": "12345"})

            self.assert_redirects(response, url_for("tracking.index"))  # 判断重定向的位置是否一致
            self.assertTrue(current_user.name == "Joe")
            self.assertFalse(current_user.is_anonymous())

    def test_users_can_logout(self):
        User.create(name="Joe", email="joe@joes.com", password="12345")

        with self.client:
            self.client.post(url_for("users.login"),
                             data={"email": "joe@joes.com",
                                   "password": "12345"})
            self.client.get(url_for("users.logout"))

            self.assertTrue(current_user.is_anonymous())

    def test_invalid_password_is_rejected(self):
        User.create(name="Joe", email="joe@joes.com", password="12345")

        with self.client:
            response = self.client.post(url_for("users.login"),
                                        data={"email": "joe@joes.com",
                                              "password": "*****"})

            self.assertTrue(current_user.is_anonymous())
            self.assert_200(response)  # 验证response.status_code是否为200
            self.assertIn(b"Invalid password", response.data)  # response.data中是否有'Invalid password', 需要字节类型哦

    def test_user_can_register_account(self):
        with self.client:
            response = self.client.post(url_for("users.register"),
                                        data={"email": "test@ing.com",
                                              "password": "5555"})

            self.assert_redirects(response, url_for("tracking.index"))
            self.assertFalse(current_user.is_anonymous())
            self.assertEqual(current_user.email, "test@ing.com")

    def test_user_is_redirected_to_index_from_logout(self):
        with self.client:
            #  有点问题哦
            response = self.client.get(url_for("users.logout"))
            self.assert_redirects(response, url_for("tracking.index"))
            self.assertTrue(current_user.is_anonymous())
