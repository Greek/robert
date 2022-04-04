import nextcord
import os

from nextcord.ext import commands
from nextcord.ext.commands import Context, errors
from nextcord import Message
from nextcord.ext import commands
from utils import default, perms
from utils.default import translate as _


class Snipe(commands.Cog):
    """Catch any previously deleted messages. :eyes:"""

    def __init__(self, bot):
        self.bot = bot
        self.snipe_author = {}
        self.snipe_author_avatar = {}
        self.snipe_content = {}
        self.snipe_channel = {}
        self.snipe_message = {}

    snipe_author = {}
    snipe_author_avatar = {}
    snipe_content = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        self.snipe_author[message.channel.id] = message.author
        self.snipe_author_avatar[message.channel.id] = message.author.avatar
        self.snipe_content[message.channel.id] = message.content

    @commands.check(perms.only_owner)
    @commands.command(name="snipe", aliases=['s'], description=_("cmds.snipe.desc"))
    @commands.cooldown(rate=1, per=4.0)
    async def get_last_deleted_message(self, ctx: Context):
        try:
            snipe_author = self.snipe_author[ctx.channel.id]
            snipe_avatar = self.snipe_author_avatar[ctx.channel.id]
            snipe_content = self.snipe_content[ctx.channel.id]

            embed = default.branded_embed(
                description=str(snipe_content),
                color=nextcord.Embed.Empty,
                inline=True,
            )

            embed.set_author(
                name=str(snipe_author),
                icon_url=snipe_author_avatar,
            )
            embed.set_footer(text=f"#{str(self.snipe_message.channel.name)}")
            embed.timestamp = self.snipe_message.created_at

            print(snipe)
            return await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            # return await ctx.send(_('cmds.snipe.failed'))

    @nextcord.slash_command(
        guild_ids=[os.environ.get('DISCORD_GUILDID')],
        name="snipe",
        description=_("cmds.snipe.desc"),
    )
    async def get_last_deleted_message_slashimpl(self, ctx: nextcord.Interaction):
        await self.get_last_deleted_message(ctx)



def setup(bot):
    bot.add_cog(Snipe(bot))
