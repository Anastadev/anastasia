# coding: utf-8

import urllib.request
import json

# Adapt the google map bounds to get more stations within the air pollution API
# This value works fine for Grenoble
const_bounds = 0.05
unavailable_stations = 0
nb_stations = 0
grenoble = "Grenoble"


def get_indice_from_bounds(url):
    """Return the average aqi of all stations founded within the area."""
    global nb_stations
    global unavailable_stations

    tmp = urllib.request.urlopen(url).read().decode('utf8')
    j = json.loads(tmp)
    nb_stations= len(j["data"])
    indice = 0
    for i in range(0,nb_stations):
        #station off
        if j["data"][i]["aqi"] == "-":
            unavailable_stations = unavailable_stations + 1
            continue;
        indice+=int(j["data"][i]["aqi"])
    diff = nb_stations-unavailable_stations
    if diff != 0:
        indice = int(indice / diff)
    return indice


def get_json_google_maps(city):
    """Return json from the request of Google Geocode API"""
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + city + "&Key=AIzaSyAxdCmDbyuyzQ5IZmVhlYrF2fCLnRmDKhI"
    tmp = urllib.request.urlopen(url).read().decode('utf8')
    return json.loads(tmp)


def get_bounds(j):
    """Return the bounds where the air stations can be found through the air pollution API"""
    res = str(j["results"][0]["geometry"]["bounds"]["southwest"]["lat"]-const_bounds) + ","
    res += str(j["results"][0]["geometry"]["bounds"]["southwest"]["lng"]-const_bounds) + ","
    res += str(j["results"][0]["geometry"]["bounds"]["northeast"]["lat"]+const_bounds) + ","
    res += str(j["results"][0]["geometry"]["bounds"]["northeast"]["lng"]+const_bounds)
    return res


def format_args(args):
    """Format the arguments for the google API"""
    res = ""
    for i in range(0, len(args)):
        res += "+"+str(args[i])
    return res


def get_airquality(args):
    if len(args) > 0:
        formated_args = format_args(args)
    else:
        formated_args = grenoble
    j = get_json_google_maps(formated_args)
    url = "http://api.waqi.info/map/bounds/?latlng="+get_bounds(j)+"&token=f092408be447fbe8a44f9849baf81f46acfc704f"
    indice = get_indice_from_bounds(url)
    airquality = "Qualité de l'air, " + j["results"][0]["formatted_address"]

    if nb_stations-unavailable_stations > 0:
        airquality += "\nIndice : " + str(indice) + " - "
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

    if unavailable_stations > 0:
        airquality += "\nStations disponibles : " + str(nb_stations-unavailable_stations) + "/" + str(nb_stations)

    return airquality


def give_airquality(bot, update, args):
    bot.sendMessage(chat_id=update.message.chat_id, text=get_airquality(args), parse_mode="Markdown")
