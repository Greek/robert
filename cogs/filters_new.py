import os

import nextcord
from nextcord.ext import commands
from pytimeparse.timeparse import timeparse
from redis.asyncio import Redis

from cogs.mod import Mod
from utils.data import Bot
from utils.embed import success_embed_ephemeral, warn_embed_ephemeral

CHARS_TO_STRIP = '=+-!@#$%^&*()_?><:"\\{}'


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
        bot_guild = message.guild.get_member(self.bot.user.id)

        if message.author.bot:
            return

        if message.author.top_role > bot_guild.top_role:
            return

        if message.author.id == message.guild.owner.id:
            return

        for word in message.content.split(" "):
            word_result = await self.find_word_to_filter(
                message.guild.id, word.lower().strip(CHARS_TO_STRIP)
            )

            print(word_result)

            if word_result is not None:
                final_word = word_result.word.lower()
                await message.delete()

                if word_result.action is None:
                    return  # Do nothing
                if word_result.action == "NONE":
                    return  # Do nothing
                if word_result.action == "KICK":
                    return await message.author.kick(
                        reason=f"Filtered word found in message: {final_word}"
                    )
                if word_result.action == "BAN":
                    return await message.author.ban(
                        reason=f"Filtered word found in message: {final_word}"
                    )
                if word_result.action == "MUTE":
                    return await Mod.mute_member(
                        context=self,
                        ctx=message,
                        member=message.author,
                        duration="10",
                    )

    @commands.group(name="filter", hidden=True)
    @commands.has_permissions(manage_guild=True)
    async def _filter(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(str(ctx.command))

    @_filter.command(name="add", hidden=True)
    async def _filter_add(self, ctx: commands.Context, action: str, word: str):
        word_to_filter = word.lower().strip(CHARS_TO_STRIP)
        existing_word = await self.find_word_to_filter(ctx.guild.id, word_to_filter)
        action_list = ["delete", "mute", "kick", "ban"]

        if existing_word:
            return await ctx.send(
                embed=warn_embed_ephemeral("That word is already on the filter list.")
            )

        if action not in action_list:
            return await ctx.send(
                embed=warn_embed_ephemeral(
                    "That's not a valid action. Actions are: delete, mute, kick and ban."
                )
            )

        if action == "delete":
            await self.bot.prisma.word_filter.create(
                data={
                    "guild_id": ctx.guild.id,
                    "word": word_to_filter,
                },
            )
        elif action == "mute":
            await self.bot.prisma.word_filter.create(
                data={
                    "guild_id": ctx.guild.id,
                    "word": word_to_filter,
                    "action": "MUTE",
                },
            )
        elif action == "kick":
            await self.bot.prisma.word_filter.create(
                data={
                    "guild_id": ctx.guild.id,
                    "word": word_to_filter,
                    "action": "KICK",
                },
            )
        elif action == "ban":
            await self.bot.prisma.word_filter.create(
                data={
                    "guild_id": ctx.guild.id,
                    "word": word_to_filter,
                    "action": "BAN",
                },
            )

        return await ctx.send(
            embed=success_embed_ephemeral(f'Added "{word_to_filter}" to the filter')
        )

    @_filter.command(name="mute", hidden=True)
    async def _filter_add_mute(
        self, ctx: commands.Context, word: str, *, duration: str = None
    ):
        word_to_filter = word.lower().strip(CHARS_TO_STRIP)
        existing_word = await self.find_word_to_filter(ctx.guild.id, word_to_filter)

        if existing_word:
            return await ctx.send(
                embed=warn_embed_ephemeral("That word is already on the filter list.")
            )

        await self.bot.prisma.word_filter.create(
            data={
                "guild_id": ctx.guild.id,
                "word": word_to_filter,
                "action": "MUTE",
                "duration": timeparse(duration),
            },
        )

        return await ctx.send(
            embed=success_embed_ephemeral(
                f'Added "{word_to_filter}" to the mute filter, which I will mute {f"for {duration}." if duration is not None else "forever."}'
            )
        )


def setup(bot):
    bot.add_cog(FiltersNew(bot))
