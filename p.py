import discord 
from discord.ext import commands
import requests
import asyncio

intents = discord.Intents.default()
intents.message_content = True
TOKEN = "MTE1NTc5MzQ2NjQyMTQyODM1NQ.GBcjAl.gX3SGzZRJnqmbku8y0iuXyn1iQUhZxJjtU6Cgs"  
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_member_remove(member):
    guild = member.guild
    admin_role = discord.utils.get(guild.roles, name="Owner")  
    if admin_role:
        admin_channel = discord.utils.get(guild.text_channels, name="admin-channel")
        if admin_channel:
            await admin_channel.send(f"{member.display_name} has left the server.")
        else:
            print("Admin channel not found.")
    else:
        print("Admin role not found.")

@bot.event
async def on_message(message):
    if message.channel.name == "rsn-name":
        new_nickname = message.content
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

@bot.command()
async def schedule_event(ctx, event_name, date_time):
    # Implement event scheduling logic
    await ctx.send(f"Event '{event_name}' scheduled for {date_time}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("You can't ban yourself!")
        return

    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} has been banned.")
    except discord.Forbidden:
        await ctx.send("I don't have the permission to ban this member.")
    except discord.HTTPException:
        await ctx.send("Failed to ban the member.")

@bot.command()
async def item_price(ctx, item_name):
    if item_name in command_cooldown:
        await ctx.send(f"Command is on cooldown. Please wait.")
        return

    url = f"https://prices.runescape.wiki/api/v1/osrs?search={item_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"]:
            item_data = data["data"][0]
            item_name = item_data["name"]
            item_high_price = item_data["high"]
            item_low_price = item_data["low"]
            await ctx.send(f"Current prices for {item_name}: High price - {item_high_price}, Low price - {item_low_price}")
            
            command_cooldown[item_name] = True
            # Remove from cooldown after 1 second
            await asyncio.sleep(1)
            del command_cooldown[item_name]
        else:
            await ctx.send("Item not found.")
    else:
        await ctx.send("Failed to retrieve item data.")
bot.run(TOKEN)
