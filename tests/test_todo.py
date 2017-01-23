from datetime import datetime, timedelta
from unittest import TestCase

from anastasia import confighelper
from anastasia import todolist


class TestTodo(TestCase):

    def test_all_to_do_list(self):
        conf = confighelper.ConfigHelper("config.ini")
        todo = todolist.Todo(conf)
        date = datetime.now()
        date += timedelta(days=1)
        try:
            todo.delete_todo(1,1)
        except:
            pass
        todo.add_todo(1,1,date,"test")
        self.assertEqual(self.countTodo(todo.all_to_do_list(1)),1)
        todo.delete_todo(1, 1)


    def test_delete_todo(self):
        conf = confighelper.ConfigHelper("config.ini")
        todo = todolist.Todo(conf)
        date = datetime.now()
        date += timedelta(days=1)
        try:
            todo.delete_todo(1,1)
        except:
            pass
        todo.add_todo(1,1,date,"test")
        todo.add_todo(1,2,date,"teste")
        self.assertEqual(self.countTodo(todo.all_to_do_list(1)),2)
        todo.delete_todo(1, 1)
        self.assertEqual(self.countTodo(todo.all_to_do_list(1)),1)
        todo.delete_todo(1, 1)
        self.assertEqual(self.countTodo(todo.all_to_do_list(1)),0)


    def test_add_todo(self):
        conf = confighelper.ConfigHelper("config.ini")
        todo = todolist.Todo(conf)
        date = datetime.now()
        date += timedelta(days=1)
        try:
            todo.delete_todo(1,1)
        except:
            pass
        todo.add_todo(1,1,date,"test")
        self.assertEqual(self.countTodo(todo.all_to_do_list(1)),1)
        todo.delete_todo(1, 1)


    def countTodo(self, string):
        return string.count('\n')
