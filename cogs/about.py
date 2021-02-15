# -*- coding: utf-8 -*-

"""
Copyright (c) 2021-present flower and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from discord.ext import commands
from utils import default
import discord
import psutil
import os

class About(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())
        self.config = default.get("config.json")

    @commands.command(aliases=['info', 'stats', 'status'])
    async def about(self, ctx):
        """ About the bot """
        try:
            ram_usage = self.process.memory_full_info().rss / 1024**2
            avg_members = round(len(self.bot.users) / len(self.bot.guilds))

            embed_color = discord.Embed.Empty
            if hasattr(ctx, 'guild') and ctx.guild is not None:
                embed_color = ctx.me.top_role.color

            embed = discord.Embed(color=embed_color)
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
                name="Servers", value=f"{len(ctx.bot.guilds)} ( averaging: {avg_members} users/server )", inline=True)
            embed.add_field(name="Commands loaded", value=len(
                [x.name for x in self.bot.commands]), inline=True)
            embed.add_field(name="RAM usage", value=f"{ram_usage:.2f} MB", inline=True)

            await ctx.send(content=f"about **{ctx.bot.user}**", embed=embed)
        except Exception as e:
            pass

def setup(bot):
    bot.add_cog(About(bot))
