import requests
import telegram
import urllib.request
import re
from bs4 import BeautifulSoup
import time
import html


def new_eat(bot, update):
    custom_keyboard = [[telegram.InlineKeyboardButton("Diderot", callback_data="Diderot"),
                        telegram.InlineKeyboardButton("Epicéa", callback_data="Epicéa"),
                        telegram.InlineKeyboardButton("Barnave", callback_data="Barnave")]]
    reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)
    bot.sendMessage(chat_id=update.message.chat_id, text="De quel restaurant veux-tu le menu ?",
                    reply_markup=reply_markup)


def eat_callback(bot, update):
    def answer(r, s, resto, sub_regex):
        reply = "Il n'y a rien à manger aujourd'hui !"
        res = r.search(s.text)
        if res is not None:
            text = res.group(1)
            r = re.compile(sub_regex, re.MULTILINE)
            res2 = r.findall(html.unescape(text))
            reply = ", ".join([text.capitalize() for text in res2])
        reply = resto + ": " + reply
        bot.sendMessage(chat_id=update.callback_query.message.chat.id, text=reply)
        update.callback_query.answer()

    if update.callback_query.data == "Epicéa":
        site = urllib.request.urlopen("http://www.crous-grenoble.fr/restaurant/ru-lepicea/")
        html_text = site.read().decode('utf-8')
        soup = BeautifulSoup(html_text, 'html.parser')

        list_menu = soup.find("div", attrs={"id": "menu-repas"}).ul.children

        regex = re.compile(r".*?Menu.*?" + str(int(time.strftime("%d"))) + "(.*\n)*", re.MULTILINE)

        result = None
        for menu in list_menu:
            extract = regex.search(str(menu))
            if extract is not None and extract.group(0) is not None:
                result = extract.group(0)

        new_soup = BeautifulSoup(result, 'html.parser')
        list_sections = new_soup(attrs={"class": "liste-plats"})

        response = None
        for item in list_sections[2]("li"):
            if response is None:
                response = str(item.string).capitalize()
            else:
                response = response + ", " + str(item.string).capitalize()

        if response is None:
            bot.sendMessage(chat_id=update.callback_query.message.chat.id, text="Il n'y a rien à manger aujourd'hui !")
            update.callback_query.answer()
        else:
            bot.sendMessage(chat_id=update.callback_query.message.chat.id, text="Epicea: " + response)
            update.callback_query.answer()

    elif update.callback_query.data == "Diderot":
        site = requests.get("http://www.crous-grenoble.fr/restaurant/ru-diderot-traditionnel/")
        regex = re.compile(r"(<h3>Menu[a-zA-Z ]*" + str(int(time.strftime(
            "%d"))) + ".*(?:(?:\n.*?)*?(?:</span></div></div></div>)){1,2})", re.MULTILINE)
        answer(regex, site, "Diderot", r"<li>(.*?)</li>")

    elif update.callback_query.data == "Barnave":
        site = requests.get("http://www.crous-grenoble.fr/restaurant/ru-barnave/")
        regex = re.compile(r"(<h3>Menu[a-zA-Z ]*" + str(int(time.strftime(
            "%d"))) + ".*(?:\n.*?)*?Déjeuner.*?<\/div>)", re.MULTILINE)
        answer(regex, site, "Barnave", r".*?(?:(?:Déjeuner.*?|<\/ul>)<span.*?>|<li>)(.*?)(?:<\/span>|<\/li>)")


def eat(bot, update):
    response = "Il n'y a rien à manger aujourd'hui !"
    r = requests.get("http://www.crous-grenoble.fr/restaurant/ru-diderot-traditionnel/")
    regex = re.compile(r"(<h3>Menu[a-zA-Z ]*" + str(int(time.strftime(
        "%d"))) + ".*(?:(?:\n.*?)*?(?:</span></div></div></div>)){1,2})", re.MULTILINE)
    res = regex.search(r.text)
    if res is not None:
        text = res.group(0)
        regex = re.compile(r"<li>(.*?)</li>", re.MULTILINE)
        res2 = regex.findall(text)
        response = ",".join(res2)
    bot.sendMessage(chat_id=update.message.chat_id, text=response)
