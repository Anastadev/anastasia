#!/usr/bin/env python3

import locale
import sys

from anastasia import airquality, confighelper, joke, loghelper, roomcommand, todolist, weather
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import Updater

from anastasia.eat import new_eat, eat_callback


def main():
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

    conf = confighelper.ConfigHelper(sys.argv[1])
    updater = Updater(token=conf.get_anastasia_key())
    dispatcher = updater.dispatcher

    room = roomcommand.RoomCommand(loghelper.log, conf.path_ics())
    todo = todolist.Todo()

    start_handler = CommandHandler('room', room.give_room)
    joke_handler = CommandHandler('joke', joke.give_joke)
    blc_handler = CommandHandler('blc', joke.give_blc)
    todo_handler = CommandHandler('todo', todo.give_todo, pass_args=True)
    addtodo_handler = CommandHandler('addtodo', todo.give_add_todo, pass_args=True)
    keskonmange_handler = CommandHandler('keskonmange', new_eat)
    weather_handler = CommandHandler('weather', weather.give_weather, pass_args=True)
    airquality_handler = CommandHandler('airquality', airquality.give_airquality)

    callback_handler = CallbackQueryHandler(eat_callback)
    callback_handler_todo = CallbackQueryHandler(todo.todo_callback)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(joke_handler)
    dispatcher.add_handler(blc_handler)
    dispatcher.add_handler(todo_handler)
    dispatcher.add_handler(addtodo_handler)
    dispatcher.add_handler(keskonmange_handler)
    dispatcher.add_handler(callback_handler, group=0)
    dispatcher.add_handler(callback_handler_todo, group=1)
    dispatcher.add_handler(weather_handler)
    dispatcher.add_handler(airquality_handler)

    if not conf.get_webhook():
        updater.start_polling()
    else:
        updater.start_webhook(
            listen='0.0.0.0',
            port=int(conf.get_webhook_port()),
            url_path=conf.get_anastasia_key(),
            key=conf.get_webhook_private_ssl(),
            cert=conf.get_webhook_certif(),
            webhook_url=
            conf.get_webhook_adress() + ":" + conf.get_webhook_port() + "/" + conf.get_anastasia_key()
        )

    updater.start_polling()
