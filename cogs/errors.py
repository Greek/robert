from nextcord.ext import commands
from nextcord.ext.commands import errors, Context
from nextcord.ext.commands.cooldowns import BucketType
from utils.data import create_error_log
from utils.default import translate as _
from utils.embed import (
    missing_permissions,
    self_missing_permissions,
    warn_embed_ephemeral,
)


class Errors(commands.Cog):
    """The description for Errors goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, err):
        if isinstance(err, errors.CommandInvokeError):
            await create_error_log(self, ctx, err)

        if isinstance(err, errors.MissingPermissions):
            await ctx.send(
                embed=missing_permissions(f"{' '.join(err.missing_permissions)}")
            )

        if isinstance(err, errors.BotMissingPermissions):
            await ctx.send(
                embed=self_missing_permissions(f"{' '.join(err.missing_permissions)}")
            )

        if isinstance(err, errors.MissingRequiredArgument):
            await ctx.send_help(str(ctx.command))
            # await ctx.send_help(str(ctx.command))

        if isinstance(err, commands.CommandOnCooldown):
            embed = warn_embed_ephemeral(
                _("events.cooldown", time="{0}", unit="s").format(int(err.retry_after))
            )

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Errors(bot))
