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

from discord import Interaction
import nextcord

from utils.default import translate as _
from utils import default, embed

owners = default.get("config.json").owners


def only_owner(ctx):
    return ctx.author.id in owners


async def check_priv(ctx, member):
    """Custom (weird) way to check permissions when handling moderation commands"""
    try:
        # Self checks
        if member.id == ctx.author.id:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.self", action=ctx.command.name)
                )
            )
    
        if member.id == ctx.bot.user.id:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.me", action=ctx.command.name)
                )
            )

        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id:
            return False

        # Now permission check
        # if member.id in owners:
        #     if ctx.author.id not in owners:
        #         return await ctx.send(f"I can't {ctx.command.name} my creator ;-;")
        #     else:
        #         pass
        if member.id == ctx.guild.owner.id:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.owner", action=ctx.command.name)
                )
            )
        if ctx.author.top_role == member.top_role:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.same_perms", action=ctx.command.name)
                )
            )
        if ctx.author.top_role < member.top_role:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.higher_than_self")
                )
            )
    except Exception:
        pass

async def check_priv_interaction(ctx: Interaction, member):
    """Custom (weird) way to check permissions when handling moderation commands"""
    try:
        # Self checks
        if member.id == ctx.user.id:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.self", action=ctx.application_command.name)
                )
            )

        # Check if user bypasses
        if ctx.user.id == ctx.guild.owner.id:
            return False

        # Now permission check
        # if member.id in owners:
        #     if ctx.author.id not in owners:
        #         return await ctx.send(f"I can't {ctx.command.name} my creator ;-;")
        #     else:
        #         pass

        if member.id == ctx.guild.owner.id:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.owner", action=ctx.application_command.name)
                )
            )
        if ctx.user.top_role == member.top_role:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.same_perms", action=ctx.application_command.name)
                )
            )
        if ctx.user.top_role < member.top_role:
            return await ctx.send(
                embed=embed.failed_embed_ephemeral(
                    _("events.priv_checks.higher_than_self")
                )
            )
    except Exception as e:
        pass


def can_react(ctx):
    return (
        isinstance(ctx.channel, nextcord.DMChannel)
        or ctx.channel.permissions_for(ctx.guild.me).add_reactions
    )
