import nextcord

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


def missing_permissions(
    description: str, footer: str = None
) -> nextcord.Embed:
    return nextcord.Embed(
        color=failed_embed_color,
        description=f"<:red_tick:954499768124583947> You're missing the `{description.lower()}` permission.",
    )


def self_missing_permissions(
    description: str, footer: str = None
) -> nextcord.Embed:
    return nextcord.Embed(
        color=failed_embed_color,
        description=f"<:red_tick:954499768124583947> I don't have the `{description.lower()}` permission.",
    )
