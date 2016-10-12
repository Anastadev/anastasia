from telegram.ext import Updater
from telegram.ext import CommandHandler
from icalendar import Calendar
from datetime import datetime, timedelta
import datetime
import time
import sys
from math import fabs
import logging

# Log system
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
steam_handler.setFormatter(formatter)
log.addHandler(steam_handler)

updater = Updater(token='281531409:AAF513XUt-FB_jv9eIxd0SSImg-BbMLeXkw')
dispatcher = updater.dispatcher

file = open('/home/metaheavens/bot_telegram/emploi_du_temps/ade.ics', 'rb')
lastUpdate = datetime.datetime.utcnow()
cal = Calendar.from_ical(file.read())


def refresh_cal():
    global log
    log.info("Refreshing calendar.")
    global cal
    cal = Calendar.from_ical(file.read())


def give_room(bot, update):
    global log
    log.info("Give the room")
    global lastUpdate
    global cal
    if datetime.datetime.utcnow() - timedelta(hours=2) > lastUpdate:
        refresh_cal()
        lastUpdate = datetime.datetime.utcnow()
    min_diff = sys.maxsize
    mine = 0
    for e in cal.walk('vevent'):
        date1 = datetime.datetime.utcnow()
        t1 = time.mktime(date1.timetuple())
        date2 = e["DTSTART"].dt
        t2 = time.mktime(date2.timetuple())
        if t1 < t2 and fabs(t2 - t1) < min_diff:
            min_diff = t2 - t1
            mine = e
    bot.sendMessage(chat_id=update.message.chat_id, text=(mine["SUMMARY"] + "\n" + mine["LOCATION"]))


start_handler = CommandHandler('room', give_room)
dispatcher.add_handler(start_handler)
updater.start_polling()
