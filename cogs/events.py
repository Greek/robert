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

import discord
import dislash
from discord.ext import commands
from discord.ext.commands import errors
from discord.ext.commands.cooldowns import BucketType
from utils import default
from utils.default import translate as _
import datetime

class Events(commands.Cog):
    """Event listeners :Smile:"""

    def __init__(self, bot):
        self.bot = bot
        self.last_timeStamp = datetime.datetime.utcfromtimestamp(0)
        self.config = default.get("config.json")

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"Logged on as {self.bot.user} on {len(self.bot.guilds)} guild(s)\n"
        )

        if self.config.status == "idle":
            status = discord.Status.idle
        elif self.config.status == "dnd":
            status = discord.Status.dnd
        else:
            status = discord.Status.online

        if self.config.playing_type == "listening":
            playing_type = 2
        elif self.config.playing_type == "watching":
            playing_type = 3
        else:
            playing_type = 0

        await self.bot.change_presence(
            activity=discord.Activity(type=playing_type, name=self.config.playing),
            status=status,
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.CommandInvokeError):
            await ctx.send(
                _("events.command_error") + "\n"
                + default.traceback_maker(err)
            )

        if isinstance(err, errors.MissingRequiredArgument):
            await ctx.send_help(_("events.missing_args") + "\n" + str(ctx.command))

        if isinstance(err, errors.BotMissingPermissions):
            await ctx.send(_("events.missing_permission"))

        if isinstance(err, commands.CommandOnCooldown):
            print(f"[COOLDOWN] {err}")

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        if isinstance(error, dislash.errors.BotMissingPermissions):
            await inter.reply(_("events.missing_permission"))

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        owner = await self.bot.fetch_user(guild.owner_id)
        log_channel = self.bot.get_channel(882216228670808074)

        embed = default.branded_embed(title=f"New Guild", description=f"Guild \"{guild.name}\"", color="green")

        embed.add_field(name="Owner", value=f"{owner.name}#{owner.discriminator}", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
        embed.add_field(name="Max presences?", value=f"{guild.max_presences}", inline=True)
        try:
            invites = await guild.invites()
            stringified = str(invites)
            embed.add_field(name="Invite", value=f"{stringified[2:25]}", inline=True)
        except discord.errors.Forbidden:
            embed.add_field(name="Invite", value=f"Could not fetch invite.", inline=True)
            pass
        embed.set_footer(text=f"Guild ID: {str(guild.id)}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        owner = await self.bot.fetch_user(guild.owner_id)
        log_channel = self.bot.get_channel(882216228670808074)
        embed = default.branded_embed(title=f"Left Guild", description=f"Guild \"{guild.name}\"", color="red")

        embed.add_field(name="Owner", value=f"{owner.name}#{owner.discriminator}", inline=True)
        embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
        embed.add_field(name="Max presences?", value=f"{guild.max_presences}", inline=True)
        embed.set_footer(text=f"Guild ID: {str(guild.id)}")
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    @commands.cooldown(1, 30, BucketType.user)
    async def on_message(self, message):
        time_difference = (datetime.datetime.utcnow() - self.last_timeStamp).total_seconds()
        if time_difference < 30:
            return
        else:
            if message.content.startswith("grubhub"):
                await message.channel.send("https://thot.wtf/i/2021/02/13/grubhub.gif")

            if message.content.startswith("fucking sex"):
                await message.channel.send("https://thot.wtf/i/2021/02/13/fucking%20sex.gif")

            if message.content.startswith("spunch bop"):
                await message.channel.send("https://tenor.com/view/spunch-bop-spongebob-crying-cube-mr-krabs-gif-19973394")

            if message.content.startswith("sex smp"):
                await message.channel.send("https://tenor.com/view/dream-dream-team-sapnap-georgenotfound-technoblade-gif-19248460")



def setup(bot):
    bot.add_cog(Events(bot))
