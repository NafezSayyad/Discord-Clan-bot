import discord
from discord import Interaction, Embed, Color, app_commands
from setup import bot
from rswiki_wrapper.osrs import Mapping, Latest
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from typing import List, Tuple, Dict, Any
import datetime
import pytz
from geopy.geocoders import Nominatim







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