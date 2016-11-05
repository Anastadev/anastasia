import requests
import re
import time
import telegram


def newEat(bot, update):
    custom_keyboard = [[telegram.InlineKeyboardButton("Diderot", callback_data="Diderot"),
                        telegram.InlineKeyboardButton("Epicéa", callback_data="Epicéa")]]
    reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)
    bot.sendMessage(chat_id=update.message.chat_id, text="De quel restaurant veux-tu le menu ?",
                    reply_markup=reply_markup)


def eatCallback(bot, update):
    def answer(r, s, resto):
        response = "Il n'y a rien à manger aujourd'hui !"
        res = r.search(s.text)
        if res is not None:
            text = res.group(0)
            r = re.compile(r"<li>(.*?)</li>", re.MULTILINE)
            res2 = r.findall(text)
            response = ",".join(res2)
        response = resto + ": " + response
        bot.sendMessage(chat_id=update.callback_query.message.chat.id, text=response)
        update.callback_query.answer()

    if update.callback_query.data == "Epicéa":
        site = requests.get("http://www.crous-grenoble.fr/restaurant/ru-lepicea/")
        regex = re.compile(r"(<h3>Menu[a-zA-Z ]*" + str(int(time.strftime(
            "%d"))) + ".*(?:(?:\n.*?)*?(?:</span></div></div></div>)){1,2})", re.MULTILINE)
        answer(regex, site, "Epicéa")

    elif update.callback_query.data == "Diderot":
        site = requests.get("http://www.crous-grenoble.fr/restaurant/ru-diderot-traditionnel/")
        regex = re.compile(r"(<h3>Menu[a-zA-Z ]*" + str(int(time.strftime(
            "%d"))) + ".*(?:(?:\n.*?)*?(?:</span></div></div></div>)){1,2})", re.MULTILINE)
        answer(regex, site, "Diderot")


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
