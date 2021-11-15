import io
from os.path import splitext
from random import choice
from string import ascii_letters
from typing import Optional

import requests
from requests import Response
from discord import (
    Attachment,
    File,
    Reaction,
    User,
)
from discord.ext.commands import (
    Bot,
    Context,
    Cog,
    command,
)

from amadeus.library.dropbox_handler import (
    fetch_filenames,
    retrieve_file_content,
    save_file,
)

class Memories(Cog):
    bot:                  Bot
    _file_save_reaction:  str
    _file_saved_reaction: str

    _VALID_IMAGE_EXTENSIONS: list[str] = ['.jpg', '.png', '.gif', '.webp']
    _VALID_VIDEO_EXTENSIONS: list[str] = ['.mp4']
     # TODO: Need to be able to support .ogg and .wav
    _VALID_AUDIO_EXTENSIONS: list[str] = ['.mp3']


    def __init__(self, bot: Bot):
        self.bot                  = bot
        self._file_save_reaction  = self.bot.configuration.discord_config.file_save_reaction
        self._file_saved_reaction = self.bot.configuration.discord_config.file_saved_reaction


    def _determine_save_location(self, extension: str) -> Optional[str]:
        if extension in self._VALID_IMAGE_EXTENSIONS:
            return self.bot.configuration.dropbox_config.dir_images
        elif extension in self._VALID_VIDEO_EXTENSIONS:
            return self.bot.configuration.dropbox_config.dir_videos
        elif extension in self._VALID_AUDIO_EXTENSIONS:
            return self.bot.configuration.dropbox_config.dir_music
        else:
            return None


    def _save_attachment(self, attachment: Attachment) -> bool:
        filename, extension = splitext(attachment.filename)
        file: Response      = requests.get(attachment.url)

        match self._determine_save_location(extension):
            case None:
                return False
            case str(save_path):
                def determine_file_save_name(filename: str) -> str:
                    if extension in self._VALID_IMAGE_EXTENSIONS:
                        return ''.join(choice(ascii_letters) for _ in range(24))
                    else:
                        return filename

                save_file(
                    dbx_client = self.bot.dropbox_client,
                    filename   = (determine_file_save_name(filename) + extension),
                    save_path  = save_path,
                    file       = file.content,
                )

                return True


    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: User):
        if reaction.emoji != self._file_save_reaction:
            return

        if (
            self._file_saved_reaction in
            [ reaction.emoji for reaction in reaction.message.reactions ]
        ):
            await reaction.message.channel.send("Hmph! I've already saved this before!")
            return

        if reaction.message.attachments[0]:
            await reaction.message.channel.send("On it! I'll try and save.")

            saved: bool = self._save_attachment(reaction.message.attachments[0])
            if saved:
                await reaction.message.channel.send(
                    f"Saved the file, {user.mention}!",
                )

                await reaction.message.add_reaction(
                    self._file_saved_reaction
                )
            else:
                await reaction.message.channel.send("Failed to save. Something's not right...")
        else:
            await reaction.message.channel.send("There's nothing to save silly!")


    @command()
    async def random(self, ctx: Context):
        root_image_directory: str = self.bot.configuration.dropbox_config.dir_images
        await ctx.channel.send("Hang on a sec, let me find you something good...")

        images: list[str] = fetch_filenames(
            dbx_client     = self.bot.dropbox_client,
            file_directory = root_image_directory,
            extension      = True
        )

        random_image_filename: str = choice(images)
        file_content: bytes = retrieve_file_content(
            dbx_client    = self.bot.dropbox_client,
            filename      = random_image_filename,
            file_location = root_image_directory,
        )

        picture: File = File(
            io.BytesIO(file_content),
            filename = random_image_filename,
        )

        await ctx.channel.send(
            f"Here you go {ctx.author.mention}!",
            file = picture,
        )
