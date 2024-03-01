import discord
from discord import Interaction, Embed, Color, app_commands
from setup import bot
import asyncio



@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    if message.guild and message.channel.name == "username-change":  #name of channel
        new_nickname = message.content

        # Check if the length of the new nickname is within the limit
        if len(new_nickname) > 32:
            new_nickname = new_nickname[:32]  # Truncate to 32 characters

        guild = message.guild
        member = message.author

        try:
            await member.edit(nick=new_nickname)
            nickname_update_message = await message.channel.send(f"Nickname updated for {member.mention}.")
            await member.send(f"Your nickname has been changed to: {new_nickname}")
            await asyncio.sleep(10)
            await message.delete()
            await nickname_update_message.delete()
        except discord.Forbidden:
            await message.channel.send("I don't have the necessary permissions to change nicknames.")

    await bot.process_commands(message)