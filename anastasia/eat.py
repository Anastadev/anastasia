import requests
import re
import time
import telegram
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
        response = "Il n'y a rien à manger aujourd'hui !"
        res = r.search(s.text)
        if res is not None:
            text = res.group(1)
            r = re.compile(sub_regex, re.MULTILINE)
            res2 = r.findall(html.unescape(text))
            response = ",".join(res2)
        response = resto + ": " + response
        bot.sendMessage(chat_id=update.callback_query.message.chat.id, text=response)
        update.callback_query.answer()

    if update.callback_query.data == "Epicéa":
        site = requests.get("http://www.crous-grenoble.fr/restaurant/ru-lepicea/")
        regex = re.compile(r"<h3>Menu[a-zA-Z ]*" + str(int(time.strftime(
            "%d"))) + ".*(?:\n.*?)*?Midi</span>(.*)", re.MULTILINE)
        answer(regex, site, "Epicéa", r".*?(?:<span.*?>|<li>)(.*?)(?:<\/span>|<\/li>)")

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
