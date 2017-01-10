#!/usr/bin/env python3
import urllib.request
from bs4 import BeautifulSoup


def get_weather():
    a = urllib.request.urlopen("http://wttr.in/grenoble").read().decode('iso-8859-1')
    soupe = BeautifulSoup(a, 'html.parser')
    reste_de_soupe = soupe.find("pre")

    petit_reste_de_soupe = ""
    nik_parser = 0
    for line in reste_de_soupe.stripped_strings:
        if nik_parser == 0 or nik_parser == 2 or nik_parser == 5:
            petit_reste_de_soupe += "\n" + line
        elif nik_parser == 7:
            petit_reste_de_soupe += " to " + line + " °C\n"
        elif nik_parser == 12:
            petit_reste_de_soupe += "Wind : " + line + " km/h\n"
        elif nik_parser == 16:
            start = line.find("mm") - 4;
            petit_reste_de_soupe += "Precipitation : " + line[start:start+3] + " mm\n"
        elif nik_parser > 16:
            break
        nik_parser=nik_parser+1

    return petit_reste_de_soupe

def give_weather(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=get_weather(),parse_mode="HTML")
