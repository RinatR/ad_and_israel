from datetime import datetime
from ad_and_israel import db, login_manager
from flask_login import UserMixin
from flask import current_app


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
	image_banner = db.relationship('Imagebanner', backref='parent_campaign', lazy=True)
	html_banner = db.relationship('Htmlbanner', backref='parent_campaign', lazy=True)
	status = db.Column(db.Boolean(), nullable=False, default=False)

	def __repr__(self):
		return f"Campaign('{self.title}', '{self.date_posted}', '{self.start_date}', '{self.finish_date}','{self.campaign_hash}')"


# соединительная таблица между Imagebanner и SSP
# используем для сопотавления названия SSP к конкретному баннеру-картинке
# потому что у каждого баннера может быть несколько сспшек в качестве источников трафика
ssps_imagebanner = db.Table('ssps_imagebanner',
    db.Column('ssp_id', db.Integer, db.ForeignKey('ssp.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('imagebanner.id'), primary_key=True)   
)

regions_imagebanner = db.Table('regions_imagebanner',
    db.Column('region_id', db.Integer, db.ForeignKey('region.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('imagebanner.id'), primary_key=True)   
)

operating_systems_imagebanner = db.Table('operating_systems_imagebanner',
    db.Column('os_id', db.Integer, db.ForeignKey('os.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('imagebanner.id'), primary_key=True)   
)

# соединительная таблица между Htmlbanner и SSP
# используем для сопотавления названия SSP к конкретному html-баннеру
# потому что у каждого баннера может быть несколько сспшек в качестве источников трафика
ssps_htmlbanner = db.Table('ssps_htmlbanner',
    db.Column('ssp_id', db.Integer, db.ForeignKey('ssp.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('htmlbanner.id'), primary_key=True)   
)

regions_htmlbanner = db.Table('regions_htmlbanner',
    db.Column('region_id', db.Integer, db.ForeignKey('region.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('htmlbanner.id'), primary_key=True)   
)

operating_systems_htmlbanner = db.Table('operating_systems_htmlbanner',
    db.Column('os_id', db.Integer, db.ForeignKey('os.id'), primary_key=True),
    db.Column('banner_id', db.Integer, db.ForeignKey('htmlbanner.id'), primary_key=True)   
)

# countries = db.Table('geos',
#     db.Column('country_id', db.Integer, db.ForeignKey('country.id'), primary_key=True),
#     db.Column('banner_id', db.Integer, db.ForeignKey('banner.id'), primary_key=True)   
# )


class Imagebanner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	width = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)	
	image_file = db.Column(db.Text, nullable=True)	
	content = db.Column(db.Text, nullable=True)
	click_link = db.Column(db.Text, nullable=False)
	audit_link = db.Column(db.Text, nullable=False)	
	status = db.Column(db.Boolean(), nullable=False, default=False)
	trafkey = db.Column(db.String(20), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
	ssps_imagebanner = db.relationship('Ssp', secondary=ssps_imagebanner, lazy='subquery', backref=db.backref('imagebanners', lazy=True))
	regions_imagebanner = db.relationship('Region', secondary=regions_imagebanner, lazy='subquery', backref=db.backref('imagebanners', lazy=True))
	operating_systems_imagebanner = db.relationship('Os', secondary=operating_systems_imagebanner, lazy='subquery', backref=db.backref('imagebanners', lazy=True))


class Htmlbanner(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	width = db.Column(db.Integer, nullable=False)
	height = db.Column(db.Integer, nullable=False)	
	content = db.Column(db.Text, nullable=False)
	click_link = db.Column(db.Text, nullable=False)
	audit_link = db.Column(db.Text, nullable=False)	
	status = db.Column(db.Boolean(), nullable=False, default=False)
	trafkey = db.Column(db.String(20), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
	ssps_htmlbanner = db.relationship('Ssp', secondary=ssps_htmlbanner, lazy='subquery', backref=db.backref('htmlbanners', lazy=True))
	regions_htmlbanner = db.relationship('Region', secondary=regions_htmlbanner, lazy='subquery', backref=db.backref('htmlbanners', lazy=True))
	operating_systems_htmlbanner = db.relationship('Os', secondary=operating_systems_htmlbanner, lazy='subquery', backref=db.backref('htmlbanners', lazy=True))

class Ssp(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)	
	type = db.Column(db.String(20), nullable=False)		
	endpoint_url = db.Column(db.String(100), nullable=False)

class Country(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	# regions = db.relationship('Region', backref='parent_country', lazy=True)

class Region(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	# country_id = db.Column(db.Integer(), db.ForeignKey('country.id'), nullable=False)
	# cities = db.relationship('City', backref='parent_region', lazy=True)

class Os(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)

# class City(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(100), nullable=False)	
# 	region_id = db.Column(db.Integer(), db.ForeignKey('region.id'), nullable=False)

# class Browser(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(100), nullable=False)

# class Domain(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(100), nullable=False)	
	






























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


