import nextcord
import json

from nextcord import Message
from nextcord.ext import commands
from pytz import timezone
from utils import default

class Messages(commands.Cog):
    """Message event handlers."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        f = open("config.json")
        config = json.load(f)
        cid = int(954634303852122112)

        log = self.bot.get_channel(cid)
        tz = timezone("EST")

        if message.author.id == self.bot.user.id:
            return

        embed: nextcord.Embed = default.branded_embed(
            title=f"Message deleted",
            description=f"<#{message.to_reference().channel_id}>",
            color="red",
            inline=True,
        )
        embed.add_field(name="Content", value=f"{message.content}")
        embed.set_author(name=message.author, icon_url=message.author.avatar)
        embed.timestamp = message.created_at.now(tz=tz)
        embed.set_footer(
            text=f"Message ID: {message.id}" + f"\nAuthor ID: {message.author.id}\n"
        )

        self.message_snipe[message.channel.id] = {
            "message": message.content,
            "author": message.author,
            "author_icon_url": message.author.avatar,
            "date": message.created_at.now(tz=tz).strftime("%I:%M %p"),
        }
        await log.send(embed=embed)


def setup(bot):
    bot.add_cog(Messages(bot))
