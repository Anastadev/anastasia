from datetime import datetime, timezone, timedelta
import sys
from math import fabs
import re
import time
from icalendar import Calendar
from loghelper import log

file = open('/home/metaheavens/bot_telegram/emploi_du_temps/ade.ics', 'rb')
lastUpdate = datetime.min
cal = Calendar.from_ical(file.read())
file.seek(0)


def refresh_cal():
    log.info("Refreshing calendar.")
    global cal
    cal = Calendar.from_ical(file.read())
    file.seek(0)


def give_room(bot, update):
    log.info("Give the room")
    global lastUpdate
    global cal
    if datetime.utcnow() - timedelta(hours=3) > lastUpdate:
        refresh_cal()
        lastUpdate = datetime.utcnow()
    min_diff = sys.maxsize
    mine = 0
    for e in cal.walk('vevent'):
        date1 = datetime.now()
        t1 = time.mktime(date1.timetuple())
        date2 = utc_to_local(e["DTSTART"].dt)
        t2 = time.mktime(date2.timetuple())
        if t1 < t2 and fabs(t2 - t1) < min_diff:
            min_diff = t2 - t1
            mine = e
    location = mine["LOCATION"]
    regex = r"[A-Z][0-9]{3}( |$|)"
    if re.match(regex, location) is not None:
        location = location[:4]
    bot.sendMessage(chat_id=update.message.chat_id, text=(
    mine["SUMMARY"] + "\n" + location + "\n" + utc_to_local(mine["DTSTART"].dt).strftime("%A %H:%M").capitalize()))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
