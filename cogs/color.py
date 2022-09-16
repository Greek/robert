import nextcord

from nextcord.ext import commands

from utils.data import Bot
from utils.default import translate as _
from utils.embed import failed_embed_ephemeral, success_embed_ephemeral


class Color(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def _create_color_role(self, ctx: commands.Context, color):
        existing_color_role: nextcord.Role = nextcord.utils.get(
            ctx.guild.roles, name=f"{str(ctx.author)}"
        )

        if existing_color_role:
            await existing_color_role.delete(reason="New color requested.")

        color_role = await ctx.guild.create_role(
            name=f"{str(ctx.author)}",
            reason=f"Created per {str(ctx.author)}",
            color=color,
        )

        return color_role

    @commands.command(name="color", description=_("cmds.color.desc"))
    async def _color_changer(self, ctx: commands.Context, color: nextcord.Colour):
        """Changes the user color if module is enabled."""
        try:
            res = await self.bot.prisma.guildconfiguration.find_unique(
                where={"id": ctx.guild.id}
            )

            try:
                if res.color_enabled is None or res.color_enabled is False:
                    return await ctx.send(
                        embed=failed_embed_ephemeral(
                            _("cmds.generic.res.disabled_module", module_name="color")
                        )
                    )
            except AttributeError:
                return await ctx.send(
                    embed=failed_embed_ephemeral(
                        _("cmds.generic.res.disabled_module", module_name="color")
                    )
                )

            color_role = await self._create_color_role(ctx, color)
            await ctx.author.add_roles(color_role, reason="Requested color role.")

            return await ctx.send(
                embed=success_embed_ephemeral("Enjoy your new color!")
            )
        except Exception as error:
            await self.bot.create_error_log(ctx, error)


def setup(bot):
    bot.add_cog(Color(bot))
