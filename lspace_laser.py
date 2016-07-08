""" lspace_laser.py

Usage:
    lspace_laser.py <start_time> <end_time> [<date>]

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
import urllib.parse

from pytz import timezone

from collections import namedtuple

from robobrowser import RoboBrowser

BookingInfo = namedtuple("BookingInfo", ["start", "end"])

HMS_ROOT = "https://lspace.nottinghack.org.uk/hms"

def get_browser(url):
    br = RoboBrowser()
    br.open(url)

    return br

def try_login(br, user, pwd):
    form = br.get_form(id="UserLoginForm")

    form["data[User][usernameOrEmail]"].value = user
    form["data[User][password]"].value = pwd

    br.submit_form(form)

def logged_in_to_lspace(br, user):
    login_div = br.select("div.login")
    
    return user in login_div[0].text

def args_to_booking_info(args):

    start = args["<start_time>"]
    end = args["<end_time>"]
    date_str = args.get("<date>", None)
    
    start_hour = int(start[0:2])
    start_min = int(start[2:4])
    start_min = math.floor(start_min / 15) * 15

    end_hour = int(end[0:2])
    end_min = int(end[2:4])
    end_min = math.floor(end_min / 15) * 15
    
    if date_str:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        date = datetime.date.today()
        
    start_dt = datetime.datetime.combine(date, datetime.time(start_hour, start_min))
    end_dt = datetime.datetime.combine(date, datetime.time(end_hour, end_min, tzinfo=timezone("Europe/London")))

    return BookingInfo(start_dt, end_dt)

def format_booking_time(booking_info):

    offset = timezone("Europe/London").utcoffset(booking_info.start)

    return "{0:%Y-%m-%d}T{0:%H}:{0:%M}:00+{1:02d}:00".format(booking_info.start, int(offset.seconds/3600))

def get_encoded_booking_url(booking_info):
    return HMS_ROOT + "/tools/addbooking/1?t=" + urllib.parse.quote(format_booking_time(booking_info))

def on_laser_booking_form(br):
    return "Add laser Booking" in br.select("h2")[0].text

def try_booking(br, booking_info):
    form = br.get_form(id="ToolAddbookingForm")
    form["data[Tool][start_hours]"].value = "{:%H}".format(booking_info.start)
    form["data[Tool][start_mins]"].value = "{:%M}".format(booking_info.start)
    form["data[Tool][end_hours]"].valueb= "{:%H}".format(booking_info.end)
    form["data[Tool][end_mins]"].value = "{:%M}".format(booking_info.end)

    br.submit_form(form)

def booking_succeesful(br):
    flash = br.select("#flashMessage")
    print(flash[0].text)
    return "Booking Added" in flash[0].text, flash[0].text

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    logging.basicConfig(level= logging.INFO)

    booking_info = args_to_booking_info(args)
    booking_url = get_encoded_booking_url(booking_info)
    
    username = os.getenv("LSPACE_USERNAME")
    pwd = os.getenv("LSPACE_PASSWORD")

    logging.info("Booking laser on {0:%Y-%m-%d}, {0:%H:%M} to {1:%H:%M}".format(
        booking_info.start, booking_info.end))

    br = get_browser(HMS_ROOT + "/members/login")

    logging.info("Attempting login as {}...".format(username))
    
    try_login(br, username, pwd)

    if not logged_in_to_lspace(br, username):
       sys.exit("Could not login to lspace")

    logging.info("Login success!")
    logging.info("Navigating to laser booking url '{}'".format(urllib.parse.unquote(booking_url)))
    
    br.open(booking_url)

    if not on_laser_booking_form(br):
        sys.exit("Could not open laser booking form")

    try_booking(br, booking_info)

    success, msg = booking_succeesful(br)
    logging.info("Booking created!" if success else "Booking not created! Reason: '{}'".format(msg))