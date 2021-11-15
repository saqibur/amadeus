from typing import Any


class DropboxConfig:
    secret:      str
    dir_images:  str
    dir_videos:  str
    dir_music:   str
    dir_sayings: str


class DiscordConfig:
    secret:              str
    command_prefix:      str
    description:         str
    dialogue_file_path:  str
    file_save_reaction:  str
    file_saved_reaction: str


class Config:
    dropbox_config: DropboxConfig
    discord_config: DiscordConfig

    def __init__(self, configuration: dict[str, Any]):
        def set_discord_configs():
            discord_configurations: Any = configuration['discord']
            discord_config: DiscordConfig = DiscordConfig()

            discord_config.secret              = discord_configurations['secret']
            discord_config.command_prefix      = discord_configurations['command_prefix']
            discord_config.description         = discord_configurations['description']
            discord_config.dialogue_file_path  = discord_configurations['dialogue_file_path']
            discord_config.file_save_reaction  = discord_configurations['file_save_reaction']
            discord_config.file_saved_reaction = discord_configurations['file_saved_reaction']

            self.discord_config = discord_config


        def set_dropbox_configs():
            dropbox_configurations: Any = configuration['dropbox']
            dropbox_config: DropboxConfig = DropboxConfig()

            dropbox_config.secret      = dropbox_configurations['secret']
            dropbox_config.dir_images  = dropbox_configurations['dir_images']
            dropbox_config.dir_videos  = dropbox_configurations['dir_videos']
            dropbox_config.dir_music   = dropbox_configurations['dir_music']
            dropbox_config.dir_sayings = dropbox_configurations['dir_sayings']

            self.dropbox_config = dropbox_config

        set_discord_configs()
        set_dropbox_configs()
