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
        self.snipe_message = {}
        self.snipe_message_old = {}
        self.snipe_message_new = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        self.snipe_message[message.channel.id] = message

    @commands.Cog.listener()
    async def on_message_edit(self, message: Message, new_message: Message):
        self.snipe_message_old[message.channel.id] = message
        self.snipe_message_new[message.channel.id] = new_message

    @commands.command(name="snipe", aliases=["s"], description=_("cmds.snipe.desc"))
    async def get_last_deleted_message(self, ctx: Context):
        try:
            embed = default.branded_embed(
                description=str(self.snipe_message[ctx.channel.id].content)
                if self.snipe_message[ctx.channel.id].content
                else "",
                color=nextcord.Embed.Empty,
                inline=True,
            )

            embed.set_author(
                name=str(self.snipe_message[ctx.channel.id].author),
                icon_url=str(self.snipe_message[ctx.channel.id].author.avatar.url),
            )
            embed.set_image(
                url=self.snipe_message[ctx.channel.id].attachments[0].proxy_url
            ) if self.snipe_message[ctx.channel.id].attachments else None
            embed.set_footer(
                text=f"#{str(self.snipe_message[ctx.channel.id].channel.name)}"
            )
            embed.timestamp = self.snipe_message[ctx.channel.id].created_at

            return await ctx.send(embed=embed)
        except KeyError:
            return await ctx.send(_("cmds.snipe.failed"))

    @commands.command(
        name="editsnipe", aliases=["es"], description=_("cmds.snipe.desc")
    )
    async def get_last_edited_message(self, ctx: Context):
        try:
            embed = default.branded_embed(
                description=str(self.snipe_message_old[ctx.channel.id].content),
                color=nextcord.Embed.Empty,
                inline=True,
            )

            embed.set_author(
                name=str(self.snipe_message_old[ctx.channel.id].author),
                icon_url=str(self.snipe_message_old[ctx.channel.id].author.avatar.url),
            )
            embed.set_footer(
                text=f"#{str(self.snipe_message_old[ctx.channel.id].channel.name)}"
            )
            embed.timestamp = self.snipe_message_old[ctx.channel.id].created_at

            return await ctx.send(embed=embed)
        except KeyError:
            return await ctx.send(_("cmds.snipe.failed"))

    @nextcord.slash_command(
        name="snipe",
        description=_("cmds.snipe.desc"),
    )
    async def get_last_deleted_message_slashimpl(self, ctx: nextcord.Interaction):
        await self.get_last_deleted_message(ctx)


def setup(bot):
    bot.add_cog(Snipe(bot))
