from flask import Flask

from .models import db
from .views import tracking

app = Flask(__name__)
app.config.from_object('config')  # 导入所有配置


@app.context_processor
def provide_constants():  # 在所有jinjia2模板中添加‘constants’变量
    return {"constants": {"TUTORIAL_PART": 1}}

db.init_app(app)  # db是sqlalchemy的实例，先初始化sqlalchemy的所有配置，然后让sqlalchemy中相关的配置(从config中导入的)生效
                  # 总而言之就是让sqlalchemy注册该app
app.register_blueprint(tracking)
