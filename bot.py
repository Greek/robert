#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nextcord
import os
from utils.data import Bot, HelpFormat
from utils.default import get
from dotenv import dotenv_values, load_dotenv

cfg = get("config.json")
dot_cfg = dotenv_values(".env")
load_dotenv('.env')

intents = nextcord.Intents(messages=True, guilds=True, members=True)
allowed_mentions = nextcord.AllowedMentions(users=False)

bot = Bot(
    command_prefix=cfg.prefix,
    prefix=cfg.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat(),
    intents=intents,
    allowed_mentions=allowed_mentions,
    case_insensitive=True,
)

bot.run(os.environ.get('DISCORD_TOKEN'))
