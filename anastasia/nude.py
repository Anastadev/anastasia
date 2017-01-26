import urllib.request
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from anastasia.loghelper import log

T_WOMEN = "women"
T_MEN = "men"

class Nude:

    def __init__(self,config_):
        client = MongoClient(config_.get_db())
        db = client[config_.get_db_name()]
        self.db = db.nudes

    def get_nude(self,bot, update, args):
        if len(args) > 0 and args[0] == "men":
            self.increase(T_MEN, update.message.from_user.id,update.message.from_user.username)
            site = urllib.request.urlopen("http://www.bonjourmonsieur.fr/monsieur/random.html")
            html = site.read().decode('iso-8859-1')
            soup = BeautifulSoup(html, 'html.parser')

            nude = soup.find("div", attrs={"class": "img"})
            bot.sendPhoto(chat_id=update.message.chat_id, photo="http://www.bonjourmonsieur.fr/" + nude.h1.img['src'])
        else:
            self.increase(T_WOMEN,update.message.from_user.id,update.message.from_user.username)
            site = urllib.request.urlopen("http://dites.bonjourmadame.fr/random")
            html = site.read().decode('iso-8859-1')
            soup = BeautifulSoup(html, 'html.parser')

            nude = soup.find("div", attrs={"class": "photo post"})
            bot.sendPhoto(chat_id=update.message.chat_id, photo=nude.a.img['src'])

    def increase(self,type_,userId_,userName_):
        cursor = self.db.find({"user.id":userId_})
        if cursor.count()==0:
            doc = {
                "user":{
                    "id":userId_,
                    "username":userName_,
                },
                "lastUsage":int(time.time()),
                "count":{
                    "daily":1,
                    "men":0,
                    "women":0
                }
            }
            log.info(doc)
            doc["count"][type_] += 1
            self.db.insert_one(doc)
        else:
            doc = cursor[0]
            doc["user"]["username"]=userName_
            currentTime = int(time.time())
            if (currentTime-(currentTime%86400))!=(doc["lastUsage"]-(doc["lastUsage"]%86400)):
                doc["count"]["daily"] = 1
            else:
                doc["count"]["daily"] += 1
            doc["lastUsage"] = currentTime
            doc["count"][type_] += 1
            self.db.replace_one({"user.id":userId_},doc)
            cursor.close()