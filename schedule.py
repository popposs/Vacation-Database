import calendar, datetime, datedelta
from reservations import Reservation
from database import db_session

c = calendar.TextCalendar(calendar.SUNDAY)
str = c.formatmonth(2018, 1)
print(str)


# The users will need to find out when the campsite is available. So the system should expose an API to provide information of the
# availability of the campsite for a given date range with the default being 1 month.
def get_availability(start_date, end_date):
    if end_date is None:
        end_date = start_date + datedelta.MONTH
    print(db_session.query(Reservation).all())
    # print(db_session.query(Reservation).filter(Reservation.arrival_date>=start_date, Reservation.departure_date<=end_date).all())

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
