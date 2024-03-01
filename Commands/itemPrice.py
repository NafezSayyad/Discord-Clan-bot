import discord
from discord import Interaction, Embed, Color, app_commands
from setup import bot
from rswiki_wrapper.osrs import Mapping, Latest
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from typing import List, Tuple, Dict, Any





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