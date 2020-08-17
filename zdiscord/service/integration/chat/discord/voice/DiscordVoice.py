from zdiscord.service.integration.chat.discord.voice.VoiceFactory import VoiceFactory

import asyncio

import discord
import youtube_dl

from discord.ext import commands
import time
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable=DiscordVoice.ffmpeg_binary), data=data)

class DiscordVoice(commands.Cog):
    ffmpeg_binary: str = ''

    def __init__(self, bot, voiceFactory: VoiceFactory , ffmpeg: str):
        DiscordVoice.ffmpeg_binary = ffmpeg
        self.current_voice_channel: discord.VoiceChannel = None
        self.__vf: VoiceFactory = voiceFactory
        self.bot = bot


    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))


    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    async def leave(self, ctx):
        """leave a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

    async def random_audio(self):
        busters: discord.Guild = self.bot.guilds[0]
        await self.stream(ctx=busters, url=self.__vf.fetch_stream_link())

    async def connect_voice_channel_routine(self, channel: str, message: discord.Message):
        busters: discord.Guild = self.bot.guilds[0]
        channel_to_join: discord.VoiceChannel = self.get_voice_channel(channel)
        if channel_to_join:
            self.current_voice_channel = channel_to_join
            await self.join(ctx=busters, channel=channel_to_join)
            await self.stream(ctx=busters, url=self.__vf.fetch_stream_link())
        else:
            await message.channel.send(f"Unable to join voice channel \"{channel}\"")

    async def disconnect_voice(self):
        busters: discord.Guild = self.bot.guilds[0]
        if self.current_voice_channel:
            await self.leave(busters)
            self.current_voice_channel = None

    def get_voice_channel(self, channel: str) -> discord.VoiceChannel:
        busters: discord.Guild = self.bot.guilds[0]
        print("getting channels")
        channels: [discord.VoiceChannel] = busters.voice_channels
        chan: discord.VoiceChannel = None
        for ch in channels:
            print("checking channel...")
            if ch.name.lower() == channel:
                return ch
        return None