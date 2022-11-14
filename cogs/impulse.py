import nextcord
from nextcord.ext import commands, menus

from utils.data import Bot
from utils.perms import only_owner


class ReactionButton(nextcord.ui.Button):
    def __init__(self, label, custom_id):
        super().__init__(
            custom_id=custom_id, label=label, style=nextcord.ButtonStyle.blurple
        )

    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Hi", ephemeral=True)


class WestCoastRoles(nextcord.ui.View):
    def __init__(self, roles, **kwargs):
        super().__init__(**kwargs)

        for role in roles:
            button = ReactionButton(label=role.name, custom_id=role.id)
            self.add_item(button)


class Impulse(commands.Cog):
    """The description for Impulse goes here."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="impulse", hidden=True)
    @commands.check(only_owner)
    async def _impulse(self, ctx: commands.Context, id: int | str):
        try:
            match id:
                case 2:
                    if ctx.author.id != 403308385539194880:
                        return await ctx.send("This isn't for you =)")

                    resolved_roles = []
                    test_roles = [
                        1041250454732021800,
                        1027254825341173760,
                        1027083493601181766,
                    ]
                    roles = [
                        1040683166052122846,
                        1040683192249757809,
                        1040683202777448590,
                        1040683173341831208,
                        1040683185303978076,
                        1040683198541221948,
                        1040683164730916924,
                        1040683183886311424,
                    ]

                    for role in test_roles:
                        full_role: nextcord.Role = ctx.guild.get_role(role)
                        resolved_roles.append(full_role)

                    await ctx.send(
                        "West Coast roles", view=WestCoastRoles(roles=resolved_roles)
                    )
                case 101:
                    return await ctx.send("Uhh, wrong game?")
                case _:
                    return
        except Exception as error:
            await self.bot.create_error_log(ctx, error)


def setup(bot):
    bot.add_cog(Impulse(bot))
