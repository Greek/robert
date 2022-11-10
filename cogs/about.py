"""
Copyright (c) 2021-present Onyx Studios

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

import os
import platform
from random import choice

import nextcord
import psutil
from nextcord.ext import commands

from utils import default
from utils.data import Bot
from utils.default import translate as _


class About(commands.Cog):
    """Basic commands providing information about the bot."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())
        self.config = default.get("config.json")

    @commands.command(
        name="about", description=_("cmds.about"), aliases=["info", "stats", "status"]
    )
    async def about(self, ctx: commands.Context):
        try:
            avg_members = sum(g.member_count for g in self.bot.guilds)

            if hasattr(ctx, "guild") and ctx.guild is not None:
                embed_color = (
                    ctx.guild.me.top_role.color
                    if isinstance(ctx, nextcord.Interaction)
                    else ctx.me.top_role.color
                )
                embed = nextcord.Embed(
                    title=f"About {self.bot.user.name}",
                    color=embed_color,
                )
                embed.set_thumbnail(url=self.bot.user.avatar)
                embed.add_field(
                    name=f"Developer{'' if len(self.config.owners) == 1 else 's'}",
                    value=",\n".join(
                        [str(await self.bot.fetch_user(x)) for x in self.config.owners]
                    ),
                )
                embed.add_field(
                    name="Servers",
                    value=f"{len(self.bot.guilds)} (serving {avg_members} members)",
                    inline=False,
                )
                embed.add_field(
                    name="Host ID",
                    value=f"{platform.node()}",
                )

                await ctx.send(content="", embed=embed)
        except Exception as error:
            await self.bot.create_error_log(ctx, error)

    @commands.command(name="ping", descriptions="Pong!")
    async def ping(self, ctx: commands.Context):
        quotes = [
            "andreas' iphone 13 pro max",
            "my tonka",
            "cloud based septic tank",
        ]

        sent = await ctx.send("Pinging...")
        await sent.edit(
            f"pinged **{choice(quotes)}**, it took {self.bot.latency * 1000:.0f}ms"
        )
        # (edit {datetime.now().timestamp() - sent.created_at.timestamp():.0f}ms)

    @nextcord.slash_command(name="about", description=_("cmds.about"))
    async def about_slash(self, ctx: nextcord.Interaction):
        """Pong!"""
        await self.about(ctx)


def setup(bot):
    bot.add_cog(About(bot))
