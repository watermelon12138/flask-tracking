from flask.ext.testing import TestCase

from . import app, db


class BaseTestCase(TestCase):
    """A base test case for flask-tracking."""

    def create_app(self):
        app.config.from_object('config.TestConfiguration')
        return app

    def setUp(self):  # 每个测试开始前自动执行
        db.create_all()

    def tearDown(self):  # 每个测试结束后自动执行
        db.session.remove()
        db.drop_all()
