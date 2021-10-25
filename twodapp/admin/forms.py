from twodapp.models import Admin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,Email,EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired(),EqualTo('password_confirm')])
    password_confirm = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")

    def check_email(self, field):
        if Admin.query.filter_by(username=field.data).first():
            raise ValidationError('Your email has been registered already!')