#!/usr/bin/env python3
import requests
import re
from bs4 import BeautifulSoup


def retrieve_fact():
    f = requests.get("http://randomfactgenerator.net/")
    fact = f.content
    soup = BeautifulSoup(fact, 'html.parser')
    facts = soup.findAll("div", {"id": "z"})
    fact = ""
    for f in facts:
        fact += f.text
    fact = re.search('(.+?)\.', fact).group(1)
    return fact


def give_fact(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=retrieve_fact())

