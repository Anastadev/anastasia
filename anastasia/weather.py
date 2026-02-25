#!/usr/bin/env python3
import urllib.request
import json

from telegram import Update
from telegram.ext import ContextTypes


def get_weather(args):
    if len(args) == 0 or len(args) > 1:
        url = "http://api.apixu.com/v1/current.json?key=cb73c1c7552d495b99e163119171101&q=Grenoble"
    elif len(args) == 1:
        url = "http://api.apixu.com/v1/current.json?key=cb73c1c7552d495b99e163119171101&q=" + args[0]

    tmp = urllib.request.urlopen(url).read().decode('utf8')

    j = json.loads(tmp)

    weather = ""
    weather += j["location"]["name"] + " - " + j["location"]["country"] + "\n"
    weather += "Température : " + str(j["current"]["temp_c"]) + " °C\n"
    weather += "Température ressentie : " + str(j["current"]["feelslike_c"]) + " °C" + "\n"
    weather += "Vent : " + str(j["current"]["wind_kph"]) + " km/h" + "\n"
    weather += "Précipitations : " + str(j["current"]["precip_mm"]) + " mm" + "\n"
    weather += "[Tendance](http:"+j["current"]["condition"]["icon"]+")"

    return weather

async def give_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return
    await update.message.reply_text(get_weather(context.args), parse_mode="Markdown")
