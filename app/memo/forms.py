from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from ..models import User

class CreateMemoForm(FlaskForm):
    title = StringField('Memo Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    reciever =  SelectField('Reciever')
    note_attatched = FileField('Attach Note', validators=[FileAllowed(['pdf'])])
    # the only accepable file formats are pdf, word and the picture formats
    submit = SubmitField('Create Memo')

    def __init__(self, *args, **kwargs):
        super(CreateMemoForm, self).__init__(*args, **kwargs)
        list_choices = User.query.all()

        # get index of logged in user in the array of User.query.all() and pop the current user out to obtain the list of the other users
        # this is done so the logged in user cant send a memo to himself
        user = User.query.get(session.get('id'))
        current_index = list_choices.index(user)
        list_choices.pop(current_index)

        # use a lambda function with mapping to obtain a new list of just the usernames of the other users/offices(later on)
        # the lambda func is passes to every element of the list_choices array
        mapped_choices = map(lambda user: user.username, list_choices)
        self.reciever.choices = list(mapped_choices)

class UpdateMemo(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    desciption = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    reciever =  SelectField('Reciever\'s Office')
    note_attatched = FileField('Attach Note')
    submit = SubmitField('Update Memo')
