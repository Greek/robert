import nextcord
import os

from nextcord.ext import commands

from pymongo import MongoClient


class EventsWelcomeListener(commands.Cog):
    """Member welcome listener"""

    def __init__(self, bot):
        self.bot = bot

        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.database = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.database["guild-configs"]

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        try:
            res = self.config_coll.find_one({"_id": member.guild.id})
            parsed_message = (
                res["welcomeGreeting"]
                .replace("@everyone", "everyone")
                .replace("@here", "here")
                .replace("{mention}", f"{member.mention}")
                .replace("{name}", f"{member.name}")
                .replace("{tag}", f"{member.name}#{member.discriminator}")
                .replace("{user.mention}", f"{member.mention}")
                .replace("{user.name}", f"{member.name}")
                .replace("{user.tag}", f"{member.name}#{member.discriminator}")
            )
            channel = self.bot.get_channel(res["welcomeChannel"])

            await channel.send(parsed_message)
        except nextcord.errors.Forbidden:
            return


def setup(bot):
    bot.add_cog(EventsWelcomeListener(bot))
