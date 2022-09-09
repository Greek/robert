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
from utils import embed as embed2, default


class EventsGuild(commands.Cog):
    """Guild event handlers"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        file = open("./config.json")
        config = json.load(file)
        # guilds = config.get("allowlistServers")

        try:
            cid = int(config.get("guild_log"))
        except ValueError:
            return

        owner: nextcord.User = await self.bot.fetch_user(guild.owner_id)
        log_channel: nextcord.TextChannel = self.bot.get_channel(cid)
        embed = default.branded_embed(
            title=f"Guild joined | {guild.name} ({guild.id})",
            color=embed2.success_embed_color,
        )

        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
        embed.add_field(name="Owner", value=f"<@{owner.id}>", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
        # embed.add_field(
        #     name="On Allowlist?",
        #     value="true" if guild.id in guilds else "false",
        #     inline=True,
        # )
        embed.set_footer(text=f"Owner ID: {guild.owner_id}")
        try:
            embed.add_field(
                name="Invite code",
                value=f"{[str(x.code) for x in await guild.invites()]}",
                inline=True,
            )
        except nextcord.errors.Forbidden:
            embed.add_field(
                name="Invite code", value="Could not fetch invite.", inline=True
            )
        # pylint: disable=W0703
        except Exception:
            embed.add_field(
                name="Invite code", value="Failed to print invites", inline=True
            )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        file = open("config.json")
        config = json.load(file)
        # guilds = config.get("allowlistServers")
        try:
            cid = int(config.get("guild_log"))
        except ValueError:
            return print(
                "[Guild Log] Tried to log guild leave, no channel ID found in config"
            )

        owner: nextcord.User = await self.bot.fetch_user(guild.owner_id)
        log_channel: nextcord.TextChannel = self.bot.get_channel(cid)
        embed = default.branded_embed(
            title=f"Guild left | {guild.name} ({guild.id})",
            color=embed2.failed_embed_color,
        )

        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
        embed.add_field(name="Owner", value=f"<@{owner.id}>", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
        # embed.add_field(
        #     name="On Allowlist?",
        #     value="true" if guild.id in guilds else "false",
        #     inline=True,
        # )
        embed.set_footer(text=f"Owner ID: {guild.owner_id}")
        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(EventsGuild(bot))
