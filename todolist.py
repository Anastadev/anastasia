import sys
from pymongo import MongoClient
from loghelper import log
from confighelper import ConfigHelper
from datetime import datetime

conf = ConfigHelper(sys.argv[1])

client = MongoClient(conf.get_db())
db = client[conf.get_db_name()]
todos = db.todos

def usage():
    return "/todo list all todo\n" \
           "/todo [-a %m%d%H task] add a todo (example : /todo -a 251200 kdo)\n" \
           "/todo [-d id] delete a todo"


def cleanList():
    todos.remove({"date": {"$lt": datetime.now()}})


def alltodolist(chat_id):
    cleanList()
    st = ""
    ct = 1
    for todo in todos.find({"chat_id": chat_id}).sort("date") :
        st +=   str(todo["date"].strftime("%d/%m %H")) + " H (" + str(ct) + ") : " + todo["task"] + "\n"
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



def give_todo(bot, update, args):
    if len(args) == 0:
        log.info("Give the todolist")
        bot.sendMessage(chat_id=update.message.chat_id, text=alltodolist(update.message.chat_id))
    elif len(args) >= 3 and args[0] == "-a":
        try:
            d = datetime.strptime(args[1], '%d%m%H')
            y = datetime.now().year
            if d.month < datetime.now().month:
                y += 1
            d = d.replace(year=y)
            addTodo(update.message.chat_id, d, ' '.join(args[2:]))
        except Exception as err:
            log.info("date format error: {0}".format(err))
            bot.sendMessage(chat_id=update.message.chat_id, text=usage())
            return
        log.info("Add to the todolist")
    elif len(args) == 2 and args[0] == "-d":
        log.info("Delete " + args[1] + " to the todolist")
        deleteTodo(update.message.chat_id, args[1])
    else:
        log.info("Bad format command")
        bot.sendMessage(chat_id=update.message.chat_id, text=usage())
