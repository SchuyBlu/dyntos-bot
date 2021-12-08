"""--------------------------------------------------
Author: Schuyler Kelly
Date: 11/02/2021
Edited: 11/02/2021
Purpose:
    Create a way to display user information.
--------------------------------------------------"""
from datetime import datetime
import hikari
import lightbulb
from lightbulb import commands, context

# Construct the plugin.
info_plugin = lightbulb.Plugin("userinfo")

# Construct the userinfo command.
@info_plugin.command
@lightbulb.option("mention", "The member to get information about.", hikari.User, required = False)
@lightbulb.command("userinfo", "Get info on a server member.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def userinfo(ctx : context.Context):

    if ctx.options.mention is None:
        user = ctx.member
    else:
        user = ctx.get_guild().get_member(ctx.options.mention)

    roles = (await user.fetch_roles())[1:]
    if len(roles) == 0:
        roles = f"{user.display_name} has no server roles."
    else:
        roles = ", ".join(role.mention for role in roles)

    created_at = int(user.created_at.timestamp())
    joined_at = int(user.joined_at.timestamp())

    # Create an embed message that will be the user profile.
    embed = (
        hikari.Embed(
            title = f"User Info - {user.display_name}",
            description = f"ID: `{user.id}`",
            color = hikari.Color(0x7D00FF),
            timestamp = datetime.now().astimezone()
        )
        .set_thumbnail(user.avatar_url)
        .set_footer(
            text = f"Requested by {ctx.member.display_name}",
            icon = ctx.member.avatar_url,
        )
        .add_field(
            name = "Bot?",
            value = user.is_bot,
            inline = True,
        )
        .add_field(
            name = "Created account on",
            value = f"<t:{created_at}:d> (<t:{created_at}:R>)",
            inline = True,
        )
        .add_field(
            name = "Joined server on",
            value = f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
            inline = True
        )
        .add_field(
            name = "Roles",
            value = roles,
            inline = False,
        )
    )

    await ctx.respond(embed)

def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)