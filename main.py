#!/usr/bin/env python3

# Made by @alcortazzo

import sys
import logging
import requests
from os import getenv

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

logging.basicConfig(level=logging.INFO)

API_TOKEN = getenv("arch_man_bot_token")
if API_TOKEN is None:
    sys.exit("You must set <arch_man_bot_token> environment variable!")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(
        "This is an <a href='https://github.com/alcortazzo/arch-man-bot'>open source</a> "
        "bot that can search man-pages on man.archlinux.org for you in in-line mode or "
        "directly in this chat."
        "\n\n/help for more info.",
        parse_mode="html",
        disable_web_page_preview=True,
    )


@dp.message_handler(commands=["help"])
async def send_welcome(message: types.Message):
    await message.reply(
        "To search with this bot you can easily type @archmanbot and then something you "
        "want to search. For example:"
        "\n\n`@archmanbot lsblk`\n`@archmanbot man`\n`@archmanbot cfdisk`"
        "\n\nOr just send your command in this chat!",
        parse_mode="Markdown",
    )


def get_status(command):
    url = f"https://man.archlinux.org/man/{command}"
    response = requests.get(url)
    return response


@dp.message_handler()
async def message_answer(message: types.Message):
    response = get_status(message.text)

    if response.status_code == 200:
        await message.reply(response.url)


@dp.inline_handler(lambda inline_query: len(inline_query.query) >= 1)
async def query_answer(inline_query: InlineQuery):
    response = get_status(inline_query.query)
    if response.status_code == 200:
        answer = InlineQueryResultArticle(
            id=response.url[-1:],
            title=f"{inline_query.query}({response.url[-1:]})",
            description="Send link to this man page",
            input_message_content=InputTextMessageContent(message_text=response.url),
        )
    await bot.answer_inline_query(inline_query.id, results=[answer], is_personal=False)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
