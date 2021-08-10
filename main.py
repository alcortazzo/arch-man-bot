#!/usr/bin/env python3

# Made by @alcortazzo

import sys
import time
import urllib
from os import getenv
from telebot import TeleBot, types


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
    except urllib.error.URLError as ex:
        if shouldBotLog:
            logger.info(f"{link} : {str(ex)}")


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
        "This is an <a href='https://github.com/alcortazzo/arch-man-bot'>open source</a> "
        "bot that can search man-pages on man.archlinux.org for you in in-line mode or "
        "directly in this chat."
        "\n\n/help for more info.",
        parse_mode="html",
        disable_web_page_preview=True,
    )


@bot.message_handler(commands=["help"])
def cmd_help(message):
    bot.send_message(
        message.chat.id,
        "To search with this bot you can easily type @archmanbot and then something you "
        "want to search. For example:"
        "\n\n`@archmanbot lsblk`\n`@archmanbot man`\n`@archmanbot cfdisk`"
        "\n\nOr just send your command in this chat!",
        parse_mode="Markdown",
    )


@bot.inline_handler(lambda query: len(query.query) == 0)
def default_query(inline_query):
    empty = types.InlineQueryResultArticle()
    try:
        bot.answer_inline_query(inline_query.id, empty)
    except Exception as ex:
        if shouldBotLog:
            logger.info(str(ex))


@bot.inline_handler(lambda query: len(query.query) >= 1)
def query_text(query):
    answers = []

    for category in range(1, 10):
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
    except Exception as ex:
        if shouldBotLog:
            logger.error(f"[{type(ex).__name__}] in query_text(): {str(ex)}")


@bot.message_handler(
    func=lambda message: message.content_type == "text" and message.text
)
def message_answer(message):
    for category in range(1, 10):
        if get_status(message.text, category) == 200:
            try:
                bot.send_message(
                    message.chat.id,
                    f"https://man.archlinux.org/man/{message.text}.{category}",
                )
            except Exception as ex:
                if shouldBotLog:
                    logger.error(
                        f"[{type(ex).__name__}] in message_answer(): {str(ex)}"
                    )


if __name__ == "__main__":
    if shouldBotLog:
        import logging

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s"
        )
        # format without time, for easy use of "systemctl"
        formatter_without_time = logging.Formatter(
            "%(filename)s:%(lineno)d %(levelname)s - %(message)s"
        )

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter_without_time)

        file_handler = logging.FileHandler("log.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as ex:
            if shouldBotLog:
                logger.error(f"[{type(ex).__name__}] in bot.polling(): {str(ex)}")
            time.sleep(5)
