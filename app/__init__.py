from config import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

db = SQLAlchemy()
scheduler = APScheduler()

def creat_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app()

    db.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app