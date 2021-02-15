"""
Copyright (c) 2020 AlexFlipnote

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

from utils.default import get
import discord
from utils import default

owners = default.get("config.json").owners

def only_owner(ctx):
    return ctx.author.id in owners

async def check_priv(ctx, member):
    try:
        # Self checks
        if member == ctx.author:
            return await ctx.send(f"you can't {ctx.command.name} yourself.")
        if member.id == ctx.bot.user.id:
            return await ctx.send("YO WTF 😡😡😡😡")

        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id:
            return False

        # Now permission check
        if member.id == ctx.guild.owner.id:
            return await ctx.send(f"the owner has more power to {ctx.command.name} you")
        if ctx.author.top_role == member.top_role:
            return await ctx.send(f"can't {ctx.command.name} someone who has the same permissions as you")
        if ctx.author.top_role < member.top_role:
            return
    except Exception:
        pass

def can_react(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).add_reactions
