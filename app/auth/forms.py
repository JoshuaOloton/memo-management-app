from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms.fields import StringField, SubmitField, PasswordField, SelectField
# from wtforms_alchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email
from ..utils import OFFICE_NAMES
from ..models import User, Office
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def office_query():
    # office = Office.query.filter_by(office_name=)
    # return office
    pass

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    set_reciever_office = SelectField('Reciever Office', choices=set(OFFICE_NAMES))
    # set_reciever_office = QuerySelectField('Reciever Office',query_factory=office_query, allow_blank=True)
    submit = SubmitField('Log In')