from . import auth 
from .forms import LoginForm, SignUpForm
from ..decorators import login_required
from ..models import User
from .. import db
from flask import session, redirect, render_template, url_for, flash, request
from ..utils import OFFICES
from sqlalchemy.exc import IntegrityError


@auth.route('/login', methods=['GET','POST'])
def login():
    # redirect user if already logged in
    if session.get('id'):
        flash('Already logged in', 'success')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        print(f"Validate:{request.form}")
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data): 
            session['id'] = user.id
            session['logged_in'] = True
            session['reciever_office'] = request.form['set_reciever_office']
            flash('You are logged in', 'success')
            return redirect(url_for('memo.recieved_memos', officename=request.form['set_reciever_office']))
        flash('Invalid username and/or password!','danger')
    return render_template('login.html', form=form)


@auth.route('/register', methods=['GET','POST'])
def register():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if form.username.data not in list(OFFICES.keys()):
            flash('Username not found!', 'danger')
            return redirect(request.ur)
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('Username is taken! Please choose another', 'danger')
            return redirect(request.url)
        flash('Sign up successfully! Please log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    session.pop('id', None)
    session.pop('reciever_office', None)
    session['logged_in'] = False
    # flash('You are logged out!','danger')
    return redirect(url_for('main.index'))