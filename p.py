import discord
from discord.ext import commands, tasks
from discord.ui import Button
# from discord_slash import cog_ext, SlashContext
# from wavelink.ext import wavelink

import requests
import asyncio
from rswiki_wrapper.osrs import Mapping, Latest
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import yt_dlp
import wom
import os
from typing import List, Tuple, Dict, Any
import json
import re
import shutil
import datetime
import pytz
from geopy.geocoders import Nominatim










intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

TOKEN = "PRIVATE INFO"
bot = discord.ext.commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
#     await load_cogs()


# async def load_cogs():
#     try:
#         print("Cogs loaded successfully.")
#     except Exception as e:
#         print(f"Error loading extension: {e}")

# print("Current working directory:", os.getcwd())
created_messages = {}

# @bot.command(name='loaded_cogs')
# async def loaded_cogs(ctx):
#     loaded_cogs = [cog.qualified_name for cog in bot.cogs]
#     await ctx.send(f"Loaded cogs: {', '.join(loaded_cogs)}")


@bot.event
async def on_member_join(member):
    # Send a welcome message or instructions to the new member
    welcome_channel = member.guild.get_channel(1178311335751188580)  
    if welcome_channel:
        # Rules to be included in the embedded message
       rules = [
       
        
        "1. Be Kind: You must respect all users, regardless of your liking towards them. Treat others the way you want to be treated.",
        "2. No Pornographic/Adult/Other NSFW Material: This is a community server and not meant to share this kind of material.",
        "3. Direct & Indirect Threats: Threats to other users of DDoS, Death, DoX, abuse, and other malicious threats are absolutely prohibited and disallowed.",
        "4. No Offensive Names and Profile Pictures: You will be asked to change your name or picture if the staff deems them inappropriate.",
        "5. No Spamming: Do not send a lot of small messages right after each other. These disrupt chat and make it hard to scroll through the server.",
        "6. No Scamming, In-Game or Out of Game: You will be reported to Runewatch and have your account flagged if you scam anyone out of in-game items!",
        "7. No Sharing or Promoting Illegal Activities: Do not share or promote any illegal activities, such as hacking, phishing, or drug use.",
        "8. No Soliciting or Begging for Money, Items, or Services: Do not solicit or beg for money, items, or services from other users.",
        "9. Dont Share Your Personal Information: Do not share your personal information or the personal information of other users without their consent. This includes phone numbers, addresses, and any other sensitive information.",
        "10. No Sharing or Distributing Hacks, Cheats, or Other Unauthorized Tools or Services: Sharing or distributing hacks, cheats, or other unauthorized tools or services is strictly prohibited on the server.",
        "11. No Sharing or Distributing Viruses or Malicious Software: Sharing or distributing viruses or malicious software can harm the server and its members and is therefore strictly prohibited.",
        "12. Do Not Impersonate Other Users, Staff Members, or Any Other Individuals or Organizations: This includes using similar usernames, profile pictures, or display names."
       ]

       # Send an embedded message with a reaction button
       embed = discord.Embed(title="Welcome to the Server!", description=f"Please click the ✅ reaction to accept the rules.", color=0x00ff00)

       # Add each rule as a separate field
       for i, rule in enumerate(rules, start=1):
            embed.add_field(name=f"Rule {i}", value=rule, inline=False)

       message = await welcome_channel.send(embed=embed)
       await message.add_reaction("✅")

        # Store the member's ID and message ID for later reference
        # You may want to use a database for a more robust solution
       reaction_info = {"member_id": member.id, "message_id": message.id}
       reactions_info.append(reaction_info)

 

@bot.event
async def on_reaction_add(reaction, user):
    # Check if the reaction is from a user and the reaction is the "✅" emoji
    if user.bot or str(reaction.emoji) != "✅":
        return

    # Check if the reaction is on one of the welcome messages
    for reaction_info in reactions_info:
        if reaction.message.id == reaction_info["message_id"]:
            # Assign a role to the user using the role ID
            guild = bot.get_guild(reaction.message.guild.id)
            member = guild.get_member(reaction_info["member_id"])
            role_id = 1177977176642048090  
            role = discord.utils.get(guild.roles, id=role_id)

            # Debug prints
            print(f"Member: {member}")
            print(f"Role: {role}")

            if role:
                await member.add_roles(role)

                # Send a private message to the user
                await member.send("Congratulations! You have successfully accepted the rules and been verified.")

                # Remove the stored reaction information
                reactions_info.remove(reaction_info)

                # Delete the message with rules and reaction button
                await reaction.message.delete()
                break









