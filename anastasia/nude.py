import urllib.request
from bs4 import BeautifulSoup


def get_nude(bot, update, args):
    if len(args) > 0 and args[0] == "men":
        site = urllib.request.urlopen("http://www.bonjourmonsieur.fr/monsieur/random.html")
        html = site.read().decode('iso-8859-1')
        soup = BeautifulSoup(html, 'html.parser')

        nude = soup.find("div", attrs={"class": "img"})
        bot.sendPhoto(chat_id=update.message.chat_id, photo="http://www.bonjourmonsieur.fr/" + nude.h1.img['src'])
    else:
        site = urllib.request.urlopen("http://dites.bonjourmadame.fr/random")
        html = site.read().decode('iso-8859-1')
        soup = BeautifulSoup(html, 'html.parser')

        nude = soup.find("div", attrs={"class": "photo post"})
        bot.sendPhoto(chat_id=update.message.chat_id, photo=nude.a.img['src'])
