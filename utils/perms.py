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
