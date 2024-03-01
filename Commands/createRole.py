import discord
from discord import Interaction, Embed, Color, app_commands
from setup import bot

# This dictionary will store message IDs and their corresponding roles for reaction handling
created_messages = {}

@bot.tree.command(name='create-role')
@app_commands.describe(title='Title of the embedded message', description='Description of the embedded message', reactions='Reactions and roles in format "emoji @RoleName", separated by commas')
async def create_role(interaction: Interaction, title: str, description: str, reactions: str):
    print(f"Command /create-role invoked by {interaction.user}")  # Debugging line

    # Check if the user has the 'Tech Team' role
    Tech_role = discord.utils.get(interaction.guild.roles, name='Tech Team')
    if Tech_role not in interaction.user.roles:
        print(f"User {interaction.user} does not have the 'Tech Team' role")  # Debugging line
        await interaction.response.send_message("You don't have permission to use this command.", ephemeral=True)
        return
    else:
        print(f"User {interaction.user} has the 'Tech Team' role")  # Debugging line

    # Create the embed message
    embed = Embed(title=title, description=description, color=Color.green())
    message = await interaction.channel.send(embed=embed)
    print(f"Embed message sent: {title}")  # Debugging line

    # Process reactions and roles
    reactions_roles = reactions.split(',')
    for reaction_role in reactions_roles:
        try:
            emoji, role_mention = reaction_role.strip().split(' ')
            role_id = role_mention.replace('@', '').replace('<', '').replace('>', '').replace('&', '')
            await message.add_reaction(emoji)
            created_messages.setdefault(message.id, {})[emoji] = role_id
            print(f"Reaction {emoji} added for role ID {role_id}")  # Debugging line
        except ValueError:
            print("Invalid format in reactions and roles.")  # Debugging line
            await interaction.response.send_message("Invalid format in reactions and roles. Ensure it's in the format: emoji @RoleName", ephemeral=True)
            return

    await interaction.response.send_message("Role creation embed sent successfully!", ephemeral=True)
    print("Role creation embed sent successfully!")  # Debugging line

@bot.event
async def on_reaction_add(reaction, user):
    print(f"Reaction {reaction.emoji} added by {user}")  # Debugging line
    if reaction.message.id in created_messages:
        role_id = created_messages[reaction.message.id].get(str(reaction.emoji))
        if role_id:
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, id=int(role_id))
            if role:
                member = guild.get_member(user.id)
                if member:
                    await member.add_roles(role)
                    print(f"Assigned role {role.name} to {member.display_name}")  # Debugging line
                else:
                    print(f"Member {user} not found in guild")  # Debugging line
            else:
                print(f"Role ID {role_id} not found in guild")  # Debugging line
        else:
            print(f"Reaction {reaction.emoji} is not tracked for any role")  # Debugging line
    else:
        print(f"Message ID {reaction.message.id} is not tracked for reactions")  # Debugging line


@bot.event
async def on_reaction_remove(reaction, user):
    print(f"Reaction {reaction.emoji} removed by {user}")  # Debugging line
    # Check if the message is one that we've tracked for role reactions
    if reaction.message.id in created_messages:
        # Get the role ID associated with the removed reaction (if any)
        role_id = created_messages[reaction.message.id].get(str(reaction.emoji))
        if role_id:
            guild = reaction.message.guild
            role = discord.utils.get(guild.roles, id=int(role_id))
            if role:
                member = guild.get_member(user.id)
                if member:
                    await member.remove_roles(role)
                    print(f"Removed role {role.name} from {member.display_name}")  # Debugging line
                else:
                    print(f"Member {user} not found in guild")  # Debugging line
            else:
                print(f"Role ID {role_id} not found in guild")  # Debugging line
        else:
            print(f"Reaction {reaction.emoji} is not tracked for any role")  # Debugging line
    else:
        print(f"Message ID {reaction.message.id} is not tracked for reactions")  # Debugging line