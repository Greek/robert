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

from discord.ext.commands import AutoShardedBot, MinimalHelpCommand
from dislash import InteractionClient
from utils import perms, default
from utils.default import translate as _

do_not_load = (
    'cogs.interactives',
    'cogs.fun_slash'
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

            guilds = [880389498570178591]
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
                        self.unload_extension(cog)
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
        return "You can get help with a specific command with \"{0}{1} <cmd>\"\n" \
            "It provides more information on what you can do with that command.".format(cfg_prefix, command_name)

    def get_opening_note(self):
        pass

    async def send_error_message(self, error):
        destination = self.get_destination(no_pm=True)
        await destination.send(error)

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
            for page in self.paginator.pages:
                await destination.send(page)
        except discord.Forbidden:
            destination = self.get_destination(no_pm=True)
            await destination.send(_("events.forbidden_dm"))
