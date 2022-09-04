from nextcord.ext import commands
import nextcord

class EventsUssy(commands.Cog):
    """The description for EventsUssy goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        if member.guild.id == 950592148816945163:
            try:
                ussy_role = member.guild.get_role(977704324840951878)

                await member.edit(nick=member.name[:3] + "ussy")
                await member.add_roles(ussy_role, reason="New member joined")
            except Exception as e:
                print(e)

def setup(bot):
    bot.add_cog(EventsUssy(bot))
