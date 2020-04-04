from flask import Flask

from .auth import login_manager
from .data import db
from .tracking.views import tracking
from .users.views import users

app = Flask(__name__)
app.config.from_object('config')


@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 2}}

db.init_app(app)  #
login_manager.init_app(app)  # 先初始化，然后再使用app中跟其有关的配置

app.register_blueprint(tracking)
app.register_blueprint(users)
