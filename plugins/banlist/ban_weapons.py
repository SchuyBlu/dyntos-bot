"""-------------------------------------------------------
Author: Schuyler Kelly
Date: 11/03/2021
Edited: 11/03/2021
Purpose:
    Add to the banlist.
-------------------------------------------------------"""
import hikari
import lightbulb
from lightbulb import commands, context
import json

# Constructthe plugin.
weapons_plugin = lightbulb.Plugin("banWeapons")

# Construct the first command, ban weapons.
@weapons_plugin.command
@lightbulb.option(
    "blades",
    "A list of blades.",
    str,
    choices = [
            "First Blade",
            "Burst Blade",
            "Vipe Blade",
            "Crusader Blade",
            "Royal Blade",
            "Optical Blade",
            "Samurai Blade",
            "Bullet Blade",
            "Aquarius Blade",
            "Aurum Blade",
            "Palutena Blade",
            "Gaol Blade"
        ]
)
@lightbulb.option(
    "staves",
    "A list of staves.",
    str,
    choices = [
            "Insight Staff",
            "Orb Staff",
            "Rose Staff",
            "Knuckle Staff",
            "Ancient Staff",
            "Lancer Staff",
            "Flintlock Staff",
            "Somewhat Staff",
            "Scorpio Staff",
            "Laser Staff",
            "Dark Pit Staff",
            "Thanatos Staff"
        ]
)
@lightbulb.option(
    "claws",
    "A list of claws",
    str,
    choices = [
             "Tiger Claws",
            "Wolf Claws",
            "Bear Claws",
            "Brawler Claws",
            "Stealth Claws",
            "Hedgehod Claws",
            "Raptor Claws",
            "Artillery Claws",
            "Cancer Claws",
            "Beam Claws",
            "Viridi Claws",
            "Pandora Claws"
        ]
)
@lightbulb.option(
    "bows",
    "A list of bows.",
    str,
    choices = [
            "Fortune Bow",
            "Silver Bow",
            "Meteor Bow",
            "Divine Bow",
            "Darkness Bow",
            "Crystal Bow",
            "Angel Bow",
            "Hawkeye Bow",
            "Sagittarius Bow",
            "Aurum Bow",
            "Palutena Bow",
            "Phosphora Bow"
        ]
)
@lightbulb.option(
    "palms",
    "A list of palms.",
    str,
    choices = [
            "Violet Palm",
            "Burning Palm",
            "Needle Palm",
            "Midnight Palm",
            "Cursed Palm",
            "Cutter Palm",
            "Pudgy Palm",
            "Ninja Palm",
            "Virgo Palm",
            "Aurum Palm",
            "Viridi Palm",
            "Great Reaper Palm"
        ]
)
@lightbulb.option(
    "clubs",
    "A list of clubs.",
    str,
    choices = [
            "Ore Club",
            "Babel Club",
            "Skyscraper Club",
            "Atlas Club",
            "Earthmaul Club",
            "Ogre Club",
            "Halo Club",
            "Black Club",
            "Capricorn Club",
            "Aurum Club",
            "Hewdraw Club",
            "Magnus Club"
        ]
)
@lightbulb.option(
    "cannons",
    "A list of the cannons.",
    str,
    choices = [
            "EZ Cannon",
            "Ball Cannon",
            "Predator Cannon",
            "Poseidon Cannon",
            "Fireworks Cannon",
            "Rail Cannon",
            "Dynamo Cannon",
            "Doom Cannon",
            "Leo Cannon",
            "Sonic Cannon",
            "Twinbellows Cannon",
            "Cragalanche Cannon"
        ]
)
@lightbulb.option(
    "orbitars",
    "A list of orbitars.",
    str,
    choices = [
             "Standard Orbitars",
            "Guardian Orbitars",
            "Shock Orbitars",
            "Eyetrack Orbitars",
            "Fairy Orbitars",
            "Paw Pad Orbitars",
            "Jetstream Orbitars",
            "Boom Orbitars",
            "Gemini Orbitars",
            "Aurum Orbitars",
            "Centurion Orbitars",
            "Arlon Orbitars"
        ]
)
@lightbulb.option(
    "arms",
    "A list of arms.",
    str, 
    choices = [
            "Crusher Arm",
            "Compact Arm",
            "Electroshock Arm",
            "Volcano Arm",
            "Drill Arm",
            "Bomber Arm",
            "Bowl Arm",
            "End-All Arm",
            "Taurus Arm",
            "Upperdash Arm",
            "Kraken Arm",
            "Phoenix Arm"
        ]
)
@lightbulb.command("banweapons", "Add weapon(s) to the server wide banlist.", aliases = ["bw"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def banweapons(ctx : context.Context):

    # Get the user.
    user = ctx.member

    # Get the users highest role.
    highest = user.get_top_role()
    
    # If the user isn't an admin, give an error message.
    if not highest.permissions.any(hikari.Permissions.ADMINISTRATOR):
        await ctx.respond("You do not have permission to use this command.")
        return

    with open("data/banlist_data/banlist_weapons.json") as data:
        banned_data = json.load(data)

    # Construct a list of options.
    weapons = [
        ctx.options.blades,
        ctx.options.staves,
        ctx.options.claws,
        ctx.options.bows,
        ctx.options.palms,
        ctx.options.clubs,
        ctx.options.cannons,
        ctx.options.orbitars,
        ctx.options.arms
        ]

    # Construct a list of valid entries from the options.
    temp_banned = []
    weapons_got_added = False
    for weapon in weapons:
        if weapon is not None:
            if weapon not in banned_data:
                banned_data.append(weapon)
                weapons_got_added = True
                temp_banned.append(weapon)

    # If no valid entries, report to user and return.
    if not weapons_got_added:
        await ctx.respond("No weapons added.")
        return

    # Construct string to report to user.
    temp_banned = ", ".join(temp_banned)

    with open("data/banlist_data/banlist_weapons.json", "w") as data:
        json.dump(banned_data, data, indent = 2)

    await ctx.respond(f"Banned weapon(s): {temp_banned}.")
    return


    # Construct the unban weapons command.
# NOTE:
#   All of the following code follows more or less
#   the same logic as the previous command.
@weapons_plugin.command
@lightbulb.option(
    "blades",
    "A list of blades.",
    str,
    choices = [
            "First Blade",
            "Burst Blade",
            "Vipe Blade",
            "Crusader Blade",
            "Royal Blade",
            "Optical Blade",
            "Samurai Blade",
            "Bullet Blade",
            "Aquarius Blade",
            "Aurum Blade",
            "Palutena Blade",
            "Gaol Blade"
        ]
)
@lightbulb.option(
    "staves",
    "A list of staves.",
    str,
    choices = [
            "Insight Staff",
            "Orb Staff",
            "Rose Staff",
            "Knuckle Staff",
            "Ancient Staff",
            "Lancer Staff",
            "Flintlock Staff",
            "Somewhat Staff",
            "Scorpio Staff",
            "Laser Staff",
            "Dark Pit Staff",
            "Thanatos Staff"
        ]
)
@lightbulb.option(
    "claws",
    "A list of claws",
    str,
    choices = [
             "Tiger Claws",
            "Wolf Claws",
            "Bear Claws",
            "Brawler Claws",
            "Stealth Claws",
            "Hedgehod Claws",
            "Raptor Claws",
            "Artillery Claws",
            "Cancer Claws",
            "Beam Claws",
            "Viridi Claws",
            "Pandora Claws"
        ]
)
@lightbulb.option(
    "bows",
    "A list of bows.",
    str,
    choices = [
            "Fortune Bow",
            "Silver Bow",
            "Meteor Bow",
            "Divine Bow",
            "Darkness Bow",
            "Crystal Bow",
            "Angel Bow",
            "Hawkeye Bow",
            "Sagittarius Bow",
            "Aurum Bow",
            "Palutena Bow",
            "Phosphora Bow"
        ]
)
@lightbulb.option(
    "palms",
    "A list of palms.",
    str,
    choices = [
            "Violet Palm",
            "Burning Palm",
            "Needle Palm",
            "Midnight Palm",
            "Cursed Palm",
            "Cutter Palm",
            "Pudgy Palm",
            "Ninja Palm",
            "Virgo Palm",
            "Aurum Palm",
            "Viridi Palm",
            "Great Reaper Palm"
        ]
)
@lightbulb.option(
    "clubs",
    "A list of clubs.",
    str,
    choices = [
            "Ore Club",
            "Babel Club",
            "Skyscraper Club",
            "Atlas Club",
            "Earthmaul Club",
            "Ogre Club",
            "Halo Club",
            "Black Club",
            "Capricorn Club",
            "Aurum Club",
            "Hewdraw Club",
            "Magnus Club"
        ]
)
@lightbulb.option(
    "cannons",
    "A list of the cannons.",
    str,
    choices = [
            "EZ Cannon",
            "Ball Cannon",
            "Predator Cannon",
            "Poseidon Cannon",
            "Fireworks Cannon",
            "Rail Cannon",
            "Dynamo Cannon",
            "Doom Cannon",
            "Leo Cannon",
            "Sonic Cannon",
            "Twinbellows Cannon",
            "Cragalanche Cannon"
        ]
)
@lightbulb.option(
    "orbitars",
    "A list of orbitars.",
    str,
    choices = [
             "Standard Orbitars",
            "Guardian Orbitars",
            "Shock Orbitars",
            "Eyetrack Orbitars",
            "Fairy Orbitars",
            "Paw Pad Orbitars",
            "Jetstream Orbitars",
            "Boom Orbitars",
            "Gemini Orbitars",
            "Aurum Orbitars",
            "Centurion Orbitars",
            "Arlon Orbitars"
        ]
)
@lightbulb.option(
    "arms",
    "A list of arms.",
    str, 
    choices = [
            "Crusher Arm",
            "Compact Arm",
            "Electroshock Arm",
            "Volcano Arm",
            "Drill Arm",
            "Bomber Arm",
            "Bowl Arm",
            "End-All Arm",
            "Taurus Arm",
            "Upperdash Arm",
            "Kraken Arm",
            "Phoenix Arm"
        ]
)
@lightbulb.command("unbanweapons", "Remove weapon(s) from the server wide banlist.", aliases = ["uw"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def unbanweapons(ctx : context.Context):

    # Get the user.
    user = ctx.member

    # Get their highest role.
    highest = user.get_top_role()

    # Check if they have admin. If they don't, send error message.
    if not highest.permissions.any(hikari.Permissions.ADMINISTRATOR):
        await ctx.respond("You do not have permission to use this command.")
        return

    with open("data/banlist_data/banlist_weapons.json") as data:

        banlist = json.load(data)

    weapons = [
        ctx.options.blades,
        ctx.options.staves,
        ctx.options.claws,
        ctx.options.bows,
        ctx.options.palms,
        ctx.options.clubs,
        ctx.options.cannons,
        ctx.options.orbitars,
        ctx.options.arms
        ]

    temp_data = []
    weapons_got_removed = False
    for weapon in weapons:
        if weapon is not None:
            if weapon in banlist:
                banlist.remove(weapon)
                weapons_got_removed = True
                temp_data.append(weapon)

    if not weapons_got_removed:
        await ctx.respond("No weapons removed.")
        return

    with open("data/banlist_data/banlist_weapons.json", "w") as data:
        json.dump(banlist, data, indent = 2)

    temp_string = ", ".join(temp_data)

    await ctx.respond(f"Weapon(s) removed from banlist: {temp_string}")


def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(weapons_plugin)