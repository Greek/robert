# -*- coding: utf-8 -*-

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

from discord import SlashOption, TextChannel
import nextcord
import os

from nextcord import Client
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Context, Greedy

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


class ActionReason(commands.Converter):
    async def convert(self, ctx, argument):
        ret = argument

        if len(ret) > 512:
            reason_max = 512 - len(ret) - len(argument)
            raise commands.BadArgument(
                f"reason is too long ({len(argument)}/{reason_max})"
            )
        return ret


class Mod(commands.Cog):
    """Commands for moderators"""

    def __init__(self, bot: Client):

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
            data = msg["data"].split("-")
            guild = self.bot.get_guild(int(data[2]))
            member = guild.get_member(int(data[1]))

            try:
                res = self.config_coll.find_one({"_id": f"{guild.id}"})
                role = guild.get_role(int(res["muteRole"]))
            except:
                return

            await member.remove_roles(role, reason="Mute expired.")

    @tasks.loop(count=1)
    async def subscribe_expiry_handler(self):
        # Subscribe to all "expired" keyevents thru pubsub and handle them.
        await self.pubsub.psubscribe(**{"__keyevent@0__:expired": self.expiry_handler})

    @tasks.loop(seconds=0.01)
    async def listen_messages(self):
        message = await self.pubsub.get_message()
        if message:
            print(f"[Redis] message")
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
    async def on_guild_channel_create(self, channel: TextChannel):
        try:
            res = self.config_coll.find_one({"_id": f"{channel.guild.id}"})
            role = channel.guild.get_role(int(res["muteRole"]))
            await channel.set_permissions(
                role,
                send_messages=False,
                reason="Found new channel, adding permissions.",
            )
        except:
            return

    @commands.command(name="kick", description=_("cmds.kick.desc"))
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_user(self, ctx, member: nextcord.Member, *, reason=None) -> None:
        try:
            if await perms.check_priv(ctx, member=member):
                return
            await member.kick(reason=default.responsible(ctx.author, reason))
            await ctx.reply(
                _("cmds.kick.res_noreason")
                if reason is None
                else _("cmds.kick.res_reason")
            )
        except Exception as e:
            await ctx.send(embed=failed_embed_ephemeral(e))

    @commands.command(name="ban", description=_("cmds.ban.desc"))
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_user(self, ctx, member: MemberID, *, reason=None) -> None:
        caller = ctx.author if isinstance(ctx, Context) else ctx.user
        m = ctx.guild.get_member(member)
        try:
            if m is not None and await perms.check_priv(ctx, m):
                return

            await ctx.guild.ban(
                nextcord.Object(id=member), reason=default.responsible(caller, reason)
            )
            await ctx.reply(
                _("cmds.ban.res_noreason")
                if reason is None
                else _("cmds.ban.res_reason")
            )
        except Exception as e:
            await ctx.send(embed=failed_embed_ephemeral(e))

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
        self, ctx: Context, member: nextcord.Member, *, duration_in_seconds: int = None
    ):
        try:
            existing_mute = await self.redis.get(f"mute-{member.id}-{ctx.guild.id}")
            res = self.config_coll.find_one({"_id": f"{ctx.guild.id}"})

            try:
                role = ctx.guild.get_role(int(res["muteRole"]))
            except KeyError:
                role = await ctx.guild.create_role(name="Muted")
                role.permissions.send_messages = False
                channels = ctx.guild.channels
                for channel in channels:
                    await channel.set_permissions(role, send_messages=False)

                self.config_coll.find_one_and_update(
                    {"_id": f"{ctx.guild.id}"}, {"$set": {f"muteRole": f"{role.id}"}}
                )

            if role is None:
                role = await ctx.guild.create_role(name="Muted")
                role.permissions.send_messages = False
                channels = ctx.guild.channels
                for channel in channels:
                    await channel.set_permissions(role, send_messages=False)

                self.config_coll.find_one_and_update(
                    {"_id": f"{ctx.guild.id}"}, {"$set": {f"muteRole": f"{role.id}"}}
                )

            if existing_mute:
                return await ctx.send(
                    embed=warn_embed_ephemeral(f"{member.mention} is already muted.")
                )

            await member.add_roles(
                role,
                reason=f"Muted by {ctx.author}"
                if isinstance(ctx, Context)
                else f"Muted by {ctx.user}",
            )

            if duration_in_seconds is None:
                await self.redis.set(f"mute-{member.id}-{ctx.guild.id}", "Muted")
            else:
                await self.redis.setex(
                    f"mute-{member.id}-{ctx.guild.id}",
                    duration_in_seconds,
                    "Muted",
                )

            await ctx.send(
                embed=success_embed_ephemeral(f"{member.mention} has been muted.")
            )
        except Exception as e:
            await create_error_log(self, ctx, e)

    @nextcord.slash_command(name="mute", description="Mute a person.")
    async def mute_member_slash(
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
        return await self.mute_member(
            ctx, member=member, duration_in_seconds=duration_in_seconds
        )

    @commands.command(name="unmute", aliases=["um"], description="Un-mute a person.")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.guild_only()
    async def unmute_member(
        self,
        ctx: Context,
        member: nextcord.Member,
    ):
        try:
            mute = await self.redis.get(f"mute-{member.id}-{ctx.guild.id}")
            if mute is None:
                return await ctx.send(
                    embed=warn_embed_ephemeral(f"{member.mention} isn't muted.")
                )

            res = self.config_coll.find_one({"_id": f"{ctx.guild.id}"})
            try:
                role = ctx.guild.get_role(int(res["muteRole"]))
            except KeyError:
                await ctx.send(
                    embed=success_embed_ephemeral(
                        f"{member.mention} has been un-muted."
                    )
                ),
                return await self.redis.delete(
                    f"mute-{member.id}-{ctx.guild.id}"
                )  # It doesn't exist anyway.

            if role is None:
                await ctx.send(
                    embed=success_embed_ephemeral(
                        f"{member.mention} has been un-muted."
                    )
                ),
                return await self.redis.delete(f"mute-{member.id}-{ctx.guild.id}")

            await self.redis.delete(f"mute-{member.id}-{ctx.guild.id}")
            await member.remove_roles(
                role,
                reason=f"Mute removed by {ctx.author}"
                if isinstance(ctx, Context)
                else f"Mute removed by {ctx.user}",
            )
            await ctx.send(
                embed=success_embed_ephemeral(f"{member.mention} has been un-muted.")
            )
        except Exception as e:
            await create_error_log(self, ctx, e)

    @nextcord.slash_command(name="unmute", description="Un-mute a person.")
    async def unmute_member_slash(
        self,
        ctx,
        member: nextcord.Member = SlashOption(
            name="person", description="Person to un-mute", required=True
        ),
    ):
        return await self.unmute_member(ctx, member=member)


def setup(bot):
    bot.add_cog(Mod(bot))
