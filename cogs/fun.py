# -*- coding: utf-8 -*-

from discord.ext import commands
import discord

class Fun(commands.Cog):
    """The description for Fun goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shitty-pun")
    async def get_shitty_pun(self, ctx):
        await ctx.send("you know what **screams** insecure?\n\n\"http://\"!")

    @commands.command(name="user")
    async def get_user_info(self, ctx, member: discord.Member = None):
        """
        Get information for a specific user.
        """
        try:
            if member is None:
                member = ctx.author
            embed = discord.Embed(colour=member.color, description=f"{member.mention}")
            embed.set_author(name=str(member), icon_url=member.avatar_url)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Join date", value=f"{member.joined_at}"[0:10])
            embed.add_field(name="Creation date", value=f"{member.created_at}"[0:10])
            embed.add_field(name="Roles", value=", ".join([r.mention for r in member.roles]), inline=False)
            embed.set_footer(text="ID: " + str(member.id))
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)

def setup(bot):
    bot.add_cog(Fun(bot))
