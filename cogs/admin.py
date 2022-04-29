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
import ast
import sys
import os
import time

from nextcord.ext import commands
from pymongo import MongoClient
from utils import default, perms, _io
from utils.default import translate as _

from utils.embed import (
    failed_embed,
    failed_embed_ephemeral,
    success_embed,
    success_embed_ephemeral,
    warn_embed,
    warn_embed_ephemeral,
)

checkmark = ":ballot_box_with_check:"


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("./config.json")
        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.collection = self.db["test12"]

    @commands.command(name="load", aliases=["l"], hidden=True)
    @commands.check(perms.only_owner)
    async def load_cog(self, ctx, cog):
        try:
            self.bot.load_extension(f"cogs.{cog}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.reply(f"{checkmark} Loaded `{cog}.py`.", mention_author=False)

    @commands.command(name="unload", aliases=["u"], hidden=True)
    @commands.check(perms.only_owner)
    async def unload_cog(self, ctx, cog):
        try:
            self.bot.unload_extension(f"cogs.{cog}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.reply(
            embed=success_embed_ephemeral(f"Unloaded `{cog}.py`."),
            mention_author=False,
        )

    @commands.command(name="reload", aliases=["r"], hidden=True)
    @commands.check(perms.only_owner)
    async def reload_cog(self, ctx, cog):
        try:
            self.bot.reload_extension(f"cogs.{cog}")
        except Exception as e:
            return await ctx.send(default.traceback_maker(e))
        await ctx.reply(
            embed=success_embed_ephemeral(f"Reloaded `{cog}.py`."),
            mention_author=False,
        )

    @commands.command(name="reloadall", aliases=["ra"], hidden=True)
    @commands.check(perms.only_owner)
    async def reload_all_cogs(self, ctx, **kwargs):
        try:
            for cog in os.listdir("cogs"):
                if cog.endswith(".py"):
                    name = cog[:-3]
                    self.bot.reload_extension(f"cogs.{name}")
        except Exception as e:
            print(e)
        await ctx.reply(
            embed=success_embed_ephemeral(f"Reloaded all cogs."),
            mention_author=False,
        )

    @commands.command(name="kill", hidden=True)
    @commands.check(perms.only_owner)
    async def kill_bot(self, ctx):
        await ctx.reply(_("cmds.kill.msg"), mention_author=False)
        time.sleep(1)
        sys.exit()

    @commands.group(name="change", hidden=True)
    @commands.check(perms.only_owner)
    async def change(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @change.command(name="playing")
    @commands.check(perms.only_owner)
    async def change_playing(self, ctx, *, playing: str = None):
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

        try:
            await self.bot.change_presence(
                activity=discord.Activity(type=playing_type, name=playing),
                status=status,
            )
            _io.change_value("./config.json", "playing", playing)
            await ctx.reply(
                embed=success_embed_ephemeral(
                    f'Changed playing status to "{playing}".'
                ),
                mention_author=False,
            )
        except discord.InvalidArgument as err:
            await ctx.send(err)
        except Exception as e:
            await ctx.send(default.traceback_maker(e))

    @commands.command(name="embedtest", hidden=True)
    @commands.check(perms.only_owner)
    async def embedtest(self, ctx: commands.Context):
        await ctx.send(
            embeds=[
                success_embed_ephemeral("Hello"),
                success_embed(ctx.author, "Hello"),
                warn_embed_ephemeral("Hello"),
                warn_embed(ctx.author, "Hello"),
                failed_embed_ephemeral("Hello"),
                failed_embed(ctx.author, "Hello"),
            ]
        )

def setup(bot):
    bot.add_cog(Admin(bot))
