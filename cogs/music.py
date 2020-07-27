from discord.ext import commands
from discord.utils import get
import discord

from youtubesearchpython import SearchVideos
import os
import youtube_dl

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
        return cls(discord.FFmpegPCMAudio(filename, executable="C:\\ffmpeg\\bin\\ffmpeg.exe", **ffmpeg_options), data=data)


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, name='leave')
    async def leave(self, ctx):
        if bot.voice_channe

    @commands.command(pass_context=True, help='Drops some sick beat')
    async def play(self, ctx, *,  phrase):
        search = SearchVideos(phrase, offset=1, mode="dict", max_results=1)
        searchResults = search.result()

        try:
            url = searchResults["search_result"][0]["link"]
            title = searchResults["search_result"][0]["title"]
            duration = searchResults["search_result"][0]["duration"]
            yt_channel = searchResults["search_result"][0]["channel"]
        except IndexError:
            await ctx.send("AlphaWolf nie znajdzie czegoś co ma za dużo słów więc postaraj się ujać tytuł w kilku słowach")

        author_vc= ctx.author.voice
        channel = ctx.author.voice.channel
        if author_vc:
            await author_vc.channel.connect()
            print(" Connected to vc : {}".format(author_vc.channel))

        player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)



def setup(bot):
    bot.add_cog(Music(bot))
