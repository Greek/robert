from nextcord.ext import commands, tasks

import os
import nextcord

from pytimeparse.timeparse import timeparse
from redis.asyncio import Redis

from utils import perms
from utils.data import Bot
from utils.embed import (
    failed_embed_ephemeral,
    success_embed_ephemeral,
    warn_embed_ephemeral,
)
from utils.default import translate as _


class Rmute(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild_id = 932369210611494982
        self.redis: Redis = Redis.from_url(
            url=os.environ.get("REDIS_URL"), decode_responses=True
        )
        self.pubsub = self.redis.pubsub()

        self.subscribe_expiry_handler.start()
        self.listen_messages.start()

    def cog_unload(self):
        self.subscribe_expiry_handler.cancel()
        self.listen_messages.cancel()

    async def expiry_handler(self, msg) -> None:
        self.bot.logger.debug(f"Recieved pubsub message:\n{msg}")
        if msg["data"].startswith("rmute"):
            try:
                data = msg["data"].split(":")
                guild = self.bot.get_guild(int(data[2]))
                member = guild.get_member(int(data[1]))

                try:
                    res = await self.bot.prisma.guildconfiguration.find_unique(
                        where={"id": self.guild_id}
                    )
                    role = guild.get_role(res.reaction_mute_role)
                except:
                    return

                self.bot.logger.debug(f"Reaction Mute expired from {self.redis}")
                await member.remove_roles(role, reason="Reaction Mute expired.")
            except Exception as error:
                ctx = self.bot
                await self.bot.create_error_log(ctx, error)

    @tasks.loop(count=1)
    async def subscribe_expiry_handler(self):
        # Subscribe to all "expired" keyevents thru pubsub and handle them.
        await self.pubsub.psubscribe(**{"__keyevent@0__:expired": self.expiry_handler})

    @tasks.loop(seconds=0.01)
    async def listen_messages(self):
        message = await self.pubsub.get_message()
        if message:
            self.bot.logger.info("Listening to expired mutes")
        else:
            pass

    @subscribe_expiry_handler.before_loop
    async def subscribe_redis_before(self):
        await self.bot.wait_until_ready()

    @listen_messages.before_loop
    async def listen_messages_before(self):
        await self.bot.wait_until_ready()
        await self.subscribe_expiry_handler()

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: nextcord.TextChannel):
        try:
            res = await self.bot.prisma.guildconfiguration.find_unique(
                where={"id": channel.guild.id}
            )
            role = channel.guild.get_role(res.reaction_mute_role)
            await channel.set_permissions(
                role,
                add_reactions=False,
                reason="Found new channel, adding permissions.",
            )
            self.bot.logger.debug("rmute: Added role to channel")
        except:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        reaction_mute_key = await self.redis.get(f"rmute:{member.id}:{member.guild.id}")
        if reaction_mute_key is not None:
            try:
                res = await self.bot.prisma.guildconfiguration.find_unique(
                    where={"id": member.guild.id}
                )
                role = member.guild.get_role(res.reaction_mute_role)
            except Exception as error:
                self.bot.logger.debug(error)

            return await member.add_roles(
                role, reason="Reaction Muted person re-joined the server. Muting again."
            )

    @commands.command(name="rmute", description=_("cmds.rmute.desc"))
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.guild_only()
    async def _reaction_mute(
        self, ctx, member: nextcord.Member, *, duration: str = None
    ):
        try:
            if isinstance(ctx, nextcord.Interaction):
                if await perms.check_priv_interaction(ctx, member=member):
                    return
            if await perms.check_priv(ctx, member=member):
                return

            existing_mute = await self.redis.get(f"rmute:{member.id}:{ctx.guild.id}")
            res = await self.bot.prisma.guildconfiguration.find_unique(
                where={"id": ctx.guild.id}
            )

            try:
                role = ctx.guild.get_role(res.reaction_mute_role)
            except AttributeError:
                role = await ctx.guild.create_role(name="Reaction Muted")
                role.permissions.send_messages = False
                channels = ctx.guild.channels
                for channel in channels:
                    await channel.set_permissions(role, add_reactions=False)

                await self.bot.prisma.guildconfiguration.upsert(
                    where={"id": ctx.guild.id},
                    data={
                        "create": {"id": ctx.guild.id, "reaction_mute_role": role.id},
                        "update": {"id": ctx.guild.id, "reaction_mute_role": role.id},
                    },
                )

            if role is None:
                role = await ctx.guild.create_role(name="Reaction Muted")
                role.permissions.send_messages = False
                channels = ctx.guild.channels
                for channel in channels:
                    await channel.set_permissions(role, add_reactions=False)

                await self.bot.prisma.guildconfiguration.upsert(
                    where={"id": ctx.guild.id},
                    data={
                        "create": {"id": ctx.guild.id, "reaction_mute_role": role.id},
                        "update": {"id": ctx.guild.id, "reaction_mute_role": role.id},
                    },
                )

            if existing_mute:
                return await ctx.send(
                    embed=warn_embed_ephemeral(
                        _("cmds.rmute.res.invalid.already_muted", person=member.mention)
                    )
                )

            try:
                await member.add_roles(
                    role,
                    reason=f"Reaction Muted by {ctx.author}"
                    if isinstance(ctx, commands.Context)
                    else f"Reaction Muted by {ctx.user}",
                )
            except nextcord.errors.Forbidden:
                return

            parsed_duration = timeparse(duration) if duration is not None else None

            # if parsed_duration is not None and parsed_duration or int(duration) >= 1209600:
            #     return await ctx.send(
            #         embed=warn_embed_ephemeral(_("cmds.rmute.res.invalid.time"))
            #     )

            if parsed_duration is None:
                await self.redis.set(
                    f"rmute:{member.id}:{ctx.guild.id}", "Reaction Muted"
                )
                await ctx.send(
                    embed=success_embed_ephemeral(
                        _("cmds.rmute.res.muted.forever", person=member.mention)
                    )
                )
            else:
                await self.redis.setex(
                    f"rmute:{member.id}:{ctx.guild.id}",
                    parsed_duration,
                    "Reaction Muted",
                )
                return await ctx.send(
                    embed=success_embed_ephemeral(
                        _(
                            "cmds.rmute.res.muted.temp",
                            person=member.mention,
                            duration=duration,
                        )
                    )
                )

        except Exception as error:
            await self.bot.create_error_log(ctx, error)

    @commands.command(name="runmute", aliases=["rum"], description="Un-mute a person.")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.guild_only()
    async def unmute_member(
        self,
        ctx: commands.Context,
        member: nextcord.Member,
    ):
        try:
            if await perms.check_priv(ctx, member=member):
                return

            mute = await self.redis.get(f"rmute:{member.id}:{ctx.guild.id}")
            if mute is None:
                return await ctx.send(
                    embed=warn_embed_ephemeral(
                        _("cmds.runmute.res.invalid.not_muted", person=member.mention)
                    )
                )

            res = await self.bot.prisma.guildconfiguration.find_unique(
                where={"id": ctx.guild.id}
            )
            try:
                role = ctx.guild.get_role(res.reaction_mute_role)

            except AttributeError:
                await ctx.send(
                    embed=success_embed_ephemeral(
                        _("cmds.runmute.res.success", person=member.mention)
                    )
                ),
                return await self.redis.delete(
                    f"rmute:{member.id}:{ctx.guild.id}"
                )  # It doesn't exist anyway.

            if role is None:
                await ctx.send(
                    embed=success_embed_ephemeral(
                        _("cmds.runmute.res.success", person=member.mention)
                    )
                ),
                return await self.redis.delete(f"rmute:{member.id}:{ctx.guild.id}")

            await self.redis.delete(f"rmute:{member.id}:{ctx.guild.id}")
            await member.remove_roles(
                role,
                reason=f"Reaction Mute removed by {ctx.author}"
                if isinstance(ctx, commands.Context)
                else f"Reaction Mute removed by {ctx.user}",
            )
            await ctx.send(
                embed=success_embed_ephemeral(
                    _("cmds.runmute.res.success", person=member.mention)
                )
            )
        except Exception as error:
            await self.bot.create_error_log(ctx, error)


def setup(bot):
    bot.add_cog(Rmute(bot))
