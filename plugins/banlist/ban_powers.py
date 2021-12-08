"""-------------------------------------------------------
Author: Schuyler Kelly
Date: 11/04/2021
Edited: 11/04/2021
Purpose:
    Allow the user to ban powers.
-------------------------------------------------------"""
import hikari
import lightbulb
from lightbulb import commands, context
import json

# Construct the powers plugin.
powers_plugin = lightbulb.Plugin("banPowers")

# Create the ban powers command.
@powers_plugin.command
@lightbulb.option(
    "movement",
    "Movement type powers.",
    str,
    choices = [
            "Sky Jump",
            "Jump Glide",
            "Rocket Jump",
            "Angelic Missile",
            "Super Speed",
            "Warp"
        ]
)
@lightbulb.option(
    "attack",
    "Attack type powers.",
    str,
    choices = [
            "Idol Transformation",
            "Mega Laser",
            "Explosive Flame",
            "Black Hole",
            "Meteor Shower",
            "Land Mine",
            "Reflect Barrier",
            "Heavenly Light",
            "Spite"
        ]
)
@lightbulb.option(
    "strengthen",
    "Attack enhancement type powers.",
    str,
    choices = [
            "Autoreticle",
            "Quick Charge",
            "Homing Boost",
            "Slip Shot",
            "Invisible Shots",
            "Random Effect",
            "Poison Attack",
            "Paralyze Attack",
            "Weaken Attack",
            "Petrify Attack",
            "Shake Attack",
            "Confuse Attack",
            "Burn Attack",
            "Freeze Attack",
            "Spin Attack",
            "Eggplant Attack",
            "Tempura Attack",
            "Power Thief",
            "Energy Charge",
            "Libra Sponge"
        ]
)
@lightbulb.option(
    "debuff",
    "Debuff type powers.",
    str,
    choices = [
            "Darkness",
            "Interference",
            "Virus"
        ]
)
@lightbulb.option(
    "enhance",
    "Ability enhancing powers.",
    str,
    choices = [
            "Super Armor",
            "Brief Invincibility",
            "Tirelessness",
            "Lightweight",
            "Trade-off",
            "Aries Armor"
        ]
)
@lightbulb.option(
    "special",
    "Special effect type powers.",
    str,
    choices = [
            "Bumblebee",
            "Counter",
            "Transparency",
            "Playing Dead"
        ]
)
@lightbulb.option(
    "recovery",
    "Recovery type powers.",
    str,
    choices = [
            "Health Recovery",
            "Effect Recovery",
            "Pisces Heal"
        ]
)
@lightbulb.option(
    "item",
    "Item type powers.",
    str,
    choices = [
            "Item Vacuum",
            "Throwing Boost",
            "Double Item"
        ]
)
@lightbulb.option(
    "misc",
    "Miscellaneous type powers.",
    str,
    choices = [
            "Fortune's Jukebox",
            "Celestial Fireworks",
            "Random"
        ]
)
@lightbulb.command("banpowers", "Add power(s) to the server wide banlist.", aliases = ["bp"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def banpowers(ctx : context.Context):

    # Get the user.
    user = ctx.member

    # Get their highest role.
    highest = user.get_top_role()

    # Check their perms. If they don't have admin, give an error message.
    if not highest.permissions.any(hikari.Permissions.ADMINISTRATOR):
        await ctx.respond("You do not have permission to use this command.")
        return

    with open("data/banlist_data/banlist_powers.json") as data:
        banned_powers = json.load(data)

    # Construct a list of all powers to be banned.
    powers = [
        ctx.options.movement,
        ctx.options.attack,
        ctx.options.strengthen,
        ctx.options.debuff,
        ctx.options.enhance,
        ctx.options.special,
        ctx.options.recovery,
        ctx.options.item,
        ctx.options.misc
    ]

    # Construct a new list of all valid entries.
    temp_banned = []
    power_got_banned = False
    for power in powers:
        if power is not None:
            if power not in banned_powers:
                banned_powers.append(power)
                power_got_banned = True
                temp_banned.append(power)

    # If not entries were valid, report to the user and return.
    if not power_got_banned:
        await ctx.respond("No powers added.")
        return

    # Construct a string to report to the user.
    temp_banned = ", ".join(temp_banned)

    with open("data/banlist_data/banlist_powers.json", "w") as data:
        json.dump(banned_powers, data, indent = 2)

    await ctx.respond(f"Banned power(s): {temp_banned}.")
    return

# Construct the unban powers command.
# NOTE:
#   All of the following code follows more or less
#   the same logic as the previous command.
@powers_plugin.command
@lightbulb.option(
    "movement",
    "Movement type powers.",
    str,
    choices = [
            "Sky Jump",
            "Jump Glide",
            "Rocket Jump",
            "Angelic Missile",
            "Super Speed",
            "Warp"
        ]
)
@lightbulb.option(
    "attack",
    "Attack type powers.",
    str,
    choices = [
            "Idol Transformation",
            "Mega Laser",
            "Explosive Flame",
            "Black Hole",
            "Meteor Shower",
            "Land Mine",
            "Reflect Barrier",
            "Heavenly Light",
            "Spite"
        ]
)
@lightbulb.option(
    "strengthen",
    "Attack enhancement type powers.",
    str,
    choices = [
            "Autoreticle",
            "Quick Charge",
            "Homing Boost",
            "Slip Shot",
            "Invisible Shots",
            "Random Effect",
            "Poison Attack",
            "Paralyze Attack",
            "Weaken Attack",
            "Petrify Attack",
            "Shake Attack",
            "Confuse Attack",
            "Burn Attack",
            "Freeze Attack",
            "Spin Attack",
            "Eggplant Attack",
            "Tempura Attack",
            "Power Thief",
            "Energy Charge",
            "Libra Sponge"
        ]
)
@lightbulb.option(
    "debuff",
    "Debuff type powers.",
    str,
    choices = [
            "Darkness",
            "Interference",
            "Virus"
        ]
)
@lightbulb.option(
    "enhance",
    "Ability enhancing powers.",
    str,
    choices = [
            "Super Armor",
            "Brief Invincibility",
            "Tirelessness",
            "Lightweight",
            "Trade-off",
            "Aries Armor"
        ]
)
@lightbulb.option(
    "special",
    "Special effect type powers.",
    str,
    choices = [
            "Bumblebee",
            "Counter",
            "Transparency",
            "Playing Dead"
        ]
)
@lightbulb.option(
    "recovery",
    "Recovery type powers.",
    str,
    choices = [
            "Health Recovery",
            "Effect Recovery",
            "Pisces Heal"
        ]
)
@lightbulb.option(
    "item",
    "Item type powers.",
    str,
    choices = [
            "Item Vacuum",
            "Throwing Boost",
            "Double Item"
        ]
)
@lightbulb.option(
    "misc",
    "Miscellaneous type powers.",
    str,
    choices = [
            "Fortune's Jukebox",
            "Celestial Fireworks",
            "Random"
        ]
)
@lightbulb.command("unbanpowers", "Remove power(s) from the server wide banlist.", aliases = ["up"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def unbanpowers(ctx : context.Context):

    # Get the user.
    user = ctx.member

    # Get highest role.
    highest = user.get_top_role()

    # Check if they have admin. If they don't, send an error message.
    if not highest.permissions.any(hikari.Permissions.ADMINISTRATOR):
        await ctx.respond("You do not have permission to use this command.")
        return

    with open("data/banlist_data/banlist_powers.json") as data:
        banned_powers = json.load(data)

    powers = [
        ctx.options.movement,
        ctx.options.attack,
        ctx.options.strengthen,
        ctx.options.debuff,
        ctx.options.enhance,
        ctx.options.special,
        ctx.options.recovery,
        ctx.options.item,
        ctx.options.misc
    ]

    temp_unbanned = []
    power_got_unbanned = False
    for power in powers:
        if power is not None:
            if power in banned_powers:
                banned_powers.remove(power)
                power_got_unbanned = True
                temp_unbanned.append(power)

    if not power_got_unbanned:
        await ctx.respond("No powers removed.")
        return

    temp_unbanned = ", ".join(temp_unbanned)

    with open("data/banlist_data/banlist_powers.json", "w") as data:
        json.dump(banned_powers, data, indent = 2)

    await ctx.respond(f"Unbanned power(s): {temp_unbanned}.")
    return


def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(powers_plugin)