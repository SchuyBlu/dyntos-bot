"""---------------------------------------------------
Author: Schuyler Kelly
Date: 11/16/2021
Edited: 11/16/2021
Purpose:
    Slap a user.
---------------------------------------------------"""
import hikari
import lightbulb
from lightbulb import commands, context
from lightbulb.commands.base import OptionModifier
from PIL import Image
import urllib.request
from io import BytesIO
import random
import json

# Construct the plugin.
fun_plugin = lightbulb.Plugin("Fun")

# Construct the first command, slap.
@fun_plugin.command
@lightbulb.option("slapped", "User to be slapped.", hikari.User)
@lightbulb.command("slap", "Slap a user.", aliases = ["s"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def slap(ctx : context.Context):

    if ctx.options.slapped is None:
        await ctx.respond("Please tag a user to be slapped.")
        return

    # Send femboy Pit if the caller tries to get pit to slap
    # himself.
    
    member = ctx.get_guild().get_member(ctx.options.slapped)
    user = ctx.get_guild().get_member(ctx.member)

    # Create slap phrases and pick arandom one.
    slap_phrase = [
        f"{member.display_name} got the shit slapped out of them by {user.display_name}!",
        f"{member.display_name} got slapped hard by {user.display_name}!",
        f"{member.display_name} was disrespected by {user.display_name}!",
        f"{member.display_name} was hurt on an emotional level by {user.display_name}!",
        f"{user.display_name} gave {member.display_name} a little love tap!",
        f"{member.display_name} was patched out of the game by {user.display_name}!",
        f"{member.display_name} asked {user.display_name} to slap them real hard <:paludegenerate:723610957066010677>"
    ]

    choice = random.choice(slap_phrase)

    # Retrieve and save the member avatar.
    member_photo = member.guild_avatar_url
    if member_photo is None:
        member_photo = member.display_avatar_url
    req = urllib.request.Request(str(member_photo), headers = {"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        img = r.read()

    # Retrieve and save the user avatar.
    user_photo = user.guild_avatar_url
    if user_photo is None:
        user_photo = user.display_avatar_url
    req = urllib.request.Request(str(user_photo), headers = {"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        img2 = r.read()

    # Convert to bytes.
    file_img = BytesIO(img) 
    file_img2 = BytesIO(img2)

    # Using pillow, create a slap image.
    batman = Image.open("images/batman_slap.jpg")

    # Retrieve both user and member images and resize.
    temp1 = Image.open(file_img)
    temp1 = temp1.resize((256, 256), Image.Resampling.LANCZOS)
    temp2 = Image.open(file_img2)
    temp2 = temp2.resize((256, 256), Image.Resampling.LANCZOS)

    # Paste both user images.
    batman.paste(temp1, (320, 235))
    batman.paste(temp2, (735, 60))
    output = BytesIO()
    batman.save(output, format = "jpeg")
    output.seek(0)

    # Send the message and edit it.
    await ctx.respond(
        content = choice,
        attachment = hikari.Bytes(output, "batman_slap.jpg")
    )
    #await message.edit(
    #    content = choice,
    #    attachment = hikari.Bytes(output, "batman_slap.jpg")
    #    )
    
    # Close all files opened.
    batman.close()
    temp1.close()
    temp2.close()
    return

# Construct the second command, uwuify.
@fun_plugin.command
@lightbulb.option("text", "Text to be uwuified.", str, modifier = OptionModifier.CONSUME_REST)
@lightbulb.command("uwuify", "Uwuifies text", aliases = ["u", "uwu"])
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def uwuify(ctx : context.Context):

    if ctx.options.text is None:
        await ctx.respond("I c-cwan't rweswond tuwu nwothwing!")
        return

    # Make sure characters fit within discord limits.
    if len(ctx.options.text) > 2000:
        await ctx.respond("Messages on discord can't be more than 2000 characters you moron.")
        return

    # Uwuify the text!

    text = ctx.options.text

    with open("data/creepy_asterisk.json", "r") as data:
        creepy = json.load(data)

    # Repalce words, phrases, and letters to uwuify!
    word_list = text.split()
    for number, word in enumerate(word_list):
        if word == "my":
            word_list[number] = "mwy"
        elif word == "to":
            word_list[number] = "tuwu"
        elif word == "had":
            word_list[number] = "hawd"
        elif word == "you":
            word_list[number] = "yuw"
        elif word == "go":
            word_list[number] = "gow"
        elif word == "and":
            word_list[number] = "awnd"
        elif word == "have":
            word_list[number] = "haw"
        
        else:
            word = word.replace("ll", "w").replace("r", "w").replace("l", "w").replace("th", "d").replace("fu", "fwu").replace("y", "wy")
            word_list[number]=word
            
        if random.randrange(0,11) == 1:
            word_list[number] = word[0]+"-"+word
            
        if "." in word:
            word_list[number] = word_list[number] + " " + random.choice(creepy)
        if "!" in word:
            word_list[number] = word_list[number] + " " + random.choice(creepy)
        if "?" in word:
            word_list[number] = word_list[number] + " " + random.choice(creepy)
            
        
    final = " ".join(word_list)
    try:
        await ctx.respond(final)
    except:
        await ctx.respond("Message was unable to send.")
    return

@fun_plugin.command
@lightbulb.option("string", "Message to send to a channel.", str, modifier = OptionModifier.CONSUME_REST)
@lightbulb.command("send", "A command to send a message to a channel.")
@lightbulb.implements(commands.PrefixCommand)
async def send(ctx: context.Context):

    if ctx.author.id != 714615961830948964:
        return

    message: str = ctx.options.string
    stringlist: list = message.split()
    
    # Remove both unecessary parts of the string.
    channel_id = stringlist.pop(0)
    message = " ".join(stringlist)

    channel_id = int(channel_id)

    # Send a message in the channel.
    await ctx.bot.rest.create_message(channel = channel_id, content = message)
    await ctx.respond("Message sent!")
    return

@fun_plugin.command
@lightbulb.option("member", "The member whose profile pic you want to retreive.", hikari.User)
@lightbulb.command("pfp", "A command to get profile pics.")
@lightbulb.implements(commands.SlashCommand)
async def profile_command(ctx: context.Context):

    # Get the member snowflake.
    member = ctx.options.member

    # Error check to make sure it was entered.
    if member is None:
        await ctx.respond("Please tag a valid member.")
        return

    # Get the member object and avatar using the snowflake.
    member = ctx.get_guild().get_member(member)
    member_pfp = member.avatar_url

    # Send the avatar.
    await ctx.respond(str(member_pfp))
    return
    
    

def load(bot : lightbulb.BotApp) -> None:
    bot.add_plugin(fun_plugin)