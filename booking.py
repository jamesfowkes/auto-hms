import math
import datetime
import urllib.parse

from pytz import timezone

from collections import namedtuple

from hms import HMS_ROOT

TOOLS = {
    'laser': 1
}

class BookingInfo(namedtuple("BookingInfo", ["start", "end"])):

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

    def get_encoded_booking_url(self, tool):
        tool_number = TOOLS[tool.lower()]
        encoded_time = urllib.parse.quote(self.format_booking_time())
        return HMS_ROOT + "/tools/addbooking/{}?t={}".format(tool_number, encoded_time)

    def format_booking_time(self):

        offset = timezone("Europe/London").utcoffset(self.start)
        return "{0:%Y-%m-%d}T{0:%H}:{0:%M}:00+{1:02d}:00".format(self.start, int(offset.seconds/3600))
