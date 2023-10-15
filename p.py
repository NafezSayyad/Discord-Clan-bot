import discord 
from discord.ext import commands
intents = discord.Intents.default()
intents.message_content = True
TOKEN = "MTE1NTc5MzQ2NjQyMTQyODM1NQ.GBcjAl.gX3SGzZRJnqmbku8y0iuXyn1iQUhZxJjtU6Cgs"
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_message(message):
    if message.channel.name == "general":  # Change to your desired channel name
        # Assuming the message content is the in-game name
        new_nickname = message.content
        guild = message.guild
        member = message.author

        # Change the nickname
        try:
            await member.edit(nick=new_nickname)
            await message.channel.send(f"Nickname updated for {member.mention}.")
        except discord.Forbidden:
            await message.channel.send("I don't have the necessary permissions to change nicknames.")

    await bot.process_commands(message)

bot.run(TOKEN)

