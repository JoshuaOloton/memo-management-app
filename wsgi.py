from app import create_app, db
from app.models import User, Memo, Office
from app.utils import OFFICE_NAMES
from flask import session

app = create_app('default')

""" Therefore to inject a new variable into the context of templates, flask provides a concept called context processor.
Context processors run before the template gets rendered and has the ability to inject new values into the context of template. """
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Memo=Memo, Office=Office)

# this function passes variables to base.html which can be used by all templates since variables cant be passed to the base through view functions
@app.context_processor
def inject_office():
    user_id = session.get('id')
    user = None
    if user_id:
        user = User.query.get(user_id)
    return dict(Office=Office, current_user=user)
    # pass current_user so all templates ca readily access the logged in user

# the objective here is to automatically create instances of the Office class with data in them
with app.app_context():
    try:
        if len(Office.query.all()) == 0:
            for office in set(OFFICE_NAMES):
                    o = Office(office_name=office)
                    db.session.add(o)
            db.session.commit()
    except:  # rollback commit if the above block ran into an error
        db.session.rollback()

if __name__ == "__main__":
    app.run(debug=True)