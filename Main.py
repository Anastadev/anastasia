#!/usr/bin/env python3

from telegram.ext import Updater
from telegram.ext import CommandHandler
import sys
import joke
import locale
from eat import eat
from room import give_room
from todolist import give_todo

locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

updater = Updater(token=sys.argv[1])
dispatcher = updater.dispatcher


def give_joke(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text=joke.retrieve_joke())


def give_blc(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="On s'en bat les couilles ♫ ")


start_handler = CommandHandler('room', give_room)
joke_handler = CommandHandler('joke', give_joke)
blc_handler = CommandHandler('blc', give_blc)
todo_handler = CommandHandler('todo', give_todo, pass_args=True)
keskonmange_handler = CommandHandler('keskonmange', eat)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(joke_handler)
dispatcher.add_handler(blc_handler)
dispatcher.add_handler(todo_handler)
dispatcher.add_handler(keskonmange_handler)

updater.start_polling()
