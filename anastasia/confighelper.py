import configparser


class ConfigHelper:
    def __init__(self, file=None):
        self.file = file
        self.config = configparser.ConfigParser()
        if self.file:
            self.config.read(self.file)

    def get_anastasia_key(self):
        return self.config.get("CONFIG", "KEY", fallback=None)

    def path_ics(self):
        return self.config.get("CONFIG", "ICS_PATH", fallback=None)
    
    def get_db_name(self):
        return self.config.get("CONFIG", "DB_NAME", fallback=None)

    def get_db(self):
        return self.config.get("CONFIG", "DB", fallback=None)

    def get_webhook(self):
        return self.config.get("CONFIG", "WEBHOOK", fallback="False") == "True"

    def get_webhook_port(self):
        return self.config.get("WEBHOOK", "PORT", fallback="443")

    def get_webhook_adress(self):
        return self.config.get("WEBHOOK", "ADRESS", fallback="https://localhost")

    def get_webhook_certif(self):
        return self.config.get("WEBHOOK", "CERTIF", fallback=None)

    def get_webhook_private_ssl(self):
        return self.config.get("WEBHOOK", "PRIVATE_SSL", fallback=None)
