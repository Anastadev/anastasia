#!/usr/bin/env python3

def give_credits(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Je suis open source, viens m'inspecter ici : https://github.com/Anastadev/anastasia")
