from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,PasswordField,DateField,SubmitField,SelectField
from wtforms.validators import DataRequired

class Mainform(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    hashtag=StringField('Hashtag', validators=[DataRequired()])
    