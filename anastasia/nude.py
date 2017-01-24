import urllib.request
from bs4 import BeautifulSoup


def get_nude(bot, update):
    site = urllib.request.urlopen("http://dites.bonjourmadame.fr/random")
    html = site.read().decode('iso-8859-1')
    soup = BeautifulSoup(html, 'html.parser')

    nude = soup.find("div", attrs={"class": "photo post"})
    bot.sendPhoto(chat_id=update.message.chat_id, photo=nude.a.img['src'])
