import nextcord
import os

from nextcord.ext import commands
from nextcord.ext.commands import Context, errors
from nextcord import Message
from nextcord.ext import commands
from utils import default
from utils.default import translate as _


class Snipe(commands.Cog):
    """Catch any previously deleted messages. :eyes:"""

    def __init__(self, bot):
        self.bot = bot
        self.snipe = Message

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        self.snipe = message

    @commands.command(name="snipe", description=_("cmds.snipe.desc"))
    @commands.cooldown(rate=1, per=4.0)
    async def get_last_deleted_message(self, ctx: Context):
        try:
            embed = default.branded_embed(
                description=str(self.snipe.content),
                color=nextcord.Embed.Empty,
                inline=True,
            )

            embed.set_author(
                name=str(self.snipe.author),
                icon_url=self.snipe.author.avatar,
            )
            embed.set_footer(text=f"#{str(self.snipe.channel.name)}")
            embed.timestamp = self.snipe.created_at

            return await ctx.send(embed=embed)
        except:
            return await ctx.send(_('cmds.snipe.failed'))

    @nextcord.slash_command(
        guild_ids=[os.environ.get('DISCORD_GUILDID')],
        name="snipe",
        description=_("cmds.snipe.desc"),
    )
    async def get_last_deleted_message_slashimpl(self, ctx: nextcord.Interaction):
        await self.get_last_deleted_message(ctx)



def setup(bot):
    bot.add_cog(Snipe(bot))
