import os

import nextcord
from discord import Interaction
from nextcord import SlashOption
from nextcord.ext import application_checks, commands
from redis.asyncio import Redis

from cogs.mod import Mod
from utils.data import Bot
from utils.default import translate as _


class ModSlash(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.redis: Redis = Redis.from_url(
            url=os.environ.get("REDIS_URL"), decode_responses=True
        )

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
        ctx: nextcord.Interaction,
        member: nextcord.Member = SlashOption(
            name="person", description="Person to mute", required=True
        ),
        duration: str = SlashOption(
            name="duration",
            description="The amount of time to mute the person",
            required=False,
        ),
    ):
        try:
            return await Mod.mute_member(
                context=self,
                ctx=ctx,
                member=member,
                duration=duration,
            )
        except Exception as error:
            await self.bot.create_error_log(ctx, error)

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
        except Exception as error:
            await self.bot.create_error_log(ctx, error)


def setup(bot):
    bot.add_cog(ModSlash(bot))
