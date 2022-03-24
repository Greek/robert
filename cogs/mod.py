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

import nextcord
import os
from nextcord import slash_command, Interaction, SlashOption
from nextcord.ext.commands import errors
from nextcord.ext import commands
from utils import default, perms
from utils.default import translate as _
from utils.embed import self_missing_permissions


class Mod(commands.Cog):
    """Commands for moderators"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", description=_("cmds.kick.desc"))
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_user(self, ctx, member: nextcord.Member, *, reason=None) -> None:
        if await perms.check_priv(ctx, member=member):
            return
        await member.kick(reason=default.responsible(ctx.author, reason))
        await ctx.reply(
            _("cmds.kick.res_noreason") if reason is None else _("cmds.kick.res_reason")
        )

    @commands.command(name="ban", description=_("cmds.ban.desc"))
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_user(self, ctx, member: nextcord.Member, *, reason=None) -> None:
        if await perms.check_priv(ctx, member=member):
            return
        await member.ban(reason=default.responsible(ctx.author, reason))
        await ctx.reply(
            _("cmds.ban.res_noreason") if reason is None else _("cmds.ban.res_reason")
        )

    @slash_command(
        name="ban",
        description=_("cmds.ban.desc"),
        guild_ids=[os.environ.get("DISCORD_GUILDID")],
    )
    async def ban_user_slash(
        self,
        ctx: nextcord.Interaction,
        member: nextcord.Member = SlashOption(
            description=_("cmds.ban.option_member"), required="true"
        ),
        *,
        reason: str = SlashOption(description=_("cmds.ban.desc"))
    ):
        pass

    @kick_user.error
    async def kick_user_errors(self, ctx, err):
        if isinstance(err, errors.BotMissingPermissions):
            return await ctx.reply(
                embed=self_missing_permissions(ctx.author, "kick_members")
            )

    @ban_user.error
    async def ban_user_errors(self, ctx, err):
        if isinstance(err, errors.BotMissingPermissions):
            return await ctx.reply(
                embed=self_missing_permissions(ctx.author, "ban_members")
            )

    @commands.command(name="purge", description=_("cmds.purge.desc"))
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def mass_delete(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount + 1)
        except discord.HTTPException:
            sent = await ctx.reply(_("events.missing_permission"))
            return await sent.delete(delay=3)
        sent = await ctx.send(
            _("cmds.purge.res", ctx=ctx.author.mention, amount=amount)
        )
        await sent.delete(delay=3)


def setup(bot):
    bot.add_cog(Mod(bot))
