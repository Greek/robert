import nextcord

from nextcord.ext import commands

from utils.default import translate as _
from utils.embed import success_embed_ephemeral

class Role(commands.Cog):
    """Role utilities"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="role", description=_("cmds.role.desc"))
    async def _role(self, ctx: commands.Context, user: nextcord.Member, role: str):
        indexed_role = nextcord.utils.get(ctx.guild.roles, name=role)

        if indexed_role in user.roles:
            await  user.remove_roles(indexed_role)
            return await ctx.send(
                embed=success_embed_ephemeral(
                    _(
                        "cmds.role.set.res.success_remove",
                        role=role,
                        user=user.mention,
                    )
                )
            )

        await user.add_roles(indexed_role)
        return await ctx.send(
            embed=success_embed_ephemeral(
                _("cmds.role.set.res.success", role=role, user=user.mention)
            )
        )

    # @_role.command(name="add", aliases=["give"])
    # async def _role_add(self, ctx: commands.Context, user: nextcord.Member, role: str):
    #     return await self._role(ctx, user=user, role=role)


def setup(bot):
    bot.add_cog(Role(bot))
