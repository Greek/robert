#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.data import Bot, HelpFormat
from utils.default import get

token = get("config.json").token

bot = Bot(
    command_prefix="ap ",
    prefix="ap",
    command_attrs=dict(hidden=True),
    help_command=HelpFormat()
)

bot.run(token)
