#!/usr/bin/env python3

0_0 # Python 3.6 and up is required.

import nextcord
import os

from utils.data import Bot, HelpFormat
from utils.default import get
from dotenv import dotenv_values, load_dotenv

cfg = get("config.json")
dot_cfg = dotenv_values(".env")
load_dotenv(".env")

intents = nextcord.Intents(messages=True, guilds=True, members=True)

bot = nextcord.Client(
    command_prefix=os.environ.get('DISCORD_PREFIX'),
    prefix=os.environ.get('DISCORD_PREFIX'),
    command_attrs=dict(hidden=True),
    help_command=HelpFormat(),
    intents=intents,
    case_insensitive=True,
)

bot.run(os.environ.get("DISCORD_TOKEN"))