@bot.command(name='create')
async def create_embed(ctx):
    # Check if the user has the "Owners" role
    owners_role = discord.utils.get(ctx.guild.roles, name='Owners')  # Replace with your actual admin role name
    if owners_role not in ctx.author.roles:
        await ctx.send("You don't have permission to use this command.")
        return

    # Ask for information to create the embedded message
    await ctx.author.send("Please provide the information for the embedded message:")
    await ctx.author.send("Enter the title:")
    title = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)
    
    await ctx.author.send("Enter the description:")
    description = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)

    # Create the embedded message
    embed = discord.Embed(title=title.content, description=description.content, color=0x00ff00)
    message = await ctx.send(embed=embed)

    # Ask for reactions and corresponding roles
    await ctx.author.send("Enter the emoji (as text) you want to use as a reaction button, and mention the role to assign (e.g., 🎮 @GamerRole):")
    await ctx.author.send("Type `done` when you've added all reactions.")

    reactions_info = {}
    while True:
        reaction_info = await bot.wait_for('message', check=lambda m: m.author == ctx.author, timeout=60)

        if reaction_info.content.lower() == 'done':
            break

        try:
            emoji, role_mention = reaction_info.content.split(' ')
            role_name = role_mention.replace('@', '').replace('<', '').replace('>', '').replace('&', '')
            reactions_info[emoji] = role_name
        except ValueError:
            await ctx.author.send("Invalid format. Please use the format: emoji @RoleName")

    # Add reactions to the message
    for emoji in reactions_info.keys():
        await message.add_reaction(emoji)

    # Store the created message and its corresponding roles
    created_messages[message.id] = reactions_info


    # Add reactions to the message
    for emoji in reactions_info.keys():
        await message.add_reaction(emoji)

    # Store the created message and its corresponding roles
    created_messages[message.id] = reactions_info

@bot.event
async def on_reaction_add(reaction, user):
    print(f"Reaction added: {reaction.emoji} by {user.name}")
    
    for message_id, roles_info in created_messages.items():
        if reaction.message.id == message_id and str(reaction.emoji) in roles_info:
            print(f"Matching message ID: {message_id}")
            print(f"Roles info: {roles_info}")

            guild = bot.get_guild(reaction.message.guild.id)
            member = guild.get_member(user.id)
            if member is None:
                print(f"Member not found: {user.name}")
                return

            role_id = roles_info[str(reaction.emoji)]  # Use role ID directly
            role = discord.utils.get(guild.roles, id=int(role_id))

            if role:
                try:
                    await member.add_roles(role)
                    print(f"Assigned role {role.name} to {member.display_name}")
                except discord.Forbidden:
                    print(f"Error: Bot doesn't have permission to assign roles.")
                except discord.HTTPException as e:
                    print(f"Error assigning role: {e}")
            else:
                print(f"Role not found: {role_id}")





project_name = 'Gfamily Bot'
contact_info = 'nafez.sayyad@gmail.com'
user_agent = f'{project_name} - {contact_info}'

def format_price(price):
    if price >= 1_000_000:
        return f'{price / 1_000_000:.3f}M'
    elif price >= 1_000:
        return f'{price / 1_000:.3f}K'
    else:
        return str(price)
    



