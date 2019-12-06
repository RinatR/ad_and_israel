from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from ad_and_israel.models import Ssp, Country, Region, Os
from datetime import datetime
from wtforms import SelectMultipleField, widgets

class MultiCheckboxField(SelectMultipleField):
	widget = widgets.ListWidget(prefix_label=False)
	option_widget = widgets.CheckboxInput()


class ImagebannerForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	width = StringField('Width', validators=[DataRequired()])
	height = StringField('Height', validators=[DataRequired()])
	image = FileField('Banner Image', validators=[FileAllowed(['jpg', 'png', 'gif'])])	
	click_link = StringField('Click link', validators=[DataRequired()])
	audit_link = StringField('Audit link')	
	submit = SubmitField('Save')

	ssps = Ssp.query.all()		
	ssp_list = []
	for ssp in ssps:
		ssp_list.append(ssp.name)

	ssp_items = [(x, x) for x in ssp_list]	
	ssp_checkboxes = MultiCheckboxField('Available SSPs', choices=ssp_items)

	# countries = Country.query.all()		
	# country_list = []
	# for country in countries:
	# 	country_list.append(country.name)

	# country_items = [(x, x) for x in country_list]	
	# country_checkboxes = MultiCheckboxField('Available countries', choices=country_items)
	
	regions = Region.query.all()			
	region_list = []
	for region in regions:
		region_dict = {}
		region_dict['id'] = region.id
		region_dict['name'] = region.name
		region_list.append(region_dict)
			
	region_items = [(str(value['id']), value['name']) for value in region_list]	
	region_list = SelectMultipleField(u'Available regions', choices=region_items)

	operating_systems = Os.query.all()			
	os_list = []
	for os in operating_systems:
		os_dict = {}
		os_dict['id'] = os.id
		os_dict['name'] = os.name
		os_list.append(os_dict)
			
	os_items = [(str(value['id']), value['name']) for value in os_list]	
	os_list = SelectMultipleField(u'Available operating systems', choices=os_items)