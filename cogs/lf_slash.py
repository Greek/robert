import os
import nextcord
import pylast

from nextcord.ext import commands
from pymongo import MongoClient

from cogs.lf import Lastfm

from utils.default import translate as _


class LfSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix = os.environ.get("DISCORD_PREFIX")
        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]

        self.lf_coll = self.db["lastfm"]
        self.lf = pylast.LastFMNetwork(
            api_key=os.environ.get("LAST_FM_KEY"),
            api_secret=os.environ.get("LAST_FM_SECRET"),
        )

    @nextcord.slash_command(
        name="lastfm", description=_("cmds.lastfm.desc"), guild_ids=[932369210611494982]
    )
    async def _lf(self, ctx: nextcord.Interaction):
        pass

    @_lf.subcommand(name="login", description=_("cmds.lastfm.login"))
    async def _lf_login(
        self,
        ctx: nextcord.Interaction,
        # username: str = nextcord.SlashOption(
        #     name="username", description="LastFM Username", required=True
        # ),
    ):
        return await ctx.send(
            f"Please use `{self.prefix}lf login` instead.", ephemeral=True
        )
        return await Lastfm._lf_login(context=self, ctx=ctx, username=username)


def setup(bot):
    bot.add_cog(LfSlash(bot))
