import nextcord
from nextcord.ext import commands

from utils.data import Bot
from utils.default import translate as _


class Snipe(commands.Cog):
    """Catch any previously deleted messages. :eyes:"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.snipe_message = {}
        self.snipe_message_old = {}
        self.snipe_message_new = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: nextcord.Message):
        if message.author.bot:
            return
        self.snipe_message[message.channel.id] = message

    @commands.Cog.listener()
    async def on_message_edit(
        self, message: nextcord.Message, new_message: nextcord.Message
    ):
        if message.author.bot:
            return
        if message.content == new_message.content:
            return  # Return if the old content matches the new content.
            # With links, the msg content automatically updates to add
            # an embed to the message. This is why we return here.

        self.snipe_message_old[message.channel.id] = message
        self.snipe_message_new[message.channel.id] = new_message

    @commands.command(name="snipe", aliases=["s"], description=_("cmds.snipe.desc"))
    async def get_last_deleted_message(self, ctx: commands.Context):
        try:
            embed = nextcord.Embed(
                description=str(self.snipe_message[ctx.channel.id].content)
                if self.snipe_message[ctx.channel.id].content
                else "",
                color=None,
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
        except Exception as error:
            await self.bot.create_error_log(ctx, error)

    @commands.command(
        name="editsnipe", aliases=["es"], description=_("cmds.snipe.desc")
    )
    async def get_last_edited_message(self, ctx: commands.Context):
        try:
            embed = nextcord.Embed(
                description=str(self.snipe_message_old[ctx.channel.id].content),
                color=None,
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

    @nextcord.slash_command(
        name="editsnipe",
        description=_("cmds.snipe.desc_edit"),
    )
    async def get_last_edited_message_slashimpl(self, ctx: nextcord.Interaction):
        await self.get_last_edited_message(ctx)


def setup(bot):
    bot.add_cog(Snipe(bot))
