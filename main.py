#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Made by @alcortazzo

import time
import urllib
import logging
import requests
from telebot import TeleBot, types, apihelper

bot = TeleBot("REPLACE YOUR TOKEN HERE")
shouldBotLog = True  # if False bot will not create and keep log.log file


def get_status(command, page):
    link = f"https://man.archlinux.org/man/{command}.{page}"
    try:
        response = urllib.request.urlopen(link)
        return response.getcode()
    except Exception as e:
        if shouldBotLog:
            logging.info(f"[Info] {link} : {str(e)}")
        return None


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
        "This bot can search man-pages in man.archlinux.org for you in in-line mode",
    )


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    try:
        empty = types.InlineQueryResultArticle()
        bot.answer_inline_query(inline_query.id, empty)
    except Exception as e:
        if shouldBotLog:
            logging.info(f"[Info] {str(e)}")


@bot.inline_handler(lambda query: len(query.query) >= 1)
def query_text(query):
    try:
        answers = []
        if get_status(query.query, "1") == 200:
            answer1 = results_compiler(
                "1",
                f"{query.query}(1)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.1",
            )
            answers.append(answer1)
        if get_status(query.query, "2") == 200:
            answer2 = results_compiler(
                "2",
                f"{query.query}(2)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.2",
            )
            answers.append(answer2)
        if get_status(query.query, "3") == 200:
            answer3 = results_compiler(
                "3",
                f"{query.query}(3)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.3",
            )
            answers.append(answer3)
        if get_status(query.query, "4") == 200:
            answer4 = results_compiler(
                "4",
                f"{query.query}(4)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.4",
            )
            answers.append(answer4)
        if get_status(query.query, "5") == 200:
            answer5 = results_compiler(
                "5",
                f"{query.query}(5)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.5",
            )
            answers.append(answer5)
        if get_status(query.query, "6") == 200:
            answer6 = results_compiler(
                "6",
                f"{query.query}(6)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.6",
            )
            answers.append(answer6)
        if get_status(query.query, "7") == 200:
            answer7 = results_compiler(
                "7",
                f"{query.query}(7)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.7",
            )
            answers.append(answer7)
        if get_status(query.query, "8") == 200:
            answer8 = results_compiler(
                "8",
                f"{query.query}(8)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.8",
            )
            answers.append(answer8)
        if get_status(query.query, "9") == 200:
            answer9 = results_compiler(
                "9",
                f"{query.query}(9)",
                "Send link to this man page",
                f"https://man.archlinux.org/man/{query.query}.9",
            )
            answers.append(answer9)
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