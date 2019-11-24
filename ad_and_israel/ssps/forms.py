from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError

class SspForm(FlaskForm):
	name = StringField('SSP Name', validators=[DataRequired()])	
	type = SelectField(u'Type of SSP', choices=[('banner', 'Banner'), ('video', 'Video'), ('native', 'Native')])
	endpoint_url = StringField('Endpoint URL', validators=[DataRequired()])
	submit = SubmitField('Save')