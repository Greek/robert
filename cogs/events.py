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

from nextcord import Guild, TextChannel, User, Message
import nextcord
import json
from nextcord.ext import commands
from utils import default
from utils import embed as embed2
from utils.data import create_error_log
from utils.default import translate as _
import datetime
from pytz import timezone


class Events(commands.Cog):
    """Event listeners :Smile:"""

    message_snipe = {}

    def __init__(self, bot):
        self.bot = bot
        self.last_timeStamp = datetime.datetime.utcfromtimestamp(0)
        self.config = default.get("config.json")

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"[Bot] Logged on as {self.bot.user} on {len(self.bot.guilds)} guild(s)\n"
        )

        if self.config.status == "idle":
            status = nextcord.Status.idle
        elif self.config.status == "dnd":
            status = nextcord.Status.dnd
        else:
            status = nextcord.Status.online

        if self.config.playing_type == "listening":
            playing_type = 2
        elif self.config.playing_type == "watching":
            playing_type = 3
        else:
            playing_type = 0

        await self.bot.change_presence(
            activity=nextcord.Activity(type=playing_type, name=self.config.playing),
            status=status,
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        f = open("config.json")
        config = json.load(f)
        guilds = config.get("allowlistServers")
        try:
            cid = int(config.get("guild_log"))
        except ValueError:
            return print("[Guild Log] Tried to log join, no channel ID found in config")

        owner: User = await self.bot.fetch_user(guild.owner_id)
        log_channel: TextChannel = self.bot.get_channel(cid)
        embed = default.branded_embed(
            title=f"Guild joined | {guild.name} ({guild.id})",
            color=embed2.success_embed_color,
        )

        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
        embed.add_field(name="Owner", value=f"<@{owner.id}>", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
        embed.add_field(
            name="On Allowlist?",
            value="true" if guild.id in guilds else "false",
            inline=True,
        )
        embed.set_footer(text=f"Owner ID: {guild.owner_id}")
        try:
            embed.add_field(
                name="Invite code",
                value=f"{[str(x.code) for x in await guild.invites()]}",
                inline=True,
            )
        except nextcord.errors.Forbidden:
            embed.add_field(
                name="Invite code", value=f"Could not fetch invite.", inline=True
            )
            pass
        except:
            embed.add_field(
                name="Invite code", value="Failed to print invites", inline=True
            )
            pass
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        f = open("config.json")
        config = json.load(f)
        guilds = config.get("allowlistServers")
        try:
            cid = int(config.get("guild_log"))
        except ValueError:
            return print(
                "[Guild Log] :: Tried to log guild leave, no channel ID found in config"
            )

        owner: User = await self.bot.fetch_user(guild.owner_id)
        log_channel: TextChannel = self.bot.get_channel(cid)
        embed = default.branded_embed(
            title=f"Guild left | {guild.name} ({guild.id})",
            color=embed2.failed_embed_color,
        )

        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
        embed.add_field(name="Owner", value=f"<@{owner.id}>", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
        embed.add_field(
            name="On Allowlist?",
            value="true" if guild.id in guilds else "false",
            inline=True,
        )
        embed.set_footer(text=f"Owner ID: {guild.owner_id}")
        await log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
