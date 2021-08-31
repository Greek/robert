#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.data import Bot, HelpFormat
from utils.default import get
from dislash import InteractionClient

cfg = get("config.json")
guilds = [880389498570178591]

bot = Bot(
    command_prefix=cfg.prefix,
    prefix=cfg.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat()
)
inter_client = InteractionClient(bot, test_guilds=guilds)

bot.run(cfg.token)
