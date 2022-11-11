"""
Copyright (c) 2020 AlexFlipnote

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

import itertools
import json
import logging
import os
import sys
import uuid

import asyncpg
import motor.motor_asyncio
import nextcord
from nextcord import Interaction
from nextcord.ext.commands import AutoShardedBot, Context, MinimalHelpCommand

from prisma import Prisma
from utils import default
from utils import embed as uembed
from utils.default import traceback_maker
from utils.default import translate as _

do_not_load = ("cogs.interactives", "cogs.gw", "cogs.mod")


class Bot(AutoShardedBot):
    """Custom bot class extending AutoShardedBot"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger("nextcord")
        self.motor_client = motor.motor_asyncio.AsyncIOMotorClient(
            os.environ.get("MONGO_DB")
        )
        self.mongo_db = self.motor_client[os.environ.get("MONGO_NAME")]

        self.guild_config = self.mongo_db.guildconfig
        self.lastfm = self.mongo_db.lastfm

        # should be async but this is init
        self.pool = asyncpg.create_pool(dsn=os.environ.get("DATABASE_DSN"))
        self.prisma = Prisma()

        try:

            self.logger.setLevel(logging.DEBUG)
            self.logger.name = "toilet"

            handler = logging.FileHandler(
                filename="./logs/discord.log", encoding="utf-8", mode="a"
            )
            handler2 = logging.StreamHandler(sys.stdout)

            handler.setFormatter(
                logging.Formatter(
                    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
                )
            )
            handler2.setFormatter(
                logging.Formatter("[%(levelname)s] [%(name)s] %(message)s")
            )

            self.logger.addHandler(handler)
            self.logger.addHandler(handler2)

            self.load_extension("jishaku")
            for cog in os.listdir("./cogs"):
                if cog.endswith(".py") and not cog.startswith("__"):
                    name = cog[:-3]
                    self.load_extension(f"cogs.{name}")

        except Exception as exc:
            print(
                f"Could not load extension {cog} due to {exc.__class__.__name__}: {exc}"
            )
            raise exc

    async def start(self, *args, **kwargs):
        await self.prisma.connect()
        self.logger.info("Connected to PostgreSQL.")

        await super().start(*args, **kwargs)

    async def create_error_log(self, ctx: Interaction, err):
        config_file = open("config.json")
        config = json.load(config_file)
        channel_id = int(config.get("error_reporting"))

        log = self.get_channel(channel_id)
        ref_id = uuid.uuid4()
        if log is None:
            return print("[Error] Couldn't find log channel. Printing:\n", err)

        embed = nextcord.Embed(
            color=uembed.WARN_EMBED_COLOR,
            description=f"⚠️ {_('events.command_error.title')}",
        )
        embed.set_footer(text=f"{ref_id}")

        embed_error = nextcord.Embed(
            color=uembed.FAILED_EMBED_COLOR,
            title="Error",
            description=f"**Information**\nInvoked command: `{ctx.message.content if isinstance(ctx, Context) else ctx.application_command}`\n"
            + f"Invoked by: `{str(ctx.author if isinstance(ctx, Context) else ctx.user)} ({ctx.author.id if isinstance(ctx, Context) else ctx.user.id})`"
            + f"\nGuild Name & ID: `{str(ctx.guild)} ({ctx.guild.id})`"
            + f"\n\nTrace: {traceback_maker(err, advance=True)}",
        )
        embed_error.set_footer(text=f"Diagnosis code: {ref_id}")

        await log.send(embed=embed_error)
        await ctx.send(embed=embed)


class HelpFormat(MinimalHelpCommand):
    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    def get_ending_note(self):
        command_name = self.invoked_with
        cfg_prefix = os.environ.get("DISCORD_PREFIX")
        return f'Run "{cfg_prefix}{command_name} <command name>" to see help for a specific command.'

    def get_opening_note(self):
        pass

    async def send_error_message(self, error):
        destination = self.get_destination(no_pm=True)
        await destination.send(error)

    async def send_bot_help(self, mapping):
        # This is derived from the original method, but made as an embed.
        ctx = self.context
        bot = ctx.bot

        destination = self.get_destination(no_pm=True)
        note = self.get_ending_note()

        no_category = f"\u200b{self.no_category}"

        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return f"{cog.qualified_name}" if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)

        embed = default.branded_embed(
            title="Help guide",
            description="A list of all the commands the bot has to offer.",
            color="green",
            inline=True,
        )

        for category, commands in to_iterate:
            commands = (
                sorted(commands, key=lambda c: c.name)
                if self.sort_commands
                else list(commands)
            )
            joined = "\u2002".join(f"`{c.name}`" for c in commands)

            embed.add_field(name=f"{category}", value=f"{joined}", inline=False)
            self.add_bot_commands_formatting(commands, category)

        embed.set_footer(text=note)

        try:
            await destination.send(embed=embed)
        except nextcord.Forbidden:
            return await self.get_destination(no_pm=True).send(_("events.forbidden_dm"))

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages(no_pm=True)

    async def send_pages(self, no_pm: bool = False):
        try:
            destination = self.get_destination(no_pm=True)
            embed = default.branded_embed(
                title="Help guide", description="", color="green", inline=True
            )
            for page in self.paginator.pages:
                embed.description += page
            await destination.send(embed=embed)
        except nextcord.Forbidden:
            destination = self.get_destination(no_pm=True)
            await destination.send(_("events.forbidden_dm"))
