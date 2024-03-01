import discord
from discord import Interaction, Embed, Color, app_commands
from setup import bot
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import wom
import json
import re



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