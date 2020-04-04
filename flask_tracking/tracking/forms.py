from datetime import datetime as dt

from flask.ext.wtf import Form
from wtforms import fields
from wtforms.validators import InputRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import Site


class SiteForm(Form):
    base_url = fields.StringField(validators=[InputRequired()])


class VisitForm(Form):
    browser = fields.StringField()
    date = fields.DateField(default=dt.now)
    event = fields.StringField()
    url = fields.StringField(validators=[InputRequired()])
    ip_address = fields.StringField()
    site = QuerySelectField(validators=[InputRequired()], query_factory=lambda: Site.query.all())