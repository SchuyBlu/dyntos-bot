"""-------------------------------------------------------------
Author: Schuyler Kelly
Date: 11/27/2021
Edited: 11/27/2021
Purpose:
    Contains all helper functions and classes for fusion
    related commands.
-------------------------------------------------------------"""
import hikari
import lightbulb
import json

#=====================================================================
# USED TO RETRIEVE THE RESULTS OF A FUSION AND ALL RELATED DATA.
# 
# Accessed in:
#   utils/fusion_utils.py
# ----------------------------
# Used in functions/methods:
#   simple_fusion()
#=====================================================================

class Result:
    """
    A Class meant to create and return fusion results.
    
    ...
    
    Attributes
    ----------
    weapon1 : str
        Represents the first weapon.
    weapon2 : str
        Represents the second weapon.
    new_ID : str
        Represents the new weapon ID as a string.
    _type1 : str
        Represents the first weapon's type.
    _type2 : str
        Represents the second weapon's type.
    _trueID1 : int
        Represents the true ID of the first weapon.
    _trueID2 : int
        Represents the true ID of the second weapon.
    
    Methods
    -------
    group() -> str
        Returns a string representation of the resulting fusion group.
    get_type() -> str
        Returns the resulting type of the final weapon.
    """
    def __init__(self, weapon1, weapon2, weapon_data):

        # Get the weapons and types.
        self._type1 = weapon1.split()[-1]
        self._type2 = weapon2.split()[-1]
        self.weapon1 = weapon1
        self.weapon2 = weapon2

        # Retrieve all IDs.
        self._ID1 = weapon_data[self._type1][self.weapon1]
        self._ID2 = weapon_data[self._type2][self.weapon2]
        new_ID = int(self._ID1) + int(self._ID2)
        if new_ID > 12:
            new_ID -= 12
        self.newID = str(new_ID)
        classID1 = weapon_data[self._type1]["class id"]
        classID2 = weapon_data[self._type2]["class id"]
        self._trueID1 = (classID1 * 12) + int(self._ID1)
        self._trueID2 = (classID2 * 12) + int(self._ID2)

    def group(self):
        """
        Purpose: Construct the new weapon ID.
        
        Parameters: weapon1_classID,
                    weapon2_classID,
                    weapon1_id,
                    weapon2_id
                    
        Returns: string of new ID
        """

        # Get the fusion group.
        temp_group = abs(self._trueID1 - self._trueID2) % 5
        if temp_group == 0:
            fusion_group = "2"
        if temp_group == 1:
            fusion_group = "4"
        if temp_group == 2:
            fusion_group = "3"
        if temp_group == 3:
            fusion_group = "1"
        if temp_group == 4:
            fusion_group = "5"
        
        return fusion_group


    def get_type(self):
        """
        Purpose: Retrieve the weapon type of the resulting
                 weapon.
                 
        Parameters: Nothing
        
        Returns: new_type
        """

        # NOTE: I am aware that the following code is disgusting. That
        # said, its necessary as I have no way to determine what formula
        # is used to create the resulting weapon type.
        if (
            (self._type1 == "blade" and self._type2 == "blade") or
            (self._type1 == "blade" and self._type2 == "staff" or self._type1 == "staff" and self._type2 == "blade") or
            (self._type1 == "staff" and self._type2 == "club" or self._type1 == "club" and self._type2 == "staff") or
            (self._type1 == "club" and self._type2 == "orbitars" or self._type1 == "orbitars" and self._type2 == "club") or
            (self._type1 == "cannon" and self._type2 == "orbitars" or self._type1 == "orbitars" and self._type2 == "cannon")
        ):
            new_type = "claws"
        
        if (
            (self._type1 == "blade" and self._type2 == "claws" or self._type1 == "claws" and self._type2 == "blade") or
            (self._type1 == "staff" and self._type2 == "orbitars" or self._type1 == "orbitars" and self._type2 == "staff") or
            (self._type1 == "claws" and self._type2 == "claws") or
            (self._type1 == "claws" and self._type2 == "bow" or self._type1 == "bow" and self._type2 == "claws") or
            (self._type1 == "bow" and self._type2 == "palm" or self._type1 == "palm" and self._type2 == "bow") 
        ):
    
            new_type = "club"

        if (
            (self._type1 == "blade" and self._type2 == "bow" or self._type1 == "bow" and self._type2 == "blade") or
            (self._type1 == "blade" and self._type2 == "orbitars" or self._type1 == "orbitars" and self._type2 == "blade") or
            (self._type1 == "bow" and self._type2 == "club" or self._type1 == "club" and self._type2 == "bow") or
            (self._type1 == "cannon" and self._type2 == "cannon") or
            (self._type1 == "orbitars" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "orbitars")
        ):
            new_type = "palm"

        if (
            (self._type1 == "blade" and self._type2 == "palm" or self._type1 == "palm" and self._type2 == "blade") or
            (self._type1 == "staff" and self._type2 == "claws" or self._type1 == "claws" and self._type2 == "staff") or
            (self._type1 == "staff" and self._type2 == "bow" or self._type1 == "bow" and self._type2 == "staff") or
            (self._type1 == "claws" and self._type2 == "palm" or self._type1 == "palm" and self._type2 == "claws") or
            (self._type1 == "palm" and self._type2 == "palm")
        ):
            new_type = "arm"

        if (
            (self._type1 == "blade" and self._type2 == "club" or self._type1 == "club" and self._type2 == "blade") or
            (self._type1 == "blade" and self._type2 == "cannon" or self._type1 == "cannon" and self._type2 == "blade") or
            (self._type1 == "claws" and self._type2 == "orbitars" or self._type1 == "orbitars" and self._type2 == "claws") or
            (self._type1 == "claws" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "claws") or
            (self._type1 == "cannon" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "cannon")
        ):
            new_type = "staff"

        if (
            (self._type1 == "blade" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "blade") or
            (self._type1 == "claws" and self._type2 == "club" or self._type1 == "club" and self._type2 == "claws") or
            (self._type1 == "claws" and self._type2 == "cannon" or self._type1 == "cannon" and self._type2 == "claws") or
            (self._type1 == "palm" and self._type2 == "orbitars" or self._type1 == "orbitars" and self._type2 == "palm") or
            (self._type1 == "arm" and self._type2 == "arm")
        ):
            new_type = "bow"

        if (
            (self._type1 == "staff" and self._type2 == "staff") or 
            (self._type1 == "staff" and self._type2 == "palm" or self._type1 == "palm" and self._type2 == "staff") or
            (self._type1 == "bow" and self._type2 == "bow") or
            (self._type1 == "bow" and self._type2 == "orbitars" or self._type1 == "orbitars" and self._type2 == "bow") or
            (self._type1 == "orbitars" and self._type2 == "orbitars")
        ):
            new_type = "cannon"

        if (
            (self._type1 == "staff" and self._type2 == "cannon" or self._type1 == "cannon" and self._type2 == "staff") or
            (self._type1 == "bow" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "bow") or
            (self._type1 == "palm" and self._type2 == "club" or self._type1 == "club" and self._type2 == "palm") or
            (self._type1 == "palm" and self._type2 == "cannon" or self._type1 == "cannon" and self._type2 == "palm") or
            (self._type1 == "club" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "club")
        ):
            new_type = "blade"

        if (
            (self._type1 == "staff" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "staff") or
            (self._type1 == "bow" and self._type2 == "cannon" or self._type1 == "cannon" and self._type2 == "bow") or
            (self._type1 == "palm" and self._type2 == "arm" or self._type1 == "arm" and self._type2 == "palm") or
            (self._type1 == "club" and self._type2 == "club") or
            (self._type1 == "club" and self._type2 == "cannon" or self._type1 == "cannon" and self._type2 == "club")
        ):
            new_type = "orbitars"

        # Deal with all exception cases.
        
        if (
            (self.weapon1 == "samurai blade" and self.weapon2 == "earthmaul club") or
            (self.weapon1 == "earthmaul club" and self.weapon2 == "samurai blade") or
            (self.weapon1 == "angel bow" and self.weapon2 == "drill arm") or
            (self.weapon1 == "drill arm" and self.weapon2 == "angel bow")
        ):
            new_type = "orbitars"
        if (
            (self.weapon1 == "rose staff" and self.weapon2 == "eyetrack orbitars") or
            (self.weapon1 == "eyetrack orbitars" and self.weapon2 == "rose staff") or
            (self.weapon1 == "knuckle staff" and self.weapon2 == "end-all arm") or
            (self.weapon1 == "end-all arm" and self.weapon2 == "knuckle staff") or 
            (self.weapon1 == "dark pit staff" and self.weapon2 == "fortune bow") or 
            (self.weapon1 == "fortune bow" and self.weapon2 == "dark pit staff")
        ):
            new_type = "blade"
        if (
            (self.weapon1 == "somewhat staff" and self.weapon2 == "virgo palm") or 
            (self.weapon1 == "virgo palm" and self.weapon2 == "somewhat staff") or
            (self.weapon1 == "pudgy palm" and self.weapon2 == "fireworks cannon") or
            (self.weapon1 == "fireworks cannon" and self.weapon2 == "pudgy palm")
        ):
            new_type = "arm"
        if (
            (self.weapon1 == "stealth claws" and self.weapon2 == "violet palm") or 
            (self.weapon1 == "violet palm" and self.weapon2 == "stealth claws") or 
            (self.weapon1 == "shock orbitars" and self.weapon2 == "volcano arm") or
            (self.weapon1 == "volcano arm" and self.weapon2 == "shock orbitars")
        ):
            new_type = "cannon"
        if (
            (self.weapon1 == "hedgehog claws" and self.weapon2 == "ogre club") or
            (self.weapon1 == "ogre club" and self.weapon2 == "hedgehog claws") or
            (self.weapon1 == "angel bow" and self.weapon2 == "phosphora bow") or 
            (self.weapon1 == "phosphora bow" and self.weapon1 == "angel bow")
        ):
            new_type = "palm"
        if (
            (self.weapon1 == "cursed palm" and self.weapon2 == "ball cannon") or
            (self.weapon1 == "ball cannon" and self.weapon2 == "cursed palm")
        ):
            new_type = "club"
        if (
            (self.weapon1 == "ogre club" and self.weapon2 == "rail cannon") or
            (self.weapon1 == "rail cannon" and self.weapon2 == "ogre club")
        ):
            new_type = "staff"

        return new_type

