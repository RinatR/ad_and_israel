import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '61bbf9d98a2e3c7a5644fa9016f2ba14'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.campaigns.routes import camps
from flaskblog.banners.routes import banners
from flaskblog.main.routes import main
from flaskblog.ssps.routes import sources

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(camps)
app.register_blueprint(banners)
app.register_blueprint(main)
app.register_blueprint(sources)



