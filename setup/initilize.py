'''Initialize the bot object'''
from discord import Intents
from discord.ext import commands

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)