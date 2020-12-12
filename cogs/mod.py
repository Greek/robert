# -*- coding: utf-8 -*-

from utils.default import traceback_maker
import discord
from discord.ext import commands
from utils import default, perms

class Mod(commands.Cog):
    """Commands for moderators"""

    def __init__(self, bot):
        self.bot = bot

    def check_msg(ctx, m):
        return m.author == ctx.user

    #region User Management

    @commands.command(name="kick")
    @commands.has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_user(self, ctx, member: discord.Member, *, reason=None) -> None:
        """ Kick a user, with an optional reason. """
        try:
            if await perms.check_priv(ctx, member=member):
                return
            await member.kick(reason=default.responsible(ctx.author, reason))
            await ctx.send(
                f"{ctx.author.name} kicked {str(member)} for no reason"
                if reason is None
                else f"{ctx.author.name} kicked {str(member)} for \"{reason}\"."
            )
        except discord.HTTPException:             
            await ctx.send("i can't do that.")
            
    @commands.command(name="ban")
    @commands.has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_user(self, ctx, member: discord.Member, *, reason=None) -> None:
        """ Ban a user, with an optional reason. """
        try:
            if await perms.check_priv(ctx, member=member):
                return
            await member.ban(reason=default.responsible(ctx.author, reason))
            await ctx.send(
                f"{ctx.author.name} banned {str(member)} for no reason"
                if reason is None
                else f"{ctx.author.name} banned {str(member)} for \"{reason}\"."
            )
        except discord.HTTPException:
            await ctx.send("i can't do that.")

    #endregion

    @commands.command(name="purge")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def mass_delete(self, ctx, amount: int, target: discord.Member = None):
        """ Mass delete messages at once. """
        try:
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"purged {amount} messages")
        except discord.HTTPException:
            await ctx.send("i can't do that.")

def setup(bot):
    bot.add_cog(Mod(bot))
