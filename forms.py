from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    arrival_date = DateField('arrival_date', format="%m/%d/%Y")
    departure_date = DateField('departure_date', format="%m/%d/%Y")


