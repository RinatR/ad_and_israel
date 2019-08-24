from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User, Campaign
from datetime import datetime

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), 
							Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), 
									EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()		
		if user:
			raise ValidationError('That username is taken. Please choose different one')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()		
		if user:
			raise ValidationError('That email is taken. Please choose different one')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = 	BooleanField('Remember Me')
	submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), 
							Length(min=2,max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])	
	picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()		
			if user:
				raise ValidationError('That username is taken. Please choose different one')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()		
			if user:
				raise ValidationError('That email is taken. Please choose different one')

class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	content = TextAreaField('Content', validators=[DataRequired()])
	image = FileField('Post Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Post')

class CampaignForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	start_date = DateField('Start Campaign',validators=[DataRequired()])	
	finish_date = DateField('Finish Campaign',validators=[DataRequired()])
	submit = SubmitField('Create')

	def validate_date(self, start_date, finish_date):		
		if start_date.data > finish_date.data: 
			raise ValidationError('The start date of campaign can''t be  later than finish date. Please check the dates and try again')

class BannerForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	image = FileField('Banner Image', validators=[FileAllowed(['jpg', 'png', 'gif'])])
	click_link = StringField('Click link', validators=[DataRequired()])
	submit = SubmitField('Create')

