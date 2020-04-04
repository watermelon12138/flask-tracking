from flask.ext.wtf import Form
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound  # 导入异常
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError
from .models import User


class LoginForm(Form):
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.StringField(validators=[InputRequired()])

    # WTForms supports "inline" validators
    # of the form `validate_[fieldname]`.
    # This validator will run after all the
    # other validators have passed.
    # WTForms支持“ validate_ [fieldname]”形式的“内联”验证器。
    # 该验证器将在所有其他验证器(定义field时所定义的验证器)通过后运行。
    def validate_password(self, field):  # 给password添加内联验证器，self是LoginForm的某个实例，field是实例中的password
        try:
            user = User.query.filter(User.email == self.email.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Invalid user")
        if user is None:
            raise ValidationError("Invalid user")
        if not user.is_valid_password(field.data):
            raise ValidationError("Invalid password")

        # Make the current user available
        # to calling code.
        self.user = user  # 验证成功的表单，给它添加一个user属性


class RegistrationForm(Form):
    name = fields.StringField("Display Name")
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.StringField(validators=[InputRequired()])

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user is not None:
            raise ValidationError("A user with that email already exists")
