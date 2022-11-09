from nextcord import TextChannel
from nextcord.ext import commands

from utils import embed
from utils.data import Bot
from utils.default import translate as _


class Logs(commands.Cog):
    """Logs configuration commands"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.group(name="logs")
    @commands.has_guild_permissions(manage_channels=True)
    async def _logs(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @_logs.group(name="message", description=_("cmds.config.logs.message.desc"))
    async def _message(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @_message.command(name="set", description=_("cmds.config.logs.message.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _message_set_logs(self, ctx: commands.Context, channel: TextChannel):
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

    @_message.command(
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

    @_message.command(
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

    @_message.command(
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

    @_message.command(
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


def setup(bot):
    bot.add_cog(Logs(bot))
