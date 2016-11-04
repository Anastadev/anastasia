import configparser


class ConfigHelper:
    def __init__(self, file):
        self.file = file
        self.config = configparser.ConfigParser()
        self.config.read(self.file)

    def get_anastasia_key(self):
        return self.config["CONFIG"]["KEY"]

    def path_ics(self):
        return self.config["CONFIG"]["ICS_PATH"]

    def get_db_user(self):
        return self.config["CONFIG"]["DB_USER"]

    def get_db_pass(self):
        return self.config["CONFIG"]["DB_PASS"]

    def get_db_name(self):
        return self.config["CONFIG"]["DB_NAME"]