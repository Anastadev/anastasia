import redis
import telegram

r = redis.Redis("localhost")


def click(bot, update):
    print("COUCOU")
    print(update.message.from_user.id)
    nb_click = 0
    redisRes = r.get(str(update.message.from_user.id) + ".click")
    if redisRes is not None:
        nb_click = redisRes
    custom_keyboard = [[telegram.InlineKeyboardButton("Click", callback_data="Click")]]
    reply_markup = telegram.InlineKeyboardMarkup(custom_keyboard)
    bot.sendMessage(chat_id=update.message.chat_id, text="Jeu du click !",
                    reply_markup=reply_markup)


def clickCallback(bot, update):
    if update.callback_query.data == "Click":
        prec = 0
        redisRes = r.get(str(update.callback_query.from_user.id) + ".click")
        if redisRes is not None:
            prec = redisRes
        r.set(str(update.callback_query.from_user.id) + ".click", int(prec) + 1)
        update.callback_query.answer(str(int(prec) + 1))


id_user = ""
r.set(id_user + "prenom", "prenom du mec")
r.set(id_user + "nom", "nom du mec")
r.set(id_user + "click", "nbclick")
