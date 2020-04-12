from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask.ext.login import login_user, logout_user
from flask import current_app
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
    return render_template('users/login.html', form=form)

# def login():  # 进入pbd模式进行调试
#     form = LoginForm(request.form)
#     import pdb; pdb.set_trace()


@users.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.create(**form.data)
        login_user(user)
        return redirect(url_for('tracking.index'))
    return render_template('users/register.html', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('tracking.index'))

# def logout():  # 生成特定的日志信息
#     current_app.debug('Attempting to log out the current user')
#     logout_user()
#     current_app.debug('Successfully logged out the current user')
#     return redirect(url_for('tracking.index'))