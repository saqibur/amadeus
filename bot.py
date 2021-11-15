# import logging
from typing import Any

from yaml import (
    YAMLError,
    safe_load,
)

from amadeus.config import Config
from amadeus.amadeus import Amadeus


def _retrieve_configuration(config_file_relative_path: str) -> dict[str, Any]:
    with open(config_file_relative_path, encoding='utf-8') as config_file:
        try:
            return safe_load(config_file)
        except YAMLError as exception:
            raise exception


# TODO: Logging
# def _setup_logger() -> logging.Logger:
#     logger = logging.getLogger('discord')
#     logger.setLevel(logging.DEBUG)
#     handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#     handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#     logger.addHandler(handler)

#     return logger


def main():
    config_file_relative_path: str = 'config.yaml'
    configuration: dict[str, Any]  = _retrieve_configuration(config_file_relative_path)
    config: Config                 = Config(configuration)

    Amadeus(config)


if __name__  == "__main__":
    main()