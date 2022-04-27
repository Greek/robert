import nextcord
from nextcord.ext import commands

from utils.embed import cancellable_embed_ephemeral


class ConfirmDeletion(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.danger)
    async def delete(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if not interaction.message.author:
            return
        # There is a clone function for this but it doesn't support position parameter
        await interaction.channel.delete()
        await interaction.guild.create_text_channel(
            name=interaction.channel.name,
            nsfw=interaction.channel.nsfw,
            topic=interaction.channel.topic,
            category=interaction.channel.category,
            position=interaction.channel.position,
            overwrites=interaction.channel.overwrites,
            slowmode_delay=interaction.channel.slowmode_delay,
        )
        self.stop()

    @nextcord.ui.button(label="Nevermind", style=nextcord.ButtonStyle.secondary)
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        if not interaction.message.author:
            return
        await interaction.message.delete()
        self.stop()

class ChannelRecreate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="nuke")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _nuke(self, ctx: commands.Context):
        view = ConfirmDeletion()
        await ctx.send(
            embed=cancellable_embed_ephemeral(
                ctx.author,
                f"Are you sure you want to re-create {ctx.channel.name}? You may need to re-adjust permissions.",
                f'If you\'d like to cancel this, press on "Nevermind!" or wait 10 seconds.',
            ),
            view=view,
        )
        await view.wait()


def setup(bot):
    bot.add_cog(ChannelRecreate(bot))
