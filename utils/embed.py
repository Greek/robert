import nextcord

from utils import default
from utils.constants import DEFAULT_IMAGE

# Colors
success_embed_color = 0x63D46F
warn_embed_color = 0xEBBD47
failed_embed_color = 0xEB4747


def success_embed_ephemeral(description: str) -> nextcord.Embed:
    return nextcord.Embed(
        color=success_embed_color,
        description=f"<:check:954163199446499389> {description}",
    )


def success_embed(user: nextcord.User, description: str) -> nextcord.Embed:
    return nextcord.Embed(
        color=success_embed_color,
        description=f"<:check:954163199446499389> {description}",
    ).set_author(name=user.name, icon_url=user.display_avatar)


def warn_embed_ephemeral(description: str, footer: str = None) -> nextcord.Embed:
    return nextcord.Embed(
        color=warn_embed_color,
        description=f"⚠️ {description}",
    )


def cancellable_embed_ephemeral(
    author: nextcord.Member, description: str, footer: str = None
) -> nextcord.Embed:
    return (
        nextcord.Embed(
            color=warn_embed_color,
            description=f"⚠️ {description}",
        )
        .set_author(
            name=author.name,
            icon_url=author.avatar
            if author.avatar
            else "https://canary.discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png",
        )
        .set_footer(text=footer)
    )


def warn_embed(
    user: nextcord.User, description: str, footer: str = None
) -> nextcord.Embed:
    return nextcord.Embed(
        color=warn_embed_color,
        description=f"⚠️ {description}",
    ).set_author(name=user.name, icon_url=user.display_avatar)


def failed_embed_ephemeral(description: str, footer: str = None) -> nextcord.Embed:
    return nextcord.Embed(
        color=failed_embed_color,
        description=f"<:red_tick:954499768124583947> {description}",
    )


def failed_embed(
    user: nextcord.User, description: str, footer: str = None
) -> nextcord.Embed:
    return nextcord.Embed(
        color=failed_embed_color,
        description=f"<:red_tick:954499768124583947> {description}",
    ).set_author(name=user.name, icon_url=user.display_avatar)


def missing_permissions(description: str, footer: str = None) -> nextcord.Embed:
    return nextcord.Embed(
        color=failed_embed_color,
        description=f"<:red_tick:954499768124583947> You're missing the `{description.lower()}` permission.",
    )


def self_missing_permissions(description: str, footer: str = None) -> nextcord.Embed:
    return nextcord.Embed(
        color=failed_embed_color,
        description=f"<:red_tick:954499768124583947> I don't have the `{description.lower()}` permission.",
    )


async def create_guild_join(guild: nextcord.Guild):
    embed = default.branded_embed(
        title=f"Guild joined | {guild.name} ({guild.id})",
        color=success_embed_color,
    )

    embed.set_author(
        name=f"{guild.name}",
        icon_url=f"{guild.icon if guild.icon else DEFAULT_IMAGE}",
    )
    embed.add_field(name="Owner", value=f"<@{guild.owner.id}>", inline=True)
    embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
    # embed.add_field(
    #     name="On Allowlist?",
    #     value="true" if guild.id in guilds else "false",
    #     inline=True,
    # )
    embed.set_footer(text=f"Owner ID: {guild.owner_id}")
    try:
        embed.add_field(
            name="Invite code",
            value=f"{[str(x.code) for x in await guild.invites()]}",
            inline=True,
        )
    except nextcord.errors.Forbidden:
        embed.add_field(
            name="Invite code", value="Could not fetch invite.", inline=True
        )
    # pylint: disable=W0703
    except Exception:
        embed.add_field(
            name="Invite code", value="Failed to print invites", inline=True
        )

    return embed


async def create_guild_leave(guild: nextcord.Guild):
    embed = default.branded_embed(
        title=f"Guild left | {guild.name} ({guild.id})",
        color=failed_embed_color,
    )

    embed.set_author(
        name=f"{guild.name}", icon_url=f"{guild.icon if guild.icon else DEFAULT_IMAGE}"
    )
    embed.add_field(name="Owner", value=f"<@{guild.owner.id}>", inline=True)
    embed.add_field(name="Member count", value=f"{guild.member_count}", inline=True)
    # embed.add_field(
    #     name="On Allowlist?",
    #     value="true" if guild.id in guilds else "false",
    #     inline=True,
    # )
    embed.set_footer(text=f"Owner ID: {guild.owner_id}")

    return embed
