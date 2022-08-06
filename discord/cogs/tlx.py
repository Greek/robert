import asyncio
import nextcord
import aiohttp

from nextcord.ext import commands
from utils.data import Bot
from utils.embed import success_embed_ephemeral


class Tlx(commands.Cog):
    """Telemetry Logging eXaminer"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="tlx", desc="Create a tlx report for guild")
    async def _submit(self, ctx: commands.Context, *, guild: nextcord.Guild = None):
        if guild is None:
            guild = ctx.guild

        url = "http://localhost:3000/tlx/"
        endpoint_url = "http://localhost:3000/api/tlx/"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{endpoint_url}submit",
                data={
                    "name": ctx.guild.name,
                    "icon": ctx.guild.icon.url,
                    "owner": int(ctx.guild.owner.id),
                    "member_count": int(ctx.guild.member_count),
                },
            ) as res:
                data = await res.json()
                return await ctx.send(
                    embed=success_embed_ephemeral(
                        f"Report available [here]({url}{data['id']})"
                    )
                )


def setup(bot):
    bot.add_cog(Tlx(bot))
