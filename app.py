from datetime import date, datetime, timedelta
import os, json

from flask_sqlalchemy_session import flask_scoped_session
from flask import Flask, render_template, redirect, url_for
from forms import SignupForm, ModifyForm

from reservations import Reservation
from database import db_session, session_factory

from schedule import reserve_dates, cancel_reservation, modify_reservation


app = Flask(__name__)
session = flask_scoped_session(session_factory, app)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/signup/<name>/<email>/<start_date>/<end_date>")
def signup_route(name, email, start_date, end_date):
    arrival_str = "{}/{}/{}".format(start_date[:2], start_date[2:4], start_date[4:])
    departure_str = "{}/{}/{}".format(end_date[:2], end_date[2:4], end_date[4:])

    arrival = datetime.strptime(arrival_str, "%m/%d/%y").date()
    departure = datetime.strptime(departure_str, "%m/%d/%y").date()
    unique_id = reserve_dates(name, email, arrival, departure, session)

    return "Unique Registration ID: {} for {} to {}".format(unique_id, arrival_str, departure_str)

# Provide an end point for reserving the campsite. The user will provide his/her email & full name at the time of reserving the campsite
# along with intended arrival date and departure date. Return a unique booking identifier back to the caller if the reservation is successful.
@app.route("/", methods=('GET', 'POST'))
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        arrival =  datetime.strptime(form.arrival_date.data.strftime('%x'), "%m/%d/%y").date()
        departure = datetime.strptime(form.departure_date.data.strftime('%x'), "%m/%d/%y").date()

        unique_id = reserve_dates(name, email, arrival, departure, session)
        arrival_str = datetime.strftime(arrival, '%m/%d/%y')
        departure_str = datetime.strftime(departure, '%m/%d/%y')

        return "Unique Registration ID: {} for {} to {}".format(unique_id, arrival_str, departure_str)
    return render_template('signup.html', form=form)

@app.route("/reserved", methods=['GET'])
def get_reserved():
    all_reservations = [value for value in session.query(Reservation).all()]
    ret = []

    for r in all_reservations:
        if r is not None and r.arrival_date and r.departure_date:
            delta = r.departure_date - r.arrival_date
            for i in range(delta.days + 1):
                reserved_date = (r.arrival_date + timedelta(i)).strftime('%m/%d/%y')
                ret.append(reserved_date)

    return json.dumps(ret)

@app.route("/cancel/<uid>")
def cancel_reserved(uid):
    return str(cancel_reservation(uid, session))

# dates input in format mmddyy
@app.route("/modify/<uid>/<start_date>/<end_date>")
def modify_reserved(uid, start_date, end_date):
    start_date = "{}/{}/{}".format(start_date[:2], start_date[2:4], start_date[4:])
    end_date = "{}/{}/{}".format(end_date[:2], end_date[2:4], end_date[4:])
    return str(modify_reservation(uid, start_date, end_date, session))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5090, debug=True)
