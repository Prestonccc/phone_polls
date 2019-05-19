from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin, AdminIndexView


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app, name='Phone Poll', template_mode='bootstrap3',
              index_view=AdminIndexView(
                  template='admin_index.html',
              ))
login = LoginManager(app)
login.login_view = 'login'


from app import routes, models, errors