#==============================================================================
# USED TO CREATE AN EMBED SPECIFIC TO THE FUSION CALCULATOR.
#
# Accessed in:
#   plugins/fusion/fusion.py
# ---------------------------------
# Used in functions/methods:
#   calc()
#==============================================================================

def create_embed(name, ranged, melee, mods, weapon_value):
    """
    Purpose: Return an embed message to create.
    
    Parameters: name, ranged, melee, mods, value
    
    Returns: embed or string
    """

    if weapon_value == "100":
        return "That's a 100 value weapon."

    # The only reaspon this block exists is to create an embed
    # containing the weapon image.
    if name is not None:

        # Retrieve the weapon type. This works as a weapon
        # such as "artillery claws" would be split into a list
        # such as ["artillery", "claws"]. At index -1, this would
        # retrieve "claws".
        name_type  = name.lower().split()[-1]
        with open("data/weapon_data/weapon_data.json") as data:
            weapons = json.load(data)

        # Retrieve weapon ID.
        weapon_id = weapons[name_type][name.lower()]
        with open("data/weapon_data/weapon_ids.json") as data:
            weapon_data = json.load(data)

        # Retrieve weapon image.
        weapon_img = weapon_data[name_type][weapon_id][-1]
        
        # Construct an embed.
        embed = (
            hikari.Embed(
            title = ":sparkles: " + name.title() + " :sparkles:",
            description = "Listed below are the value calculator results.",
            color = hikari.Color(0x7D00FF),
            )
            .set_image(weapon_img)
            .add_field(
                name = "Value",
                value = weapon_value
            )
            .add_field(
                name = "Stars",
                value = f"Ranged: {ranged}\nMelee: {melee}",
            )
        )

        # As embed messages cannot have values containing empty strings,
        # only add the following field if the string isn't empty.
        if mods != "":
            embed.add_field(
                name = "Modifiers",
                value = mods
            )

        return embed

    else:
        embed = (
            hikari.Embed(
            title = ":sparkles: Value Calculator :sparkles:",
            description = "Listed below are the value calculator results.",
            color = hikari.Color(0x7D00FF),
            )
            .add_field(
                name = "Value",
                value = weapon_value
            )
            .add_field(
                name = "Stars",
                value = f"Ranged: {ranged}\nMelee: {melee}",
            )
        )
        if mods != "":
            embed.add_field(
                name = "Modifiers",
                value = mods,
            )
            
        return embed

