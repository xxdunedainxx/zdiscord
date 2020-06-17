# TODO: package & organize
# TODO: containerize
# TODO: install on rpi
# TODO: upload ghe
from zdiscord.util.logging.LogFactory import LogFactory
from zdiscord.util.error.ErrorFactory import errorStackTrace
from zdiscord.App import App
# https://discordpy.readthedocs.io/en/latest/api.html#discord-api-events
# TODO CLI configuration for app.json
# TODO If app crashes, restart discord bot?
# https://stackoverflow.com/questions/42999961/ffmpeg-binary-not-found-python

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
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options, executable="C:\\Users\\zach\\Documents\\ffmpeg\\ffmpeg-20200615-9d80f3e-win64-static\\bin\\ffmpeg.exe"), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""
        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url, t=None):
        """Streams from a url (same as yt, but doesn't predownload)"""

        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        #await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Relatively simple music bot example')

chan: discord.VoiceChannel
@bot.event
async def on_ready():
    busters: discord.Guild = bot.guilds[0]
    print("getting channels")
    channels: [discord.VoiceChannel] = busters.voice_channels
    chan: discord.VoiceChannel = None
    for ch in channels:
        print("checking channel...")
        if ch.name == 'Team Rheem':
            chan = ch
            break



    c: Music = bot.get_cog("Music")
    await c.join(ctx=busters,channel=chan)
    #await c.stream(ctx=busters,url="https://youtu.be/M11SvDtPBhA")   #"https://youtu.be/EBudj01e9OY")
    #for chan in channels:

    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')

@bot.event
async def on_voice_state_update(member, before, after):
    if member.name == bot.user or member.bot is True:
        return
    if after.channel != None:
        busters: discord.Guild = bot.guilds[0]
        c: Music = bot.get_cog("Music")
        await c.stream(ctx=busters,url="https://www.youtube.com/embed/kYXRfwXfz5A", t=6)   #"https://youtu.be/EBudj01e9OY")

bot.add_cog(Music(bot))


bot.run('')
bot.extra_events
#c.join(ctx=bot, channel=)
exit(0)
"""
app = App(config_path="./zdiscord/app.json")

if __name__ == "__main__":
    try:
        main_log=LogFactory.get_logger(logName="main")
        main_log.info('Init main')
        app = App(config_path="./zdiscord/app.json")
    except Exception as e:
        main_log.error(f"CRITICAL ERROR IN MAIN APP!!! {errorStackTrace(e)}")
        exit(-1)
exit(0)

"""