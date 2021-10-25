from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,SubmitField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms.fields.html5 import DateField

class BetForm(FlaskForm):
    date = DateField('Date')
    value =StringField("Value",validators=[DataRequired()])
    product =StringField("အဆ",validators=[DataRequired()])
    amount = StringField("Amount",validators=[DataRequired()])
    time = SelectField("အချိန်",choices=[('morning','မနက်'),('evening','ညနေ')])
    agents = SelectField("ထိုးသား",choices=[])
    submit = SubmitField("Submit")    