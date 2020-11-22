# -*- coding: utf-8 -*-

from discord.ext import commands
from discord.ext.commands import errors
from utils import default
import discord


class Events(commands.Cog):
    """Event listeners :Smile:"""

    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.Cog.listener()
    async def on_ready(self):
        if self.config.status == "idle":
            status = discord.Status.idle
        elif self.config.status == "dnd":
            status = discord.Status.dnd
        else:
            status = discord.Status.online

        if self.config.playing_type == "listening":
            playing_type = 2
        elif self.config.playing_type == "watching":
            playing_type = 3
        else:
            playing_type = 0

        await self.bot.change_presence(
            activity=discord.Activity(type=playing_type, name=self.config.playing),
            status=status,
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument):
            pass


def setup(bot):
    bot.add_cog(Events(bot))
