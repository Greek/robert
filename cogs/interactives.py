# -*- coding: utf-8 -*-
import dislash
from discord import Embed
from discord.ext import commands
import discord
from dislash import slash_command, Option, OptionType


class Interactives(commands.Cog):
    """The description for Interactives goes here."""

    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="ip", description="What's the IP?",
                   options=[Option("mention", "Mention a user and make the message public", OptionType.USER)])
    @dislash.has_guild_permissions(manage_messages=True)
    async def ip(self, inter, mention):
        embed = discord.Embed(title="What's the IP?", description=
        "Pyrelic is currently under development, " +
        "a release date will be announced in #announcements, " +
        "so keep an eye out!",
                              colour=Embed.Empty)
        if mention:
            await inter.respond(f"{mention.mention}", embed=embed, ephemeral=False)
        else:
            await inter.respond(embed=embed, ephemeral=True)

    @ip.error
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, discord.errors.NotFound):
            pass # Ignore exception.
        embed = discord.Embed(title="What's the IP?", description=
        "Pyrelic is currently under development, " +
        "a release date will be announced in #announcements, " +
        "so keep an eye out!",
                              colour=Embed.Empty)
        await inter.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(Interactives(bot))
