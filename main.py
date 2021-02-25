#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Made by @alcortazzo

import sys
import time
import urllib
from os import getenv
import logging
import requests
from telebot import TeleBot, types, apihelper


Bot_TOKEN = getenv("arch_man_bot_token")
if Bot_TOKEN is None:
    sys.exit("You must set <arch_man_bot_token> environment variable!")

bot = TeleBot(Bot_TOKEN)
shouldBotLog = True  # if False bot will not create and keep log.log file


def get_status(command, page):
    link = f"https://man.archlinux.org/man/{command}.{page}"
    try:
        response = urllib.request.urlopen(link)
        return response.getcode()
    except urllib.error.URLError as e:
        if shouldBotLog:
            logging.info(f"[Info] {link} : {str(e)}")


def results_compiler(id, title, description, message):
    answer = types.InlineQueryResultArticle(
        id=id,
        title=title,
        description=description,
        input_message_content=types.InputTextMessageContent(message_text=message),
    )
    return answer


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        "This is an <a href='https://github.com/alcortazzo/arch-man-bot'>open source</a> bot that can search man-pages on man.archlinux.org for you in in-line mode",
        parse_mode="html",
    )


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    empty = types.InlineQueryResultArticle()
    try:
        bot.answer_inline_query(inline_query.id, empty)
    except Exception as e:
        if shouldBotLog:
            logging.info(f"[Info] {str(e)}")


@bot.inline_handler(lambda query: len(query.query) >= 1)
def query_text(query):
    answers = []
    man_page_categories = ("1", "2", "3", "4", "5", "6", "7", "8", "9")

    for category in man_page_categories:
        if get_status(query.query, category) == 200:
            answer = results_compiler(
                category,
                f"{query.query}({category})",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.{category}",
            )
            answers.append(answer)

    try:
        bot.answer_inline_query(query.id, answers, is_personal=False)
    except Exception as e:
        if shouldBotLog:
            logging.error(f"[Error] {str(e)}")


if __name__ == "__main__":
    if shouldBotLog:
        logging.getLogger("requests").setLevel(logging.CRITICAL)
        logging.basicConfig(
            format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s",
            level=logging.INFO,
            filename="log.log",
            datefmt="%d.%m.%Y %H:%M:%S",
        )
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            time.sleep(5)