#===================================================================================
# THE FOLLOWING HELPER FUNCTION IS SPECIFIC TO THE FUSION COMMAND, ALTHOUGH IS ALSO
# CALLED IN THE SEARCH COMMAND WHEN THE USER ENTERS JUST TWO WEAPONS.
#
# Accessed in:
#   plugins/fusion/fusion.py
# -----------------------------
# Used in functions/methods:
#   fusion()
#   search()
#====================================================================================

async def simple_fusion(
    ctx: lightbulb.context.Context,
    weapon1: str,
    weapon2: str
):
    """
    Purpose: Construct an embed that displays the result of 
             a fusion.
    
    Returns: new_embed: hikari.Embed
    """

    # Check if either option is None and report to user if True.
    if weapon1 is None or weapon2 is None:
        await ctx.respond("Both weapons need to be entered.")
        return

    # Construct the Resulting weapon object if possible.
    try:
        with open("data/weapon_data/weapon_data.json") as data:
            weapon_data = json.load(data)
        fusion_result = Result(weapon1, weapon2, weapon_data)
    except:
        await ctx.respond("Please enter valid parameters.")
        return

    # Retrieve all necessary parameters to construct
    # the embed that will be sent to the user.
    new_id = fusion_result.newID
    new_type = fusion_result.get_type()
    fusion_group = fusion_result.group()
    with open("data/weapon_data/weapon_ids.json") as data:
        weapon_ids = json.load(data)

    final_data = weapon_ids[new_type][new_id]
    final_weapon = final_data[0]
    weapon_image = final_data[-1]

    new_embed = (
        hikari.Embed(
            title = ":sparkles: Weapon Fusion Result :sparkles:",
            description = "Listed below are the fusion results.",
            color = hikari.Color(0x7D00FF),
        )
        .set_image(weapon_image)
        .add_field(
            name = "Weapon 1",
            value = f"{weapon1.title()}",
            inline = True,
        )
        .add_field(
            name = "Weapon 2",
            value = f"{weapon2.title()}",
            inline = True,
        )
        .add_field(
            name = "Result",
            value = f"{final_weapon.title()}",
            inline = False,
        )
        .add_field(
            name = "Fusion Group",
            value = f"Group {fusion_group}",
            inline = False,
        )
    )
    return new_embed

