# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from discord.ext.commands import errors
from discord.ext.commands.cooldowns import BucketType
from utils import default
import datetime


class Events(commands.Cog):
    """Event listeners :Smile:"""

    def __init__(self, bot):
        self.bot = bot
        self.last_timeStamp = datetime.datetime.utcfromtimestamp(0)
        self.config = default.get("config.json")

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"Logged on as {self.bot.user} on {len(self.bot.guilds)} guild(s)"
        )

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
        if isinstance(err, errors.CommandInvokeError):
            await ctx.send(
                "oops, something bad happened! contact andreas#0001 for help.\n"
                + default.traceback_maker(err)
            )

        if isinstance(err, errors.MissingRequiredArgument):
            await ctx.send_help(str(ctx.command))

        if isinstance(err, commands.CommandOnCooldown):
            await print(f"[COOLDOWN] {err}")

    @commands.Cog.listener()
    @commands.cooldown(1, 30, BucketType.user)
    async def on_message(self, message):
        time_difference = (datetime.datetime.utcnow() - self.last_timeStamp).total_seconds()
        if time_difference < 30:
            return
        else:
            if message.content.startswith("grubhub"):
                with open("./media/grubhub.gif", "rb") as file:
                    await message.channel.send(file=discord.File(file, "grubhub.gif"))

            if message.content.startswith("fucking sex"):
                with open("./media/fucking sex.gif", "rb") as file:
                    await message.channel.send(file=discord.File(file, "fucking sex.gif"))

            if message.content.startswith("spunch bop"):
                await message.channel.send("https://tenor.com/view/spunch-bop-spongebob-crying-cube-mr-krabs-gif-19973394")
            
            if message.content.startswith("sex smp"):
                await message.channel.send("https://tenor.com/view/dream-dream-team-sapnap-georgenotfound-technoblade-gif-19248460")


def setup(bot):
    bot.add_cog(Events(bot))
