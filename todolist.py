import re
import sys
from pymongo import MongoClient
from loghelper import log
from confighelper import ConfigHelper
from datetime import datetime

from telegramcalendar import create_calendar

# contains the month printed by addtodo and the todos content
current_shown_dates = {}

conf = ConfigHelper(sys.argv[1])

client = MongoClient(conf.get_db())
db = client[conf.get_db_name()]
todos = db.todos

def usage():
    return "/todo list all todo\n" \
           "/todo [-d id] delete a todo"


def cleanList():
    todos.remove({"date": {"$lt": datetime.now()}})


def alltodolist(chat_id):
    cleanList()
    st = ""
    ct = 1
    for todo in todos.find({"chat_id": chat_id}).sort("date") :
        st +=   str(todo["date"].strftime("%d/%m")) + " (" + str(ct) + ") : " + todo["task"] + "\n"
        ct += 1
    return st

def deleteTodo(chat_id, id):
    todos.remove(todos.find({"chat_id": chat_id}).sort("date")[int(id)  - 1])


def addTodo(chat_id, date, task):
    todo = {
        "chat_id": chat_id,
        "task": task,
        "date": date
    }
    id = todos.insert_one(todo)
    log.info("insert id : "+str(id))
    return todo


def give_addtodo(bot, update, args) :
    now = datetime.now() #Current date
    chat_id = update.message.chat.id
    date = (now.year,now.month)
    current_shown_dates[chat_id] = [date,' '.join(args)]#Saving the current date in a dict
    markup= create_calendar(now.year,now.month)
    bot.send_message(update.message.chat.id, "Please, choose a date", reply_markup=markup)

def todoCallback(bot, update):
    if update.callback_query.data == "next-month":
        next_month(bot,update)
    elif update.callback_query.data == "previous-month":
        previous_month(bot,update)
    elif update.callback_query.data == "ignore":
        bot.answer_callback_query(update.callback_query.id, text="")
    else:
        choosedday(bot,update)

def choosedday(bot,update):
    ma = re.match("calendar-day-([0-9]+)", update.callback_query.data)
    if ma is not None:
        chat_id = update.callback_query.message.chat.id
        date = datetime.strptime(str(current_shown_dates[chat_id][0][0]) + str(current_shown_dates[chat_id][0][1]),
                                 '%Y%m').replace(day=int(ma.group(1)))
        todo = addTodo(chat_id, date, current_shown_dates[chat_id][1])
        log.info("add todo : " + str(todo))
        bot.edit_message_text(str(todo["date"].strftime("%d/%m")) + " : " + todo["task"], update.callback_query.from_user.id, update.callback_query.message.message_id,
                              reply_markup="")

def previous_month(bot,update):
    chat_id = update.callback_query.message.chat.id
    saved_date = current_shown_dates.get(chat_id)[0]
    if (saved_date is not None):
        year, month = saved_date
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        date = (year, month)
        current_shown_dates[chat_id][0] = date
        markup = create_calendar(year, month)
        bot.edit_message_text("Please, choose a date", update.callback_query.from_user.id, update.callback_query.message.message_id,
                              reply_markup=markup)
        bot.answer_update.callback_queryback_query(update.callback_query.id, text="")
    else:
        # Do something to inform of the error
        pass

def next_month(bot,update):
    chat_id = update.callback_query.message.chat.id
    saved_date = current_shown_dates.get(chat_id)[0]
    if(saved_date is not None):
        year,month = saved_date
        month+=1
        if month>12:
            month=1
            year+=1
        date = (year,month)
        current_shown_dates[chat_id][0] = date
        markup= create_calendar(year,month)
        bot.edit_message_text("Please, choose a date", update.callback_query.from_user.id, update.callback_query.message.message_id, reply_markup=markup)
        bot.answer_callback_query(update.callback_query.id, text="")
    else:
        #Do something to inform of the error
        pass

def give_todo(bot, update, args):
    if len(args) == 0:
        log.info("Give the todolist")
        bot.sendMessage(chat_id=update.message.chat_id, text=alltodolist(update.message.chat_id))
    elif len(args) == 2 and args[0] == "-d":
        log.info("Delete " + args[1] + " to the todolist")
        deleteTodo(update.message.chat_id, args[1])
    else:
        log.info("Bad format command")
        bot.sendMessage(chat_id=update.message.chat_id, text=usage())
