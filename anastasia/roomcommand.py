from datetime import datetime, timezone, timedelta
import sys
from math import fabs
import re
import time
from icalendar import Calendar
import urllib.request


class RoomCommand:
    lastUpdate = datetime.min

    @staticmethod
    def utc_to_local(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    def __init__(self, log, path_ics):
        self.logger = log
        self.path_ics = path_ics
        self.lastUpdate = datetime.min

    def __refresh_cal_if_too_old(self):
        if datetime.utcnow() - timedelta(hours=3) > self.lastUpdate:
            self.logger.info("Refreshing calendar.")
            self.file = urllib.request.urlopen(self.path_ics)
            self.calendar = Calendar.from_ical(self.file.read().decode("iso-8859-1"))
            self.lastUpdate = datetime.utcnow()

    def room(self):
        self.logger.info("Give the room")
        self.__refresh_cal_if_too_old()
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
