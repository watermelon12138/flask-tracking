from random import SystemRandom

from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property

from flask_tracking.data import CRUDMixin, db


class User(UserMixin, CRUDMixin, db.Model):  # 继承3个类，User的实例可以使用这三个类中的属性和方法
    __tablename__ = 'users_user'
    # __table_args__ = {'extend_existing': True}     继承CRUDMixin
    # id = db.Column(db.Integer, primary_key=True)   继承CRUDMixin
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    _password = db.Column(db.LargeBinary(120))
    _salt = db.Column(db.String(120))
    sites = db.relationship('Site', backref='owner', lazy='dynamic')

    @hybrid_property
    def password(self):  # 将该方法标记为一个属性，名为password，该类的实例可以直接当作属性来调用
        return self._password  # 如：user = User(), user.password

    # In order to ensure that passwords are always stored
    # hashed and salted in our database we use a descriptor
    # here which will automatically hash our password
    # when we provide it (i. e. user.password = "12345")

    # hashed and salted 经过哈希算法并且随机生成
    @password.setter
    def password(self, value):  # password属性的描述器，当给password赋值的时候就是调用该方法
        # When a user is first created, give them a salt
        if self._salt is None:
            self._salt = str(SystemRandom().getrandbits(128))  # 指定128个比特位，随机返回一个0到2**128-1之间的整数
            self._salt = self._salt.encode("utf-8")
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        """Ensure that the provided password is valid.

        We are using this instead of a ``sqlalchemy.types.TypeDecorator``
        (which would let us write ``User.password == password`` and have the incoming
        ``password`` be automatically hashed in a SQLAlchemy query)
        because ``compare_digest`` properly compares **all***
        the characters of the hash even when they do not match in order to
        avoid timing oracle side-channel attacks."""
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._password)  # 常数时间比较两个hash值

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)
        buff = pbkdf2_hmac("sha512", pwd, salt, iterations=100000)  # 加密
        return bytes(buff)

    def __repr__(self):
        return "<User #{:d}>".format(self.id)
