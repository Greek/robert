from nextcord.ext import commands
import nextcord

from utils import embed
from utils.default import translate as _


class Welcome(commands.Cog):
    """Welcome configuration commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="welcome")
    async def welcome(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(str(ctx.command))

    @welcome.command(name="set", description=_("cmds.config.welcome.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def change_welcome_message(
        self, ctx, channel: nextcord.TextChannel, *, message: str
    ):
        try:
            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {
                        "id": ctx.guild.id,
                        "welcome_channel": channel.id,
                        "welcome_greeting": message,
                    },
                    "update": {
                        "id": ctx.guild.id,
                        "welcome_channel": channel.id,
                        "welcome_greeting": message,
                    },
                },
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
        except Exception as error:
            await ctx.send(error)

    @welcome.command(name="clear", description=_("cmds.config.welcome.desc"))
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clear_welcome_message(self, ctx: commands.Context):
        try:
            await self.bot.prisma.guildconfiguration.upsert(
                where={"id": ctx.guild.id},
                data={
                    "create": {
                        "id": ctx.guild.id,
                        "welcome_channel": None,
                        "welcome_greeting": None,
                    },
                    "update": {
                        "id": ctx.guild.id,
                        "welcome_channel": None,
                        "welcome_greeting": None,
                    },
                },
            )
            await ctx.send(
                embed=embed.success_embed_ephemeral(
                    _(
                        "cmds.config.welcome.removal_success",
                    )
                )
            )
        except Exception as error:
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Welcome(bot))
