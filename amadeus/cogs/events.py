from random import choice

from discord import Message
from discord.ext.commands.errors import CommandError
from discord.ext.commands import (
    Bot,
    Cog,
    CommandNotFound,
    Context,
)


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot


    @Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user} is back online!')


    @Cog.listener()
    async def on_message(self, message: Message):
        if (
            self.bot.user.mentioned_in(message) and
            message.content == f'{self.bot.user}'
        ):
            await message.channel.send('Yes..? Might I suggest - `help`?')


    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: CommandError):
        if isinstance(error, CommandNotFound):
            # HACK: Instead of falling back on an error, we're sending a random
            #       dialogue upstream. At the time, I couldn't find a better way
            #       to handle this.
            # FIXME: await ctx.channel.send("Sorry, I don't know how to do that.")
            await ctx.channel.send(choice(self.bot.dialogue_options))
        else:
            raise error
