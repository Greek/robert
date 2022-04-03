#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nextcord
import os
import pymongo
from utils.data import Bot, HelpFormat
from utils.default import get
from dotenv import dotenv_values, load_dotenv

cfg = get("config.json")
dot_cfg = dotenv_values(".env")
load_dotenv(".env")

client = pymongo.MongoClient(os.environ.get("MONGO_DB"))
intents = nextcord.Intents(messages=True, guilds=True, members=True)

bot = Bot(
    command_prefix=cfg.prefix,
    prefix=cfg.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat(),
    intents=intents,
    case_insensitive=True,
)

bot.run(os.environ.get("DISCORD_TOKEN"))
