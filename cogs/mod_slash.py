import nextcord
from discord import Interaction
from nextcord import SlashOption
from nextcord.ext import application_checks, commands

from cogs.mod import Mod
from utils.data import Bot
from utils.default import translate as _


class ModSlash(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @nextcord.slash_command(name="kick", description=_("cmds.kick.desc"))
    @application_checks.has_guild_permissions(kick_members=True)
    @application_checks.bot_has_guild_permissions(kick_members=True)
    async def _kick(
        self,
        ctx: Interaction,
        member: nextcord.Member = SlashOption(
            name="person", description=_("cmds.kick.option_member")
        ),
        *,
        reason: str = SlashOption(
            name="reason", description=_("cmds.kick.option_reason"), required=False
        )
    ):
        try:
            return await Mod.kick_user(
                context=self, ctx=ctx, member=member, reason=reason
            )
        except:
            pass

    @nextcord.slash_command(name="ban", description=_("cmds.ban.desc"))
    @application_checks.has_guild_permissions(ban_members=True)
    @application_checks.bot_has_guild_permissions(ban_members=True)
    async def _ban(
        self,
        ctx,
        member: nextcord.Member = SlashOption(
            name="person", description=_("cmds.ban.option_member")
        ),
        *,
        reason: str = SlashOption(
            name="reason", description=_("cmds.ban.option_reason"), required=False
        )
    ):
        try:
            await Mod.ban_user(context=self, ctx=ctx, member=member.id, reason=reason)
        except:
            pass

    @nextcord.slash_command(name="purge", description=_("cmds.purge.desc"))
    @application_checks.has_guild_permissions(manage_messages=True)
    @application_checks.bot_has_guild_permissions(manage_messages=True)
    async def _clear(
        self,
        ctx,
        amount: int = SlashOption(
            name="amount", description=_("cmds.purge.option_amount"), required=True
        ),
    ):
        try:
            return await Mod.mass_delete(context=self, ctx=ctx, amount=amount)
        except:
            pass

    @nextcord.slash_command(name="mute", description=_("cmds.mute.desc"))
    @application_checks.has_guild_permissions(manage_messages=True)
    @application_checks.bot_has_guild_permissions(manage_roles=True)
    async def _mute(
        self,
        ctx,
        member: nextcord.Member = SlashOption(
            name="person", description="Person to mute", required=True
        ),
        duration_in_seconds: int = SlashOption(
            name="duration_in_seconds",
            description="The amount of time to mute the person (must be in seconds)",
            required=False,
        ),
    ):
        try:
            return await Mod.mute_member(
                context=self,
                ctx=ctx,
                member=member,
                duration_in_seconds=duration_in_seconds,
            )
        except:
            pass

    @nextcord.slash_command(name="unmute", description=_("cmds.unmute.desc"))
    @application_checks.has_guild_permissions(manage_messages=True)
    @application_checks.bot_has_guild_permissions(manage_roles=True)
    async def _unmute(
        self,
        ctx,
        member: nextcord.Member = SlashOption(
            name="person", description="Person to un-mute", required=True
        ),
    ):
        try:
            return await Mod.unmute_member(context=self, ctx=ctx, member=member)
        except:
            pass


def setup(bot):
    bot.add_cog(ModSlash(bot))
