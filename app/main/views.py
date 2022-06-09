from flask import redirect, render_template, url_for, session
from . import main
from ..decorators import login_required
from ..models import Memo, User
from .. import db

@main.route('/')
@main.route('/home')
def index():
    user = None
    if session.get('id'):
        user = User.query.get(session.get('id'))
    return render_template('index.html', user=user)
