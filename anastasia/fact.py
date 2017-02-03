#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup

def retrieve_citation():
    site = requests.get("https://www.fortunes-fr.org/fortunes.php")
    html = site.content
    soup = BeautifulSoup(html, 'html.parser')
    citas = soup.findAll("p", {"class": "fortune"})
    cita = ""
    for c in citas:
        cita += c.text
    cita = re.sub("\s\s+", " ", cita)
    return cita


def give_citation(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=retrieve_citation())


def retrieve_fact():
    site = requests.get("http://www.savoir-inutile.com/")
    html = site.content
    soup = BeautifulSoup(html, 'html.parser')
    facts = soup.findAll("h2", {"id": "phrase"})
    fact = ""
    for f in facts:
        fact += f.text
    fact = re.sub("\s\s+", " ", fact)
    return fact


def give_fact(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=retrieve_fact())

