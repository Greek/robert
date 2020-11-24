# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
from utils import default, perms

class Mod(commands.Cog):
    """Commands for moderators"""

    def __init__(self, bot):
        self.bot = bot

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

def setup(bot):
    bot.add_cog(Mod(bot))
