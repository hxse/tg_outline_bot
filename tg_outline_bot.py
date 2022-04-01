#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import json
import pdb


def get_config(dir):
    with open(dir + "config.default.json", "r", encoding="utf-8") as file:
        defaultJson = json.load(file)
    with open(dir + "config.custom.json", "r", encoding="utf-8") as file:
        customJson = json.load(file)
    defaultJson.update(customJson)
    return defaultJson


config = get_config("./")
token = config["token"]
proxy_url = config["proxy"]

REQUEST_KWARGS = REQUEST_KWARGS = {
    "proxy_url": proxy_url,
    # "urllib3_proxy_kwargs": {
    #     "username": "***",
    #     "password": "***",
    # },
}

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        rf"Hi {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    help = """转发到本bot,会返回一个markdown格式链接,链接到频道
    可以批量转发,然后批量复制,再用/clean命令清洗一下,就能得到一个outline大纲了
    mp3音频在转发的时候,没有转发标志,所以链接是NONE这个不是机器人的问题,是tg设计问题
    """
    update.message.reply_text(help)


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    print(update.message)
    update.message.reply_text(update.message.text)


def clean(update: Update, context: CallbackContext):
    # 清洗文本格式
    # import pdb; pdb.set_trace()
    text = update["message"]["text"]
    textStrip = text[len("/clean ") :].strip()
    textArr = [i.strip() for i in textStrip.split("\n") if i.strip() != ""]
    textResult = [v for i, v in enumerate(textArr) if i % 2 != 0]
    print(textResult, len(textResult))
    update.message.reply_text("\n".join(textResult))


def forward(update: Update, context: CallbackContext):
    # 转发text时总会在文件前面,这是tg的问题,不是机器人的问题
    # update.message.reply_text(update.message.text)
    update_id = update["update_id"]
    forward_from_chat = update["message"]["forward_from_chat"]
    forward_from_chat_id = forward_from_chat["id"] if forward_from_chat else None
    forward_from_chat_id = str(forward_from_chat_id).replace("-100", "", 1)
    forward_from_message_id = update["message"]["forward_from_message_id"]
    tgForwardUrl = f"https://t.me/c/{forward_from_chat_id}/{forward_from_message_id}"
    caption = update["message"]["caption"]
    text = update["message"]["text"]
    title = caption if caption else text
    title = title.split("\n")[0]  # 只保留第一行
    print(update)
    print(update_id, forward_from_chat_id, forward_from_message_id)
    update.message.reply_text(f"[{title}]({tgForwardUrl})")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token, request_kwargs=REQUEST_KWARGS)
    updater.bot.set_my_commands([("start", "开始"), ("clean", "清理文本格式"), ("help", "帮助")])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("clean", clean))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.filters.html?highlight=Filters#telegram.ext.filters.Filters.mime_type
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.all & ~Filters.command, forward))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
