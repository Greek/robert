from attr import has
import nextcord
import os

from nextcord import TextChannel
from nextcord.ext import commands

from pymongo import MongoClient

from utils import embed
from utils.data import Bot, create_error_log
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
            # self.config_coll.find_one_and_update(
            # {"_id": ctx.guild.id},
            # {"$set": {"messageLog": channel.id}},
            # upsert=True,
            # )
            self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$set": {"messageLog": channel.id}},
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.logs.message.success",
                        channel=channel.mention,
                    )
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except:
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
            res = self.config_coll.find_one({"_id": ctx.guild.id})

            try:
                if str(channel.id) in res["messageLogIgnore"]:
                    return await ctx.send(
                        embed=embed.warn_embed_ephemeral(
                            _(
                                "cmds.config.logs.message.res.whitelist.already_whitelisted"
                            )
                        )
                    )
            except:
                pass

            self.bot.mguild_config.find_one_and_update(
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
            await create_error_log(self, ctx, error)

    @messages.command(
        name="unwhitelist", description=_("cmds.config.logs.message.desc_whitelist")
    )
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist_remove(self, ctx, channel: TextChannel):
        try:
            res = self.config_coll.find_one({"_id": ctx.guild.id})

            try:
                if channel.id not in res["messageLogIgnore"]:
                    return await ctx.send(
                        embed=embed.warn_embed_ephemeral(
                            _("cmds.config.logs.message.res.whitelist.not_found")
                        )
                    )
            except Exception as e:
                return await ctx.send(
                    embed=embed.warn_embed_ephemeral(
                        _("cmds.config.logs.message.res.whitelist.not_found")
                    )
                )

            self.bot.mguild_config.find_one_and_update(
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
            await create_error_log(self, ctx, error)

    @messages.command(
        name="clearwhitelist", description=_("cmds.config.logs.message.desc_whitelist")
    )
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist_clear(self, ctx):
        try:
            self.bot.mguild_config.find_one_and_update(
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
            await create_error_log(self, ctx, error)

    @messages.command(
        name="clear", description=_("cmds.config.logs.message.desc_clear")
    )
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clear_message_logs(self, ctx):
        try:
            self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$unset": {"messageLog": ""}},
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.logs.message.success_clear",
                    )
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except Exception as e:
            print(e)

    # Logs end

    # Welcome

    @welcome.command(name="set", description=_("cmds.config.welcome.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def change_welcome_message(self, ctx, channel: TextChannel, *, message: str):
        try:
            self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {
                    "$set": {
                        "welcomeChannel": channel.id,
                        "welcomeGreeting": message,
                    }
                },
                upsert=True,
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
        except Exception as e:
            await ctx.send(e)

    @welcome.command(name="clear", description=_("cmds.config.welcome.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clear_welcome_message(self, ctx: commands.Context):
        try:
            self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$unset": {"welcomeChannel": "", "welcomeGreeting": ""}},
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.welcome.removal_success",
                    )
                )
            )
        except Exception as e:
            await ctx.send(e)

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

            self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {
                    "$set": {
                        "giveawayChannel": channel.id,
                    }
                },
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.giveaway.set.res.success",
                        channel=channel.mention,
                    )
                )
            )
        except Exception as e:
            await ctx.send(e)

    @giveaways.command(name="clear", description=_("cmds.config.giveaway.set.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clear_giveaway_channel(self, ctx: commands.Context):
        try:
            self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {
                    "$unset": {
                        "giveawayChannel": "",
                    }
                },
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.giveaway.set.res.cleared",
                    )
                )
            )
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Config(bot))
