import math
import datetime
import urllib.parse

from pytz import timezone

from collections import namedtuple

TOOLS = {
    'laser': 1
}

class BookingInfo(namedtuple("BookingInfo", ["start", "end", "name"])):

    __slots__ = ()

    @classmethod
    def from_args(cls, args):

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

        return cls(start_dt, end_dt)

    @classmethod
    def from_datetimes(cls, date, start, end, name):
        start_dt = datetime.datetime.combine(date, start)
        end_dt = datetime.datetime.combine(date, end)
        if end_dt < start_dt:
            end_dt += datetime.timedelta(days=1)
        return cls(start_dt, end_dt, name)

    def get_encoded_booking_url(self, root, tool):
        tool_number = TOOLS[tool.lower()]
        encoded_time = urllib.parse.quote(self.format_booking_time())
        return root + "/tools/addbooking/{}?t={}".format(tool_number, encoded_time)

    def format_booking_time(self):

        offset = timezone("Europe/London").utcoffset(self.start)
        return "{0:%Y-%m-%d}T{0:%H}:{0:%M}:00+{1:02d}:00".format(self.start, int(offset.seconds/3600))

def get_calendar_url(root, tool):
    tool_number = TOOLS[tool.lower()]
    return root + "/tools/view/{}".format(tool_number)

def get_day_of_week(booking_div):
    class_attrs = booking_div["class"]
    day =  next(c for c in class_attrs if c.startswith("day_"))
    return int(day[-1]) - 1

def get_start_time(booking_div):
    class_attrs = booking_div["class"]
    start =  next(c for c in class_attrs if c.startswith("start_"))
    hour = int(start[6:8])
    minute = int(start[8:10])
    return datetime.time(hour, minute)

def get_end_time(booking_div):
    class_attrs = booking_div["class"]
    duration = next(c for c in class_attrs if c.startswith("len_"))
    duration = int(duration[4:])
    start_time = get_start_time(booking_div)
    dummy_date = datetime.datetime.combine(datetime.date.today(), start_time)

    return (dummy_date + datetime.timedelta(minutes=duration)).time()

def get_booking_date_from_div(div):
    date_start_of_week = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
    booking_day_of_week = get_day_of_week(div)
    booking_date = date_start_of_week + datetime.timedelta(days=booking_day_of_week)
    return booking_date

def get_name(div):
    return div.text

def div_to_booking(div):
    booking_date = get_booking_date_from_div(div)
    start_time = get_start_time(div)
    end_time = get_end_time(div)
    name = get_name(div)

    return BookingInfo.from_datetimes(booking_date, start_time, end_time, name)

def convert_divs_to_bookings(divs):
    return [div_to_booking(div) for div in divs]
