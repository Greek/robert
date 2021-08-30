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

from utils.default import traceback_maker
import discord
from discord.ext import commands
from utils import default, perms
from utils.default import translate as _

class Mod(commands.Cog):
    """Commands for moderators"""

    def __init__(self, bot):
        self.bot = bot

    def check_msg(ctx, m):
        return m.author == ctx.user

    @commands.command(name="kick")
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_user(self, ctx, member: discord.Member, *, reason=None) -> None:
        """ Kick a user, with an optional reason. """
        try:
            if await perms.check_priv(ctx, member=member):
                return
            await member.kick(reason=default.responsible(ctx.author, reason))
            sent = await ctx.reply(
                f"successfully kicked {str(member)} for no reason."
                if reason is None
                else f"successfully kicked {str(member)} for \"{reason}\"."
            )
            await sent.delete(delay=3)
        except discord.HTTPException:
            sent = await ctx.reply(_("events.missing_permission"))
            await sent.delete(delay=3)
            
    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_user(self, ctx, member: discord.Member, *, reason=None) -> None:
        """ Ban a user, with an optional reason. """
        try:
            if await perms.check_priv(ctx, member=member):
                return
            await member.ban(reason=default.responsible(ctx.author, reason))
            sent = await ctx.send(
                f"successfully banned {str(member)} for no reason."
                if reason is None
                else f"successfully banned {str(member)} for \"{reason}\"."
            )
            await sent.delete(delay=3)
        except discord.HTTPException:
            sent = await ctx.reply(_("events.missing_permission"))
            await sent.delete(delay=3)

    @commands.command(name="purge")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def mass_delete(self, ctx, amount: int):
        """ Mass delete messages at once. """
        try:
            await ctx.channel.purge(limit=amount + 1)
            sent = await ctx.send(f"purged {amount} messages")
            await sent.delete(delay=3)
        except discord.HTTPException:
            sent = await ctx.reply(_("events.missing_permission"))
            await sent.delete(delay=3)

def setup(bot):
    bot.add_cog(Mod(bot))
