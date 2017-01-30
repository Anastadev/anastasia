#!/usr/bin/env python3
import urllib.request
import requests
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


def get_chatte(bot, update):
    site = requests.get("http://random.cat/meow")
    html = site.text
    print(html)
    photo = re.search('http[^"]*', html)
    photo = photo.group()
    photo = re.sub(r"\\", "", photo)
    bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)

def get_chienne(bot, update):
    site = requests.get("http://random.dog/")
    html = site.content
    soup = BeautifulSoup(html, 'html.parser')
    photo = soup.findAll("img")[0].get('src')
    photo = "http://random.dog/" + photo
    bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)