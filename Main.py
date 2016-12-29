#!/usr/bin/env python3

from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
import sys
from joke import give_blc, give_joke
import locale
from eat import newEat, eatCallback
from roomcommand import RoomCommand
from todolist import give_todo, give_addtodo, todoCallback
from loghelper import log
from confighelper import ConfigHelper


locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

conf = ConfigHelper(sys.argv[1])
updater = Updater(token=conf.get_anastasia_key())
dispatcher = updater.dispatcher

room = RoomCommand(log, conf.path_ics())

start_handler = CommandHandler('room', room.give_room)
joke_handler = CommandHandler('joke', give_joke)
blc_handler = CommandHandler('blc', give_blc)
todo_handler = CommandHandler('todo', give_todo, pass_args=True)
addtodo_handler = CommandHandler('addtodo', give_addtodo, pass_args=True)
keskonmange_handler = CommandHandler('keskonmange', newEat)
callback_handler = CallbackQueryHandler(eatCallback)
callback_handler_todo = CallbackQueryHandler(todoCallback)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(joke_handler)
dispatcher.add_handler(blc_handler)
dispatcher.add_handler(todo_handler)
dispatcher.add_handler(addtodo_handler)
dispatcher.add_handler(keskonmange_handler)
dispatcher.add_handler(callback_handler, group=0)
dispatcher.add_handler(callback_handler_todo, group=1)

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