#=======================================================================
# THE FOLLOWING FUNCTIONS ARE SPECIFIC TO CREATING AND FLIPPING THROUGH
# EMBED MESSAGES WHEN BUTTONS ARE NEEDED.
#
# Accessed in:
#   plugins/fusion/fusion.py
#=======================================================================

async def _handle_pages(
    bot: lightbulb.BotApp,
    author: hikari.User,
    message: hikari.Message,
    pages: list,
    index: int,
    embed_title: str
):
    """
    Purpose: Handle flipping through pages.
    
    Returns: Nothing
    """

    async with bot.stream(hikari.InteractionCreateEvent, 120).filter(
        lambda e: (
            isinstance(e.interaction, hikari.ComponentInteraction) and
            e.interaction.user == author and
            e.interaction.message == message
        )
    ) as stream:
        async for event in stream:
            button_id = event.interaction.custom_id
            if button_id == "next":
                index += 1
                if index > len(pages) - 1:
                    index = 0
            elif button_id == "prev":
                index -= 1
                if index < 0:
                    index = len(pages) - 1
            embed = (
                hikari.Embed(
                title = embed_title,
                description = pages[index],
                color = hikari.Color(0x7D00FF),
            )
            .set_footer(f"Page {index + 1}/{len(pages)}")
        )
            try:
                await event.interaction.create_initial_response(
                    hikari.ResponseType.MESSAGE_UPDATE,
                    embed=embed,
                )
            except hikari.NotFoundError:
                await event.interaction.edit_initial_response(
                    embed=embed,
                )
    await message.edit(
    # Set components to an empty list to get rid of them.
    components=[]
    )


