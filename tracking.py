from os.path import abspath, dirname, join
from flask import flash, Flask, Markup, redirect, render_template, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import fields
from wtforms.ext.sqlalchemy.fields import QuerySelectField

_cwd = dirname(abspath(__file__))

SECRET_KEY = 'flask-session-insecure-secret-key'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + join(_cwd, 'flask-tracking.db')
SQLALCHEMY_ECHO = True
WTF_CSRF_SECRET_KEY = 'this-should-be-more-random'  # 用于生成安全令牌的随机数据。如果未设置，则使用SECRET_KEY


app = Flask(__name__)
app.config.from_object(__name__)  # flask从本模块加载配置，配置名必须英文大写

db = SQLAlchemy(app)


class Site(db.Model):
    __tablename__ = 'tracking_site'

    id = db.Column(db.Integer, primary_key=True)
    base_url = db.Column(db.String)
    visits = db.relationship('Visit', backref='tracking_site', lazy='select')

    def __repr__(self):
        return '<Site %r>' % self.base_url

    def __str__(self):
        return self.base_url


class Visit(db.Model):
    __tablename__ = 'tracking_visit'

    id = db.Column(db.Integer, primary_key=True)
    browser = db.Column(db.String)
    date = db.Column(db.DateTime)
    event = db.Column(db.String)
    url = db.Column(db.String)
    ip_address = db.Column(db.String)
    site_id = db.Column(db.Integer, db.ForeignKey('tracking_site.id'))

    def __repr__(self):
        return '<Visit %r - %r>' % (self.url, self.date)


class VisitForm(Form):
    browser = fields.StringField()
    date = fields.DateField()
    event = fields.StringField()
    url = fields.StringField()
    ip_address = fields.StringField("IP Address")
    site = QuerySelectField(query_factory=Site.query.all)  # 实时查询数据库并显示


class SiteForm(Form):
    base_url = fields.StringField()


@app.route("/")
def index():
    site_form = SiteForm()
    visit_form = VisitForm()
    return render_template("index.html",
                           site_form=site_form,
                           visit_form=visit_form)


@app.route("/site", methods=("POST", ))
def add_site():
    form = SiteForm()
    if form.validate_on_submit():
        site = Site()
        form.populate_obj(site)  # 将表单中fields的值去填充site的fields的值，field的名称必须对应
        db.session.add(site)  # 将该表添加到数据库中
        db.session.commit()
        flash("Added site")  # 消息闪现
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)


@app.route("/visit", methods=("POST", ))
def add_visit():
    form = VisitForm()
    if form.validate_on_submit():
        visit = Visit()
        form.populate_obj(visit)
        visit.site_id = form.site.data.id
        db.session.add(visit)
        db.session.commit()
        flash("Added visit for site " + form.site.data.base_url)
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)


@app.route("/sites")
def view_sites():
    query = Site.query.filter(Site.id >= 0)
    data = query_to_list(query)  # data是迭代器
    # try:
    #     for row in data:
    #         print('row: \n', row)
    # except StopIteration:
    #     pass
    data = [next(data)] + [[_make_link(cell) if i == 0 else cell for i, cell in enumerate(row)] for row in data]
    # print('data: \n', data)  [[id, base_url], [超链接1，网址],[超链接2，网址], [超链接3，网址]]
    return render_template("data_list.html", data=iter(data), type="Sites")


_LINK = Markup('<a href="{url}">{name}</a>')


def _make_link(site_id):
    url = url_for("view_site_visits", site_id=site_id)
    return _LINK.format(url=url, name=site_id)


@app.route("/site/<int:site_id>")
def view_site_visits(site_id=None):
    site = Site.query.get_or_404(site_id)
    query = Visit.query.filter(Visit.site_id == site_id)  # query此时是BaseQuery类对象，加上all()才有结果
    # print('query: \n', type(query))
    # print('query.all: \n', query.all())
    data = query_to_list(query)  # 生成器返回的是一个迭代器
    # print('data: \n', data)
    title = "visits for " + site.base_url
    return render_template("data_list.html", data=data, type=title)


def query_to_list(query, include_field_names=True):  # 生成器
    """Turns a SQLAlchemy query into a list of data values."""
    column_names = []
    for i, obj in enumerate(query.all()):
        # print('%d:' % i)
        # print(obj)
        # print(type(obj))
        if i == 0:
            column_names = [c.name for c in obj.__table__.columns]
            # print('column_names:\n', column_names)
            if include_field_names:
                yield column_names
        yield obj_to_list(obj, column_names)


def obj_to_list(sa_obj, field_order):
    """Takes a SQLAlchemy object - returns a list of all its data"""
    return [getattr(sa_obj, field_name, None) for field_name in field_order]

if __name__ == "__main__":
    app.debug = True
    db.create_all()
    app.run()
