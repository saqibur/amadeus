# Amadeus

> Amadeus is the name of a memory storage ~~and artificial intelligence~~ system.


## Rationale
This project was an exercise in developing a discord bot for me and my friends,
while practising `Python`.


## What can Amadeus do?
- Spout random nonsense from the
[`Steins;Gate`](https://myanimelist.net/anime/9253/Steins_Gate) anime.
- Search and stream music from Dropbox
- Save music, videos and images (after basic compression) in Dropbox from Discord
chats
- Retrieve images at random
- Handle reminders
- Slap...


## Getting Started
- Read the [Discord.py Introduction](https://discordpy.readthedocs.io/en/stable/intro.html)
to get set-up.
- Create a copy of `config_template.yaml`, and rename to `config.yaml`.
- Create a Discord bot token through the
[Discord Developer Portal](https://discord.com/developers/docs/intro).
- Create a Dropbox app token token through the
[Dropbox API](https://www.dropbox.com/developers/reference/getting-started?_tk=guides_lp&_ad=guides2&_camp=get_started).
- Set up your folders in Dropbox as per the examples in `config_template.yaml`.
Note: The leading `/`s are required.
- Feel free to change the reaction emojis to your preference.
- Create and activate a virtual environment after cloning the project.

```bash
pip install -r requirements.txt
python bot.py

# If successful, you should see - "amadeus is back online!"
```

## Additional Data
Makise Kurisu Dialogue - https://www.kaggle.com/carlosacevedomorales/steins-gate
