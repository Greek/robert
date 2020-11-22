# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Dummycog(commands.Cog):
    """The description for Dummycog goes here."""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Dummycog(bot))
