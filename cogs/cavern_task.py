import nextcord

from nextcord import AutoShardedClient
from nextcord.ext import tasks, commands

class CavernTask(commands.Cog):
    def __init__(self, bot: AutoShardedClient):
        self.bot = bot
        self.index = 0
        self.printer.start()    

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(minutes=3)
    async def printer(self):
        try:
            channel = self.bot.get_channel(960209486319079455)
            return await channel.send("Vanity chat")
        except:
            self.printer.cancel() # Kill the task, there's no point if we fail.

    @printer.before_loop
    async def before_load(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(CavernTask(bot))
