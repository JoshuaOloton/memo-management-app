from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..utils import OFFICE_NAMES
from ..models import User, Office
from wtforms.ext.sqlalchemy.fields import QuerySelectField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')