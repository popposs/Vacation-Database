import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import SignupForm

from reservations import Reservation
from database import db_session

from schedule import get_availability

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

# Provide an end point for reserving the campsite. The user will provide his/her email & full name at the time of reserving the campsite
# along with intended arrival date and departure date. Return a unique booking identifier back to the caller if the reservation is successful.
@app.route("/", methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            signup = Reservation(name=form.name.data, email=form.email.data, arrival_date=None, departure_date=None)
            db_session.add(signup)
            db_session.commit()
            get_availability(datetime.datetime.now(), None)
            return "Unique Registration ID: {}".format(db_session.query(Reservation.id).filter_by(name=form.name.data).filter_by(email=form.email.data).first()[0])
        except Exception as e:
            print(e)
            return "{}".format(e)
    return render_template('signup.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
