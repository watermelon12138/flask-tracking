from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Site


class SiteForm(Form):
    base_url = fields.StringField()


class VisitForm(Form):
    browser = fields.StringField()
    date = fields.DateField()
    event = fields.StringField()
    url = fields.StringField()
    ip_address = fields.StringField("IP Address")
    site = QuerySelectField(query_factory=lambda: Site.query.all())  # lambda是一个函数，
    # 确保VisitForm实例化时才执行查询语句，以为此时Site表还没建立
