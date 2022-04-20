import nextcord
import json

from nextcord.ext import commands
from nextcord import Guild, TextChannel, User, Message
from utils import embed as embed2, default


class EventsGuild(commands.Cog):
    """Guild event handlers."""

    def __init__(self, bot):
        self.bot = bot

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
                "[Guild Log] Tried to log guild leave, no channel ID found in config"
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
        # embed.add_field(
        #     name="On Allowlist?",
        #     value="true" if guild.id in guilds else "false",
        #     inline=True,
        # )
        embed.set_footer(text=f"Owner ID: {guild.owner_id}")
        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(EventsGuild(bot))
