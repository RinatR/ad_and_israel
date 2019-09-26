from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	campaigns = db.relationship('Campaign', backref='author', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	image_file = db.Column(db.String(20), nullable=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

class Campaign(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	campaign_hash = db.Column(db.String(20), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	start_date = db.Column(db.Date, nullable=False)
	finish_date = db.Column(db.Date, nullable=False)			
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	banners = db.relationship('Banner', backref='parent_campaign', lazy=True)
	status = db.Column(db.Boolean(), nullable=False, default=False)

	def __repr__(self):
		return f"Campaign('{self.title}', '{self.date_posted}', '{self.start_date}', '{self.finish_date}','{self.campaign_hash}')"


# соединительная таблица между Banner и SSP
# используем для сопотавления названия SSP к конкретному баннеру
# потому что у каждого баннера может быть несколько сспшек в качестве источников трафика
#  поле use_ssp говорит нам о том, используется ли конкретная ссп в этом баннере. 0 не используется, 1 - используется
ssps = db.Table('ssps',
    db.Column('ssp_id', db.Integer, db.ForeignKey('ssp.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('banner.id'), primary_key=True)   
)

countries = db.Table('geos',
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('banner.id'), primary_key=True)   
)



class Banner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=True)
	image_file = db.Column(db.Text, nullable=False)
	click_link = db.Column(db.Text, nullable=False)
	campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
	status = db.Column(db.Boolean(), nullable=False, default=False)
	trafkey = db.Column(db.String(20), nullable=False)
	ssps = db.relationship('Ssp', secondary=ssps, lazy='subquery',
	    backref=db.backref('banners', lazy=True))
	countries = db.relationship('Country', secondary=countries, lazy='subquery',
	    backref=db.backref('banners', lazy=True))

class Ssp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)	
	type = db.Column(db.String(20), nullable=False)		
	endpoint_url = db.Column(db.String(100), nullable=False)

class Country(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	cities = db.relationship('City', backref='parent_country', lazy=True)

class City(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	region = db.Column(db.String(200), nullable=False)
	country_id = db.Column(db.Integer(), db.ForeignKey('country.id'), nullable=False)

class Browser(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)

class Os(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)

class Domain(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)	
	






























# class Banner_Click_Stats(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	banner_id = db.Column(db.Integer, db.ForeignKey('banner.id'), nullable=False)
# 	src = db.Column(db.Text, nullable=False)

# 	def __repr__(self):
# 		return f"Banner_Click_Stats('{self.id}', '{self.banner_id}', '{self.src}')"


# class Banner_Impression_Stats(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	banner_id = db.Column(db.Integer, db.ForeignKey('banner.id'), nullable=False)
# 	src = db.Column(db.Text, nullable=False)

# 	def __repr__(self):
# 		return f"Banner_Impression_Stats('{self.id}', '{self.banner_id}', '{self.src}')"	


# class Banner_Nurl_Stats(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	banner_id = db.Column(db.Integer, db.ForeignKey('banner.id'), nullable=False)
# 	src = db.Column(db.Text, nullable=False)

# 	def __repr__(self):
# 		return f"Banner_Nurl_Stats('{self.id}', '{self.banner_id}', '{self.src}')"


