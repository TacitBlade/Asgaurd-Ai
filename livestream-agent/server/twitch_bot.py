from twitchio.ext import commands
from server.config import config, TWITCH_TOKEN

class StreamBot(commands.Bot):
    def __init__(self, message_callback):
        self.channel_name = config.get("twitch", {}).get("channel", "your_twitch_channel_name")
        prefix = config.get("twitch", {}).get("bot_prefix", "!")
        super().__init__(
            token=TWITCH_TOKEN,
            prefix=prefix,
            initial_channels=[self.channel_name]
        )
        self.message_callback = message_callback
        self.banned_words = config.get("moderation", {}).get("banned_words", [])

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.echo:
            return

        print(f"[Twitch] {message.author.name}: {message.content}")

        # Basic moderation check
        if any(bad_word.lower() in message.content.lower() for bad_word in self.banned_words):
            print(f"Filtered message from {message.author.name}")
            return # Skip passing to AI

        # Pass message to callback (which will invoke AI)
        await self.message_callback(message.author.name, message.content, is_host=False)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Hello {ctx.author.name}!')
