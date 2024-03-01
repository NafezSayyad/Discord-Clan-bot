import discord
from discord import Interaction, Embed, Color, app_commands
from setup import bot
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import yt_dlp
import wom
import json
reactions_info = []


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