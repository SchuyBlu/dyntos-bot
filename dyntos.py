"""------------------------------------------------
Author: Schuyler Kelly
Date: 11/01/2021
Edited: 11/02/2021
Purpose: 
    Create a multipurpose bot for the Kid icarus
    Uprising Multiplayer discord server.
------------------------------------------------"""
import hikari
import lightbulb

with open("secrets/token", "r") as a_file:
    token = a_file.read().strip()

extensions = [
    "plugins/banlist",
    "plugins/fun",
    "plugins/fusion",
    "plugins/help",
    "plugins/profile",
    "plugins/solo"
]

# Construct bot instance.
bot = lightbulb.BotApp(
    token, prefix = "$",
    intents = hikari.Intents.ALL,
    help_class = None,
    banner = "dyntos_banner",
    default_enabled_guilds = (
        707504970777231381, 
        814033573614452758,
    )
)

# Load all bot extensions.
for extension in extensions:
    bot.load_extensions_from(extension, must_exist = True)
bot.run(
    activity = hikari.Activity(name = "/help or $help")
)