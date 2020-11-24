import discord
import os
import logging

from discord.ext.commands import AutoShardedBot, MinimalHelpCommand
from utils import perms

class Bot(AutoShardedBot):
    """ Custom bot class extenting AutoShardedBot """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            for cog in os.listdir("cogs"):
                if cog.endswith(".py"):
                    name = cog[:-3]
                    self.load_extension(f"cogs.{name}")
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
        return "You can get help with a specific command with \"{0}{1} <cmd>\"\n" \
            "It provides more information on what you can do with that command.".format(self.clean_prefix, command_name)
    
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
            await destination.send("turn on your dms :flushed:")