async def _generate_buttons(bot : lightbulb.BotApp):
    """
    Purpose: Create the backward and forward buttons.
    
    Returns: buttons: Squence[hikari.api.ActionRowBuilder]
    """

    buttons = []

    button = bot.rest.build_action_row()

    (
        button.add_button(
            hikari.ButtonStyle.SECONDARY,
            "prev"
        )
        .set_emoji("\u25C0")
        .add_to_container()
        .add_button(
            hikari.ButtonStyle.SECONDARY,
            "next"
        )
        .set_emoji("\u25B6")
        .add_to_container()

    )

    buttons.append(button)

    return buttons

#======================================================================
# THE FOLLOWING FUNCTIONS ARE ALL MEANT TO BE AS A WAY TO CONSTRUCT
# JSON FILES THAT CONTAIN DATA RELEVENT TO SEARCH COMMAND PARAMETERS.
#
# Accessed in:
#   plugins/fuision/fusion.py
#======================================================================

async def _construct_weapon(weapon1, weapon2, weapon_data, weapon_ids):

    # Construct the Resulting weapon object if possible.
    fusion_result = Result(weapon1, weapon2, weapon_data)

    new_id = fusion_result.newID
    new_type = fusion_result.get_type()
    fusion_group = fusion_result.group()

    final_data = weapon_ids[new_type][new_id]
    final_weapon = final_data[0]

    return final_weapon, fusion_group


async def _json_creation_helper(
    ctx: lightbulb.context.Context,
    weapon_data: dict,
    weapon_ids: dict,
    all_weapons: list,
    output_list: list,
    found_list: list,
    temp_results: list,
    searched_for: str,
    is_group = False,
    accepts_result = True
):
    """
    Purpose: Creates pages for search command.
    
    Returns: output_list: list
    """

    # Construct a list of all weapons.
    for category in weapon_data:
        for temp_weapon in weapon_data[category]:
            if temp_weapon == "class id":
                continue
            all_weapons.append(temp_weapon)

    # Now we can deal with cases where the weapon doesn't exist. Only do
    # this in cases where searching by weapon.
    if not is_group:
        if searched_for not in all_weapons:
            await ctx.respond(f"{searched_for.title()} doesn't exist.")
            return
        
    # Find each possible result for each weapon in the game.
    for weapon1 in all_weapons:
        for category in weapon_data:
            for weapon2 in weapon_data[category]:
                if weapon2 == "class id":
                    continue


                # Try to retrieve a new weapon.
                
                weapon, group = await _construct_weapon(weapon1, weapon2, weapon_data, weapon_ids)

                # Construct the resulting pages.
                temp_results = await _construct_by_type(
                    weapon,
                    group,
                    searched_for,
                    temp_results,
                    output_list,
                    found_list,
                    weapon1,
                    weapon2,
                    is_group,
                    accepts_result
                )
                
            
    if temp_results:
        output_list.append(temp_results)

    return output_list

