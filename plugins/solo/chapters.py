"""------------------------------------------------------------
Author: Schuyler Kelly
Date: 11/16/2021
Edited: 11/16/2021
Purpose:
    Add scores to solo chapters.
------------------------------------------------------------"""
import hikari
import lightbulb
from lightbulb import commands, context
import json

# Construct the chapter plugin.
chapter_plugin = lightbulb.Plugin("Chapter")

# Construct the first chapter command, soloscore.
@chapter_plugin.command
@lightbulb.option("member", "A list of members whose scores can be registered.", hikari.User)
@lightbulb.option("score", "The score of the user.", int)
@lightbulb.option("chapter", "The number for the chapter the score was achieved for.", str)
@lightbulb.command("soloscore", "Allows admins and volunteers to add scores for users.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def soloscore(ctx : context.Context):

    # Create a score variable.

    score = ctx.options.score

    # The following makes sure that only admins and volunteers can
    # call the command.

    valid = False
    for role in ctx.member.get_roles():
        if (
            role.name == "Point Secretary and Spreader of Sheets" or
            role.permissions.ADMINISTRATOR
        ):
            valid = True

    if not valid:
        await ctx.respond("Only admins and volunteers are allowed to use this command.")
        return

    # Makes sure that all necessary parameters are given.
    if ctx.options.member is None or ctx.options.score is None or ctx.options.chapter is None:
        await ctx.respond("Please enter both member and score fields.")
        return

    # Retrieve the member object.
    member = ctx.get_guild().get_member(ctx.options.member)
    member_id = str(member.id)

    with open("data/chapter_data.json") as data:
        chapter_data = json.load(data)

    # Make sure the chapter given is still valid.
    try:
        chapter = chapter_data[ctx.options.chapter]
    except:
        await ctx.respond(f"{ctx.options.chapter} is not a valid chapter number.")
        return

    # Deal with cases where the leaderboard is empty.

    leaderboard = chapter["leaderboard"]

    if not leaderboard:
        leaderboard.insert(0, f"{member_id} {score}")
        with open("data/chapter_data.json", "w") as data:
            json.dump(chapter_data, data, indent = 2)
        await ctx.respond(f"{member.display_name}'s score of {score} has been added!")
        return

    # Create a value to check if it's been inserted.
    inserted = False
    to_pop = None
    for index in range(len(leaderboard)):

        # Split the user's score to be interpreted. 
        temp_user, temp_score = leaderboard[index].split()
        temp_score = int(temp_score)

        # Deal with all cases of the member already having a score.
        if temp_user == member_id and temp_score > score:
            await ctx.respond(f"{member.display_name} already has a higher score!")
            return
        elif temp_user == member_id and temp_score <= score:
            to_pop = index

        # If the member's score hasn't been inserted, insert it.
        if not inserted and score > temp_score:
            leaderboard.insert(index, f"{member_id} {score}")
            inserted = True

    # Deal with cases when the value still isn't inserted.

    if not inserted:
        leaderboard.append(f"{member_id} {score}")

    # Deal with cases where the last user score is in the last element
    # of the list, which wasn't looked at. Also pop the user's previous score
    # if it exists.
    else:
        last = leaderboard[-1]
        last_user, temp_score = last.split()
        if last_user == member_id:
            leaderboard.pop(-1)
        elif to_pop is not None:
            leaderboard.pop(to_pop)

    # Save the data.
    with open("data/chapter_data.json", "w") as data:
        json.dump(chapter_data, data, indent = 2)

    await ctx.respond(f"{member.display_name}'s score of {score} has been added!")
    return

# Construct the second chapter command, chapter.
@chapter_plugin.command
@lightbulb.option("number", "Please enter the chapter number.", str)
@lightbulb.command("chapter", "A command that sends chapter data.", aliases = ["ch"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def chapter(ctx: context.Context):

    # Make sure that chapter isn't none.
    if ctx.options.number is None:
        await ctx.respond("A chapter needs to be given.")
        return

    # Retrieve the chpater number.
    num = ctx.options.number.strip()

    with open("data/chapter_data.json") as data:
        chapter_data = json.load(data)

    # Make sure the chapter is valid.
    try:
        chapter = chapter_data[num]
    except:
        await ctx.respond(f"{num} isn't a valid chapter number.")
        return
    
    title = chapter["name"]
    weapons = chapter["weapons"]
    img = chapter["img"]
    old_leaderboard = chapter["leaderboard"]

    leaderboard = ""
    for rank in range(5):
        try:
            member_id, score = old_leaderboard[rank].split()
            member = ctx.get_guild().get_member(int(member_id))
            leaderboard += f"{rank + 1}. {member.display_name}: {score}\n"
        except:
            break

    embed = (
        hikari.Embed(
            title = f"{title}",
            description = f"Drop data and leaderboards for {title}!",
            color = hikari.Color(0x7D00FF),
        )
        .set_thumbnail(img)
        .add_field(
            name = "Weapon Drops",
            value = weapons,
            inline = True
        )
    )

    if leaderboard != "":
        embed.add_field(
            name = "Leaderboards",
            value = leaderboard,
            inline = True
        )

    await ctx.respond(embed)
    return


def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(chapter_plugin)