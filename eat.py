import requests
import re
import time


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