async def _construct_by_type(
    weapon: str,
    group: str,
    searched_for: str,
    temp_results: list,
    output_list: list,
    found_list: list,
    weapon1: str,
    weapon2: str,
    is_group = False,
    accepts_result = True
):
    """
    Purpose: Helper function for json_creation_helper(). Essentially
             determines what to do depending on whether a json is based
             on weapon or group.
             
    Returns: Nothing
    """

    if is_group:
        desired = group
    else:
        desired = weapon

    if accepts_result:

        # If the new weapon exists, construct a list that can represent pages.
        if searched_for == desired:
            if len(temp_results) == 5:
                output_list.append(temp_results)
                temp_results = []

            if f"{weapon1} {weapon2}" in found_list or f"{weapon2} {weapon1}" in found_list:
                return temp_results
            temp_results.append(f"**Weapons**: {weapon1.title()} + {weapon2.title()}\n**Result**: {weapon.title()}\n**Fusion Group**: {group}\n")
            found_list.append(f"{weapon1} {weapon2}")

    elif not accepts_result:

        if weapon1 == searched_for:
            if len(temp_results) == 5:
                output_list.append(temp_results)
                temp_results = []

            if f"{weapon1} {weapon2}" in found_list or f"{weapon2} {weapon1}" in found_list:
                return temp_results
            temp_results.append(f"**Weapons**: {weapon1.title()} + {weapon2.title()}\n**Result**: {weapon.title()}\n**Fusion Group**: {group}\n")
            found_list.append(f"{weapon1} {weapon2}")

    return temp_results


async def _create_result(
    ctx: lightbulb.context.Context,
    result: str,
):

    """
    Purpose: Creates a list of pages if searched by result.
    
    Returns: result_list: list
    """

    # First, deal with cases when the weapon is None.
    with open("data/weapon_data/weapon_data.json") as data:
        weapon_data = json.load(data)
    with open("data/weapon_data/weapon_ids.json") as data:
        weapon_ids = json.load(data)

    result_list = []
    temp_results = []
    all_weapons = []
    found_list = []

    # Construct the result list.
    result_list = await _json_creation_helper(
        ctx,
        weapon_data,
        weapon_ids,
        all_weapons,
        result_list,
        found_list,
        temp_results,
        result,
        is_group = False,
        accepts_result = True
    )

    # Save the new list to a file and return it.
    temp_name = result.replace(" ", "_")
    with open(f"data/fusion_data/by_result/{temp_name}.json", "w") as data:
        json.dump(result_list, data, indent = 2)

    return result_list


async def _create_weapons(
    ctx: lightbulb.context.Context,
    weapon: str = None
):
    """
    Purpose: Creates a list of pages if searched by weapon.
    
    Returns: weapon_list: list
    """

    # First, deal with cases when the weapon is None.
    with open("data/weapon_data/weapon_data.json") as data:
        weapon_data = json.load(data)
    with open("data/weapon_data/weapon_ids.json") as data:
        weapon_ids = json.load(data)

    weapon_list = []
    temp_results = []
    all_weapons = []
    found_list = []

    # Construct the result list.
    weapon_list = await _json_creation_helper(
        ctx,
        weapon_data,
        weapon_ids,
        all_weapons,
        weapon_list,
        found_list,
        temp_results,
        weapon,
        is_group = False,
        accepts_result = False
    )

    # Save the new list to a file and return it.

    weapon_temp = weapon.replace(" ", "_")
    
    with open(f"data/fusion_data/by_weapon/{weapon_temp}.json", "w") as data:
        json.dump(weapon_list, data, indent = 2)

    return weapon_list

