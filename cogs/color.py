from nextcord.ext import commands

from utils.data import Bot
from utils.default import translate as _
from utils.embed import failed_embed_ephemeral


class Color(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="color", description=_("cmds.color.desc"))
    async def _color_changer(self, ctx: commands.Context):
        """Changes the user color if module is enabled."""

        res = await self.bot.prisma.guildconfiguration.find_unique(
            where={"id": ctx.guild.id}
        )

        if res.color_enabled is None or res.color_enabled is False:
            return await ctx.send(
                embed=failed_embed_ephemeral(
                    _("cmds.generic.res.disabled_module", module_name="color")
                )
            )

        return await ctx.send("Fuuuck. FUUUCK.")


def setup(bot):
    bot.add_cog(Color(bot))
