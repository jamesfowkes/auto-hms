""" auto_laser.py

Usage:
    auto_laser.py <start_time> <end_time> [<date>]

Options:
    <start_time>    Booking start time in hhmm format
    <end_time>      Booking end time in hhmm format
    [<date>]        Booking date in yyyy-mm-dd format (defaults today if not present)
"""

import os
import sys
import math
import docopt
import datetime
import logging

from hms import HMS

from booking import BookingInfo

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    logging.basicConfig(level= logging.INFO)

    booking_info = BookingInfo.from_args(args)
    
    username = os.getenv("HMS_USERNAME")
    pwd = os.getenv("HMS_PASSWORD")

    if not username:
        sys.exit("HMS_USERNAME environment variable not set!")

    if not pwd:
        sys.exit("HMS_PASSWORD environment variable not set!")

    logging.info("Booking laser on {0:%Y-%m-%d}, {0:%H:%M} to {1:%H:%M}".format(
        booking_info.start, booking_info.end))

    logging.info("Attempting login as {}...".format(username))
    
    hms = HMS()
    hms.try_login(username, pwd)

    if not hms.is_logged_in(username):
       sys.exit("Could not login to hms")

    logging.info("Login success!")
    
    hms.open_tools_booking_form(booking_info, "laser")

    if not hms.on_laser_booking_form():
        sys.exit("Could not open laser booking form")

    hms.try_booking(booking_info)

    success, msg = hms.booking_successful()

    logging.info("Booking created!" if success else "Booking not created! Reason: '{}'".format(msg))
