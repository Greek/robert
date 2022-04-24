import nextcord

from nextcord.ext import commands

class Filter(commands.Cog):
    """The description for Filter goes here."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def check_message_content(self, message: nextcord.Message):
        filtered_words = ["testing", "wow1"] 
        msg_split = message.content.split()

        for word in msg_split:            # return
            if word in filtered_words:
                try:
                    await message.delete()
                except:
                    return

    # @commands.command(name="filter")
    # async def _filter(self, ctx: commands.Context):
    #     # if ctx.invoked_subcommand is None:
    #     #     return await ctx.send_help(str(ctx.command))
    #     pass

    # @_filter.command(name="add")
    # async def _filter_add(self, ctx: commands.Context, word: str):
    #     pass

def setup(bot):
    bot.add_cog(Filter(bot))
