import asyncio
from contextvars import Context
from discord import Interaction
import nextcord
import random
import time
import os

from pymongo import MongoClient
from redis.asyncio import Redis
from nextcord.ext import commands, tasks
from pytimeparse.timeparse import timeparse

from utils.data import Bot, create_error_log
from utils.embed import success_embed_ephemeral, warn_embed_ephemeral
from utils.default import translate as _

from dotenv import dotenv_values, load_dotenv

dot_cfg = dotenv_values(".env")
load_dotenv(".env")


class Giveaways(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.redis: Redis = Redis.from_url(
            url=os.environ.get("REDIS_URL"), decode_responses=True
        )
        self.pubsub = self.redis.pubsub()

        self.subscribe_expiry_handler.start()
        self.listen_messages.start()

    def cog_unload(self):
        self.subscribe_expiry_handler.cancel()
        self.listen_messages.cancel()
        self.disconnect_redis()

    async def disconenct_redis(self):
        await self.redis.close()

    async def expiry_handler(self, msg) -> None:
        if msg["data"].startswith("giveaway:"):
            try:
                # giveaway:guild.id:channel:id:msg.id:prize
                data = msg["data"].split(":")

                guild = self.bot.get_guild(int(data[1]))
                channel: nextcord.TextChannel = guild.get_channel(int(data[2]))
                message = await channel.fetch_message(int(data[3]))

                reactions = await message.reactions[0].users().flatten()

                new_message: nextcord.Message = await channel.send(
                    f"Congratulations {random.choice(reactions).mention}, you won: {data[4]}"
                )
                await message.edit(
                    embed=success_embed_ephemeral(
                        f"Giveaway has ended, see results [here]({new_message.to_reference().jump_url})"
                    )
                )
            except Exception as e:
                ctx = self.bot
                await create_error_log(self, ctx, e)

    @tasks.loop(count=1)
    async def subscribe_expiry_handler(self):
        # Subscribe to all "expired" keyevents thru pubsub and handle them.
        await self.pubsub.psubscribe(**{"__keyevent@0__:expired": self.expiry_handler})

    @tasks.loop(seconds=0.01)
    async def listen_messages(self):
        message = await self.pubsub.get_message()
        if message:
            print(f"[Giveaways] Watching expired giveaways")
        else:
            pass

    @subscribe_expiry_handler.before_loop
    async def subscribe_redis_before(self):
        await self.bot.wait_until_ready()

    @listen_messages.before_loop
    async def listen_messages_before(self):
        await self.bot.wait_until_ready()
        await self.subscribe_expiry_handler()

    @commands.has_permissions(manage_guild=True)
    @commands.group(name="giveaway", aliases=["gw"])
    async def _giveaway(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
        pass

    @commands.has_permissions(manage_guild=True)
    @_giveaway.command(
        name="create", description="Create a new giveaway!", aliases=["c"]
    )
    async def _create(self, ctx: commands.Context):
        def author_check(author):
            def inner_check(message):
                return message.author == author

            return inner_check

        def check(message):
            return message.author == ctx.author

        res = self.bot.mguild_config.find_one({"_id": ctx.guild.id})
        try:
            res["giveawayChannel"]
        except KeyError:
            return await ctx.send("Please provide a giveaway channel in the config!")

        await ctx.send(
            "Hey! This is the creation flow for a new giveaway. Would you like to continue? (yes/no)"
        )
        msg = await self.bot.wait_for("message", check=check, timeout=30)
        if msg.content == "yes".lower():
            await ctx.send("What are you giving away?")
            try:
                gw_prize = await self.bot.wait_for("message", check=check, timeout=30)
                if len(gw_prize.content) > 48:
                    return await ctx.send("Please provide a shorter giveaway prize.")
            except asyncio.TimeoutError:
                return await ctx.send("You took too long! Action cancelled.")

            # TODO(greek): cba to do this. host seperate giveaways for multiple winners LOL
            # await ctx.send("How many winners do you want?")
            # try:
            #     gw_winner_count: nextcord.Message = await self.bot.wait_for(
            #         "message", check=check, timeout=30
            #     )
            # except asyncio.TimeoutError:
            #     return await ctx.send("You took too long! Action cancelled.")

            await ctx.send("When would you like this to end?")
            try:
                gw_duration = await self.bot.wait_for(
                    "message", check=check, timeout=30
                )
                parsed_gw_duration = timeparse(f"{gw_duration.content}")
            except asyncio.TimeoutError:
                return await ctx.send("You took too long! Action cancelled.")
            dedicated_channel: nextcord.TextChannel = self.bot.get_channel(
                int(res["giveawayChannel"])
            )

            try:
                if parsed_gw_duration is None:
                    return await ctx.send(
                        "Please re-run the command with a valid time. (30s, 2h, 3d, etc..)"
                    )
                giveaway_embed = (
                    nextcord.Embed(
                        title=f"Giveaway: {gw_prize.content}",
                        description=f"React with :tada: to enter this giveaway!\nThis giveaway will end <t:{parsed_gw_duration + int(time.time())}:R>.",
                        color=nextcord.Embed.Empty,
                    ).set_author(
                        name=ctx.author.name,
                        icon_url=ctx.author.avatar
                        if ctx.author.avatar
                        else "https://canary.discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png",
                    )
                    # .set_footer(text=f"")
                )
                msg = await dedicated_channel.send(embed=giveaway_embed)
                await msg.add_reaction("🎉")
                await asyncio.sleep(2)
                return await self.redis.setex(
                    f"giveaway:{ctx.guild.id}:{msg.channel.id}:{msg.id}:{gw_prize.content}",
                    parsed_gw_duration,
                    "Giveaway",
                )

            except Exception as e:
                await create_error_log(self, ctx, e)
        else:
            return await ctx.send("As you wish, captain.")

    # @nextcord.slash_command(name="giveaway")
    # async def _slash_giveaway(self, interaction: nextcord.Interaction):
    #     pass

    # @_slash_giveaway.subcommand(name="create", description="Create a new giveaway!")
    # async def _slash_giveaway_create(self, interaction: Interaction):
    #     return await self._create(context=self)


def setup(bot):
    bot.add_cog(Giveaways(bot))
