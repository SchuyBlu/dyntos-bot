"""----------------------------------------------
Author: Schuyler Kelly
Date: 11/04/2021
Edited: 11/05/2021
Purpose:
    Call the server banlist.
----------------------------------------------"""
import hikari
import lightbulb
from lightbulb import commands, context
import json

# Construct the banlist plugin.
banlist_plugin = lightbulb.Plugin("Banlist")

# Construct the first command, banlist.
@banlist_plugin.command
@lightbulb.command("banlist", "Displays the banlist.", aliases = ["b"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def banlist(ctx : context.Context):

    # Retrieves all banlist data.
    with open("data/banlist_data/banlist_weapons.json") as data:
        weapon_banlist = json.load(data)

    with open("data/banlist_data/banlist_powers.json") as data:
        power_banlist = json.load(data)

    if len(weapon_banlist) == 0:
        banlist_string = "No weapons have been banned."
    else:
        banlist_string = "- " + "\n- ".join(weapon_banlist)

    if len(power_banlist) == 0:
        power_string = "No powers have been banned."
    else:
        power_string = "- " + "\n- ".join(power_banlist)
    
    embed_message = (
        hikari.Embed(
            title = "Banlist",
            description = "Listed below are all the banned weapons and powers.",
            color = hikari.Color(0x7D00FF),
        )
        .add_field(
            name = ":sparkles: Weapons :sparkles:",
            value = banlist_string,
            inline = False,
        )
        .add_field(
            name = ":sparkles: Powers :sparkles:",
            value = power_string,
            inline = False,
        )
    )

    await ctx.respond(embed_message)
    return

# Construct the second command, banlist reset.
@banlist_plugin.command
@lightbulb.command("banlistreset", "Resets the server wide banlist.", aliases = ["br"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def banlistreset(ctx : context.Context):

    # Get the user.
    user = ctx.member

    # Get their top role.
    highest = user.get_top_role()

    # Check if they have admin. If they don't raise an error message.
    if not highest.permissions.any(hikari.Permissions.ADMINISTRATOR):
        await ctx.respond("You do not have permission to use this command.")
        return

    # Essentially just replace both banlist files with empty lists.
    weapons_ban = []
    powers_ban = []

    with open("data/banlist_data/banlist_weapons.json", "w") as data:
        json.dump(weapons_ban, data, indent = 2)

    with open("data/banlist_data/banlist_powers.json", "w") as data:
        json.dump(powers_ban, data, indent = 2)

    await ctx.respond("Banlist reset.")
    return


def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(banlist_plugin)