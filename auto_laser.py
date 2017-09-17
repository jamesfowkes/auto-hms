""" auto_laser.py

Usage:
    auto_laser.py <start_time> <end_time> [<date>]
    auto_laser.py --list

Options:
    <start_time>    Booking start time in hhmm format
    <end_time>      Booking end time in hhmm format
    [<date>]        Booking date in yyyy-mm-dd format (defaults today if not present)
    --list          List the rest of today's bookings
"""

import os
import sys
import math
import docopt
import datetime
import logging

from hms import HMS

import booking

def filter_bookings_for_rest_of_day(b):
    pass_filter = b.end > datetime.datetime.now()
    pass_filter = pass_filter and b.start.date() == datetime.date.today()
    return pass_filter

def book_laser(hms, booking_info):


    logging.info("Booking laser on {0:%Y-%m-%d}, {0:%H:%M} to {1:%H:%M}".format(
        booking_info.start, booking_info.end))
    
    hms.open_tools_booking_form(booking_info, "laser")

    if not hms.on_laser_booking_form():
        sys.exit("Could not open laser booking form")

    hms.try_booking(booking_info)

    success, msg = hms.booking_successful()

    logging.info("Booking created!" if success else "Booking not created! Reason: '{}'".format(msg))

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    logging.basicConfig(level= logging.INFO)

    
    username = os.getenv("HMS_USERNAME")
    pwd = os.getenv("HMS_PASSWORD")

    if not username:
        sys.exit("HMS_USERNAME environment variable not set!")

    if not pwd:
        sys.exit("HMS_PASSWORD environment variable not set!")

    logging.info("Attempting login as {}...".format(username))
    
    hms = HMS()
    hms.try_login(username, pwd)

    if not hms.is_logged_in(username):
       sys.exit("Could not login to hms")

    logging.info("Login success!")

    if args["--list"]:
        booking_divs = hms.get_calendar("laser")
        bookings = booking.convert_divs_to_bookings(booking_divs)
        
        bookings = filter(filter_bookings_for_rest_of_day, bookings)
        
        for b in bookings:
            print("{:%H:%M} to {:%H:%M} ({})".format(b.start, b.end, b.name))

    else:
        booking_info = booking.BookingInfo.from_args(args)
        book_laser(hms, booking_info)