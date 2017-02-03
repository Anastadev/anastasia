from pymongo import MongoClient
from anastasia.loghelper import log

class MongoDA:

    __mongo = None
    __uri = None
    __dbName = None
    __connect = None

    @staticmethod
    def init(config_):
        MongoDA.__uri = config_.get_db()
        MongoDA.__dbName = config_.get_db_name()

    @staticmethod
    def getDB():
        if MongoDA.__mongo is None:
            log.info("Database initialization")
            MongoDA.__connect = MongoClient(MongoDA.__uri)
            MongoDA.__mongo = MongoDA.__connect[MongoDA.__dbName]
        return MongoDA.__mongo

def getDB():
    return MongoDA.getDB()


