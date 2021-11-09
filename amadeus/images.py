import discord
import enum


class AMADEUS_IMAGES(enum.Enum):
    BACK_ONLINE = 1


def create_image(image_name: str) -> discord.File:
    with open("img/" + image_name, "rb") as image_file:
        return discord.File(image_file, filename=image_name)


amadeus_images = {
    AMADEUS_IMAGES.BACK_ONLINE: create_image("amadeus_intro.gif")
}
