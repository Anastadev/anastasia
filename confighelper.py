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
    
    def get_db_name(self):
        return self.config["CONFIG"]["DB_NAME"]

    def get_db(self):
        return self.config["CONFIG"]["DB"]

    def get_webhook(self):
        return self.config["CONFIG"]["WEBHOOK"] == "True"

    def get_webhook_port(self):
        return self.config["WEBHOOK"]["PORT"]

    def get_webhook_adress(self):
        return self.config["WEBHOOK"]["ADRESS"]

    def get_webhook_certif(self):
        return self.config["WEBHOOK"]["CERTIF"]

    def get_webhook_private_ssl(self):
        return self.config["WEBHOOK"]["PRIVATE_SSL"]
