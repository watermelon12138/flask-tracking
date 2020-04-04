from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CRUDMixin(object):  # 实现数据的增删改查(Create,Re,Update,Delete)简称CRUD
    __table_args__ = {'extend_existing': True}  # Table.extend_existing或Table.keep_existing
    # 这两个表参数必须指定其一，在创建表时，extend_existing=True表示如果表已经存在则覆盖，返回新表
    # keep_existing=True表示如果表存在则返回旧表，不覆盖
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def create(cls, commit=True, **kwargs):  # User继承了CRUDMixin，所以该类方法也是User中的类方法
        instance = cls(**kwargs)  # User或者User的实例调用create()方法时，cls表示的都是User类本身
        return instance.save(commit=commit)  #  所以上条语句等于: instance = User(**kwargs), 创建了一个User的实例

    @classmethod
    def get(cls, id):
        return cls.query.get(id)

    # We will also proxy Flask-SqlAlchemy's get_or_44
    # for symmetry
    @classmethod
    def get_or_404(cls, id):
        return cls.query.get_or_404(id)

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


def query_to_list(query, include_field_names=True):
    """Turns a SQLAlchemy query into a list of data values."""
    column_names = []
    for i, obj in enumerate(query.all()):
        if i == 0:
            column_names = [c.name for c in obj.__table__.columns]
            if include_field_names:
                yield column_names
        yield obj_to_list(obj, column_names)


def obj_to_list(sa_obj, field_order):
    """Takes a SQLAlchemy object - returns a list of all its data"""
    return [getattr(sa_obj, field_name, None) for field_name in field_order]
