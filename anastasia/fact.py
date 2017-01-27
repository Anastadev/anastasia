#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup

def retrieve_fact():
    site = requests.get("https://www.fortunes-fr.org/fortunes.php")
    html = site.content
    soup = BeautifulSoup(html, 'html.parser')
    facts = soup.findAll("p", {"class": "fortune"})
    fact = ""
    for f in facts:
        fact += f.text
    fact = re.sub("\s\s+", " ", fact)
    return fact


def give_fact(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=retrieve_fact())

