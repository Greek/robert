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

import json
import nextcord

from nextcord.ext import commands
from utils import embed as embed2
from utils.data import Bot


class EventsGuild(commands.Cog):
    """Guild event handlers"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        file = open("./config.json", encoding="utf8")
        config = json.load(file)

        try:
            cid = int(config.get("guild_log"))
        except ValueError:
            return

        log_channel: nextcord.TextChannel = self.bot.get_channel(cid)
        embed = await embed2.create_guild_join(guild)

        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        file = open("config.json", encoding="utf8")
        config = json.load(file)

        try:
            cid = int(config.get("guild_log"))
        except ValueError:
            return print(
                "[Guild Log] Tried to log guild leave, no channel ID found in config"
            )

        log_channel: nextcord.TextChannel = self.bot.get_channel(cid)
        embed = await embed2.create_guild_leave(guild)

        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(EventsGuild(bot))
