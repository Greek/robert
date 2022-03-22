#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from discord import AllowedMentions
import nextcord
from utils.data import Bot, HelpFormat
from utils.default import get

cfg = get("config.json")

intents = nextcord.Intents(messages=True, guilds=True, members=True)

bot = Bot(
    command_prefix=cfg.prefix,
    prefix=cfg.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat(),
    intents=intents,
    allowed_mentions=AllowedMentions(everyone=False, users=False),
    case_insensitive=True,
)

bot.run(cfg.token)
