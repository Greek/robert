import nextcord

# Colors
success_embed_color = 0x63D46F
warn_embed_color = 0xEBBD47
failed_embed_color = 0xEB4747


async def success_embed_ephemeral(description: str) -> nextcord.Embed:
    embed = nextcord.Embed(
        color=success_embed_color,
        description=f"<:check:954163199446499389> {description}",
    )
    return embed


async def success_embed(user: nextcord.User, description: str) -> nextcord.Embed:
    embed = nextcord.Embed(
        color=success_embed_color,
        description=f"<:check:954163199446499389> {description}",
    )
    embed.set_author(name=user.name, icon_url=user.display_avatar)

    return embed


async def warn_embed_ephemeral(description: str, footer: str = None) -> nextcord.Embed:
    embed = nextcord.Embed(
        color=warn_embed_color,
        description=f"⚠️ {description}",
    )
    return embed


async def warn_embed(
    user: nextcord.User, description: str, footer: str = None
) -> nextcord.Embed:
    embed = nextcord.Embed(
        color=warn_embed_color,
        description=f"⚠️ {description}",
    )
    embed.set_author(name=user.name, icon_url=user.display_avatar)

    return embed
