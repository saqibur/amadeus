import enum

DISCORD_SECRET: str = open('discord.secret').readline()
DROPBOX_SECRET: str = open('dropbox.secret').readline()
AMADUES_CHANNEL_ID  = 907495808721629214

class AMADEUS_EMOJI(enum.Enum):
    TSUNDERE  = 1
    ENTERS_VC = 2
    ERROR     = 3
    EXITS_VC  = 4
    SAVE      = 5
    SAVED     = 6

AMADEUS_EMOJIS = {
    AMADEUS_EMOJI.TSUNDERE:  "<:ama_tsun:906108393817792512>",
    AMADEUS_EMOJI.ENTERS_VC: "<:ama_joins_vc:907341183657836646>",
    AMADEUS_EMOJI.ERROR:     "<:ama_error:907342008635506788>",
    AMADEUS_EMOJI.EXITS_VC:  "<:ama_leaves_vc:907342753518731264>",
    AMADEUS_EMOJI.SAVE:      "<:ama_save:907345268062699621>",
    AMADEUS_EMOJI.SAVED:     "<:ama_saved:907487701526278144>",
}