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

import discord
import os
import logging
import warnings
import itertools

from discord.ext.commands import AutoShardedBot, MinimalHelpCommand
from dislash import InteractionClient
from utils import perms, default
from utils.default import translate as _

do_not_load = (
    'cogs.interactives',
    'cogs.fun_slash',
    'cogs.fun',
    'cogs.mod',
    'cogs.about'
)

class Bot(AutoShardedBot):
    """ Custom bot class extending AutoShardedBot """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            logger = logging.getLogger('discord')
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
            handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
            logger.addHandler(handler)

            guilds = [896945819121512500]
            inter_client = InteractionClient(self, test_guilds=guilds)
            
            for cog in os.listdir("cogs"):
                if cog.endswith(".py"):
                    name = cog[:-3]
                    self.load_extension(f"cogs.{name}")

            # Do not load following cogs
            for cog in do_not_load:
                try:
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")  # silencing async warnings here
                        self.unload_extension(str(cog))
                        inter_client.delete_global_commands()
                except Exception as e:
                    print(f"Couldn't unload extenstion {cog}\n{e}")

        except Exception as exc:
            print(
                "Could not load extension {0} due to {1.__class__.__name__}: {1}".format(
                    cog, exc
                )  # ignore this pylance err
            )


class HelpFormat(MinimalHelpCommand):
    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    def get_ending_note(self):
        command_name = self.invoked_with
        cfg_prefix = default.get("config.json").prefix
        return "Run \"{0}{1} <command name>\" to see help for a specific command.".format(cfg_prefix, command_name)

    def get_opening_note(self):
        pass

    async def send_error_message(self, error):
        destination = self.get_destination(no_pm=True)
        await destination.send(error)

    async def send_bot_help(self, mapping):
        # This is derived from the original method, but made as an embed.
        ctx = self.context
        bot = ctx.bot

        destination = self.get_destination()
        note = self.get_ending_note()
                
        no_category = f'\u200b{self.no_category}'

        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return f"{cog.qualified_name}" if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)

        embed = default.branded_embed(title="Command list", description=f"A list of all the commands the bot has to offer.", color="green", inline=True)

        for category, commands in to_iterate:
            commands = sorted(commands, key=lambda c: c.name) if self.sort_commands else list(commands)
            joined = '\u2002'.join(f"`{c.name}`" for c in commands)
            
            embed.add_field(name=f"{category}", value=f"{joined}", inline=False)
            self.add_bot_commands_formatting(commands, category)
    
        embed.set_footer(text=note)

        try:
            if perms.can_react(self.context):
                await self.context.message.add_reaction(chr(0x2709))
        except discord.Forbidden:
            pass
        try:
            await destination.send(embed=embed)
        except discord.Forbidden:
            return await self.get_destination(no_pm=True).send(_("events.forbidden_dm"))

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages(no_pm=True)

    async def send_pages(self, no_pm: bool = False):
        try:
            if perms.can_react(self.context):
                await self.context.message.add_reaction(chr(0x2709))
        except discord.Forbidden:
            pass

        try:
            destination = self.get_destination(no_pm=no_pm)
            embed = default.branded_embed(title="Command guide", description=f"", color="green", inline=True)
            for page in self.paginator.pages:
                embed.description += page
            await destination.send(embed=embed)
        except discord.Forbidden:
            destination = self.get_destination(no_pm=True)
            await destination.send(_("events.forbidden_dm"))
