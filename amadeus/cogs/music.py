from random import choice
from re import S

from discord.ext.commands import (
    Bot,
    Context,
    Cog,
    command,
)

from amadeus.library.dropbox_handler import fetch_filenames
from amadeus.library.music_player import MusicPlayer


class Music(Cog):
    bot:  Bot
    music_player: MusicPlayer

    def __init__(self, bot: Bot):
        self.bot = bot
        self.music_player = MusicPlayer(
            self.bot.dropbox_client,
            self.bot.configuration.dropbox_config.dir_music
        )


    @command()
    async def songs(self, ctx: Context):
        songs: list[str] = fetch_filenames(
            dbx_client     = self.bot.dropbox_client,
            file_directory = self.bot.configuration.dropbox_config.dir_music,
            extension      = False
        )

        printable_list_of_songs: str = ', '.join(
            [ f'`{song}`' for song in songs ]
        )

        await ctx.channel.send(f"I can sing: {printable_list_of_songs}")


    @command()
    async def sing(self, ctx: Context, maybe_song_name: str = None):
        if ctx.voice_client is None:
            await ctx.send("Please connect to a voice channel first.")
            return

        songs: list[str] = fetch_filenames(
            dbx_client=self.bot.dropbox_client,
            file_directory=self.bot.configuration.dropbox_config.dir_music,
            extension=False
        )

        match maybe_song_name:
            case None:
                random_song: str = choice(songs)
                message: str = f"I choose --- `{random_song}`"
                await ctx.channel.send(message)
                await ctx.channel.send(f"Adding to queue: `{random_song}`")
                await self.music_player.play(ctx, random_song)
            case str(song_name):
                if song_name in songs:
                    await ctx.channel.send(f"Adding to queue: `{song_name}`")
                    await self.music_player.play(ctx, song_name)
                else:
                    await ctx.channel.send(
                        f"Sorry, I don't know how to sing: `{song_name}`.\n" +
                        "Consider uploading it, or try something from the " +
                        "`songs` list."
                    )


    @command()
    async def next(self, ctx: Context):
        if ctx.voice_client is None:
            await ctx.send("Please connect to a voice channel first.")
            return

        await ctx.send("Skipping to next song")
        await self.music_player.next(ctx)


    @command()
    async def leave(self, ctx: Context):
        if ctx.voice_client is not None:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.channel.send("Goodbye")
        else:
            await ctx.send("But I'm not even singing in a voice channel :(")
