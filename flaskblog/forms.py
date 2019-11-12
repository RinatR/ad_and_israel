# from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileAllowed
# from flask_login import current_user
# from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from flaskblog.models import User, Campaign, Banner, Ssp, Country, Region
# from datetime import datetime
# from wtforms import SelectMultipleField, widgets

# class RegistrationForm(FlaskForm):
# 	username = StringField('Username', validators=[DataRequired(), 
# 							Length(min=2,max=20)])
# 	email = StringField('Email', validators=[DataRequired(), Email()])
# 	password = PasswordField('Password', validators=[DataRequired()])
# 	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
# 									EqualTo('password')])
# 	submit = SubmitField('Sign Up')

# 	def validate_username(self, username):
# 		user = User.query.filter_by(username=username.data).first()		
# 		if user:
# 			raise ValidationError('That username is taken. Please choose different one')

# 	def validate_email(self, email):
# 		user = User.query.filter_by(email=email.data).first()		
# 		if user:
# 			raise ValidationError('That email is taken. Please choose different one')

# class LoginForm(FlaskForm):
# 	email = StringField('Email', validators=[DataRequired(), Email()])
# 	password = PasswordField('Password', validators=[DataRequired()])
# 	remember = 	BooleanField('Remember Me')
# 	submit = SubmitField('Login')

# class UpdateAccountForm(FlaskForm):
# 	username = StringField('Username', validators=[DataRequired(), 
# 							Length(min=2,max=20)])
# 	email = StringField('Email', validators=[DataRequired(), Email()])	
# 	picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
# 	submit = SubmitField('Update')

# 	def validate_username(self, username):
# 		if username.data != current_user.username:
# 			user = User.query.filter_by(username=username.data).first()		
# 			if user:
# 				raise ValidationError('That username is taken. Please choose different one')

# 	def validate_email(self, email):
# 		if email.data != current_user.email:
# 			user = User.query.filter_by(email=email.data).first()		
# 			if user:
# 				raise ValidationError('That email is taken. Please choose different one')

# class PostForm(FlaskForm):
# 	title = StringField('Title', validators=[DataRequired()])
# 	content = TextAreaField('Content', validators=[DataRequired()])
# 	image = FileField('Post Picture', validators=[FileAllowed(['jpg', 'png'])])
# 	submit = SubmitField('Post')

# class CampaignForm(FlaskForm):
# 	title = StringField('Title', validators=[DataRequired()])
# 	start_date = DateField('Start Campaign',validators=[DataRequired()])	
# 	finish_date = DateField('Finish Campaign',validators=[DataRequired()])
# 	submit = SubmitField('Save')

	# def validate_date(self, start_date, finish_date):		
	# 	if start_date.data > finish_date.data: 
	# 		raise ValidationError('The start date of campaign can''t be  later than finish date. Please check the dates and try again')

# class MultiCheckboxField(SelectMultipleField):
# 	widget = widgets.ListWidget(prefix_label=False)
# 	option_widget = widgets.CheckboxInput()


# class BannerForm(FlaskForm):
# 	title = StringField('Title', validators=[DataRequired()])
# 	width = StringField('Width', validators=[DataRequired()])
# 	height = StringField('Height', validators=[DataRequired()])
# 	image = FileField('Banner Image', validators=[FileAllowed(['jpg', 'png', 'gif'])])
# 	content = TextAreaField('HTML Code')
# 	click_link = StringField('Click link', validators=[DataRequired()])
# 	audit_link = StringField('Audit link')	
# 	submit = SubmitField('Save')

# 	ssps = Ssp.query.all()		
# 	ssp_list = []
# 	for ssp in ssps:
# 		ssp_list.append(ssp.name)

# 	ssp_items = [(x, x) for x in ssp_list]	
# 	ssp_checkboxes = MultiCheckboxField('Available SSPs', choices=ssp_items)

# 	# countries = Country.query.all()		
# 	# country_list = []
# 	# for country in countries:
# 	# 	country_list.append(country.name)

# 	# country_items = [(x, x) for x in country_list]	
# 	# country_checkboxes = MultiCheckboxField('Available countries', choices=country_items)
	
# 	regions = Region.query.all()			
# 	region_list = []
# 	for region in regions:
# 		region_dict = {}
# 		region_dict['id'] = region.id
# 		region_dict['name'] = region.name
# 		region_list.append(region_dict)
			
# 	region_items = [(str(value['id']), value['name']) for value in region_list]	
	
# 	# region_checkboxes = MultiCheckboxField('Available regions', choices=region_items)
# 	region_list = SelectMultipleField(u'Available regions', choices=region_items,validators=[DataRequired()])

# class SspForm(FlaskForm):
# 	name = StringField('SSP Name', validators=[DataRequired()])	
# 	type = SelectField(u'Type of SSP', choices=[('banner', 'Banner'), ('video', 'Video'), ('native', 'Native')])
# 	endpoint_url = StringField('Endpoint URL', validators=[DataRequired()])
# 	submit = SubmitField('Save')























# class MultiCheckboxField(SelectMultipleField):
# 	widget = widgets.ListWidget(prefix_label=False)
# 	option_widget = widgets.CheckboxInput()

# class BannerForm(FlaskForm):
# 	title = StringField('Title', validators=[DataRequired()])
# 	image = FileField('Banner Image', validators=[FileAllowed(['jpg', 'png', 'gif'])])
# 	click_link = StringField('Click link', validators=[DataRequired()])
# 	submit = SubmitField('Save')

# 	ssps = Ssp.query.all()	
# 	ssp_list = []
# 	for ssp in ssps:
# 		ssp_list.append(ssp.name)

# 	ssp_items = [(x, x) for x in ssp_list]	
# 	ssp_checkboxes = MultiCheckboxField('Available SSPs', choices=ssp_items)


# 	countries = Country.query.all()
# 	countries_name_list = []

# 	for c in countries:
# 		countries_name_list.append(c.name)

# 	country_items = [(x, x) for x in countries_name_list]	
# 	country_checkboxes = MultiCheckboxField('Geo targetings', choices=country_items)

# 	# cities = City.query.all()	
# 	# city_list = []
# 	# for city in cities:
# 	# 	city_list.append(city.region)

# 	# city_list = set(city_list)
	
# 	# cities_list = []

# 	# for city in city_list:
# 	# 	cities_list.append(city)

# 	# cities_list.sort()

# 	# city_items = [(x, x) for x in cities_list]	
# 	# city_checkboxes = MultiCheckboxField('Available regions', choices=city_items)
	

# class SspForm(FlaskForm):
# 	name = StringField('SSP Name', validators=[DataRequired()])	
# 	type = SelectField(u'Type of SSP', choices=[('banner', 'Banner'), ('video', 'Video'), ('native', 'Native')])
# 	endpoint_url = StringField('Endpoint URL', validators=[DataRequired()])
# 	submit = SubmitField('Save')

# class CountryForm(FlaskForm):
# 	name = StringField('Geo Name', validators=[DataRequired()])	
# 	submit = SubmitField('Save')




