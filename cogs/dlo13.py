# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Dlo13(commands.Cog):
    """The description for Dlo13 goes here."""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Dlo13(bot))
