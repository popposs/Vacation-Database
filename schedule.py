import datedelta
from datetime import date, datetime, timedelta
from reservations import Reservation
from database import db_session
from dateutil.relativedelta import relativedelta

# The users will need to find out when the campsite is available. So the system should expose an API to provide information of the
# availability of the campsite for a given date range with the default being 1 month.
def get_availability(start_date, end_date):
    start_date = datetime.strptime(start_date, '%m/%d/%y').date()

    if end_date is None:
        end_date = start_date + datedelta.MONTH

    end_date = datetime.strptime(end_date, '%m/%d/%y').date()

    print('testing', start_date, end_date)

    base_valid_days = set()

    delta = end_date - start_date
    for i in range(delta.days + 1):
        base_valid_days.add((start_date + timedelta(i)).strftime('%m/%d/%y'))

    reservedDates = db_session.query(Reservation).filter(Reservation.arrival_date>=start_date, Reservation.departure_date<=end_date).all()
    reserved = set()

    for r in reservedDates:
        if r is not None and r.arrival_date and r.departure_date:
            delta = r.departure_date - r.arrival_date
            for i in range(delta.days + 1):
                reserved.add((r.arrival_date + timedelta(i)).strftime('%m/%d/%y'))

    # return available days
    return list(base_valid_days - reserved)

### Returns (boolean for pass/fail, string for description)
# The campsite can be reserved for max 3 days.
# The campsite can be reserved minimum 1 day(s) ahead of arrival and up to 1 month in advance.
def check_conditions(start_date, end_date):
    availability = get_availability(start_date, end_date)
    print('available', availability, start_date, end_date)

    start_date_obj = datetime.strptime(start_date, '%m/%d/%y').date()
    end_date_obj = datetime.strptime(end_date, '%m/%d/%y').date()
    today = date.today()

    if start_date not in availability or end_date not in availability:
        return (False, "Dates are already reserved.")

    elif (end_date_obj - start_date_obj).days > 3:
        return (False, "Duration cannot be longer than 3 days.")

    elif start_date_obj <= today:
        return (False, "Cannot reserve less than 1 day in advance.")

    elif end_date_obj > today + relativedelta(months=+1):
        return (False, "Cannot reserve more than a month in advance.")

    return (True, "")

def reserve_dates(name, email, start_date, end_date):
    start_date = start_date.strftime('%m/%d/%y')
    end_date = end_date.strftime('%m/%d/%y')

    check = check_conditions(start_date, end_date)
    if check[0] is True:
        signup = Reservation(name=name, email=email, arrival_date=start_date, departure_date=end_date)
        db_session.add(signup)
        db_session.commit()
        return db_session.query(Reservation.id).filter_by(name=name).filter_by(email=email).first()[0]
    else:
        return check[1] # user readable error


# The unique booking identifier can be used to modify or cancel the reservation later on. Provide appropriate end point(s) to allow
# modification/cancellation of an existing reservation
def cancel_reservation(unique_id):
    try:
        reservation_query = db_session.query(Reservation).filter_by(id=unique_id).delete()
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def modify_reservation(unique_id, start_date, end_date):
    start_date = datetime.strptime(start_date, '%m/%d/%y').date()
    end_date = datetime.strptime(end_date, '%m/%d/%y').date()

    query_result = db_session.query(Reservation).filter_by(id=unique_id).update({"arrival_date": start_date, "departure_date": end_date})
    db_session.commit()

    return True
