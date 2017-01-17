from datetime import datetime, timezone, timedelta
import sys
from math import fabs
import re
import time
from icalendar import Calendar


class RoomCommand:
    lastUpdate = datetime.min

    @staticmethod
    def utc_to_local(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def __init__(self, log, path_ics):
        self.logger = log
        try:
            self.file = open(path_ics, "r", -1, "iso-8859-1")
        except IOError:
            print("Error: ICS file does not appear to exist.")
            return
        self.calendar = Calendar.from_ical(self.file.read())
        self.lastUpdate = datetime.min
        self.file.seek(0)

    def refresh_cal(self):
        self.logger.info("Refreshing calendar.")
        self.calendar = Calendar.from_ical(self.file.read())
        self.file.seek(0)

    def room(self):
        self.logger.info("Give the room")
        if datetime.utcnow() - timedelta(hours=3) > self.lastUpdate:
            self.refresh_cal()
            self.lastUpdate = datetime.utcnow()
        min_diff = sys.maxsize
        mine = 0
        for e in self.calendar.walk('vevent'):
            date1 = datetime.now()
            t1 = time.mktime(date1.timetuple())
            date2 = self.utc_to_local(e["DTSTART"].dt)
            t2 = time.mktime(date2.timetuple())
            if t1 < t2 and fabs(t2 - t1) < min_diff:
                min_diff = t2 - t1
                mine = e
        location = mine["LOCATION"]
        regex = r"[A-Z][0-9]{3}( |$|)"
        if re.match(regex, location) is not None:
            location = location[:4]
        return mine["SUMMARY"] + "\n" + location + "\n" + self.utc_to_local(mine["DTSTART"].dt).strftime("%A %H:%M").capitalize()

    def give_room(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=(self.room()))
