from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AgentForm(FlaskForm):
    name = StringField("Name",validators=[DataRequired()])
    submit = SubmitField("သွင်း")