# -*- coding: utf-8 -*-
from discord import Embed
from discord.ext import commands
from dislash import slash_command, ActionRow, Button, ButtonStyle, Option, OptionType
import discord

class Dislashcmds(commands.Cog):
    """branch slashcommands"""

    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="dislashcmds, slashcommands")
    async def test(self, inter):
        await inter.respond("hi")

    @slash_command(name="name",
                   description="What is your name?",
                   options=[
                        Option("name", "Your name", OptionType.USER, required=True)],
                   )
    async def name_test(self, inter, name=None):
        name = name or inter.author
        await inter.respond(f"their name is {name.name}" if name is inter.author else f"your name is {name.name}")

    # @slash_command(name="user",
    #                description="Get info about a specific user.",
    #                options=[
    #                    Option("member", "The user you want info from.", OptionType.USER, required=True)],
    #                )
    # async def get_user_info_slash(self, inter, member=None):
    #     member = member or inter.author
    #
    #     embed = discord.Embed(colour=Embed.Empty, description=f"{member.mention}")
    #     await inter.reply(embed=embed)

def setup(bot):
    bot.add_cog(Dislashcmds(bot))
