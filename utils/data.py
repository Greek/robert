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

import nextcord
import itertools
import sys
import logging
import os
import json
import uuid

from nextcord import Interaction
from nextcord.ext.commands import AutoShardedBot, MinimalHelpCommand, Context

from utils import default, embed as uembed
from utils.default import translate as _, traceback_maker

from pymongo import MongoClient

do_not_load = ("cogs.interactives",)


class Bot(AutoShardedBot):
    """Custom bot class extending AutoShardedBot"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            logger = logging.getLogger("nextcord")
            logger.setLevel(logging.INFO)

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

            logger.addHandler(handler)
            logger.addHandler(handler2)

            self.load_extension("jishaku")
            for cog in os.listdir("./cogs"):
                if cog.endswith(".py") and not cog.startswith("__"):
                    name = cog[:-3]
                    self.load_extension(f"cogs.{name}")

            # Do not load following cogs
            # for cog in do_not_load:
            #     try:
            #         with warnings.catch_warnings():
            #             warnings.simplefilter("ignore")  # silencing async warnings here
            #             self.unload_extension(str(cog))
            #     except Exception as e:
            #         print(f"{cog} was never loaded.")

        except Exception as exc:
            print(
                "Could not load extension {0} due to {1.__class__.__name__}: {1}".format(
                    cog, exc
                )  # ignore this pylance err
            )
            raise exc

    async def start(self, *args, **kwargs):
        self.mclient = MongoClient(os.environ.get("MONGO_DB"))
        self.mdb = self.mclient[os.environ.get("MONGO_NAME")]

        self.mguild_config = self.mdb.guildconfig
        self.mlastfm = self.mdb.lastfm

        await super().start(*args, **kwargs)


class HelpFormat(MinimalHelpCommand):
    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    def get_ending_note(self):
        command_name = self.invoked_with
        cfg_prefix = os.environ.get("DISCORD_PREFIX")
        return 'Run "{0}{1} <command name>" to see help for a specific command.'.format(
            cfg_prefix, command_name
        )

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
            description=f"A list of all the commands the bot has to offer.",
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

        # try:
        #     await destination.send(embed=embed)
        # except nextcord.Forbidden:
        #     return await self.get_destination(no_pm=True).send(_("events.forbidden_dm"))
        await self.context.send(
            "Check out the help guide here: http://s.apap04.com/0trneJ4\nIf you need any further help, join our Discord: discord.gg/YqkpR4g5dX"
        )

    async def send_command_help(self, command):
        global _cmd
        _cmd = command
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages(no_pm=True)

    async def send_pages(self, no_pm: bool = False):
        try:
            destination = self.get_destination(no_pm=True)
            embed = default.branded_embed(
                title=f"Help guide", description=f"", color="green", inline=True
            )
            for page in self.paginator.pages:
                embed.description += page
            await destination.send(embed=embed)
        except nextcord.Forbidden:
            destination = self.get_destination(no_pm=True)
            await destination.send(_("events.forbidden_dm"))


async def create_error_log(self, ctx: Interaction, err):
    f = open("config.json")
    config = json.load(f)
    cid = int(config.get("error_reporting"))

    log = self.bot.get_channel(cid)
    ref_id = uuid.uuid4()
    if log is None:
        return print("[Error] Couldn't find log channel. Printing:\n", err)

    embed = nextcord.Embed(
        color=uembed.warn_embed_color,
        description=f"⚠️ {_('events.command_error.title')}",
    )
    embed.set_footer(text=f"{ref_id}")

    embed_error = nextcord.Embed(
        color=uembed.failed_embed_color,
        title="Error",
        description=f"**Information**\nInvoked command: `{ctx.message.content if isinstance(ctx, Context) else ctx.application_command}`\n"
        + f"Invoked by: `{str(ctx.author if isinstance(ctx, Context) else ctx.user)} ({ctx.author.id if isinstance(ctx, Context) else ctx.user.id})`"
        + f"\nGuild Name & ID: `{str(ctx.guild)} ({ctx.guild.id})`"
        + f"\n\nTrace: {traceback_maker(err, advance=True)}",
    )
    embed_error.set_footer(text=f"Diagnosis code: {ref_id}")

    await log.send(embed=embed_error)
    await ctx.send(embed=embed)
