from flask import redirect, render_template, url_for, session, flash, request, send_from_directory, current_app
from . import memo
from .forms import RecieveMemoForm, UpdateMemoForm, FilterMemoForm, SendMemoForm
from ..decorators import login_required
from ..models import Memo, User, Office, Recipients
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
    user = User.query.get(session.get('id'))
    # session['reciever_office'] = officename
    form = RecieveMemoForm()
    office = Office.query.filter_by(office_name=officename).first()
    if form.validate_on_submit():
        print(f'Form Note: {form.note_attached.data}')
        print(f'Request fILES: {request.files}')
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
            recieved_by = user.username,
            office_reciever_id=reciever_office.id)
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
    # pop start date and end dates from session if they exist
    session.pop('start_date', None)
    session.pop('end_date', None)
    page = request.args.get('page', 1, type=int)
    session['reciever_office'] = officename
    office = Office.query.filter_by(office_name=officename).first()
    pagination = office.recieved_memos.paginate(page, per_page=current_app.config['MEMOS_PER_PAGE'],error_out=False)
    memos = pagination.items
    return render_template('recieved_memos.html', pagination=pagination, memos=memos, User=User)


@memo.route('/memos/recieved/<officename>/<start_date>/<end_date>')
@login_required
def filtered_memos(officename, start_date, end_date):
    page = request.args.get('page', 1, type=int)

    format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, format).date()
    end_date = datetime.strptime(end_date, format).date()
    filtr = func.date(Memo.timestamp)
    office = Office.query.filter_by(office_name=officename).first()
    pagination = office.recieved_memos.filter(
        and_(filtr >= start_date, filtr <= end_date)).\
        paginate(page, per_page=current_app.config['MEMOS_PER_PAGE'], error_out=False)

    memos = pagination.items
    return render_template('recieved_memos.html', pagination=pagination, memos=memos, st_dt=start_date, end_dt=end_date)

@memo.route('/memos/recieved/<officename>/<start_date>/<end_date>/full')
def filtered_memos_full(officename, start_date, end_date):
    page = request.args.get('page', 1, type=int)

    format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, format).date()
    end_date = datetime.strptime(end_date, format).date()
    filtr = func.date(Memo.timestamp)
    office = Office.query.filter_by(office_name=officename).first()
    memos = office.recieved_memos.filter(and_(filtr >= start_date, filtr <= end_date))

    return render_template('recieved_memos_full.html', memos=memos)

    
@memo.route('/memos/recieved/<officename>/full')
@login_required
def recieved_memos_full(officename):
    session['reciever_office'] = officename
    office = Office.query.filter_by(office_name=officename).first()
    memos = office.recieved_memos
    return render_template('recieved_memos_full.html', memos=memos, User=User)

    
@memo.route('/memos/<int:memo_id>/update', methods=['GET','POST'])
@login_required
def update_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    filename=memo.note_attached
    form = UpdateMemoForm()
    if form.validate_on_submit():
        # if user clicks optioal button to reupload new file
        if 'file' not in request.files:
            flash('No file part in request','danger')
            return redirect(request.url)            
        file = request.files.get('file')
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.root_path, app.config['UPLOAD_FOLDER'], filename))

        memo.title = form.title.data
        memo.description = form.description.data
        memo.note_attached = filename
        # memo.note_attached=filename
        db.session.commit()

        flash('Memo successfully updated!', 'success')
        return redirect(url_for('memo.recieved_memos',officename=session.get('reciever_office')))
    elif request.method == 'GET':
        form.title.data = memo.title
        form.description.data = memo.description
        # form.note_attached.data = memo.note_attached
    return render_template('update_memo.html', form=form, a=form.title.data,b=form.description.data, memo_title=memo.title, memo_description=memo.description, memo_note=memo.note_attached)


@memo.route('/memos/<int:memo_id>')
@login_required
def view_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    return render_template('memo.html', memo=memo)


@memo.route('/memos/filter', methods=['GET','POST'])
@login_required
def filter_memos():
    form = FilterMemoForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        session['start_date'] = start_date
        session['end_date'] = end_date
        return redirect(url_for('memo.filtered_memos',officename=session.get('reciever_office'), start_date=form.start_date.data, end_date=form.end_date.data))
    return render_template('filter_memos.html', form=form)


@memo.route('/memos/<memo_id>/send', methods=['GET','POST'])
@login_required
def send_memo(memo_id):
    memo = Memo.query.get_or_404(memo_id)
    form = SendMemoForm()
    # get logged-in user 
    user_id = session.get('id')
    user = User.query.get_or_404(user_id)
    current_office = user.office
    # recipient_choices = Office.query.all()
    # recipient_choices.remove(current_office)

    # obtain a list of the recipients OFFICENAMES using the current memo recipients (memo.recipients)
    memo_recipients_names = list(map(lambda x: x.recipient_office_name, memo.recipients)) 
    # using list comprehension create tuples of office names asides the current office
    # the first and second values of each tuple corresponding to the value and name of each selectfield option
    recipient_choices = [
        (office.office_name, office.office_name) for office in Office.query.all() if office.office_name != current_office and office.office_name not in memo_recipients_names
        ]
    form.recipient_offices.choices = recipient_choices
    
    print(form.validate_on_submit())
    if form.validate_on_submit():
        recipients = form.recipient_offices.data
        print(recipients)
        for recipient in recipients:
            r = Recipients(recipient_office_name=recipient,
                recieved_memo_id=memo_id)
            db.session.add(r)
        memo.sent = True
        db.session.commit()
        flash('Memo sent successfully!','success')
        return redirect(url_for('memo.view_memo', memo_id=memo.id))
    return render_template('send_memo.html', form=form)