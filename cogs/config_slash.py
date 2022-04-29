import nextcord
import os

from nextcord import ChannelType, Interaction, SlashOption
from nextcord.ext import commands, application_checks
from cogs.config import Config
from utils.default import translate as _
from pymongo import MongoClient


class ConfigSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.db["guild-configs"]

    @nextcord.slash_command(
        name="config",
        description="Configure the bot for your server's needs",
        default_permission=False
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
        return await Config.set_message_logs(self, interaction, channel=channel)

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


def setup(bot):
    bot.add_cog(ConfigSlash(bot))
