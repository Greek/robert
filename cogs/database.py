from nextcord.ext import commands
import nextcord

class Database(commands.Cog):
    """The description for Database goes here."""

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Database(bot))
