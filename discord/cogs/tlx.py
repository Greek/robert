import nextcord
import aiohttp
import os

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

        url = "http://toilet.apap04.com/tlx/"
        endpoint_url = "http://toilet.apap04.com/api/tlx/"

        async with aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {os.environ.get('TOILET_API_TOKEN')}"}
        ) as session:
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
                        f"Report available [here]({url}{data})"
                    )
                )


def setup(bot):
    bot.add_cog(Tlx(bot))
