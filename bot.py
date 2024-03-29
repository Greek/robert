#!/usr/bin/env python3

# pylint: disable=E0237,W0104

import os

import nextcord
from dotenv import dotenv_values, load_dotenv

from utils.data import Bot, HelpFormat
from utils.default import get

0_0  # Python 3.6 and up is required.

cfg = get("config.json")
dot_cfg = dotenv_values("./.env")
load_dotenv("./.env")

intents = nextcord.Intents.default()
intents.guild_messages = True
intents.message_content = True
intents.members = True

bot = Bot(
    command_prefix=os.environ.get("DISCORD_PREFIX"),
    help_command=HelpFormat(),
    intents=intents,
    case_insensitive=True,
)

bot.run(os.environ.get("DISCORD_TOKEN"))
