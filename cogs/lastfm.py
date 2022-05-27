import nextcord
import pylast

from nextcord.ext import commands

from utils.default import translate as _

class Lastfm(commands.Cog):
    """LastFM utilities"""

    def __init__(self, bot):
        self.bot = bot
        self.lf = pylast.LastFMNetwork(
            api_key="fed79d59307284767924964ce68355dc",
            api_secret="9717f8228c4f5e105e85ffe0e00d1482"
        )

    @commands.group(name="lastfm", description="A collection of LastFM utilities ", aliases=["lf"])
    async def _lf(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send(_("cmds.lastfm.help"))

    @_lf.command(name="nowplaying", description="Get the current playing track.", aliases=["np", "fm"])
    async def _lf_nowplaying(self, ctx: commands.Context):
        lfuser = self.lf.get_user("isthisandywandy")
        print(lfuser.get_recent_tracks(now_playing=True))
        await ctx.send(lfuser.get_now_playing())

def setup(bot):
    bot.add_cog(Lastfm(bot))
