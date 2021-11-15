from dropbox import Dropbox
from discord.ext.commands import (
    Bot,
    when_mentioned_or,
)

from amadeus.config import Config
from amadeus.cogs.events import Events
from amadeus.cogs.music import Music
from amadeus.cogs.memories import Memories


class Amadeus(Bot):
    configuration:    Config
    dialogue_options: list[str]
    dropbox_client:   Dropbox


    def __init__(self, configuration: Config):
        self.configuration = configuration
        self._initialize_bot()


    def _initialize_bot(self):
        super().__init__(
            case_insensitive = True,
            command_prefix   = when_mentioned_or(self.configuration.discord_config.command_prefix),
            description      = self.configuration.discord_config.description,
        )

        def _retrieve_dialogue_options(path_to_dialogue_file: str) -> list[str]:
            with open(path_to_dialogue_file, "r", encoding="utf-8") as dialogue_file:
                return dialogue_file.readlines()

        self.dialogue_options = _retrieve_dialogue_options(
                self.configuration.discord_config.dialogue_file_path
            )

        self.dropbox_client = Dropbox(self.configuration.dropbox_config.secret)

        self.add_cog(Events(self))
        self.add_cog(Music(self))
        self.add_cog(Memories(self))

        self.run(self.configuration.discord_config.secret)
