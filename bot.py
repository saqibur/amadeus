from amadeus import (
    config,
    images,
    dialogue
)

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

import requests
from random import choice
import random as py_random
from string import ascii_letters

from asyncio import sleep
import dropbox
import io

import os
import os.path

# TODO: There might be a way to re-use the CDN images. Try and do some research
#       into this.

instantiated_dropbox = dropbox.Dropbox(config.DROPBOX_SECRET)

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("ama-"),
    case_insensitive=True,
    description="""
            Amadeus is the name of a memory storage ~~and artificial intelligence~~ system.
            React to an image with :ama_save: and I'll save it to the dropbox.
        """,
)

### EVENTS ###

# @bot.event
# async def on_message(message):
#     if bot.user.mentioned_in(message):
#         await message.channel.send(dialogue.random_kurisu_line())

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        # await ctx.send("I don't really know how to do that. Sorry. Trying using the `halp` or `help` command instead.")
        # await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.ERROR)}")
        await ctx.channel.send(dialogue.random_kurisu_line())
        return
    raise error


@bot.event
async def on_ready():
    print(f'Signed in as {bot.user}')
    await bot.get_channel(config.AMADUES_CHANNEL_ID).send(
        "Amadeus is back online!",
        file=images.amadeus_images.get(images.AMADEUS_IMAGES.BACK_ONLINE),
    )


@bot.event
async def on_reaction_add(reaction, user):
    if str(reaction) == config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.SAVE):
        if config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.SAVED) in [str(reaction) for reaction in reaction.message.reactions]:
            await bot.get_channel(config.AMADUES_CHANNEL_ID).send("I've already saved this before.")
            await bot.get_channel(config.AMADUES_CHANNEL_ID).send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.TSUNDERE)}")
        else:
            await bot.get_channel(config.AMADUES_CHANNEL_ID).send("Trying to save...")
            await bot.get_channel(config.AMADUES_CHANNEL_ID).send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.SAVE)}")

            for attachment in reaction.message.attachments:
                url = attachment.url
                image_file = requests.get(url)

                filename = ''.join(choice(ascii_letters) for i in range(24))

                instantiated_dropbox.files_upload(image_file.content, f"/screenshots/{filename}.jpg")

                await bot.get_channel(config.AMADUES_CHANNEL_ID).send(f"I think I saved it... {user.mention}")
                await reaction.message.add_reaction(config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.SAVED))
    else:
        print("Nothing to save!")


### COMMANDS ###

@bot.command()
async def halp(ctx):
    await ctx.channel.send(f"Use the :ama_save: react to save an image to the shared dropbox!")
    sayings = os.listdir("audio/sayings/")
    cleaned_sayings = [ saying[:-4] for saying in sayings ]
    await ctx.channel.send(f"Things I can say: {cleaned_sayings}")

    songs = os.listdir("audio/songs/")
    cleaned_songs = [ song[:-4] for song in songs ]
    await ctx.channel.send(f"Things I can sing: {cleaned_songs}")


@bot.command()
async def christina(ctx):
    await ctx.channel.send(f"Tina ja nai yo. {ctx.message.author.mention} no baka.")
    await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.TSUNDERE)}")


@bot.command()
async def say(ctx, file_name):
    print(file_name)
    if os.path.isfile("audio/sayings/" + file_name + ".mp3"):
        user = ctx.message.author
        voice_channel = user.voice.channel
        channel = None

        if voice_channel != None:
            channel = voice_channel.name
            await ctx.send(f"~Entering `{channel}`~")
            await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.ENTERS_VC)}")

            vc = await voice_channel.connect()
            vc.play(
                discord.FFmpegPCMAudio("audio/sayings/" + file_name + ".mp3"),
                after=lambda e: print('Started playing', e),
            )

            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()
            await ctx.send(f"~Left `{channel}`~")
            await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.EXITS_VC)}")
        else:
            await ctx.send('User is not in a channel.')
            await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.ERROR)}")
    else:
        await ctx.send(f"I don't know how to say `{file_name}`")
        await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.ERROR)}")

@bot.command()
async def sing(ctx, file_name):
    print(file_name)
    if os.path.isfile("audio/songs/" + file_name + ".mp3"):
        user = ctx.message.author
        voice_channel = user.voice.channel
        channel = None

        if voice_channel != None:
            channel = voice_channel.name

            vc = None

            if ctx.voice_client is not None:
                vc = ctx.voice_client
                vc.stop()
            else:
                await ctx.send(f"~Entering `{channel}`~")
                await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.ENTERS_VC)}")
                vc = await voice_channel.connect()

            vc.play(
                discord.FFmpegPCMAudio("audio/songs/" + file_name + ".mp3"),
                after=lambda e: print('Started playing', e),
            )

            while vc.is_playing():
                await sleep(1)
            await vc.disconnect()
            await ctx.send(f"~Left `{channel}`~")
            await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.EXITS_VC)}")
        else:
            await ctx.send('User is not in a channel.')
            await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.ERROR)}")
    else:
        await ctx.send(f"I don't know how to sing `{file_name}`")
        await ctx.channel.send(f"{config.AMADEUS_EMOJIS.get(config.AMADEUS_EMOJI.ERROR)}")


@bot.command()
async def random(ctx):
    await ctx.channel.send("Getting a random picture...")
    the_chosen_one = py_random.choice(instantiated_dropbox.files_list_folder("/screenshots").entries)

    _, res = instantiated_dropbox.files_download(path=f"/screenshots/{the_chosen_one.name}")


    f = io.BytesIO(res.content)

    picture = discord.File(f, filename=the_chosen_one.name)

    await ctx.channel.send(file=picture)



bot.run(config.DISCORD_SECRET)



## Possibly proper way to do it.
# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as', self.user)

#     async def on_message(self, message):
#         # Don't respond to ourselves
#         if message.author == self.user:
#             return

#         # If bot is mentioned, reply with a message
#         if self.user in message.mentions:
#             await message.channel.send("You can type `!vx help` for more info.")
#             return

# def main():
#     client = MyClient()
#     client.run(DISCORD_TOKEN)

# if __name__ == "__main__":
#     main()