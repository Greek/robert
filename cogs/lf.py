import nextcord
import pylast
import os

from nextcord.ext import commands
from utils.constants import LASTFM_EMBED_COLOR

from utils.default import translate as _


class Lastfm(commands.Cog):
    """LastFM utilities"""

    def __init__(self, bot):
        self.bot = bot
        self.lf = pylast.LastFMNetwork(
            api_key=os.environ.get("LAST_FM_KEY"),
            api_secret=os.environ.get("LAST_FM_SECRET"),
        )

    @commands.group(name="lastfm", description=_("cmds.lastfm.desc"), aliases=["lf"])
    async def _lf(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send(_("cmds.lastfm.help"))

    @_lf.command(
        name="nowplaying",
        description=_("cmds.lastfm.nowplaying.desc"),
        aliases=["np", "fm"],
    )
    async def _lf_nowplaying(self, ctx: commands.Context):
        lfuser = self.lf.get_user("isthisandywandy")
        current_track = lfuser.get_now_playing()

        if current_track is None:
            return await ctx.send(_("cmds.lastfm.nowplaying.res.not_playing"))

        lastfm_embed = nextcord.Embed(color=LASTFM_EMBED_COLOR)
        lastfm_embed.set_author(name=f"Currently playing - {ctx.author.name}")
        lastfm_embed.set_thumbnail(url=current_track.get_cover_image(2))
        lastfm_embed.set_footer(
            text=f"Scrobbles: {current_track.get_userplaycount():,} | "
            f"Total play count: {current_track.get_playcount():,} requested by {lfuser.get_name()}"
        )

        lastfm_embed.description = f"[{current_track.get_name()}]({current_track.get_url()})\n**by** \
                 *[{current_track.get_artist()}]({current_track.get_artist().get_url()})*\n \
                 **on** *[{current_track.get_album()}]({current_track.get_album().get_url()})*"

        return await ctx.send(embed=lastfm_embed)

    @commands.command(
        name="nowplaying",
        description=_("cmds.lastfm.nowplaying.desc"),
        aliases=["fm", "np"],
    )
    async def _nowplaying(self, ctx: commands.Context):
        return await self._lf_nowplaying(context=ctx)


def setup(bot):
    bot.add_cog(Lastfm(bot))
