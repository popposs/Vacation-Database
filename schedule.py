import datedelta
from datetime import date, datetime, timedelta
from reservations import Reservation
from database import db_session

# The users will need to find out when the campsite is available. So the system should expose an API to provide information of the
# availability of the campsite for a given date range with the default being 1 month.
def get_availability(start_date, end_date):
    if end_date is None:
        end_date = start_date + datedelta.MONTH

    today = date.today()

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

def check_conditions(start_date, end_date):
    pass
    # if start_date in ret or end_date in ret:
    #     return (False, "Dates are already reserved.")

    # elif end_date - start_date > 3:
    #     return (False, "Duration cannot be longer than 3 days.")

    # elif start_date <= today:
    #     return (False, "Cannot reserve less than 1 day in advance.")

    # elif end_date > today + timedelta(months=1):
    #     return (False, "Cannot reserve more than a month in advance.")

    # return (True, "")

# The campsite can be reserved for max 3 days.
# The campsite can be reserved minimum 1 day(s) ahead of arrival and up to 1 month in advance.
# For sake of simplicity assume the check-in & check-out time is 12:00 AM
def reserve_dates(start_date, end_date):
    pass

# The unique booking identifier can be used to modify or cancel the reservation later on. Provide appropriate end point(s) to allow
# modification/cancellation of an existing reservation
def cancel_reservation(unique_id):
    pass

def modify_reservation(unique_id):
    pass
