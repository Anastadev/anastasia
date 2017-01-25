import urllib.request
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

T_WOMEN = 0
T_MEN = 1

class Nude:

    def __init__(self,config_):
        client = MongoClient(config_.get_db())
        db = client[config_.get_db_name()]
        self.db = db.nudes

    def get_nude(self,bot, update, args):
        if len(args) > 0 and args[0] == "men":
            self.increase(T_MEN, update)
            site = urllib.request.urlopen("http://www.bonjourmonsieur.fr/monsieur/random.html")
            html = site.read().decode('iso-8859-1')
            soup = BeautifulSoup(html, 'html.parser')

            nude = soup.find("div", attrs={"class": "img"})
            bot.sendPhoto(chat_id=update.message.chat_id, photo="http://www.bonjourmonsieur.fr/" + nude.h1.img['src'])
        else:
            self.increase(T_WOMEN,update)
            site = urllib.request.urlopen("http://dites.bonjourmadame.fr/random")
            html = site.read().decode('iso-8859-1')
            soup = BeautifulSoup(html, 'html.parser')

            nude = soup.find("div", attrs={"class": "photo post"})
            bot.sendPhoto(chat_id=update.message.chat_id, photo=nude.a.img['src'])

    def increase(self,type_,update_):
        doc = self.db.find_one({"userId:",update_.callback_query.from.id})
        if doc is None:
            doc = {
                "userId":update_.callback_query.from.id,
                "lastUsage":int(time.time()),
                "count":{
                    "daily":1,
                    "men":0,
                    "women":0
                }
            }
            if type_ == T_WOMEN:
                doc.count.women += 1
            elif type_ == T_MEN:
                doc.count.man += 1
            self.db.insert_one(doc)
        else:
            currentTime = int(time.time())
            if (currentTime-currentTime%86400)!=(doc.lastUsage-doc.lastUsage%86400):
                doc.count.daily = 1
            else:
                doc.count.daily += 1
            doc.lastUsage = currentTime
            if type_ == T_WOMEN:
                doc.count.women += 1
            elif type_ == T_MEN:
                doc.count.man += 1
            self.db.replace_one({"userId:",update_.callback_query.from.id},doc)