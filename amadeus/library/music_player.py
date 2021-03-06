import asyncio
from typing import Optional

from discord import FFmpegPCMAudio
from discord.ext.commands import Context
from dropbox.dropbox_client import Dropbox

from amadeus.library.dropbox_handler import retrieve_temporary_file_link

class MusicPlayer:
    _dropbox_client: Dropbox
    _music_location: str
    # TODO: Playlist also needs to download and store bytes.
    _playlist:       list[str]
    _playing:        bool
    _repeat:         bool


    def __init__(self, dbx_client: Dropbox, music_location: str):
        self._dropbox_client = dbx_client
        self._music_location = music_location
        self._playlist       = []
        self._playing        = False

    async def player(self, ctx: Context):
        while self._playlist:
            self._playing = True
            voice_channel = ctx.message.author.voice.channel
            voice_client  = ctx.voice_client

            music_file_link: Optional[str] = None
            match self.current_song():
                case str(song):
                    # HACK: Need to abstract "now playing" into the discord cog.
                    await ctx.send(f"Now Playing: `{song}`")
                    music_file_link = retrieve_temporary_file_link(self._dropbox_client, song, self._music_location)
                case None:
                    pass

            try:
                voice_client = await voice_channel.connect()
            except Exception as exn:
                print(exn)

            if music_file_link:
                # TODO: Need to catch an exception when already playing a file.
                voice_client.play(FFmpegPCMAudio(music_file_link))
                while self._playing:
                    await asyncio.sleep(1)
                self._playing = False

            self._playlist = self._playlist[1:]
        else:
            self._playing = False
            await voice_client.disconnect()


    async def play(self, ctx: Context, songs: list[str]):
        self._playlist = songs
        await self.player(ctx)


    async def next(self, ctx: Context):
        self._playlist = self._playlist[1:]
        ctx.voice_client.stop()
        await self.player(ctx)


    def current_song(self) -> Optional[str]:
        if self._playlist == []:
            return None
        else:
            return self._playlist[0]
