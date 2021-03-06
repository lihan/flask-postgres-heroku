from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)


db_user = os.environ.get('POSTGRES_DB_USER')
db_psw = os.environ.get('POSTGRES_DB_PSW')
db_host = os.environ.get('SERVICE_POSTGRES_SERVICE_HOST')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{0}:{1}@{2}/launchpage'.format(
    db_user, db_psw, db_host
)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email


# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')


# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
