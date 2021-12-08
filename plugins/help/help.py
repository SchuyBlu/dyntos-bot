"""------------------------------------------------
Author: Schuyler Kelly
Date: 11/14/2021
Edited: 11/14/2021
Purpose:
    Create a help message to send to the user.
------------------------------------------------"""
import hikari
import lightbulb
from lightbulb import commands, context
from datetime import datetime
import asyncio

# Construct the plugin.
help_plugin = lightbulb.Plugin("Help")

@help_plugin.command
@lightbulb.command("help", "Sends a help message.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def help(ctx : context.Context):

    # Retrieve the user and fetch the DM channel.
    user = ctx.user
    user_dms = await user.fetch_dm_channel()

    # Create an embed message that will be the help message.
    embed_message = (
        hikari.Embed(
            title = ":sparkles: Dyntos :sparkles:",
            description = "Hello! All commands, as listed below, are slash commands rather than prefix commands.",
            color = hikari.Color(0x7D00FF),
        )
        .add_field(
            name = "Banlist Commands",
            value = (
                ":small_blue_diamond: */banlist* :small_blue_diamond:\n"
                "This command allows users to check the banlist in place.\n\n"
                "Admin only Banlist Commands:\n"
                ":small_blue_diamond: */banweapons: weapon(s)* :small_blue_diamond:\n"
                "This command allows admins to add weapons to the banlist.\n\n"
                ":small_blue_diamond: */unbanweapons: weapon(s)* :small_blue_diamond:\n"
                "This command allows admins to remove weapons from the banlist.\n\n"
                ":small_blue_diamond: */banpowers: power(s)* :small_blue_diamond:\n"
                "This command allows admins to add powers to the banlist.\n\n"
                ":small_blue_diamond: */unbanpowers: power(s)* :small_blue_diamond:\n"
                "This command allows admins to remove powers from the banlist.\n\n"
                ":small_blue_diamond: */banlistreset* :small_blue_diamond:\n"
                "This command allows admins to completely reset the banlist."
            ),
        )
        .add_field(
            name = "Fusion Commmands",
            value = (
                ":small_blue_diamond: */fusion* :small_blue_diamond:\n"
                "This command allows users to check the fusion result, including fusion group, of two weapons.\n\n"
                ":small_blue_diamond: */calc: mods 1-6, stars, name(optional)* :small_blue_diamond:\n"
                "This command allows the user to calculate the value of a potential weapon.\n\n"
                ":small_blue_diamond: */search: weapon1, weapon2, group, result* :small_blue_diamond:\n"
                "Please only enter two parameters. This command allows you to make complex fusion "
                "result searches according to your chosen paramters."
            ),
        )
        .add_field(
            name = "Solo Commands",
            value = (
                ":small_blue_diamond: */chapter: number* :small_blue_diamond:\n"
                "This command allows you to check common drops and score leaderboard for a chapter.\n\n"
                "Admin only Solo Commands:\n"
                ":small_blue_diamond: */soloscore: chapter, score, member* :small_blue_diamond:\n"
                "This command allows admins and volunteers to add a chapter score for a member."
            ),
        )
        .add_field(
            name = "Profile Commands",
            value = (
                ":small_blue_diamond: */userinfo: member(Optional)* :small_blue_diamond:\n"
                "This command allows the user to request any server member's profile."
            ),
        )
        .add_field(
            name = "Fun Commands",
            value = (
                ":small_blue_diamond: */uwuify : text* :small_blue_diamond:\n"
                "This command allows the user to turn any text they type into uwu style text.\n\n"
                ":small_blue_diamond: */slap: member* :small_blue_diamond:\n"
                "This commands allows you to slap another server member. Have fun!"
            )
        )
    )

    # Send the help message.
    help_message = await user_dms.send(embed_message)
    await ctx.respond("Help message sent!")

    # Sleep the program and delete the message.
    await asyncio.sleep(900)
    await help_message.delete()
    return

def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(help_plugin)