from . import db
from .utils import OFFICES, OFFICE_NAMES
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Memo(db.Model):
    __tablename__ = 'memo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    note_attatched = db.Column(db.String(130))
    timestamp = db.Column(db.DateTime, default = datetime.now)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reciever_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Memo: From <{self.sender_id}> To <{self.reciever_id}>'

class Office(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    office_name = db.Column(db.String(64), nullable=False)

    # @staticmethod
    # def assign_offices():
    #     for office in set(OFFICE_NAMES):
    #         o = Office(office_name=office)
    #         db.session.add(o)
    #     db.session.commit()

    def __repr__(self):
        return f'Office: {self.office_name}'


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True,nullable=False)
    email = db.Column(db.String(64), index=True, nullable=False)
    password_hash = db.Column(db.String(130))
    office = db.Column(db.String(64), nullable=False)
    sent_memos = db.relationship('Memo',
                                foreign_keys=[Memo.sender_id],
                                backref='sender', lazy=True)
    recieved_memos = db.relationship('Memo',
                                    foreign_keys=[Memo.reciever_id],
                                    backref='reciever', lazy=True)

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
