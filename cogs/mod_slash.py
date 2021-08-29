# -*- coding: utf-8 -*-
import dislash
from discord.ext import commands
import discord
from dislash import slash_command, Option, OptionType

from utils import perms, default


class ModSlash(commands.Cog):
    """The description for ModSlash goes here."""

    def __init__(self, bot):
        self.bot = bot

    def check_msg(ctx, m):
        return m.author == ctx.user

    @slash_command(name="kick", description="Kick a user from the server.", options=[
        Option("member", "Person to kick", OptionType.USER, required=True),
        Option("reason", "The reason as to why you're kicking the person.", OptionType.STRING)
    ])
    @dislash.has_guild_permissions(kick_members=True)
    @dislash.guild_only()
    async def kick_user(self, inter, member=None, reason=None) -> None:
        """ Kick a user, with an optional reason. """
        try:
            if await perms.check_priv(inter, member=member):
                return
            await member.kick(reason=default.responsible(inter.author, reason))
            await inter.reply(f"successfully kicked {str(member)} for no reason."
                              if reason is None
                              else f"successfully kicked {str(member)} for \"{reason}\".", ephemeral=True)
        except discord.HTTPException:
            await inter.reply("i can't do that for you.", ephemeral=True)

    @slash_command(name="ban", description="Ban a user from the server.", options=[
        Option("member", "Person to ban", OptionType.USER, required=True),
        Option("reason", "The reason as to why you're banning the person.", OptionType.STRING)
    ])
    @dislash.has_guild_permissions(ban_members=True)
    @dislash.guild_only()
    async def ban_user(self, inter, member=None, reason=None) -> None:
        """ Ban a user, with an optional reason. """
        try:
            if await perms.check_priv(inter, member=member):
                return
            await member.ban(reason=default.responsible(inter.author, reason))
            await inter.reply(f"successfully banned {str(member)} for no reason."
                              if reason is None
                              else f"successfully banned {str(member)} for \"{reason}\".", ephemeral=True)
        except discord.HTTPException:
            await inter.reply("i can't do that for you.", ephemeral=True)

def setup(bot):
    bot.add_cog(ModSlash(bot))
