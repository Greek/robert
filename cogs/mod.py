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

import nextcord
import os

from nextcord import Client
from nextcord.ext import commands, tasks
from nextcord.ext.commands import Context
from nextcord.utils import get
from redis.asyncio import Redis
from utils import default, perms
from utils.embed import success_embed_ephemeral
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
        self.redis = Redis.from_url(
            url=os.environ.get('REDIS_URL')
        )
        self.pubsub = self.redis.pubsub()

        self.subscribe_expiry_handler.start()
        # self.listen_messages.start()

    def cog_unload(self):
        self.subscribe_expiry_handler.cancel()
        # self.listen_messages.cancel()

    async def expiry_handler(self, msg) -> None:
        decoded = msg["data"].decode("utf-8")
        split = decoded.split("-")
        guild = self.bot.get_guild(int(split[2]))
        member = guild.get_member(int(split[1]))
        role = get(guild.roles, name='ban perms')

        await member.remove_roles(role, reason="Mute expired. Un-muting.")

    @tasks.loop(count=1)
    async def subscribe_expiry_handler(self):
        # Subscribe to all "expired" keyevents thru pubsub and handle them.
        await self.pubsub.psubscribe(**{"__keyevent@0__:expired": self.expiry_handler})

    @tasks.loop(seconds=0.01)
    async def listen_messages(self):
        message = await self.pubsub.get_message()
        if message:
            print(message)
        else:
            pass

    @subscribe_expiry_handler.before_loop
    async def subscribe_redis_before(self):
        await self.bot.wait_until_ready()

    @listen_messages.before_loop
    async def listen_messages_before(self):
        await self.bot.wait_until_ready()
        await self.subscribe_expiry_handler()

    @commands.command(name="kick", description=_("cmds.kick.desc"))
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick_user(self, ctx, member: nextcord.Member, *, reason=None) -> None:
        if await perms.check_priv(ctx, member=member):
            return
        await member.kick(reason=default.responsible(ctx.author, reason))
        await ctx.reply(
            _("cmds.kick.res_noreason") if reason is None else _("cmds.kick.res_reason")
        )

    @commands.command(name="ban", description=_("cmds.ban.desc"))
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.guild_only()
    async def ban_user(self, ctx, member: MemberID, *, reason=None) -> None:
        caller = ctx.author if isinstance(ctx, Context) else ctx.user
        m = ctx.guild.get_member(member)
        if m is not None and await perms.check_priv(ctx, m):
            return

        await ctx.guild.ban(
            nextcord.Object(id=member), reason=default.responsible(caller, reason)
        )
        await ctx.reply(
            _("cmds.ban.res_noreason") if reason is None else _("cmds.ban.res_reason")
        )

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

    @commands.command(name="mute", aliases=["m"], description="No description.")
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    @commands.check(perms.only_owner)
    async def mute_member(
        self,
        ctx: Context,
        member: nextcord.Member,
        *,
        duration: int = None,
        reason: str = None,
    ):
        await self.redis.setex(f"mute-{member.id}-{ctx.guild.id}", duration, reason)
        await ctx.send("Sent")


def setup(bot):
    bot.add_cog(Mod(bot))
