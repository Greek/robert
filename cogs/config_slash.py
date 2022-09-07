"""
Copyright (c) 2021-present Onyx Studios

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

import os
import nextcord

from nextcord import ChannelType, Interaction, SlashOption
from nextcord.ext import commands, application_checks
from pymongo import MongoClient
from cogs.config import Config
from utils.default import translate as _


class ConfigSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.db["guild-configs"]

    # pylint: disable=E0213,E1120,E1123
    @nextcord.slash_command(
        name="config",
        description="Configure the bot for your server's needs",
    )
    async def config_slash(interaction: Interaction):
        pass

    @config_slash.subcommand(
        name="welcome", description="Configure the bot for your server's needs"
    )
    async def welcome_slash(interaction: Interaction):
        pass

    @config_slash.subcommand(
        name="logs", description="Configure the bot for your server's needs"
    )
    async def logs_slash(interaction: Interaction):
        pass

    @config_slash.subcommand(
        name="giveaway", description="Configure the bot for your server's needs"
    )
    async def giveaway_slash(interaction: Interaction):
        pass

    # Welcome
    @welcome_slash.subcommand(name="set", description=_("cmds.config.welcome.desc"))
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def change_welcome_message_slash(
        self,
        ctx: Interaction,
        channel: nextcord.abc.GuildChannel = SlashOption(
            name="channel",
            channel_types=[ChannelType.text],
            description=_("cmds.config.welcome.desc"),
            required=True,
        ),
        message: str = SlashOption(
            name="greeting", description=_("cmds.config.welcome.desc")
        ),
    ):
        return await Config.change_welcome_message(
            context=self, ctx=ctx, channel=channel, message=message
        )

    @welcome_slash.subcommand(
        name="clear", description=_("cmds.config.welcome.desc_clear")
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def clear_welcome_message_slash(self, ctx: Interaction):
        return await Config.clear_welcome_message(context=self, ctx=ctx)

    # Welcome end

    # Logs

    @logs_slash.subcommand(
        name="messages-set", description="Configure the bot for your server's needs"
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs(
        self,
        interaction: Interaction,
        channel: nextcord.abc.GuildChannel = SlashOption(
            name="channel",
            channel_types=[ChannelType.text],
            description=_("cmds.config.welcome.desc"),
            required=True,
        ),
    ):
        return await Config.set_message_logs(self, ctx=interaction, channel=channel)

    @logs_slash.subcommand(
        name="messages-whitelist",
        description="Configure the bot for your server's needs",
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist(
        self,
        interaction: Interaction,
        channel: nextcord.abc.GuildChannel = SlashOption(
            name="channel",
            channel_types=[ChannelType.text],
            description=_("cmds.config.welcome.desc"),
            required=True,
        ),
    ):
        return await Config.set_message_logs_whitelist(
            self, ctx=interaction, channel=channel
        )

    @logs_slash.subcommand(
        name="messages-unwhitelist",
        description="Configure the bot for your server's needs",
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist_remove(
        self,
        interaction: Interaction,
        channel: nextcord.abc.GuildChannel = SlashOption(
            name="channel",
            channel_types=[ChannelType.text],
            description=_("cmds.config.welcome.desc_whitellist_remove"),
            required=True,
        ),
    ):
        return await Config.set_message_logs_whitelist_remove(
            self, ctx=interaction, channel=channel
        )

    @logs_slash.subcommand(
        name="messages-clearwhitelist",
        description="Configure the bot for your server's needs",
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def set_message_logs_whitelist_clear(
        self,
        interaction: Interaction,
        channel: nextcord.abc.GuildChannel = SlashOption(
            name="channel",
            channel_types=[ChannelType.text],
            description=_("cmds.config.welcome.desc_whitellist_clear"),
            required=True,
        ),
    ):
        return await Config.set_message_logs_whitelist_clear(
            self, interaction, channel=channel
        )

    @logs_slash.subcommand(
        name="messages-clear", description="Configure the bot for your server's needs"
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def clear_message_log(
        self,
        interaction: Interaction,
    ):
        return await Config.clear_message_logs(self, interaction)

    # Logs end
    @giveaway_slash.subcommand(
        name="set", description="Configure the bot for your server's needs"
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def set_giveaway_channel(
        self,
        interaction: Interaction,
        channel: nextcord.abc.GuildChannel = SlashOption(
            name="channel",
            channel_types=[ChannelType.text],
            description=_("cmds.config.welcome.desc"),
            required=True,
        ),
    ):
        return await Config.set_giveaway_channel(self, interaction, channel=channel)

    @giveaway_slash.subcommand(
        name="clear", description="Configure the bot for your server's needs"
    )
    @application_checks.has_guild_permissions(manage_channels=True)
    @application_checks.bot_has_guild_permissions(manage_channels=True)
    async def clear_giveaway_channel(
        self,
        interaction: Interaction,
    ):
        return await Config.clear_giveaway_channel(self, interaction)


def setup(bot):
    bot.add_cog(ConfigSlash(bot))
