#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.data import Bot, HelpFormat
from utils.default import get

cfg = get("config.json")

bot = Bot(
    command_prefix=cfg.prefix,
    prefix=cfg.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat()
)

bot.run(cfg.token)
