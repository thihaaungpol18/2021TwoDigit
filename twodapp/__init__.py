import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "admin.login"

from twodapp.bets.views import bets
from twodapp.admin.views import admin
from twodapp.agents.views import agents
from twodapp.daily.views import daily
from twodapp.error_pages.views import bp
# Register the apps
app.register_blueprint(admin)
app.register_blueprint(bets)
app.register_blueprint(agents)
app.register_blueprint(daily)
app.register_blueprint(bp)