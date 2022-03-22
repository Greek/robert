import nextcord

from nextcord.ext import commands
from nextcord.ext.commands import Context
from pytz import timezone
from nextcord import Message
from nextcord.ext import commands
from utils import default
from utils.default import translate as _


class Snipe(commands.Cog):
    """The description for Snipe goes here."""

    def __init__(self, bot):
        self.bot = bot
        self.snipe = Message

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        self.snipe = message

    @commands.command(name="snipe")
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

            return await ctx.reply(embed=embed, mention_author=False)
        except:
            return await ctx.send(_("cmds.snipe.failed"), mention_author=False)


def setup(bot):
    bot.add_cog(Snipe(bot))