async def _create_group(
    ctx: lightbulb.context.Context,
    group: str,
):
    """
    Purpose: Creates a list of pages if searched by group.
    
    Returns: output_list: list
    """

    with open("data/weapon_data/weapon_data.json") as data:
        weapon_data = json.load(data)
    with open("data/weapon_data/weapon_ids.json") as data:
        weapon_ids = json.load(data)

    output_list = []
    temp_results = []
    all_weapons = []
    found_list = []

    output_list = await _json_creation_helper(
        ctx,
        weapon_data,
        weapon_ids,
        all_weapons,
        output_list,
        found_list,
        temp_results,
        group,
        is_group = True,
        accepts_result = True
    )

    with open(f"data/fusion_data/by_group/group_{group}.json", "w") as data:
        json.dump(output_list, data, indent = 2)

    return output_list

#===========================================================================
# THE FOLLOWING HELPER FUNCTIONS ARE ALL SUB-HELPER FUNCTIONS FOR THE MAIN
# HELPER FUNCTIONS THAT WILL BE CALLED IN THE SEARCH COMMAND.
#
# Accessed in:
#   utils/fusion_utils.py
#===========================================================================

async def _button_handling(
    ctx: lightbulb.context.Context,
    searchType: str,
    is_search: str,
    page_list: list
):
    """
    Purpose: Specifically used to handle turning pages
             in the search command.
             
    Returns: Nothing
    """

    # Generate the buttons.
    buttons = await _generate_buttons(ctx.bot)

    # Create an initial response.
    response = await ctx.respond(
        hikari.Embed(
            title = f":sparkles: {is_search}: {searchType.title()} :sparkles:",
            description = page_list[0],
            color = hikari.Color(0x7D00FF),
        )
        .set_footer(f"Page 1/{len(page_list)}"),
        components = buttons
    )

    message = await response.message()

    # Hande changing pages.

    await _handle_pages(
        ctx.bot,
        ctx.author,
        message,
        page_list,
        index = 0,
        embed_title = f":sparkles: {is_search}: {searchType.title()} :sparkles:"
    )


async def _construct_result_list(
    ctx: lightbulb.context.Context,
    result: str
):
    """
    Purpose: Creates the result list if needed.
    
    Returns: result_list: list
    """

    try:
        temp_result = result.replace(" ", "_")
        with open(f"data/fusion_data/by_result/{temp_result}.json") as data:
            result_list = json.load(data)

    except:
        result_list = await _create_result(ctx, result)
    
    return result_list


async def _construct_weapon_list(
    ctx: lightbulb.context.Context,
    weapon: str
):
    """
    Purpose: Creates the weapon list if needed.
    
    Returns: weapon_list: list
    """

    weapon_temp = weapon.replace(" ", "_")
    try:
        with open(f"data/fusion_data/by_weapon/{weapon_temp}.json") as data:
            weapon_list = json.load(data)

    except:
        weapon_list = await _create_weapons(ctx, weapon)

    return weapon_list


async def _construct_group_list(
    ctx: lightbulb.context.Context,
    group: str
):
    try:
        with open(f"data/fusion_data/by_group/group_{group}.json") as data:
            group_list = json.load(data)
    
    except:
        group_list = await _create_group(ctx, group)

    return group_list

#===========================================================================
# THE FOLLOWING FUNCTIONS ARE TO BE CALLED DIRECTLY IN THE SEARCH COMMAND.
#
# Accessed by:
#   plugins/fusion/fusion.py
# ----------------------------
# Used in functions/methods:
#   search()
#===========================================================================

async def result_only(
    ctx: lightbulb.context.Context,
    result: str
):
    """
    Purpose: Handles cases when searched by result only. Creates
             pages and embed.
             
    Returns: Nothing
    """

    # Make lowercase.
    result = result.lower()

    # Retrieve the result list.
    result_list = await _construct_result_list(ctx, result)
    if result_list is None: return

    # Construct a list containing strings.
    page_list = []
    for page in result_list:
        string = "\n".join(page)
        page_list.append(string)

    await _button_handling(ctx, result, "Search by Result", page_list)


