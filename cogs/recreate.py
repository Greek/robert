import nextcord

from nextcord.ext import commands

from utils.default import translate as _
from utils.embed import cancellable_embed_ephemeral, warn_embed_ephemeral


class ConfirmDeletion(nextcord.ui.View):
    def __init__(self, ctx: commands.Context, **kwargs):
        super().__init__(**kwargs)
        self.timeout = 10.0
        self.ctx = ctx

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            await interaction.send(
                embed=warn_embed_ephemeral(_("events.not_your_interaction")),
                ephemeral=True,
            )
        return self.ctx.author == interaction.user

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.danger)
    async def _delete(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
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
    async def _cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.message.delete()
        self.stop()


class ChannelRecreate(commands.Cog):
    def __init__(self, bot: nextcord.Client):
        self.bot = bot

    @commands.command(name="recreate")
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def _recreate(self, ctx: commands.Context):
        def check(interaction: nextcord.Interaction):
            return interaction.user

        view = ConfirmDeletion(ctx)
        await ctx.send(
            embed=cancellable_embed_ephemeral(
                ctx.author,
                _("cmds.recreate.warning.desc", channel=ctx.channel.mention),
                _("cmds.recreate.warning.footer", timeout=f"{view.timeout:.0f}"),
            ),
            view=view,
        )
        await view.wait()


def setup(bot):
    bot.add_cog(ChannelRecreate(bot))
