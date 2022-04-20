import nextcord
import pymongo
import os

from nextcord import Message
from nextcord.ext import commands
from pytz import timezone
from utils import default, embed as eutil


class Messages(commands.Cog):
    """Message event handlers."""

    def __init__(self, bot):
        self.bot = bot
        self.cluster = pymongo.MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.message_log_coll = self.db["guild-configs"]

    @commands.Cog.listener()
    async def on_message_delete(self, message: Message):
        try:
            res = self.message_log_coll.find_one({"_id": f"{message.guild.id}"})
            cid = int(res["messageLog"])
        except:
            return

        log = self.bot.get_channel(cid)
        tz = timezone("EST")

        if message.author.id == self.bot.user.id:
            return

        if message.author.bot:
            return

        embed: nextcord.Embed = default.branded_embed(
            title=f"Message deleted",
            description=f"<#{message.to_reference().channel_id}>",
            color=eutil.failed_embed_color,
            inline=True,
        )
        embed.add_field(name="Content", value=f"{message.content}") if message.content else None
        embed.set_author(name=message.author, icon_url=message.author.avatar)
        # embed.set_image(url=message.attachments[0].proxy_url) if message.attachments else None
        embed.timestamp = message.created_at.now(tz=tz)
        embed.set_footer(
            text=f"Message ID: {message.id}" + f"\nAuthor ID: {message.author.id}\n"
        )

        await log.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, message: Message, new_message: Message):
        try:
            if message.content == new_message.content:
                return

            res = self.message_log_coll.find_one({"_id": f"{message.guild.id}"})
            cid = int(res["messageLog"])
            log = self.bot.get_channel(cid)
        
            tz = timezone("EST")

            if message.author.id == self.bot.user.id:
                return

            if message.author.bot:
                return

            embed: nextcord.Embed = default.branded_embed(
                title=f"Message edited",
                description=f"<#{message.to_reference().channel_id}> ([Go to message]({message.to_reference().jump_url}))",
                color=eutil.warn_embed_color,
                inline=True,
            )
            embed.add_field(name="Before", value=f"{message.content}", inline=False)
            embed.add_field(name="After", value=f"{new_message.content}", inline=False)
            embed.set_author(name=message.author, icon_url=message.author.avatar)
            embed.timestamp = message.created_at.now(tz=tz)
            embed.set_footer(text=f"Author ID: {message.author.id}\n")

            await log.send(embed=embed)
        except:
            return


def setup(bot):
    bot.add_cog(Messages(bot))
