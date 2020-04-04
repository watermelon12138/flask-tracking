from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_required, login_user, logout_user

from .forms import LoginForm, RegistrationForm
from .models import User

users = Blueprint('users', __name__)


@users.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash("Logged in successfully.")
        # There's a subtle security hole in this code, which we will be fixing in our next article.
        # Don't use this exact pattern in anything important.
        return redirect(request.args.get("next") or url_for("tracking.index"))
        # request.args可以拿到get请求中的所有参数，返回字典格式
        # request.form可以拿到post请求中的所有参数，返回字典格式
    return render_template('users/login.html', form=form)


@users.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('form.data: \n', form.data)  # 表单数据为字典格式
        # user = User.create(**form.data)
        # login_user(user)
        #                         # *表示拆分元组赋值。**表示拆分字典赋值，参数名必须对应key值。
        User.create(**form.data)  # User或者User的实例调用create()方法时，cls表示的都是User类本身。
        # 上语句的作用是用LoginForm表单的数据创建User表并保存到数据库
        return redirect(url_for('tracking.index'))  # url_for调用其它蓝图中的路由方法时必须加上蓝图名
    return render_template('users/register.html', form=form)


@users.route('/logout/')
@login_required  # 确保进行logout操作时user是loggedin状态
def logout():
    logout_user()
    return redirect(url_for('tracking.index'))
