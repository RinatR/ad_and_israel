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

from ad_and_israel.users.routes import users
from ad_and_israel.posts.routes import posts
from ad_and_israel.campaigns.routes import camps
from ad_and_israel.image_banners.routes import image_banner
from ad_and_israel.html_banners.routes import html_banner
from ad_and_israel.main.routes import main
from ad_and_israel.ssps.routes import sources

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(camps)
app.register_blueprint(image_banner)
app.register_blueprint(html_banner)
app.register_blueprint(main)
app.register_blueprint(sources)



