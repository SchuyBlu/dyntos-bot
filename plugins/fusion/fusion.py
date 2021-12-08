"""----------------------------------------------------
Author: Schuyler Kelly
Date: 11/14/2021
Edited: 11/14/2021
Purpose:
    Create the value calculator.
----------------------------------------------------"""
import lightbulb
from lightbulb import commands, context
import json
import math
import utils.fusion_utils as fuse

# Construct the fusion plugin.
fusion_plugin = lightbulb.Plugin("Fusion")

# Create the first command, the calculator.
@fusion_plugin.command
@lightbulb.option("mod6", "The sixth modifier. Please spell as given in the game.", str, required = False)
@lightbulb.option("mod5", "The fifth modifier. Please spell as given in the game.", str, required = False)
@lightbulb.option("mod4", "The fourth modifier. Please spell as given in the game.", str, required = False)
@lightbulb.option("mod3", "The third modifier. Please spell as given in the game.", str, required = False)
@lightbulb.option("mod2", "The second modifier. Please spell as given in the game.", str, required = False)
@lightbulb.option("mod1", "The first modifier. Please spell as given in the game.", str, required = False)
@lightbulb.option("stars_melee", "Melee stars. Please format as a floating point number.", str, required = False)
@lightbulb.option("stars_ranged", "Ranged stars. Please format as a floating point number.", str, required = False)
@lightbulb.option("weapon", "The name of the weapon given.", str, required = False)
@lightbulb.command("calc", "Calculator to determine weapon value.")
@lightbulb.implements(commands.SlashCommand)
async def calc(ctx : context.Context):

    # Construct the weapon name. It does not matter if this
    # is None or not, as that is handled in the create_embed()
    # function.
    weapon_name = ctx.options.weapon

    # Construct a list of the modifiers.
    temp_mods = [
        ctx.options.mod1,
        ctx.options.mod2,
        ctx.options.mod3,
        ctx.options.mod4,
        ctx.options.mod5,
        ctx.options.mod6
    ]

    # Create a value variable to append to.
    value = 100

    # Retrieve and construct the stars..
    temp = ctx.options.stars_ranged
    if temp is None:
        temp = "0"
    temp = str(float(temp))

    # Load the star data file.
    with open("data/weapon_data/star_data.json") as data:
        star_data = json.load(data)

    # Use a try block to make sure the user input for the 
    # ranged star values is valid.
    try:
        value += star_data["ranged"][temp]
    except KeyError as err:
        await ctx.respond(f"Input error raised: {err}.")
        return

    # Split the ranged star at the decimal. Essentially
    # just constructs the string with star ACSII characters.
    temp1, temp2 = temp.split(".")
    ranged = "\u2605" * int(temp1)
    if temp2 == "5":
        ranged += "\u2606"

    # Retrieve and construct the melee value.   
    temp = ctx.options.stars_melee
    if temp is None:
        temp = "0"
    temp = str(float(temp))

    # raise errors if the star data is out of range.
    try:
        value += star_data["melee"][temp]
    except KeyError as err:
        await ctx.respond(f"Input error raised: {err}.")
        return

    temp1, temp2 = temp.split(".")
    melee = "\u2605" * int(temp1)
    if temp2 == "5":
        melee += "\u2606"

    # Retrieve the available modifiers.
    with open("data/weapon_data/mod_data.json") as data:
        mod_data = json.load(data)
    mods = []

    # For each mod, format it, add its value to the total value
    # and add it to the list of mods.
    for mod in temp_mods:
        if mod is not None:
            mod_name, mod_attri = mod[:-2].lower().strip(), mod[-2:].lower().strip()

            try:
                value += mod_data[mod_name][mod_attri]
            except KeyError as err:
                await ctx.respond(f"Input error rasied: {err}.")
                return
                
            mods.append(mod_name.title() + " " + mod_attri)

    # Construct the mod string.
    string = ""
    for mod in mods:
        string += mod + "\n"

    value = str(math.floor(value))

    # Use a try block to handle errors.
    try:
        embed = fuse.create_embed(weapon_name, ranged, melee, string, value)
    except KeyError as err:
        await ctx.respond(f"Input error raised: {err}.")
        return

    await ctx.respond(embed)


# Create the second command for the plugin, the fusion calc.
@fusion_plugin.command
@lightbulb.option("weapon2", "The second weapon in the fusion.", str)
@lightbulb.option("weapon1", "The first weapon in the fusion.", str)
@lightbulb.command("fusion", "Displays the result of a fusion.", aliases = ["fu"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def fusion(ctx : context.Context):

    weapon1 = ctx.options.weapon1.lower()
    weapon2 = ctx.options.weapon2.lower()

    # Create the fusion.
    embed = await fuse.simple_fusion(
        ctx,
        weapon1,
        weapon2
    )

    await ctx.respond(embed)
    return

@fusion_plugin.command
@lightbulb.option("result", "The resulting weapon in the fusion.", str, required = False)
@lightbulb.option("group", "the fusion group.", str, choices = ["1", "2", "3", "4", "5"], required = False)
@lightbulb.option("weapon2", "The second weapon in the fusion.", str, required = False)
@lightbulb.option("weapon1", "The first weapon in the fusion.", str, required = False)
@lightbulb.command("search", "Displays results of a fusion.")
@lightbulb.implements(commands.SlashCommand)
async def search(ctx: context.Context):

    # Construct all options.
    weapon1: str = ctx.options.weapon1
    weapon2: str = ctx.options.weapon2
    result: str = ctx.options.result
    group: str = ctx.options.group

    # The following code makes sure at least two fields are entered.
    temp_list = [weapon1, weapon2, result, group]
    amount = 0
    for temp in temp_list:
        if temp is None:
            amount += 1

    if amount > 3 or amount < 2:
        await ctx.respond("Please enter 1-2 fields.")
        return
    
    # Deal with cases when the result is a simple fusion.
    if weapon1 is not None and weapon2 is not None and amount == 2:
        
        # Make existing weapons into lowercase.
        weapon1 = weapon1.lower()
        weapon2 = weapon2.lower()

        embed = await fuse.simple_fusion(
            ctx,
            weapon1,
            weapon2
        )
        await ctx.respond(embed)
        return

    # Deal with cases when only searching by result.
    elif result is not None and amount == 3:

        await fuse.result_only(ctx, result)

    # Deal with cases when only searching by group.
    elif group is not None and amount == 3:

        await fuse.group_only(ctx, group)

    # Deal with cases when a weapon and result are given.
    elif result is not None and group is None and amount == 2:

        await fuse.result_and_weapon(ctx, weapon1, weapon2, result)

    # Deal with cases when searching by result and group.
    elif result is not None and group is not None:
        
        await fuse.result_and_group(ctx, result, group)

    # Deal with cases when only searching by weapon.

    elif (
        (weapon1 is not None and amount == 3) or
        (weapon2 is not None and amount == 3)
    ):

        await fuse.weapons_only(ctx, weapon1, weapon2)

    elif (
        (weapon1 is not None and group is not None and amount == 2) or
        (weapon2 is not None and group is not None and amount == 2)
    ):

        await fuse.weapon_and_group(ctx, group, weapon1, weapon2)


def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(fusion_plugin)