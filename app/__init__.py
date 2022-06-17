from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate

db = SQLAlchemy()
moment = Moment()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)

    # register blueprint(s)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .memo import memo as memo_blueprint
    app.register_blueprint(memo_blueprint)

    return app
