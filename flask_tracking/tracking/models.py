from flask_tracking.data import CRUDMixin, db


class Site(CRUDMixin, db.Model):
    __tablename__ = 'tracking_site'

    base_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    visits = db.relationship('Visit', backref='site', lazy='select')
    # visits = db.relationship('Visit', backref=db.backref('site', lazy='select'), lazy='select')
    # lazy='select'时，使用Site.visits和Visit.site会得到相应的查询结果，lazy的默认值就是select
    # lazy='dynamic'时，使用SiteSite.visits和Visit.site会得到查询语句的对象(BaseQueryObject)
    # lazy='dynamic只适用1对多或者多对多的关系中，而且必须写在1的那一侧
    def __repr__(self):
        return '<Site {:d} {}>'.format(self.id, self.base_url)

    def __str__(self):
        return self.base_url


class Visit(CRUDMixin, db.Model):  # 一个Site对象可以对应多个Visit对象
    __tablename__ = 'tracking_visit'
    browser = db.Column(db.String)
    date = db.Column(db.DateTime)
    event = db.Column(db.String)
    url = db.Column(db.String)
    ip_address = db.Column(db.String)
    location = db.Column(db.String)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    site_id = db.Column(db.Integer, db.ForeignKey('tracking_site.id'))

    def __repr__(self):
        r = '<Visit for site ID {:d}: {} - {:%Y-%m-%d %H:%M:%S}>'
        return r.format(self.site_id, self.url, self.date)
