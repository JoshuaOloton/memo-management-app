from flask import session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from ..models import User, Office
from ..utils import OFFICE_NAMES

class RecieveMemoForm(FlaskForm):
    title = StringField('Memo Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    reciever =  SelectField('Reciever')
    sender_office = SelectField('Sender Office')
    note_attached = FileField('Attach Note', validators=[FileAllowed(['pdf'])])
    # the only accepable file formats are pdf, word and the picture formats
    submit = SubmitField('Recieve Memo')

    def __init__(self, *args, **kwargs):
        super(RecieveMemoForm, self).__init__(*args, **kwargs)
        # get index of logged in office in the array of Office.query.all() and pop the current office out to obtain the list of the other offices
        # this is done so the logged in office cant send a memo to itself
    
        # use a lambda function with mapping to obtain a new list of just the usernames of the other users/offices(later on)
        # the lambda func is passes to every element of the list_choices array
        user_id = session.get('id')
        user = User.query.get_or_404(user_id)
        if user.in_general():
            office_name = session.get('reciever_office')
            office = Office.query.filter_by(office_name=office_name).first()
            gen_office = Office.query.filter_by(office_name='General').first()
            list_ch = Office.query.all()
            curr_index = list_ch.index(office)
            gen_office_index = list_ch.index(gen_office)
            list_ch.remove(office)

            mapped_choices = map(lambda office: office.office_name, list_ch)
            self.reciever.choices = list(mapped_choices)
            self.sender_office.choices = list(map(lambda office: office.office_name, list_ch))
        else:
            office_name = session.get('reciever_office')
            office = Office.query.filter_by(office_name=office_name).first()
            gen_office = Office.query.filter_by(office_name='General').first()
            list_ch = Office.query.all()
            curr_index = list_ch.index(office)
            gen_office_index = list_ch.index(gen_office)
            # list_ch.pop(curr_index)
            list_ch.remove(office)
            # list_ch.pop(gen_office_index-1)
            list_ch.remove(gen_office)

            mapped_choices = map(lambda office: office.office_name, list_ch)

            self.sender_office.choices = list(mapped_choices)
            self.reciever.choices = [user.office]


class UpdateMemoForm(FlaskForm):
    title = StringField('Memo Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    note_attached = FileField('Attach Note', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Update Memo')
