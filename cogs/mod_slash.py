from discord import Interaction
import nextcord
import os

from nextcord import SlashOption
from nextcord.ext import commands, application_checks

from redis.asyncio import Redis
from pymongo import MongoClient

from cogs.mod import Mod

from utils import perms, embed as eutil
from utils.default import translate as _


class ModSlash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.db["guild-configs"]

        self.redis: Redis = Redis.from_url(
            url=os.environ.get("REDIS_URL"), decode_responses=True
        )

    @nextcord.slash_command(
        name="kick", description=_("cmds.kick.desc"), guild_ids=[932369210611494982]
    )
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

    @nextcord.slash_command(
        name="ban", description=_("cmds.ban.desc"), guild_ids=[932369210611494982]
    )
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

    @nextcord.slash_command(name="mute", description="Mute a person.")
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

    @nextcord.slash_command(name="unmute", description="Un-mute a person.")
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
