# coding: utf-8

import urllib.request
import json


def get_indice_from_url(url):
    tmp = urllib.request.urlopen(url).read().decode('utf8')
    j = json.loads(tmp)
    return int(j["data"]["aqi"])


def get_indice_grenoble():
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
    indice = int(indice / 5)
    return indice


def get_json_google_maps(city):
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + city + "&Key=AIzaSyAxdCmDbyuyzQ5IZmVhlYrF2fCLnRmDKhI"
    tmp = urllib.request.urlopen(url).read().decode('utf8')
    return json.loads(tmp)

def get_latitude_longitute(j):
    res = str(j["results"][0]["geometry"]["location"]["lat"]) + ";"
    res += str(j["results"][0]["geometry"]["location"]["lng"])
    return res


def get_formatted_address(j):
    return j["results"][0]["formatted_address"]


def format_args(args):
    res = ""
    for i in range(0, len(args)):
        res += "+"+str(args[i])
    return res


def get_airquality(args):
    if len(args) == 0:
        indice = get_indice_grenoble()
        airquality = "Qualité de l'air, Grenoble\n"
    else:
        if len(args) > 1:
            formated_args = format_args(args)
        else:
            formated_args = args[0]
        j = get_json_google_maps(formated_args)
        url = "http://api.waqi.info/feed/geo:"+get_latitude_longitute(j)+"/?token=f092408be447fbe8a44f9849baf81f46acfc704f"
        indice = get_indice_from_url(url)
        airquality = "Qualité de l'air, " + get_formatted_address(j) + "\n"

    airquality += "Indice : " + str(indice) + " - "
    if 0 < indice < 51:
        airquality += "Bon"
    elif 50 < indice < 101:
        airquality += "Modéré"
    elif 100 < indice < 151:
        airquality += "Malsain pour les gens sensibles"
    elif 150 < indice < 201:
        airquality += "Malsain"
    elif 200 < indice < 251:
        airquality += "Vraiment malsain"
    elif 250 < indice:
        airquality += "Dangereux pour la santé"

    return airquality


def give_airquality(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text=get_airquality(args), parse_mode="Markdown")
