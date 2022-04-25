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


import string
import nextcord

from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from nextcord.ext.commands import Context
from utils import default
from utils.default import translate as _
from utils.data import create_error_log


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="who", aliases=["userinfo", "w", "ui"], description=_("cmds.who.desc")
    )
    async def get_user_info(self, ctx, member: nextcord.Member = None):

        if isinstance(ctx, Interaction):
            member = member or ctx.user
        else:
            member = member or ctx.author
        embed = nextcord.Embed(colour=member.color, description=f"{member.mention}")
        embed.set_author(name=str(member), icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(
            name="Dates",
            value=f":door: **Joined**: <t:{int(member.joined_at.timestamp())}>\n"
            + f":hammer_pick: **Created**: <t:{int(member.created_at.timestamp())}>",
        )
        embed.add_field(
            name="Roles",
            value=f", ".join([r.mention for r in member.roles[::-1]]),
            inline=False,
        )
        embed.set_footer(text="ID: " + str(member.id))
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="who", description=_("cmds.who.desc"))
    async def get_user_info_slash(
        self,
        ctx,
        member: nextcord.Member = nextcord.SlashOption(
            "user", description="The user you want to get", required=False
        ),
    ):
        await self.get_user_info(ctx, member=member)

    @commands.command(name="xkcd", description=_("cmds.xkcd.desc"))
    async def get_xkcd(self, ctx, *, comic: int = None):
        if comic:
            try:
                json = await default.fetch_xkcd_comic(comic=comic)
            except Exception:
                await ctx.reply(_("cmds.xkcd.could_not_find_comic"))
                return
        else:
            json = await default.fetch_xkcd_comic()
        embed = default.branded_embed(
            title=f"{json['safe_title']}",
            description=f"{json['alt']}",
            color=0x909090,
            title_url=f"https://xkcd.com/{json['num']}",
        )
        embed.set_image(url=f"{json['img']}")
        embed.set_footer(
            text=_(
                "cmds.xkcd.posted_on", m=json["month"], d=json["day"], y=json["year"]
            )
        )
        if comic:
            embed.set_author(
                name=f"xkcd comic #{comic}", url=f"https://xkcd.com/{comic}"
            )
        else:
            embed.set_author(name=f"The latest xkcd comic", url=f"https://xkcd.com")
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="xkcd", description=_("cmds.xkcd.desc"))
    async def get_xkcd_slash(
        self,
        ctx,
        *,
        comic: int = SlashOption(
            "id", description=_("cmds.xkcd.options.id"), required=False
        ),
    ):
        await self.get_xkcd(ctx, comic=comic)

    @commands.command(name="avatar")
    async def get_user_avatar(self, ctx, *, member: nextcord.Member = None):
        try:
            if isinstance(ctx, Interaction):
                member = member or ctx.user
            else:
                member = member or ctx.author
            await ctx.send(member.avatar.with_format("webp").with_size(2048))
        except Exception as e:
            await create_error_log(self, ctx, e)

    @nextcord.slash_command(name="avatar", description=_("cmds.avatar.desc"))
    async def get_user_avatar_slash(
        self,
        ctx,
        *,
        member: nextcord.Member = SlashOption(
            name="member", description=_("cmds.avatar.options.user"), required=False
        ),
    ):
        await self.get_user_avatar(ctx, member=member)

    @commands.command(name="im", hidden=True)
    async def _im(self, ctx: Context, *, u: nextcord.Member = None):
        if u is None:
            return await ctx.send("Huh?")
        if u is ctx.author:
            return await ctx.send("Yes, we know.")
        await ctx.send(f"No, you're {ctx.author.name}!")

    @commands.command(name="emoji", aliases=["e", "emote", "jumbo"])
    async def _enlarge_emoji(
        self, ctx: commands.Context, emoji: nextcord.PartialEmoji | nextcord.Emoji
    ):
        return await ctx.send(emoji.url)


def setup(bot):
    bot.add_cog(Fun(bot))
