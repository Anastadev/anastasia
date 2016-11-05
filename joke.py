#!/usr/bin/env python3
import urllib.request
import re
from bs4 import BeautifulSoup


def retrieve_joke():
    # f = urllib.request.urlopen("http://noussommesquatrevingt.com/ESSAYER/")
    f = urllib.request.urlopen("http://humour-blague.com/blagues-2/index.php")
    joke = f.read().decode('iso-8859-1')
    soup = BeautifulSoup(joke, 'html.parser')
    # jokes = soup.findAll("p", { "class" : "vSpace-large _joke-target" })
    jokes = soup.findAll("p", {"class": "blague"})
    joke = ""
    for j in jokes:
        joke += j.text
    joke = re.sub("\s\s+", " ", joke)
    return joke


def give_joke(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=retrieve_joke())


def give_blc(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="On s'en bat les couilles ♫ ")