async def weapons_only(
    ctx: lightbulb.context.Context,
    weapon1,
    weapon2,
):
    """
    Purpose: Handles cases when searched by result only. Creates
             pages and embed.
             
    Returns: Nothing
    """

    if weapon1 is None:
        weapon: str = weapon2
    else:
        weapon: str = weapon1

    weapon: str = weapon.lower()

    weapon_list = await _construct_weapon_list(ctx, weapon)

    page_list = []
    for page in weapon_list:
        string = "\n".join(page)
        page_list.append(string)

    await _button_handling(ctx, weapon, "Search by Weapon", page_list)


async def group_only(
    ctx: lightbulb.context.Context,
    group: str
):
    """
    Purpose: Handles cases when searched by group only. Creates
             pages and embed.
             
    Returns: Nothing
    """

    if not group.isdigit():
        await ctx.respond("The group entered is not valid.")
        return

    group_list = await _construct_group_list(ctx, group)
    if group_list is None: return

    page_list = []
    for page in group_list:
        string = "\n".join(page)
        page_list.append(string)
    
    await _button_handling(ctx, f"Group {group}", "Search by", page_list)


async def result_and_weapon(
    ctx: lightbulb.context.Context,
    weapon1: str,
    weapon2: str,
    result: str
):
    """
    Purpose: Deals when cases when searched by result and weapon.
             creates an embed.
             
    Returns: Nothing
    """

    # Retrieve the weapon that isn't none.
    if weapon1 is not None:
        weapon = weapon1
    else:
        weapon = weapon2

    # Make the weapon lowercase.
    weapon = weapon.lower()
    result = result.lower()

    # Retrieve the result list.
    result_list = await _construct_result_list(ctx, result)
    if result_list is None: return

    # This part differs from the previous case, as it creates a string out of
    # fusions that include the weapon given.

    final_string = ""
    for page in result_list:
        for line in page:
            if weapon.title() in line:
                final_string += f"{line}\n"

    # Catch cases where it isn't possible (If that even exists lol).
    if not final_string:
        await ctx.respond(f"{result.title()} can't be made from the {weapon.title()}.")
        return

    embed = (
        hikari.Embed(
            title = f":sparkles: Search by Result and Weapon :sparkles:",
            description = final_string,
            color = hikari.Color(0x7D00FF),
        )
    )

    await ctx.respond(embed)


async def result_and_group(
    ctx: lightbulb.context.Context,
    result: str,
    group: str
):
    """
    Purpose: Deals with cases when searching by result and group.
             Creates an embed and pages.
             
    Returns: Nothing
    """

    result = result.lower()
    if not group.isdigit():
        await ctx.respond("The fusion group must be a digit.")
        return

    # Retrieve the result list.
    result_list = await _construct_result_list(ctx, result)
    if result_list is None: return

    # The following loop creates pages only containing fuses of the 
    # specified fusion group.
    page_list = []
    string = ""
    count = 0
    for page in result_list:
        for line in page:
            if count == 5:
                page_list.append(string)
                count = 0
                string = ""
            if group in line:
                string += f"{line}\n"
                count += 1
    if string:
        page_list.append(string)

    await _button_handling(ctx, f"{result} & Group {group}", "Result", page_list)


async def weapon_and_group(
    ctx: lightbulb.context.Context,
    group: str,
    weapon1,
    weapon2
):
    """
    Purpose: Deals with cases when searching by weapon and group.
             Creates pages and embeds.
             
    Returns: Nothing
    """

    # Create the weapon string.
    if weapon1 is None:
        weapon: str = weapon2
    else:
        weapon: str = weapon1

    weapon = weapon.lower()

    # Get the weapon list.
    weapon_list = await _construct_weapon_list(ctx, weapon)
    if weapon_list is None: return

    # The following loop creates pages only containing fuses of the 
    # specified fusion group.
    page_list = []
    string = ""
    count = 0
    for page in weapon_list:
        for line in page:
            if count == 5:
                page_list.append(string)
                count = 0
                string = ""
            if group in line:
                string += f"{line}\n"
                count += 1
    if string:
        page_list.append(string)

    await _button_handling(ctx, f"{weapon} & Group {group}", "Weapon", page_list)