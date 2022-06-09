from flask import redirect, render_template, url_for, session, flash, request, send_from_directory
from . import memo
from .forms import CreateMemoForm
from ..decorators import login_required
from ..models import Memo, User
from .. import db, create_app
# from ..utils import allowed_file
from werkzeug.utils import secure_filename
import os

app = create_app()

@memo.route('/download/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@memo.route('/memos/new', methods=['GET','POST'])
@login_required
def send_memo():
    form = CreateMemoForm()
    user = User.query.get(session.get('id'))
    if form.validate_on_submit():
        reciever = User.query.filter_by(username=form.reciever.data).first()
        print(f'File: {request.files}')
        print(f'Path: {app.root_path}')
        if 'file' not in request.files:
            flash('No file part in request','danger')
            return redirect(request.url)
        file = request.files.get('file')
        if file.filename == "":
            flash('No file uploaded','danger')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))
        memo = Memo(
            title=form.title.data,
            description=form.description.data,
            note_attatched=filename,
            sender_id=user.id,
            reciever_id=reciever.id)
        db.session.add(memo)
        db.session.commit()
        flash('Memo sent successfully!', 'success')
        return redirect(url_for('memo.recieved_memos', office='Office 1', name=filename))

    return render_template('create_memo.html', form=form)

@memo.route('/memos/sent')
@login_required
def sent_memos():
    user = User.query.get(session.get('id'))
    # user = User.query.first()
    memos = user.sent_memos
    return render_template('sent_memos.html', memos=memos, User=User)


@memo.route('/memos/recieved/<office>')
@login_required
def recieved_memos(office):
    user = User.query.get(session.get('id'))
    # user = User.query.first()
    memos = user.recieved_memos
    return render_template('recieved_memos.html', memos=memos, User=User)

        