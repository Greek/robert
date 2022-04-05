import nextcord
import os

from nextcord import TextChannel
from nextcord.ext import commands
from nextcord.ext.commands import Context, Greedy
from pymongo import MongoClient
from utils import embed
from utils.default import translate as _


class Config(commands.Cog):
    """The description for Config goes here."""

    def __init__(self, bot):
        self.bot = bot

        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.db["guild-configs"]

    @commands.group(name="config", aliases=['c', 'z', 'zen'])
    async def config(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))
    
    @config.group(name="welcome")
    async def welcome(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @welcome.command(name="set", description=_('cmds.config.welcome.desc'))
    async def change_welcome_message(
        self, ctx: Context, channel: TextChannel, *, message: str
    ):
        try:
            self.config_coll.find_one_and_update(
                {"_id": f"{ctx.guild.id}"},
                {
                    "$set": {
                        "welcomeChannel": f"{channel.id}",
                        "welcomeGreeting": message,
                    }
                },
                upsert=True,
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.welcome.success",
                        message=message,
                        channel=channel.mention,
                    )
                    # f'Set welcome message to "{message}" in {channel.mention}.'
                )
            )
        except Exception as e:
            await ctx.send(e)


def setup(bot):
    bot.add_cog(Config(bot))
