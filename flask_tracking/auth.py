from flask.ext.login import AnonymousUserMixin, LoginManager

from flask_tracking.users.models import User

login_manager = LoginManager()


class AnonymousUser(AnonymousUserMixin):
    id = None


login_manager.anonymous_user = AnonymousUser
login_manager.login_view = "users.login"


@login_manager.user_loader  # user_loader是一个装饰器，利用装饰器实现回调函数的注册
def load_user(user_id):     # 即实现load_user(user_id)的注册，在LoginManager的实例调用reload_user()时会调用回调函数
    return User.query.get(user_id)  # LoginManager中有很多实现回调函数的注册的装饰器
