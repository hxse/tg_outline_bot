#!/usr/bin/env python3
# coding: utf-8
import json
from telegram import Bot, utils


def get_config(dir):
    with open(dir + "config.default.json", "r", encoding="utf-8") as file:
        defaultJson = json.load(file)
    with open(dir + "config.custom.json", "r", encoding="utf-8") as file:
        customJson = json.load(file)
    defaultJson.update(customJson)
    return defaultJson


config = get_config("./")
token = config["token"]
chat_id = config["chat_id"]
print(token)
print(chat_id)

proxy = utils.request.Request(proxy_url="http://127.0.0.1:7890")
bot = Bot(token=token, request=proxy)
bot.send_message(chat_id=chat_id, text="新消息")
