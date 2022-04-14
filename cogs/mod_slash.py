from discord import ButtonStyle, Interaction
import nextcord
import os

from nextcord import SlashOption
from nextcord.ext import commands

from redis.asyncio import Redis
from pymongo import MongoClient

from cogs.mod import Mod

from utils import perms, embed as eutil
from utils.default import translate as _


class Pet(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(
            "Your pet",
            timeout=5 * 60,  # 5 minutes
        )

        self.name = nextcord.ui.TextInput(
            label="Your pet's name",
            min_length=2,
            max_length=50,
        )
        self.add_item(self.name)

        self.description = nextcord.ui.TextInput(
            label="Description",
            style=nextcord.TextInputStyle.paragraph,
            placeholder="Information that can help us recognise your pet",
            required=False,
            max_length=1800,
        )
        self.add_item(self.description)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        response = f"{interaction.user.mention}'s favourite pet's name is {self.name.value}."
        if self.description.value != "":
            response += f"\nTheir pet can be recognized by this information:\n{self.description.value}"
        await interaction.send(response)


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
        return await Mod.kick_user(context=self, ctx=ctx, member=member, reason=reason)

    @nextcord.slash_command(
        name="ban", description=_("cmds.ban.desc"), guild_ids=[932369210611494982]
    )
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
        await Mod.ban_user(context=self, ctx=ctx, member=member.id, reason=reason)

    @nextcord.slash_command(name="purge", description=_("cmds.purge.desc"))
    async def _clear(
        self,
        ctx,
        amount: int = SlashOption(
            name="amount", description=_("cmds.purge.option_amount"), required=True
        ),
    ):
        return await Mod.mass_delete(context=self, ctx=ctx, amount=amount)

    @nextcord.slash_command(name="mute", description="Mute a person.")
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
        return await Mod.mute_member(
            context=self,
            ctx=ctx,
            member=member,
            duration_in_seconds=duration_in_seconds,
        )

    @nextcord.slash_command(name="unmute", description="Un-mute a person.")
    async def _unmute(
        self,
        ctx,
        member: nextcord.Member = SlashOption(
            name="person", description="Person to un-mute", required=True
        ),
    ):
        return await Mod.unmute_member(context=self, ctx=ctx, member=member)


def setup(bot):
    bot.add_cog(ModSlash(bot))
