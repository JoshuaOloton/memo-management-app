from . import auth
from .forms import LoginForm
from ..decorators import login_required
from ..models import User
from flask import session, redirect, render_template, url_for, flash
# from wtforms_alchemy.fields import QuerySelectField


@auth.route('/login', methods=['GET','POST'])
def login():
    # redirect user if already logged in
    if session.get('id'):
        flash('Already logged in', 'success')
        return redirect(url_for('index'))
    # in order to set he default values 
    form = LoginForm(set_reciever_office='General')
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(form.password.data): 
            session['id'] = user.id
            session['logged_in'] = True
            session['reciever_office'] = form.set_reciever_office.data
            flash('You are logged in', 'success')
            return redirect(url_for('memo.recieved_memos', office=form.set_reciever_office.data))
        flash('Invalid username and/or password!','danger')
    return render_template('login.html', form=form)


@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    session.pop('id', None)
    session.pop('reciever_office', None)
    session['logged_in'] = False
    flash('You are logged out!','danger')
    return redirect(url_for('main.index'))