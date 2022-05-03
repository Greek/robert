import asyncio
import nextcord
import os

from redis.asyncio import Redis
from nextcord.ext import commands, tasks
from pymongo import MongoClient

from utils.data import create_error_log
from utils.embed import warn_embed_ephemeral
from utils.default import translate as _

from dotenv import dotenv_values, load_dotenv

dot_cfg = dotenv_values(".env")
load_dotenv(".env")


class Giveaways(commands.Cog):
    def __init__(self, bot: nextcord.Client):
        self.bot = bot
        self.redis: Redis = Redis.from_url(
            url=os.environ.get("REDIS_URL"), decode_responses=True
        )
        self.pubsub = self.redis.pubsub()

        self.cluster = MongoClient(os.environ.get("MONGO_DB"))
        self.db = self.cluster[os.environ.get("MONGO_NAME")]
        self.config_coll = self.db["guild-configs"]

        self.subscribe_expiry_handler.start()
        self.listen_messages.start()

    def cog_unload(self):
        self.subscribe_expiry_handler.cancel()
        self.listen_messages.cancel()

    async def expiry_handler(self, msg) -> None:
        if msg["data"].startswith("giveaway"):
            try:
                print("I Jus turned a 5 2 Üh 60")
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
            print(f"[Giveaways] Listening to expired keys through Pub/Sub")
        else:
            pass

    @subscribe_expiry_handler.before_loop
    async def subscribe_redis_before(self):
        await self.bot.wait_until_ready()

    @listen_messages.before_loop
    async def listen_messages_before(self):
        await self.bot.wait_until_ready()
        await self.subscribe_expiry_handler()

    @commands.group(name="giveaway")
    async def _giveaway(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)
        pass

    @_giveaway.command(name="create")
    async def _create(self, ctx: commands.Context):
        def author_check(author):
            def inner_check(message):
                return message.author == author

            return inner_check

        def check(message):
            return message.author == ctx.author and message.content

        res = self.config_coll.find_one({"_id": f"{ctx.guild.id}"})
        try:
            res["giveawayChannel"]
        except KeyError:
            return await ctx.send("Please provide a giveaway channel in the config!")

        await ctx.send(
            "Hey! This is the creation flow for a new giveaway. Would you like to continue?"
        )
        msg = await self.bot.wait_for("message", check=check, timeout=30)
        if msg.content == "yes":
            await ctx.send("What are you giving away?")
            try:
                prize = await self.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long! Action cancelled.")

            await ctx.send("How many winners do you want?")
            try:
                winner_count: nextcord.Message = await self.bot.wait_for(
                    "message", check=check, timeout=30
                )
            except asyncio.TimeoutError:
                return await ctx.send("You took too long! Action cancelled.")

            await ctx.send("When would you like this to end?")
            try:
                duration = await self.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                return await ctx.send("You took too long! Action cancelled.")

            dedicated_channel: nextcord.TextChannel = self.bot.get_channel(
                int(res["giveawayChannel"])
            )
            try:
                giveaway_embed = (
                    nextcord.Embed(
                        title=f"Giveaway: {prize.content}",
                        description="React with :tada: to enter this giveaway!\n\nEnding in x",
                        color=nextcord.Embed.Empty,
                    )
                    .set_author(
                        name=ctx.author.name,
                        icon_url=ctx.author.avatar
                        if ctx.author.avatar
                        else "https://canary.discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png",
                    )
                    .set_footer(text=f"{winner_count.content} winners")
                )
                msg = await dedicated_channel.send(embed=giveaway_embed)
                await msg.add_reaction("🎉")
            except Exception as e:
                await create_error_log(self, ctx, e)


def setup(bot):
    bot.add_cog(Giveaways(bot))
