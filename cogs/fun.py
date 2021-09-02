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
from discord.ext import commands
import discord
import requests

from utils import default
from utils.default import translate as _


class Fun(commands.Cog):
    """The description for Fun goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shitty-pun")
    async def get_shitty_pun(self, ctx, asd: int):
        await ctx.send("you know what **screams** insecure?\n\n\"http://\"!")

    @commands.command(name="who", description=_("cmds.who.desc"))
    async def get_user_info(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(colour=member.color, description=f"{member.mention}")
        embed.set_author(name=str(member), icon_url=member.avatar)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Join date", value=f"{member.joined_at}"[0:10])
        embed.add_field(name="Creation date", value=f"{member.created_at}"[0:10])
        embed.add_field(name="Roles", value=", ".join([r.mention for r in member.roles[1:]]), inline=False)
        embed.set_footer(text="ID: " + str(member.id))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="xkcd", description=_("cmds.xkcd.desc"))
    async def get_random_xkcd(self, ctx, *, comic: int = None):
        if comic:
            try:
                r = requests.get(f"https://xkcd.com/{comic}/info.0.json")
                r.raise_for_status()
            except Exception:
                await ctx.reply(_("cmds.xkcd.could_not_find_comic"))
                return
        else:
            r = requests.get(f"https://xkcd.com/info.0.json")
        res = r.json()
        embed = default.branded_embed(title=f"{res['safe_title']}", description=f"{res['alt']}", color=0x909090,
                                      title_url=f"https://xkcd.com/{res['num']}")
        embed.set_image(url=f"{res['img']}")
        embed.set_footer(text=_("cmds.xkcd.posted_on", m=res['month'], d=res['day'], y=res['year']))
        if comic:
            embed.set_author(name=f"xkcd comic #{comic}", url=f"https://xkcd.com/{comic}")
        else:
            embed.set_author(name=f"the latest xkcd comic", url=f"https://xkcd.com")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="xkcd", description=_("cmds.xkcd.desc"))
    async def get_random_xkcd(self, ctx, *, comic: int = None):
        if comic:
            try:
                r = requests.get(f"https://xkcd.com/{comic}/info.0.json")
                r.raise_for_status()
            except Exception:
                await ctx.reply(_("cmds.xkcd.could_not_find_comic"))
                return
        else:
            r = requests.get(f"https://xkcd.com/info.0.json")
        res = r.json()
        embed = default.branded_embed(title=f"{res['safe_title']}", description=f"{res['alt']}", color=0x909090,
                                      title_url=f"https://xkcd.com/{res['num']}")
        embed.set_image(url=f"{res['img']}")
        embed.set_footer(text=_("cmds.xkcd.posted_on", m=res['month'], d=res['day'], y=res['year']))
        if comic:
            embed.set_author(name=f"xkcd comic #{comic}", url=f"https://xkcd.com/{comic}")
        else:
            embed.set_author(name=f"the latest xkcd comic", url=f"https://xkcd.com")
        await ctx.send(embed=embed)

    @commands.command(name="8ball", description=_("cmds.8ball.desc"))
    async def random_response_generator(self, ctx):  # i know, lame name
        pass

    # @commands.command(name="avatar")
    # async def get_user_avatar(self, ctx):
    #     try:
    #         await ctx.send(ctx.guild.icon.with_format("png").with_size(2048))
    #     except Exception as e:
    #         await ctx.send(default.traceback_maker(err=e))


def setup(bot):
    bot.add_cog(Fun(bot))
