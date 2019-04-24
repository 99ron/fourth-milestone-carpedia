from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Enter your Username', validators=[DataRequired()])
    password = PasswordField('Enter your Password', validators=[DataRequired()])
    submit = SubmitField('Login')

