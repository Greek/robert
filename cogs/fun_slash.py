# -*- coding: utf-8 -*-
from discord import PartialEmoji, Emoji
from discord.ext import commands
from discord.ext.commands import EmojiConverter
from dislash import slash_command, Option, OptionType, ActionRow, Button, ButtonStyle
import discord

from utils import default


class FunSlash(commands.Cog):
    """The description for FunSlash goes here."""

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="user",
                   description="Get info about a user.",
                   options=[Option("member", "The user you want.", OptionType.USER, required=True)]
    )
    async def get_user_info(self, ctx, member=None):
        """
        Get information for a specific user.
        """
        try:
            member = member or ctx.author
            embed = discord.Embed(color=member.color, description=f"{member.mention}")
            embed.set_author(name=str(member), icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Join date", value=f"{member.joined_at}"[0:10])
            embed.add_field(name="Creation date", value=f"{member.created_at}"[0:10])
            embed.add_field(name="Roles", value=", ".join([r.mention for r in member.roles[1:]]), inline=False)
            embed.set_footer(text="ID: " + str(member.id))
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(default.traceback_maker(e))

def setup(bot):
    bot.add_cog(FunSlash(bot))
