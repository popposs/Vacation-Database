from datetime import date, datetime, timedelta
import os, json

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
            arrival =  datetime.strptime(form.arrival_date.data.strftime('%x'), "%m/%d/%y").date()
            departure = datetime.strptime(form.departure_date.data.strftime('%x'), "%m/%d/%y").date()

            signup = Reservation(name=form.name.data, email=form.email.data, arrival_date=arrival, departure_date=departure)
            db_session.add(signup)
            db_session.commit()

            availability = get_availability(arrival, departure)
            print('\n>>>\n', arrival , departure, availability, '\n>>>\n')

            arrival_str = datetime.strptime(arrival, '%m/%d/%y')
            departure_str = datetime.strptime(departure, '%m/%d/%y')

            return "Unique Registration ID: {} for {} to {}".format(db_session.query(Reservation.id).filter_by(name=form.name.data).filter_by(email=form.email.data).first()[0], arrival_str, departure_str)
        except Exception as e:
            print(e)
            return "{}".format(e)
    return render_template('signup.html', form=form)

@app.route("/reserved", methods=['GET'])
def get_reserved():
    all_reservations = [value for value in db_session.query(Reservation).all()]
    ret = []

    for r in all_reservations:
        if r is not None and r.arrival_date and r.departure_date:
            delta = r.departure_date - r.arrival_date
            for i in range(delta.days + 1):
                reserved_date = (r.arrival_date + timedelta(i)).strftime('%m/%d/%y')
                ret.append(reserved_date)

    return json.dumps(ret)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
