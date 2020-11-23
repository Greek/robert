# -*- coding: utf-8 -*-

from discord.ext import commands
from utils import default
import discord
import psutil
import os

class About(commands.Cog):
    """The description for About goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())
        self.config = default.get("config.json")

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ About the bot """
        ramUsage = self.process.memory_full_info().rss / 1024**2
        avgmembers = round(len(self.bot.users) / len(self.bot.guilds))

        embedColour = discord.Embed.Empty
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            embedColour = ctx.me.top_role.colour

        embed = discord.Embed(colour=embedColour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        # embed.add_field(name="Last boot", value=default.timeago(
        #     datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(
            name=f"Developer{'' if len(self.config.owners) == 1 else 's'}",
            value=', '.join([str(self.bot.get_user(x))
                             for x in self.config.owners]),
            inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(
            name="Servers", value=f"{len(ctx.bot.guilds)} ( averaging: {avgmembers} users/server )", inline=True)
        embed.add_field(name="Commands loaded", value=len(
            [x.name for x in self.bot.commands]), inline=True)
        embed.add_field(name="RAM usage", value=f"{ramUsage:.2f} MB", inline=True)

        await ctx.send(content=f"about **{ctx.bot.user}** | **{self.config.version}**", embed=embed)

def setup(bot):
    bot.add_cog(About(bot))
