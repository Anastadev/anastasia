#!/usr/bin/env python3

from telegram.ext import Updater
from telegram.ext import CommandHandler
from icalendar import Calendar
from datetime import datetime, timedelta, timezone
import time
import sys
from math import fabs
import logging
import joke
import re


# Log system
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
steam_handler.setFormatter(formatter)
log.addHandler(steam_handler)

#MASTER KEY
#updater = Updater(token='281531409:AAF513XUt-FB_jv9eIxd0SSImg-BbMLeXkw')

#DEV KEY
updater = Updater(token='264517660:AAHvQbyH5VygrJ_hhp1_IhFLcUeZP6iqPVI')

dispatcher = updater.dispatcher

file = open('/home/metaheavens/bot_telegram/emploi_du_temps/ade.ics', 'rb')
lastUpdate = datetime.min
cal = Calendar.from_ical(file.read())
file.seek(0)


def refresh_cal():
    global log
    log.info("Refreshing calendar.")
    global cal
    global file
    cal = Calendar.from_ical(file.read())
    file.seek(0)


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def give_joke(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=joke.retrieve_joke())


def give_blc(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="On s'en bat les couilles &#9835")


def give_room(bot, update):
    global log
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
    bot.sendMessage(chat_id=update.message.chat_id, text=(mine["SUMMARY"] + "\n" + location + "\n" + utc_to_local(mine["DTSTART"].dt).strftime("%Y-%m-%d %H:%M")))


start_handler = CommandHandler('room', give_room)
joke_handler = CommandHandler('joke', give_joke)
blc_handler = CommandHandler('blc', give_blc)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(joke_handler)
dispatcher.add_handler(blc_handler)
updater.start_polling()
