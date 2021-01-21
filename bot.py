import os
import asyncio
import discord
import logging
import asyncpg
import ast
import random
import ffmpeg
from collections import deque
from tempfile import TemporaryFile
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from gtts import gTTS
from dotenv import load_dotenv

global variableName

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

table_name = 'guilds'
bot = discord.ext.commands.Bot(command_prefix='-')
bot.remove_command('help')


async def status():
    while True:
        game = discord.Game(f'In {len(bot.guilds)} servers.')
        await bot.change_presence(status=discord.Status.online, activity=game)
        await asyncio.sleep(30)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong!')


@bot.command()
async def connect(ctx, *, channel:discord.VoiceChannel=None)
    """You get syntax error here, copy, delete this whole string, run,
    and pasting this makes it work

    Raises:
        discord.InvalidVoiceChannel: [description]
        discord.VoiceConnectionError: [description]
    """
    cls=<class 'discord.voice_client.VoiceClient'>

    if not channel:
        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise discord.InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')
    
    vc = ctx.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        try:
            await vc.move_to(channel)
        except asyncio.TimeoutError:
            raise discord.VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(f'Connected to: **{channel}**', delete_after=20)


@bot.command()
async def repeat(ctx, *, text=None):
    """
    A command which saves `text` into a speech file with
    gtts and then plays it back in the current voice channel.

    Params:
     - text [Optional]
        This will be the text we speak in the voice channel
    """
    if not text:
        # We have nothing to speak
        await ctx.send(f"Hey {ctx.author.mention}, I need to know what to say please.")
        return

    vc = ctx.voice_client # We use it more then once, so make it an easy variable
    if not vc:
        # We are not currently in a voice channel
        await ctx.send("I need to be in a voice channel to do this, please use the connect command.")
        return

    # Lets prepare our text, and then save the audio file
    tts = gTTS(text=text, lang="en")
    tts.save("text.mp3")

    try:
        # Lets play that mp3 file in the voice channel
        vc.play(discord.FFmpegPCMAudio('text.mp3'), after=lambda e: print(f"Finished playing: {e}"))

        # Lets set the volume to 1
        vc.source = discord.PCMVolumeTransformer(vc.source)
        vc.source.volume = 3

    # Handle the exceptions that can occur
    except discord.ClientException as e:
        await ctx.send(f"A client exception occured:\n`{e}`")
    except TypeError as e:
        await ctx.send(f"TypeError exception:\n`{e}`")
    except discord.opus.OpusNotLoaded as e:
        await ctx.send(f"OpusNotLoaded exception: \n`{e}`")


@bot.command()
async def disconnect(ctx):
    """
    Disconnect from a voice channel, if in one
    """
    vc = ctx.voice_client

    if not vc:
        await ctx.send("I am not in a voice channel.")
        return

    await vc.disconnect()
    await ctx.send("I have left the voice channel!")


def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)


@bot.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command() # below will be auto delete(hide) commands
async def on_message(message):

    if "-repeat" in message.content:
        await bot.send_message(messaage.channel, 'yes')

@bot.event
async def owner_or_permissions(**perms):
    original = commands.has_permissions(**perms).predicate
    async def extended_check(ctx):
        if ctx.guild is None:
            return False
        return ctx.guild.owner_id == ctx.author.id or await original(ctx)
    return commands.check(extended_check)


bot.run(TOKEN)
