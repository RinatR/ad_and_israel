from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view ='users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	
	bcrypt.init_app(app)
	login_manager.init_app(app)	

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



	return app