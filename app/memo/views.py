from flask import redirect, render_template, url_for, session, flash, request, send_from_directory, current_app
from . import memo
from .forms import RecieveMemoForm, UpdateMemoForm, FilterMemoForm
from ..decorators import login_required
from ..models import Memo, User, Office
from .. import db, create_app
from werkzeug.utils import secure_filename
from sqlalchemy import func, and_
import os
from datetime import datetime

app = create_app()

@memo.route('/download/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)

@memo.route('/memos/recieve/<officename>', methods=['GET','POST'])
@login_required
def recieve_memo(officename):
    user = user = User.query.get(session.get('id'))
    print(f'Office: {type(user.office)}')
    # session['reciever_office'] = officename
    form = RecieveMemoForm()
    office = Office.query.filter_by(office_name=officename).first()
    print(f"Title: {form.title.data}")
    print(f"Description: {form.description.data}")
    print(f"Reciever: {form.reciever.data}")
    print(f"Data: {form.sender_office.data}")
    print(form.validate_on_submit())
    if form.validate_on_submit():
        print(f'File: {request.files}')
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
        reciever_office = Office.query.filter_by(office_name=form.reciever.data).first()
        memo = Memo(
            title=form.title.data,
            description=form.description.data,
            note_attached=filename,
            sender_office = form.sender_office.data,
            reciever_id=reciever_office.id)
        db.session.add(memo)
        db.session.commit()
        flash('Memo recieved successfully!', 'success')
        return redirect(url_for('memo.recieved_memos', officename=officename, name=filename))
    # else:
    #     flash('Error!', 'danger')

    return render_template('recieve_memo.html', form=form)


@memo.route('/memos/recieved/<officename>')
@login_required
def recieved_memos(officename):
    page = request.args.get('page', 1, type=int)
    session['reciever_office'] = officename
    office = Office.query.filter_by(office_name=officename).first()
    pagination = office.recieved_memos.paginate(page, per_page=current_app.config['MEMOS_PER_PAGE'],error_out=False)
    memos = pagination.items
    return render_template('recieved_memos.html', pagination=pagination, memos=memos, User=User)


@memo.route('/memos/recieved/<officename>/<start_date>/<end_date>')
def filtered_memos(officename, start_date, end_date):
    page = request.args.get('page', 1, type=int)

    format = "%m-%d-%y"
    start_date = datetime.strptime(start_date, format).date()
    end_date = datetime.strptime(end_date, format).date()
    filtr = func.date(Memo.timestamp)
    office = Office.query.filter_by(office_name=officename).first()
    pagination = office.recieved_memos.filter(
        and_(filtr >= start_date, filtr <= end_date)).\
        paginate(page, per_page=current_app.config['MEMOS_PER_PAGE'], error_out=False)

    memos = pagination.items
    return render_template('recieved_memos.html', pagination=pagination, memos=memos)

    
@memo.route('/memos/recieved/<officename>/full')
@login_required
def recieved_memos_full(officename):
    session['reciever_office'] = officename
    office = Office.query.filter_by(office_name=officename).first()
    memos = office.recieved_memos
    return render_template('recieved_memos_full.html', memos=memos, User=User)


@memo.route('/memos/<int:memo_id>/delete')
def delete_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    db.session.delete(memo)
    db.session.commit()
    flash('Memo deleted!', 'danger')
    return redirect(url_for('memo.recieved_memos',officename=session.get('reciever_office')))

    
@memo.route('/memos/<int:memo_id>/update', methods=['GET','POST'])
def update_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    print(f'Memo: {request.method}')
    form = UpdateMemoForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No file part in request','danger')
            return redirect(url_for('main.index'))
        file = request.files.get('file')
        if file.filename == "":
            flash('No file uploaded','danger')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

            memo.title = form.title.data
            memo.description = form.description.data
            memo.note_attached=filename
            db.session.commit()
        flash('Memo successfully updated!', 'success')
        return redirect(url_for('memo.recieved_memos',oficename=session.get('reciever_office')))
    elif request.method == 'GET':
        form.title.data = memo.title
        form.description.data = memo.description
        form.note_attached.data = memo.note_attached
    return render_template('update_memo.html', form=form)


@memo.route('/memos/<int:memo_id>')
def view_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    return render_template('memo.html', memo=memo)


@memo.route('/ss')
def filter_memos():
    form = FilterMemoForm()
    if form.validate_on_submit():
        pass
