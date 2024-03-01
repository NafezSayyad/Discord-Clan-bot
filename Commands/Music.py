import discord
from discord import Interaction, Embed, Color, app_commands, commands
import yt_dlp
from setup import bot
import asyncio



ffmpeg_options = {
    'options': '-vn',
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
}


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}



class MusicControl(discord.ui.View):
    def __init__(self, bot, ctx, song_title):
        super().__init__()
        self.bot = bot
        self.ctx = ctx
        self.song_title = song_title

    def update_message(self):
        self.message.content = f"Now playing: {self.song_title}"

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.primary, custom_id="pause_button")
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.bot.get_context(interaction.message)
        await ctx.invoke(self.bot.get_command("pause"))
        await interaction.response.send_message("Music paused", ephemeral=True)

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.primary, custom_id="skip_button")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.bot.get_context(interaction.message)
        await ctx.invoke(self.bot.get_command("skip"))
        await interaction.response.send_message("Skipped to the next song", ephemeral=True)

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.primary, custom_id="resume_button")
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        ctx = await self.bot.get_context(interaction.message)
        await ctx.invoke(self.bot.get_command("resume"))
        await interaction.response.send_message("Music resumed", ephemeral=True)




@commands.command()
async def my_command(ctx):
    view = MusicControl(bot)
    await ctx.send("Some message", view=view)

song_queue = []  

def search_yt(query):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return {'source': info['entries'][0]['url'], 'title': info['entries'][0]['title']}

@bot.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, *, query=None):
    voice_channel = ctx.message.author.voice.channel

    if not voice_channel:
        await ctx.send('You need to be in a voice channel to play music!')
        return

    if query is None:
        await ctx.send('Please provide a song to play.')
        return

    if not ctx.voice_client:
        voice_channel = await voice_channel.connect()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        url = info['entries'][0]['url']

    ffmpeg_options = {
        'options': '-vn',
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    }

    source = discord.FFmpegPCMAudio(executable="ffmpeg", source=url, **ffmpeg_options)

    if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        # Queue the song
        song_queue.append({'title': info['entries'][0]['title'], 'url': url})
        await ctx.send(f'{query} has been added to the queue!')
    else:
        ctx.voice_client.play(discord.PCMVolumeTransformer(source), after=lambda e: print('Player error: %s' % e) if e else None)

        # Create the view and message with buttons
        view = MusicControl(bot, ctx, info['entries'][0]['title'])
        message = await ctx.send("Now playing: {}".format(info['entries'][0]['title']), view=view)

        # Wait for the audio to finish before moving to the next song
        while ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
            await asyncio.sleep(1)

        # Move to the next song in the queue
        if song_queue:
            next_song = song_queue.pop(0)
            await play(ctx, query=next_song['title'])
            view.update_message()
        else:
            # No more songs in the queue, disconnect only if not paused
            if not ctx.voice_client.is_paused():
                await ctx.voice_client.disconnect()
                await ctx.send('Queue is empty. Disconnecting.')

        await ctx.send(f'Finished playing: {info["entries"][0]["title"]}')




@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        
    else:
        await ctx.send('The bot is not paused.')

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        
    else:
        await ctx.send('There is no song to skip.')

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        
    else:
        await ctx.send('The bot is not playing.')


@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@bot.command()
async def queue(ctx):
    if not song_queue:
        await ctx.send('The queue is empty.')
    else:
        queued_songs = '\n'.join(song['title'] for song in song_queue)
        await ctx.send(f'Queue:\n{queued_songs}')
    