@bot.command(name='price')
async def get_price(ctx, *, item_name):
    # Query the item mapping to get all item names
    mapping_query = Mapping(user_agent=user_agent)
    # Filter out items that contain 'corrupted' in their names
    item_mapping = {item['name'].lower(): item['id'] for item in mapping_query.content if 'corrupted' not in item['name'].lower()}

    # Use fuzzy matching to find the closest matching item name
    matches = process.extract(item_name.lower(), item_mapping.keys(), limit=1)
    closest_match, similarity = matches[0]

    # Check if the similarity is above a certain threshold
    if similarity >= 80:
        item_id = item_mapping[closest_match]

        # Query the latest prices for the specified item ID
        latest_query = Latest(id=item_id, user_agent=user_agent)
        item_price_info = latest_query.content.get(str(item_id))

        if item_price_info:
            high_price = item_price_info['high']
            low_price = item_price_info['low']
            current_price = (high_price + low_price) // 2  # Calculate the average

            formatted_high = format_price(high_price)
            formatted_low = format_price(low_price)
            formatted_current = format_price(current_price)

            embed = discord.Embed(title=f"Price Information for {closest_match}", color=0x00ff00)
            embed.add_field(name="High Price", value=formatted_high, inline=False)
            embed.add_field(name="Low Price", value=formatted_low, inline=False)
            embed.add_field(name="Current Price", value=formatted_current, inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Unable to retrieve price information for {closest_match}")
    else:
        await ctx.send(f"Item '{item_name}' not found. Did you mean '{closest_match}'?")


    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore messages from the bot itself

    if message.guild and message.channel.name == "rsn-name":
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
    

client = wom.Client(
    "ainq24zly893fc56ll00vptq",  # The wom api key to use.
    user_agent="@Gfamily bot",
    api_base_url="https://api.wiseoldman.net/v2",
)







@bot.command(name="rank")
async def rank(ctx, group_id: int):
    # Instantiate the wom client (replace with actual instantiation code)
    client = wom.Client()

    try:
        # Start the client
        await client.start()

        # Get group details
        result = await client.groups.get_details(group_id)

        if result.is_ok:
            details = result.unwrap()
            
            # Extract relevant information for serialization
            group_info = {
                "group_name": details.group.name,
                "memberships": [str(membership) for membership in details.memberships],
            }

            # Save the data as JSON
            with open(f"group_details_{group_id}.json", "w") as file:
                json.dump(group_info, file)

            # Send the JSON file in the chat
            with open(f"group_details_{group_id}.json", "rb") as file:
                file_data = discord.File(file)
                await ctx.send(content="Group Details:", file=file_data)

        else:
            await ctx.send(f"Error: {result.unwrap_err()}")

    finally:
        # Close the client
        await client.close()



@bot.command(name="extract")
async def extract(ctx, group_id: int):
    # Read the JSON file
    file_path = f"group_details_{group_id}.json"
    try:
        with open(file_path, "r") as file:
            group_info = json.load(file)

        # Extract information
        memberships = group_info.get("memberships", [])

        # Prepare the extracted information as a list of dictionaries
        extracted_info = []
        pattern = re.compile(r"display_name='(.*?)'.*?role=<GroupRole\.(\w+):")
        for membership in memberships:
            match = pattern.search(membership)
            if match:
                display_name = match.group(1)
                group_role = match.group(2)
                player_info = {
                    "display_name": display_name,
                    "group_role": group_role
                }
                extracted_info.append(player_info)

        # Write the extracted information to a JSON file
        output_file_path = f"extracted_info_{group_id}.json"
        with open(output_file_path, "w") as output_file:
            json.dump(extracted_info, output_file, indent=2)

        await ctx.send(f"Extracted information has been saved to {output_file_path}.")

    except FileNotFoundError:
        await ctx.send(f"Error: File not found. Please use the !rank command first.")



@bot.command(name="modify")
async def modify(ctx, group_id: int):
    # Read the JSON file
    file_path = f"extracted_info_{group_id}.json"
    output_file_path = f"role_modifications_{group_id}.txt"

    try:
        with open(file_path, "r") as file:
            extracted_info = json.load(file)

        # Mapping of group roles to Discord server role IDs
        role_mapping = {
            "Bronze": 1135088824985325609,
            "Iron": 1135088902936461342,
            "Steel": 1135089239479042060,
            "Mithril": 1135089304796921956,
            "Adamant": 1135089559756091513,
            "Rune": 1135089678958215169,
            "Gold": 1135089866741395517,
            "Dragon": 1135089747736399953,
            "Gold": 1135089866741395517,
        }

        # List to store information about modified roles
        role_modifications = []

        # Iterate through extracted information and modify Discord server roles
        for player_info in extracted_info:
            display_name = player_info.get("display_name")
            group_role = player_info.get("group_role")

            # Attempt to find a member in the server with a similar display name
            member = discord.utils.find(lambda m: m.display_name.lower().startswith(display_name.lower()) or m.name.lower().startswith(display_name.lower()), ctx.guild.members)

            if member:
                print(f"Found member: {member.display_name}")

                # Assign the Discord server role based on the mapping
                role_id = role_mapping.get(group_role)
                if role_id:
                    role = ctx.guild.get_role(role_id)
                    if role:
                        try:
                            await member.add_roles(role)
                            print(f"Assigned role {role.name} to {member.display_name}")
                            role_modifications.append(f"Modified roles for {member.display_name}: Added role {role.name}")
                        except discord.Forbidden:
                            role_modifications.append(f"Error: Insufficient permissions to modify roles for {member.display_name}")
                    else:
                        role_modifications.append(f"Error: Role {group_role} not found in the server.")
                else:
                    role_modifications.append(f"Error: No role mapping found for {group_role}")
            else:
                role_modifications.append(f"Member not found for display name: {display_name}")

        # Write the role modifications to a text file
        with open(output_file_path, "w") as output_file:
            for modification in role_modifications:
                output_file.write(modification + "\n")

        await ctx.send(f"Role modification process completed. Role modifications saved to {output_file_path}")

    except FileNotFoundError:
        await ctx.send(f"Error: File not found. Please use the !extract command first.")



@bot.command(name='ban')
async def ban_user(ctx, member: discord.Member, *, reason=None):
    # Check if the command invoker has the necessary permissions
    if ctx.author.guild_permissions.ban_members:
        try:
            # Ban the member with an optional reason
            await member.ban(reason=reason)
            
            # Notify the channel about the ban
            await ctx.send(f'{member.mention} has been banned. Reason: {reason}')

        except discord.Forbidden:
            # Handle cases where the bot doesn't have permission to ban
            await ctx.send("I don't have the necessary permissions to ban members.")

        except discord.HTTPException as e:
            # Handle other errors that might occur during banning
            await ctx.send(f"An error occurred: {e}")

    else:
        # Notify if the command invoker lacks permission
        await ctx.send("You don't have permission to use this command.")


@bot.command(name='kick')
async def kick_user(ctx, member: discord.Member, *, reason=None):
    # Check if the command invoker has the necessary permissions
    if ctx.author.guild_permissions.kick_members:
        try:
            # Kick the member with an optional reason
            await member.kick(reason=reason)
            
            # Notify the channel about the kick
            await ctx.send(f'{member.mention} has been kicked. Reason: {reason}')

        except discord.Forbidden:
            # Handle cases where the bot doesn't have permission to kick
            await ctx.send("I don't have the necessary permissions to kick members.")

        except discord.HTTPException as e:
            # Handle other errors that might occur during kicking
            await ctx.send(f"An error occurred: {e}")

    else:
        # Notify if the command invoker lacks permission
        await ctx.send("You don't have permission to use this command.")



@bot.command(name='time')
async def time_command(ctx, *, location):
    try:
        # Use geopy to get the location information (city, country)
        geolocator = Nominatim(user_agent="time_bot")
        location_data = geolocator.geocode(location)

        if location_data:
            # Use the city and country to get the time zone
            city = location_data.address.split(",")[0]
            country = location_data.address.split(",")[-1].strip()
            time_zone = pytz.timezone(f'{country}/{city}')

            # Get the current time in the specified time zone
            current_time = datetime.datetime.now(time_zone)

            # Format the time for display
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S %Z")

            # Send the formatted time to the channel
            await ctx.send(f"The current time in {city}, {country} is: {formatted_time}")

        else:
            await ctx.send(f"Error: Could not find location information for {location}. Please provide a valid city name.")

    except pytz.UnknownTimeZoneError:
        await ctx.send(f"Error: Unknown time zone for {location}. Please provide a valid city name.")














reactions_info = []



bot.run(TOKEN)
