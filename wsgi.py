from app import create_app, db
from app.models import User, Memo, Office
from app.utils import OFFICE_NAMES

app = create_app('default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Memo=Memo, Office=Office)

@app.context_processor
def inject_office():
    return dict(Office=Office)

# the objective here is to automatically create instances of the Office class with data in them
with app.app_context():
    try:
        if len(Office.query.all()) == 0:
            for office in set(OFFICE_NAMES):
                    o = Office(office_name=office)
                    db.session.add(o)
            db.session.commit()
    except:  # the above block was running into an error
        db.session.rollback()

if __name__ == "__main__":
    app.run(debug=True)