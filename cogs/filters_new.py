import os
import nextcord


from nextcord.ext import commands
from cogs.mod import Mod
from utils.data import Bot
from redis.asyncio import Redis


class FiltersNew(commands.Cog):
    """Word filter system"""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.redis: Redis = Redis.from_url(
            url=os.environ.get("REDIS_URL"), decode_responses=True
        )

    async def get_filter_list(self, guild_id):
        result = await self.bot.prisma.word_filter.find_many(
            where={"guild_id": guild_id}
        )

        return result

    async def find_word_to_filter(self, guild_id, word):
        result = await self.bot.prisma.word_filter.find_first(
            where={"guild_id": guild_id, "word": word}
        )

        return result

    @commands.Cog.listener(name="on_message")
    async def check_message_content(self, message: nextcord.Message):
        for word in message.content.split(" "):
            word_result = await self.find_word_to_filter(message.guild.id, word)

            if word_result is not None:
                await message.delete()

                if word_result.action is None:
                    return  # Do nothing
                if word_result.action == "NONE":
                    return  # Do nothing
                if word_result.action == "KICK":
                    return await message.author.kick(
                        reason=f"Filtered word found in message: {word_result.word}"
                    )
                if word_result.action == "BAN":
                    return await message.author.ban(
                        reason=f"Filtered word found in message: {word_result.word}"
                    )
                if word_result.action == "MUTE":
                    return await Mod.mute_member(
                        context=self,
                        ctx=message,
                        member=message.author,
                        duration="",
                    )

    @commands.group(name="filter", hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def _filter(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(str(ctx.command))

    @_filter.group(name="add", hidden=True)
    async def _filter_add(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(str(ctx.command))


def setup(bot):
    bot.add_cog(FiltersNew(bot))
