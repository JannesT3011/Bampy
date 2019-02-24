import json

def new_config():
    print("Oops.. I cant find a config file! Enter your config now:")
    data = {
        "token": input("Enter your bot token: "),
        "owner": input("Enter your ID: "),
        "prefix": input("Enter your default prefix: "),
        "description": input("Enter the description of your bot: "),
        "api": {
          "pastebin": input("Enter your Pastebin API key: ")
        },
        "database": {
            "user": input("Enter the database user (default=postgres): "),
            "db": input("Enter the database you want to use: "),
            "password": input("Enter the password of your database: "),
            "host": input("Enter the host address of your database (default=127.0.0.1): ")
        }
    }
    with open("core/config.json", "w") as fp:
        json.dump(data, fp, indent=3)

class Config:
    def __init__(self, config_file_name="config"):
        self.name = config_file_name
        """
        Gets all config elements!
        
        :param str config_file_name: name of the config file!
        :raises FileNotFoundError: If file not founds
        """
        try:
            with open("core/config.json") as fp:
                self.config = json.load(fp)
        except FileNotFoundError:
            new_config()

    try:
        # bot stuff
        def token(self):
            return self.config["token"]
        def owner(self):
            return self.config["owner"]
        def prefix(self):
            return self.config["prefix"]
        def description(self):
            return self.config["description"]
        # api stuff
        def pastebin(self):
            return self.config["api"]["pastebin"]
        # database stuff:
        def dbuser(self):
            return self.config["database"]["user"]
        def dbdb(self):
            return self.config["database"]["db"]
        def dbpw(self):
            return self.config["database"]["password"]
        def dbhost(self):
            return self.config["database"]["host"]
        def dblogin(self):
            return {"user": self.dbuser(), "password": self.dbpw(), "database": self.dbdb(), "host": self.dbhost()}
    except AttributeError:
        pass