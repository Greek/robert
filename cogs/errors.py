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

from nextcord.ext import commands, application_checks
from nextcord.ext.commands import errors

from utils.data import create_error_log
from utils.default import translate as _
from utils.embed import (
    missing_permissions,
    self_missing_permissions,
    warn_embed_ephemeral,
)


class Errors(commands.Cog):
    """Command error handlers"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err):
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

    @commands.Cog.listener()
    async def on_application_command_error(
        self, interaction: nextcord.Interaction, err
    ):
        if isinstance(err, application_checks.errors.ApplicationMissingPermissions):
            return await interaction.response.send_message(
                embed=missing_permissions(f"{' '.join(err.missing_permissions)}")
            )

        if isinstance(err, application_checks.errors.ApplicationBotMissingPermissions):
            return await interaction.response.send_message(
                embed=self_missing_permissions(f"{' '.join(err.missing_permissions)}")
            )


def setup(bot):
    bot.add_cog(Errors(bot))
