from nextcord.ext import commands
import nextcord
from utils.data import Bot
from cogs.color import Color


class EventsUssy(commands.Cog):
    """The description for EventsUssy goes here."""

    def __init__(self, bot: Bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_member_join(self, member: nextcord.Member):
    #     if member.guild.id == 950592148816945163:
    #         try:
    #             ussy_role = member.guild.get_role(977704324840951878)

    #             await member.edit(nick=member.name[:3] + "ussy")
    #             await member.add_roles(ussy_role, reason="New member joined")
    #         except nextcord.errors.Forbidden as error:
    #             print(error)

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        if message.guild.id == 950592148816945163:
            if message.channel.id == 997825708082602034:
                if message.author.id == self.bot.user.id:
                    return
                if message.content == "reset":
                    role = nextcord.utils.get(
                        message.guild.roles, name=str(message.author)
                    )
                    await role.delete(reason="Reset color")
                    await message.delete()

                # await message.delete()

                try:
                    converted = nextcord.Color(int(message.content, 16))
                except ValueError:
                    reply = await message.reply(
                        "not a valid color Pls try again.\nif your hex code has a `#`, get rid of it"
                    )
                    await message.delete()
                    return await reply.delete(delay=3)

                existing_color_role: nextcord.Role = nextcord.utils.get(
                    message.guild.roles, name=f"{str(message.author)}"
                )
                ussy_role = message.guild.get_role(977704324840951878)

                if existing_color_role:
                    await existing_color_role.delete(reason="New color requested.")

                color_role = await message.guild.create_role(
                    name=f"{str(message.author)}",
                    reason=f"Created per {str(message.author)}",
                    color=converted,
                )
                await color_role.edit(position=ussy_role.position + 1)
                await message.delete()

                return await message.author.add_roles(
                    color_role, reason="requested color"
                )


def setup(bot):
    bot.add_cog(EventsUssy(bot))
