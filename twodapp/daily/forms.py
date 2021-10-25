from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,SelectField
from wtforms.fields.html5 import DateField

class TwoDigitForm(FlaskForm):
    submitField = SubmitField("Get Updates")

class TwoDigitAddForm(FlaskForm):
    value = StringField("Value")
    date = DateField("Date:")
    time = SelectField("အချိန်",choices=[('morning','မနက်'),('evening','ညနေ')])
    submit = SubmitField("Add A New TwoDigit")