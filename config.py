import configparser
import os
import time

path = 'config.cfg'
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
def create_config():
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "bot_token", "token")
    config.set("Settings", "bot_login", "token")

    config.set("Settings", "admin_id", "0:1")

    config.set("Settings", "qiwi_number", "0")
    config.set("Settings", "qiwi_token", "0")

    config.set("Settings", "api_smsactivate", "10")

    config.set("Settings", "min_bank", "10")
    config.set("Settings", "range_game_list", "10")
    config.set("Settings", "percent", "8")

    #CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    with open(path, "w") as config_file:
        config.write(config_file)

#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
def check_config_file():
    if not os.path.exists(path):
        create_config()
        
        print('Config created')
        time.sleep(3)
        exit(0)

#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
def config(what):
    
    config = configparser.ConfigParser()
    config.read(path)

    value = config.get("Settings", what)

    return value


def edit_config(setting, value):
    config = configparser.ConfigParser()
    config.read(path)

    config.set("Settings", setting, value)

    with open(path, "w") as config_file:
        config.write(config_file)


check_config_file()