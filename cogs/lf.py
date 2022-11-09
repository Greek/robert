import os
import nextcord
import pylast

from nextcord.ext import commands

from utils.constants import LASTFM_EMBED_COLOR
from utils.default import translate as _
from utils.embed import warn_embed_ephemeral
from utils.perms import only_owner
from utils.data import Bot


class Lastfm(commands.Cog):
    """LastFM utilities"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.lastfm = pylast.LastFMNetwork(
            api_key=os.environ.get("LAST_FM_KEY"),
            api_secret=os.environ.get("LAST_FM_SECRET"),
        )

    @commands.group(name="lastfm", description=_("cmds.lastfm.desc"), aliases=["lf"])
    @commands.check(only_owner)
    async def _lf(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send(_("cmds.lastfm.help"))

    @_lf.command(name="login", description=_("cmds.lastfm.login.desc"))
    async def _lf_login(self, ctx: commands.Context, username: str):
        caller = ctx.user if isinstance(ctx, nextcord.Interaction) else ctx.author

        try:
            if self.bot.lastfm.find_one({"_id": caller.id, "username": f"{username}"}):
                return await ctx.send(
                    embed=warn_embed_ephemeral(
                        _("cmds.lastfm.login.res.already_claimed")
                    )
                )
        except:
            pass

        # try:
        #     if self.lf_coll.find({"username": f"{username}"}):
        #         return await ctx.send(
        #             embed=failed_embed_ephemeral(
        #                 _("cmds.lastfm.login.res.already_exists")
        #             )
        #         )

        # except:
        # pass
        self.bot.lastfm.find_one_and_update(
            {"_id": caller.id},
            {"$set": {"username": f"{username}"}},
            upsert=True,
        )

        return await ctx.send("Hi")

    @_lf.command(
        name="nowplaying",
        description=_("cmds.lastfm.nowplaying.desc"),
        aliases=["np", "fm"],
    )
    async def _lf_nowplaying(self, ctx: commands.Context):
        await ctx.trigger_typing()
        caller = ctx.user if isinstance(ctx, nextcord.Interaction) else ctx.author

        res = self.bot.lastfm.find_one({"_id": caller.id})

        try:
            lfuser = self.lastfm.get_user(res["username"])
        except:
            return await ctx.send(
                embed=warn_embed_ephemeral(_("cmds.lastfm.res.user_not_set"))
            )

        current_track = lfuser.get_now_playing()
        most_current_track = lfuser.get_recent_tracks(limit=1)

        if current_track is None:
            # return await ctx.reply(
            #     embed=failed_embed_ephemeral(
            #         _("cmds.lastfm.nowplaying.res.not_playing")
            #     ),
            #     mention_author=False,
            # )

            try:
                for track in most_current_track:
                    lastfm_embed = nextcord.Embed(color=LASTFM_EMBED_COLOR)
                    lastfm_embed.set_author(
                        name=f"Currently playing - {ctx.author.name}"
                    )
                    # lastfm_embed.set_thumbnail(url=track.track.get_cover_image())
                    lastfm_embed.set_footer(
                        text=f"Scrobbles: {track.track.get_userplaycount():,} | "
                        f"Total play count: {track.track.get_playcount():,} requested by {lfuser.get_name()}"
                    )

                    lastfm_embed.description = f"[{track.track.get_name()}]({track.track.get_url()})\n**by** \
                 *[{track.track.get_artist()}]({track.track.get_artist()})*\n \
                 **on** *[{track.track.get_album()}]({track.track.get_album()})*"

                    return await ctx.send(embed=lastfm_embed)
            except Exception as exc:
                return await self.bot.create_error_log(self, ctx, exc)

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
