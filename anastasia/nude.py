import urllib.request
from bs4 import BeautifulSoup
import datetime
import random

T_WOMEN = "women"
T_MEN = "men"
T_BLACKLIST = [252593638]
T_MAXFORBLACKLISTED = 30


def get_nude(bot, update, args):
    if len(args) > 0 and args[0] == "men":
        site = urllib.request.urlopen("http://www.pausephp.com/monsieur/random.html")
        html = site.read().decode('iso-8859-1')
        soup = BeautifulSoup(html, 'html.parser')

        nude = soup.find("div", attrs={"class": "img"})
        bot.sendPhoto(chat_id=update.message.chat_id, photo="http://www.pausephp.com/" + nude.h1.img['src'])
    else:
        days_before = random.randint(0, 200)
        day = (datetime.datetime.now() - datetime.timedelta(days_before))
        while day.weekday() == 6 or day.weekday() == 5:
            days_before = random.randint(0, 200)
            day = (datetime.datetime.now() - datetime.timedelta(days_before))
        day_str = day.strftime("%Y/%m/%d")
        url = "https://www.bonjourmadame.fr/" + str(day_str)
        print(url)
        site = urllib.request.urlopen(url)
        html = site.read().decode('iso-8859-1')
        soup = BeautifulSoup(html, 'html.parser')

        nude = soup.find("div", attrs={"class": "post-content"})
        bot.sendPhoto(chat_id=update.message.chat_id, photo=nude.p.img['src'])
