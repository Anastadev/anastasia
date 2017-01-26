#!/usr/bin/env python3
import urllib.request
import re
from bs4 import BeautifulSoup


def retrieve_fact():
    f = urllib.request.urlopen("http://randomfactgenerator.net/")
    fact = f.read().decode('iso-8859-1')
    soup = BeautifulSoup(fact, 'html.parser')
    facts = soup.findAll("div", {"id": "z"})
    fact = facts.text
    return fact


def give_fact(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=retrieve_fact())

