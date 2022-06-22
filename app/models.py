from . import db
from .utils import OFFICES, OFFICE_NAMES
from flask import session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Memo(db.Model):
    __tablename__ = 'memo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    note_attached = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default = datetime.now)
    sender_office = db.Column(db.String(64), nullable=False)
    recieved_by = db.Column(db.String(64), nullable=False)
    recipients = db.relationship('Recipients', backref='recieved_memo', lazy=True)
    sent = db.Column(db.Boolean, default=False)
    office_reciever_id = db.Column(db.Integer, db.ForeignKey('office.id'))

    # # Serialize Memo Resource to JSON
    # def to_json(self):
    #     json_memo = {
    #         'url': url_for('api.get_memo',id=self.id),
    #         'body_html':self.body_html,
    #         'date_created': self.date_created,
    #         'author_url' : url_for('api.get_user',id=self.author.id),
    #         'comment_url': url_for('api.get_post_comments',id=self.id),
    #         'comment_count': self.comments.count()
    #     }
    #     return json_memo

    def __repr__(self):
        return f'Memo: To <{self.office_reciever_id}>'

class Office(db.Model):
    __tablename__ = 'office'
    id = db.Column(db.Integer, primary_key=True)
    office_name = db.Column(db.String(64), nullable=False)
    recieved_memos = db.relationship('Memo', backref='reciever', lazy='dynamic')

    def __repr__(self):
        return f'Office: {self.office_name}'


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(130))
    office = db.Column(db.String(64), nullable=False)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        # dynamically assign every user object on creation to their predefined offices
        self.office = OFFICES[self.username]

    def __repr__(self):
        return f'User {self.id}'

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    # the setter is called when we assign some value to the password property generating a password hash from it
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipients(db.Model):
    __tablename__ = 'recipients'
    id = db.Column(db.Integer, primary_key=True)
    recipient_office_name = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default = datetime.now)
    recieved_memo_id = db.Column(db.Integer, db.ForeignKey('memo.id'))

    def __repr__(self):
        return f'Office: {self.recipient_office_name}'
