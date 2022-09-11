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

import nextcord

from nextcord import TextChannel
from nextcord.ext import commands

from utils import embed
from utils.data import Bot
from utils.default import translate as _


class Config(commands.Cog):
    """Guild-specific configurations."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(name="config", aliases=["z", "zen"])
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @config.group(name="welcome")
    async def welcome(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @config.group(name="logs")
    async def logs(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @config.group(name="giveaway")
    async def giveaways(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    # Logs

    @logs.group(name="messages")
    async def messages(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @messages.command(name="set", description=_("cmds.config.logs.message.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs(self, ctx, channel: TextChannel):
        try:
            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {
                        "id": ctx.guild.id,
                        "message_log_channel_id": channel.id,
                    },
                    "update": {
                        "id": ctx.guild.id,
                        "message_log_channel_id": channel.id,
                    },
                },
            )

            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.logs.message.success",
                        channel=channel.mention,
                    )
                )
            )
        except Exception as error:
            print(error)
            await ctx.send(
                embed=embed.failed_embed_ephemeral("Could not change logging channel.")
            )

    @messages.command(
        name="whitelist", description=_("cmds.config.logs.message.desc_whitelist")
    )
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist(self, ctx, channel: TextChannel):
        try:
            res = await self.bot.mguild_config.find_one({"_id": ctx.guild.id})

            try:
                if channel.id in res["messageLogIgnore"]:
                    return await ctx.send(
                        embed=embed.warn_embed_ephemeral(
                            _(
                                "cmds.config.logs.message.res.whitelist.already_whitelisted"
                            )
                        )
                    )
            except:
                pass

            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$push": {"messageLogIgnore": channel.id}},
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.logs.message.res.whitelist.success",
                        channel=channel.mention,
                    )
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except Exception as error:
            self.bot.logger.error(error)
            await self.bot.create_error_log(ctx, error)

    @messages.command(
        name="unwhitelist", description=_("cmds.config.logs.message.desc_whitelist")
    )
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist_remove(self, ctx, channel: TextChannel):
        try:
            res = await self.bot.mguild_config.find_one({"_id": ctx.guild.id})

            try:
                if channel.id not in res["messageLogIgnore"]:
                    return await ctx.send(
                        embed=embed.warn_embed_ephemeral(
                            _("cmds.config.logs.message.res.whitelist.not_found")
                        )
                    )
            except Exception:
                return await ctx.send(
                    embed=embed.warn_embed_ephemeral(
                        _("cmds.config.logs.message.res.whitelist.not_found")
                    )
                )

            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$pull": {"messageLogIgnore": channel.id}},
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.logs.message.res.whitelist.remove.success",
                        channel=channel.mention,
                    )
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except Exception as error:
            await self.bot.create_error_log(ctx, error)

    @messages.command(
        name="clearwhitelist", description=_("cmds.config.logs.message.desc_whitelist")
    )
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist_clear(self, ctx):
        try:
            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$unset": {"messageLogIgnore": f""}},
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _("cmds.config.logs.message.res.whitelist.clear.success")
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except Exception as error:
            await self.bot.create_error_log(ctx, error)

    @messages.command(
        name="clear", description=_("cmds.config.logs.message.desc_clear")
    )
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clear_message_logs(self, ctx):
        try:
            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {
                        "id": ctx.guild.id,
                        "message_log_channel_id": None,
                        "message_log_ignore_list": None,
                    },
                    "update": {
                        "id": ctx.guild.id,
                        "message_log_channel_id": None,
                        "message_log_ignore_list": None,
                    },
                },
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.logs.message.success_clear",
                    )
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except Exception as error:
            print(error)

    # Logs end

    # Welcome

    @welcome.command(name="set", description=_("cmds.config.welcome.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def change_welcome_message(self, ctx, channel: TextChannel, *, message: str):
        try:
            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {
                        "id": ctx.guild.id,
                        "welcome_channel": channel.id,
                        "welcome_greeting": message,
                    },
                    "update": {
                        "id": ctx.guild.id,
                        "welcome_channel": channel.id,
                        "welcome_greeting": message,
                    },
                },
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.welcome.success",
                        message=message,
                        channel=channel.mention,
                    )
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except Exception as error:
            await ctx.send(error)

    @welcome.command(name="clear", description=_("cmds.config.welcome.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clear_welcome_message(self, ctx: commands.Context):
        try:
            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {
                        "id": ctx.guild.id,
                        "welcome_channel": None,
                        "welcome_greeting": None,
                    },
                    "update": {
                        "id": ctx.guild.id,
                        "welcome_channel": None,
                        "welcome_greeting": None,
                    },
                },
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.welcome.removal_success",
                    )
                )
            )
        except Exception as error:
            await ctx.send(error)

    # Welcome end

    # Giveaways

    @giveaways.command(name="set", description=_("cmds.config.giveaway.set.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def set_giveaway_channel(
        self, ctx: commands.Context, channel: nextcord.TextChannel
    ):
        try:
            if channel is None:
                return await ctx.send(_("cmds.config.giveaway.set.not_found"))

            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {"id": ctx.guild.id, "giveaway_channel": channel.id},
                    "update": {"id": ctx.guild.id, "giveaway_channel": channel.id},
                },
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.giveaway.set.res.success",
                        channel=channel.mention,
                    )
                )
            )
        except Exception as error:
            await ctx.send(error)

    @giveaways.command(name="clear", description=_("cmds.config.giveaway.set.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clear_giveaway_channel(self, ctx: commands.Context):
        try:
            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {"id": ctx.guild.id, "giveaway_channel": None},
                    "update": {"id": ctx.guild.id, "giveaway_channel": None},
                },
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.giveaway.set.res.cleared",
                    )
                )
            )
        except Exception as error:
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Config(bot))
