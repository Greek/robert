import nextcord
from nextcord.ext import commands

from utils.data import Bot


class EventsLmaAutorole(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if member.guild.id != 1010560422283325590:
            return
        lma_role = member.guild.get_role(1040437387962093661)

        return await member.add_roles(lma_role)


def setup(bot):
    bot.add_cog(EventsLmaAutorole(bot))
