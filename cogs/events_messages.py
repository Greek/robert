import nextcord

from nextcord.ext import commands

from pytz import timezone

from utils import default, embed as eutil
from utils.data import Bot


class Messages(commands.Cog):
    """Message event handlers (primarily logging)"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message: nextcord.Message):
        try:
            res = self.bot.mguild_config.find_one({"_id": message.guild.id})
            cid = res["messageLog"]
        except:
            return

        log = self.bot.get_channel(cid)
        timezone_est = timezone("EST")

        try:
            if message.channel.id in res["messageLogIgnore"]:
                return
        except:
            pass

        if message.author.id == self.bot.user.id:
            return

        if message.author.bot:
            return

        embed: nextcord.Embed = default.branded_embed(
            title="Message deleted",
            description=f"<#{message.to_reference().channel_id}>",
            color=eutil.failed_embed_color,
            inline=True,
        )
        embed.add_field(
            name="Content", value=f"{message.content}"
        ) if message.content else None
        embed.set_author(
            name=message.author,
            icon_url=message.author.avatar
            if message.author.avatar
            else "https://canary.discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png",
        )
        # embed.set_image(url=message.attachments[0].proxy_url) if message.attachments else None
        embed.timestamp = message.created_at.now(tz=timezone_est)
        embed.set_footer(
            text=f"Message ID: {message.id}" + f"\nAuthor ID: {message.author.id}\n"
        )

        await log.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(
        self, message: nextcord.Message, new_message: nextcord.Message
    ):
        try:
            if message.content == new_message.content:
                return

            res = self.bot.mguild_config.find_one({"_id": message.guild.id})
            cid = res["messageLog"]
            log = self.bot.get_channel(cid)

            timezone_est = timezone("EST")

            try:
                if message.channel.id in res["messageLogIgnore"]:
                    return
            except:
                pass

            if message.author.id == self.bot.user.id:
                return

            if message.author.bot:
                return

            embed: nextcord.Embed = default.branded_embed(
                title="Message edited",
                description=f"<#{message.to_reference().channel_id}> ([Go to message]({message.to_reference().jump_url}))",
                color=eutil.warn_embed_color,
                inline=True,
            )
            embed.add_field(name="Before", value=f"{message.content}", inline=False)
            embed.add_field(name="After", value=f"{new_message.content}", inline=False)
            embed.set_author(
                name=message.author,
                icon_url=message.author.avatar
                if message.author.avatar
                else "https://canary.discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png",
            )
            embed.timestamp = message.created_at.now(tz=timezone_est)
            embed.set_footer(text=f"Author ID: {message.author.id}\n")

            await log.send(embed=embed)
        except Exception as error:
            print(error)


def setup(bot):
    bot.add_cog(Messages(bot))
