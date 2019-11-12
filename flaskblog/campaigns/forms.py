from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,DateField 
from wtforms.validators import DataRequired, ValidationError


class CampaignForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	start_date = DateField('Start Campaign',validators=[DataRequired()])	
	finish_date = DateField('Finish Campaign',validators=[DataRequired()])
	submit = SubmitField('Save')

	