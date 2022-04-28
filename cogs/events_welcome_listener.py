import nextcord
import os

from nextcord import Member
from nextcord.ext import commands
from nextcord.ext.commands import Context
from pymongo import MongoClient


class EventsWelcomeListener(commands.Cog):
    """The description for EventsWelcomeListener goes here."""

    def __init__(self, bot):
        self.bot = bot

        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.db["guild-configs"]

    @commands.Cog.listener()
    async def on_member_join(self, member: Member):
        try:
            res = self.config_coll.find_one({"_id": f"{member.guild.id}"})
            parsed_message = (
                str(res["welcomeGreeting"])
                .replace("@everyone", "everyone")
                .replace("@here", "here")
                .replace("{mention}", f"{member.mention}")
                .replace("{name}", f"{member.name}")
                .replace("{tag}", f"{member.name}#{member.discriminator}")
                .replace("{user.mention}", f"{member.mention}")
                .replace("{user.name}", f"{member.name}")
                .replace("{user.tag}", f"{member.name}#{member.discriminator}")
            )
            channel = self.bot.get_channel(int(res["welcomeChannel"]))

            await channel.send(parsed_message)
        except Exception as e:
            return

def setup(bot):
    bot.add_cog(EventsWelcomeListener(bot))
