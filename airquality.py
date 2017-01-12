#!/usr/bin/env python3
import urllib.request
import json

def get_indice_from_url(url):
    tmp = urllib.request.urlopen(url).read().decode('utf8')
    j = json.loads(tmp)
    return int(j["data"]["aqi"])

def get_airquality():
    airquality = "Qualité de l'air, Grenoble\n"
    indice = 0

    # 5 air quality stations in Grenoble
    # based Latitude/Longitude ==> GRAND BOULEVARD
    url = "http://api.waqi.info/feed/geo:45.1666700;5.7166700/?token=f092408be447fbe8a44f9849baf81f46acfc704f"
    indice += get_indice_from_url(url)

    # based Latitude/Longitude ==> SMH
    url = "http://api.waqi.info/feed/geo:45.1766700;5.7566700/?token=f092408be447fbe8a44f9849baf81f46acfc704f"
    indice += get_indice_from_url(url)

    # based Latitude/Longitude ==> ROCADE SUD
    url = "http://api.waqi.info/feed/geo:45.1566700;5.7166700/?token=f092408be447fbe8a44f9849baf81f46acfc704f"
    indice += get_indice_from_url(url)

    # based Latitude/Longitude ==> LES FRENES
    url = "http://api.waqi.info/feed/geo:45.1566700;5.7266700/?token=f092408be447fbe8a44f9849baf81f46acfc704f"
    indice += get_indice_from_url(url)

    # based Latitude/Longitude ==> FONTAINE
    url = "http://api.waqi.info/feed/geo:45.1766700;5.6866700/?token=f092408be447fbe8a44f9849baf81f46acfc704f"
    indice += get_indice_from_url(url)

    indice = int(indice/5)

    airquality += "Indice : " + str(indice) + " - "
    if(indice > 0 and indice < 51):
        airquality += "Bon"
    elif(indice > 50 and indice < 101):
        airquality += "Modéré"
    elif (indice > 100 and indice < 151):
        airquality += "Insalubre pour les gens sensibles"
    elif (indice > 150 and indice < 201):
        airquality += "Insalubre"
    elif (indice > 200 and indice < 251):
        airquality += "Malsain"
    elif (indice > 250 and indice < 251):
        airquality += "Dangereux pour la santé"

    return airquality


def give_airquality(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=get_airquality(), parse_mode="Markdown")

