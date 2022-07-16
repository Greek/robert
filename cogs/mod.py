"""
Copyright (c) 2021-present flower and contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import nextcord
import os

from nextcord.ext import commands, tasks

from pytimeparse.timeparse import timeparse
from redis.asyncio import Redis
from pymongo import MongoClient


from utils import default, perms
from utils.data import create_error_log
from utils.embed import (
    failed_embed_ephemeral,
    success_embed_ephemeral,
    warn_embed_ephemeral,
)
from utils.default import translate as _

from dotenv import dotenv_values, load_dotenv

dot_cfg = dotenv_values(".env")
load_dotenv(".env")

# Source: https://github.com/Rapptz/RoboDanny/blob/rewrite/cogs/mod.py
class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(
                    f"{argument} is not a valid member or member ID."
                ) from None
        else:
            return m.id


class Mod(commands.Cog):
    """Commands for moderators"""

    def __init__(self, bot: nextcord.Client):

        self.bot = bot
        self.guild_id = 932369210611494982
        self.redis: Redis = Redis.from_url(
            url=os.environ.get("REDIS_URL"), decode_responses=True
        )
        self.pubsub = self.redis.pubsub()

        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.db["guild-configs"]

        self.subscribe_expiry_handler.start()
        self.listen_messages.start()

    def cog_unload(self):
        self.subscribe_expiry_handler.cancel()
        self.listen_messages.cancel()

    async def expiry_handler(self, msg) -> None:
        if msg["data"].startswith("mute"):
            try:
                data = msg["data"].split("-")
                guild = self.bot.get_guild(int(data[2]))
                member = guild.get_member(int(data[1]))

                try:
                    res = self.config_coll.find_one({"_id": guild.id})
                    role = guild.get_role(res["muteRole"])
                except:
                    return

                await member.remove_roles(role, reason="Mute expired.")
            except Exception as e:
                ctx = self.bot
                await create_error_log(self, ctx, e)

    @tasks.loop(count=1)
    async def subscribe_expiry_handler(self):
        # Subscribe to all "expired" keyevents thru pubsub and handle them.
        await self.pubsub.psubscribe(**{"__keyevent@0__:expired": self.expiry_handler})

    @tasks.loop(seconds=0.01)
    async def listen_messages(self):
        message = await self.pubsub.get_message()
        if message:
            print(f"[Mute] Listening to expired mutes")
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
            res = self.config_coll.find_one({"_id": channel.guild.id})
            role = channel.guild.get_role(int(res["muteRole"]))
            await channel.set_permissions(
                role,
                send_messages=False,
                reason="Found new channel, adding permissions.",
            )
        except:
            return

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        mute_key = await self.redis.get(f"mute-{member.id}-{member.guild.id}")
        if mute_key is not None:
            try:
                res = self.config_coll.find_one({"_id": member.guild.id})
                role = member.guild.get_role(res["muteRole"])
            except:
                return

            return await member.add_roles(
                role, reason="Muted person re-joined the server. Muting again."
            )

    @commands.command(name="kick", description=_("cmds.kick.desc"))
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_user(self, ctx, member: nextcord.Member, *, reason=None) -> None:
        try:
            if isinstance(ctx, nextcord.Interaction):
                if await perms.check_priv_interaction(ctx, member=member):
                    return
            if await perms.check_priv(ctx, member=member):
                return
            await member.kick(
                reason=default.responsible(
                    ctx.author if isinstance(ctx, commands.Context) else ctx.user,
                    reason,
                )
            )
            await ctx.send(
                _("cmds.kick.res_noreason", user=member)
                if reason is None
                else _("cmds.kick.res_reason", user=member, reason=reason)
            )
        except Exception as e:
            await create_error_log(self, ctx, e)
            await ctx.send(embed=failed_embed_ephemeral("I can't kick that person."))

    @commands.command(name="ban", description=_("cmds.ban.desc"))
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_user(self, ctx, member: MemberID, *, reason=None) -> None:
        caller = ctx.author if isinstance(ctx, commands.Context) else ctx.user
        m = ctx.guild.get_member(member)
        try:
            if m is not None and await perms.check_priv(ctx, m):
                return

            await ctx.guild.ban(
                nextcord.Object(id=member),
                reason=default.responsible(caller, reason),
                delete_message_days=0,
            )
            await ctx.send(
                _("cmds.ban.res_noreason", user=f"{m.name}#{m.discriminator}")
                if reason is None
                else _("cmds.ban.res_reason", user=m, reason=reason)
            )
        except Exception as e:
            await ctx.send(embed=failed_embed_ephemeral("I can't ban that person."))

    @commands.command(
        name="purge", aliases=["clear", "c"], description=_("cmds.purge.desc")
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def mass_delete(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)
        sent = await ctx.send(
            embed=success_embed_ephemeral(
                _("cmds.purge.res", ctx=ctx.author.mention, amount=amount)
                if amount > 1
                else _("cmds.purge.res_singular", ctx=ctx.author.mention, amount=amount)
            )
        )
        await sent.delete(delay=3)

    @commands.command(name="mute", aliases=["m"], description="Mute a person.")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.guild_only()
    async def mute_member(
        self, ctx: commands.Context, member: nextcord.Member, *, duration: str = None
    ):
        try:
            if isinstance(ctx, nextcord.Interaction):
                if await perms.check_priv_interaction(ctx, member=member):
                    return
            if await perms.check_priv(ctx, member=member):
                return

            existing_mute = await self.redis.get(f"mute-{member.id}-{ctx.guild.id}")
            res = self.config_coll.find_one({"_id": ctx.guild.id})

            try:
                role = ctx.guild.get_role(res["muteRole"])
            except KeyError:
                role = await ctx.guild.create_role(name="Muted")
                role.permissions.send_messages = False
                channels = ctx.guild.channels
                for channel in channels:
                    await channel.set_permissions(role, send_messages=False)

                self.config_coll.find_one_and_update(
                    {"_id": ctx.guild.id}, {"$set": {f"muteRole": role.id}}
                )

            if role is None:
                role = await ctx.guild.create_role(name="Muted")
                role.permissions.send_messages = False
                channels = ctx.guild.channels
                for channel in channels:
                    await channel.set_permissions(role, send_messages=False)

                self.config_coll.find_one_and_update(
                    {"_id": ctx.guild.id}, {"$set": {f"muteRole": role.id}}
                )

            if existing_mute:
                return await ctx.send(
                    embed=warn_embed_ephemeral(
                        _("cmds.mute.res.invalid.already_muted", person=member.mention)
                    )
                )

            try:
                await member.add_roles(
                    role,
                    reason=f"Muted by {ctx.author}"
                    if isinstance(ctx, commands.Context)
                    else f"Muted by {ctx.user}",
                )
            except nextcord.errors.Forbidden:
                return

            parsed_duration = timeparse(duration) if duration is not None else None
            
            # if parsed_duration is not None and parsed_duration or int(duration) >= 1209600:
            #     return await ctx.send(
            #         embed=warn_embed_ephemeral(_("cmds.mute.res.invalid.time"))
            #     )

            if parsed_duration is None:
                await self.redis.set(f"mute-{member.id}-{ctx.guild.id}", "Muted")
                await ctx.send(
                    embed=success_embed_ephemeral(
                        _("cmds.mute.res.muted.forever", person=member.mention)
                    )
                )
            else:
                await self.redis.setex(
                    f"mute-{member.id}-{ctx.guild.id}",
                    parsed_duration,
                    "Muted",
                )
                return await ctx.send(
                    embed=success_embed_ephemeral(
                        _(
                            "cmds.mute.res.muted.temp",
                            person=member.mention,
                            duration=duration,
                        )
                    )
                )

        except Exception as e:
            await create_error_log(self, ctx, e)

    @commands.command(name="unmute", aliases=["um"], description="Un-mute a person.")
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

            mute = await self.redis.get(f"mute-{member.id}-{ctx.guild.id}")
            if mute is None:
                return await ctx.send(
                    embed=warn_embed_ephemeral(
                        _("cmds.unmute.res.invalid.not_muted", person=member.mention)
                    )
                )

            res = self.config_coll.find_one({"_id": ctx.guild.id})
            try:
                role = ctx.guild.get_role(res["muteRole"])
            except KeyError:
                await ctx.send(
                    embed=success_embed_ephemeral(
                        _("cmds.unmute.res.success", person=member.mention)
                    )
                ),
                return await self.redis.delete(
                    f"mute-{member.id}-{ctx.guild.id}"
                )  # It doesn't exist anyway.

            if role is None:
                await ctx.send(
                    embed=success_embed_ephemeral(
                        _("cmds.unmute.res.success", person=member.mention)
                    )
                ),
                return await self.redis.delete(f"mute-{member.id}-{ctx.guild.id}")

            await self.redis.delete(f"mute-{member.id}-{ctx.guild.id}")
            await member.remove_roles(
                role,
                reason=f"Mute removed by {ctx.author}"
                if isinstance(ctx, commands.Context)
                else f"Mute removed by {ctx.user}",
            )
            await ctx.send(
                embed=success_embed_ephemeral(
                    _("cmds.unmute.res.success", person=member.mention)
                )
            )
        except Exception as e:
            await create_error_log(self, ctx, e)

    @commands.command(
        name="servermute", aliases=["sm"], description="Server mute a person."
    )
    async def _sm(self, ctx: commands.Context, member: nextcord.Member):
        if await perms.check_priv(ctx, member=member):
            return

        await member.edit(mute=False)
        return await ctx.send(
            embed=success_embed_ephemeral(f"Server muted {member.mention}")
        )


def setup(bot):
    bot.add_cog(Mod(bot))
