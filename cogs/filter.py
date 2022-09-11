import asyncio

import nextcord

from nextcord.ext import commands
from utils.data import Bot

from utils.default import translate as _
from utils.embed import success_embed_ephemeral, warn_embed_ephemeral


class Filter(commands.Cog):
    """Message filters."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def check_message_content(self, message: nextcord.Message):
        try:
            try:
                filtered_words = await self.bot.mguild_config.find_one(
                    {"_id": message.guild.id}
                )
            except:
                return

            msg_split = message.content.lower().split()

            try:
                link_filtering = filtered_words["linksDelete"]
            except:
                pass

            try:
                mute_list = filtered_words["muteWordList"]
            except:
                pass

            try:
                delete_list = filtered_words["deleteWordList"]
            except:
                delete_list = None

            try:
                ban_list = filtered_words["banWordList"]
            except:
                ban_list = None

            try:
                exemption_list = filtered_words["exemptionFilterList"]
            except:
                pass

            if message.author.id == message.guild.owner_id:
                return

            # if message.author.top_role > message.guild.me.top_role:
            #     return

            for word in msg_split:
                if message.author.bot:
                    return

                if ban_list:
                    if word in ban_list:
                        try:
                            await message.delete()
                            await message.author.ban(
                                reason=f"Detected disallowed phrase: {word}",
                                delete_message_days=0,
                            )
                        except Exception as e:
                            print(e)

                if delete_list:
                    if word in delete_list:
                        try:
                            await message.delete()
                        except Exception as error:
                            print(error)

                try:
                    if link_filtering:
                        if word.startswith(
                            "http" or "https" or "https://" or "http://" or "www"
                        ) or word.endswith(
                            ".com" or ".net" or ".org" or ".gg" or ".xxx"
                        ):
                            await message.delete()
                except:
                    pass

        except Exception as e:
            print(e)

    @commands.group(name="filter")
    @commands.has_permissions(manage_guild=True)
    async def _filter(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(str(ctx.command))

    @_filter.group(name="add")
    async def _filter_add(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send_help(str(ctx.command))

    @_filter_add.command(name="delete", description=_("cmds.filter.desc"))
    async def _filter_add_delete(self, ctx: commands.Context, *, word: str):
        word_list = await self.bot.mguild_config.find_one({"_id": ctx.guild.id})

        try:
            if word in word_list["deleteWordList"]:
                return await ctx.send(
                    embed=warn_embed_ephemeral(f"That word is already on the list.")
                )
        except:
            pass  # There is nothing to check.

        await self.bot.mguild_config.find_one_and_update(
            {"_id": ctx.guild.id},
            {"$push": {"deleteWordList": f"{word}"}},
            upsert=True,
        )

        return await ctx.send(
            embed=success_embed_ephemeral(f'Added "{word}" to the delete filter.')
        )

    @_filter_add.command(name="ban", description=_("cmds.filter.desc_ban"))
    async def _filter_add_ban(self, ctx: commands.Context, *, word: str):
        word_list = await self.bot.mguild_config.find_one({"_id": ctx.guild.id})

        try:
            if word in word_list["banWordList"]:
                return await ctx.send(
                    embed=warn_embed_ephemeral("That word is already on the list.")
                )
        except:
            pass  # There is nothing to check.

        await asyncio.sleep(0.2)

        await self.bot.mguild_config.find_one_and_update(
            {"_id": ctx.guild.id},
            {"$push": {"banWordList": f"{word}"}},
            upsert=True,
        )

        return await ctx.send(
            embed=success_embed_ephemeral(f'Added "{word}" to the ban filter.')
        )

    @_filter.command(name="links", description=_("cmds.filter.desc_ban"))
    async def _filter_add_links(self, ctx: commands.Context):
        res = await self.bot.mguild_config.find_one({"_id": ctx.guild.id})

        if res["linksDelete"] == True:
            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$set": {"linksDelete": False}},
                upsert=True,
            )

            return await ctx.send(
                embed=success_embed_ephemeral(_("cmds.filter.res.success.allow"))
            )
        else:
            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$set": {"linksDelete": True}},
                upsert=True,
            )

            return await ctx.send(
                embed=success_embed_ephemeral(_("cmds.filter.res.success.delete"))
            )

    @_filter.command(name="remove", description=_("cmds.filter.desc_remove"))
    async def _filter_remove(self, ctx: commands.Context, word: str):
        try:
            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$pull": {"banWordList": f"{word}"}},
                upsert=True,
            )
        except:
            pass

        try:
            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$pull": {"deleteWordList": f"{word}"}},
                upsert=True,
            )
        except:
            pass

        return await ctx.send(
            embed=success_embed_ephemeral(f'Removed "{word}" from the filter.')
        )

    @_filter.command(
        name="exempt", description=_("cmds.filter.desc_exempt"), hidden=True
    )
    async def _filter_exempt(self, ctx: commands.Context, role: nextcord.Role):
        pass

    @_filter.command(name="reset", description=_("cmds.filter.desc_reset"))
    async def _filter_reset(self, ctx: commands.Context):
        try:
            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$unset": {"banWordList": ""}},
                upsert=True,
            )
        except:
            pass

        try:
            await self.bot.mguild_config.find_one_and_update(
                {"_id": ctx.guild.id},
                {"$unset": {"deleteWordList": ""}},
                upsert=True,
            )
        except:
            pass

        return await ctx.send(
            embed=success_embed_ephemeral("Successfully reset all filters.")
        )


def setup(bot):
    bot.add_cog(Filter(bot))
