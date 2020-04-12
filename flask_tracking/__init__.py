from flask import Flask

from .auth import login_manager
from .data import db
import flask_tracking.errors as errors
import flask_tracking.logs as logs
from .tracking.views import tracking
from .users.views import users
from flask import request

app = Flask(__name__)
app.config.from_object('config.BaseConfiguration')
# app.config.from_object('config.DebugConfiguration')

@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 3}}

@app.before_request
def log_entry():  # 每次访问前都生成一条log
    msg = {
        'url': request.path,
        'method': request.method,
        'ip': request.environ.get("REMOTE_ADDR")
    }
    app.logger.debug(msg)

# Setup extensions
db.init_app(app)
login_manager.init_app(app)

# Internal extensions for managing
# logs and adding error handlers
logs.init_app(app, remove_existing_handlers=True)
errors.init_app(app)

app.register_blueprint(tracking)
app.register_blueprint(users)
