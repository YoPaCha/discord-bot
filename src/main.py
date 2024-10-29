import os
import random
import logging
import subprocess
import discord
from discord import app_commands

# le TOKEN

TOKEN = os.getenv('DISCORD_TOKEN')

# un peu de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('discord_bot')

# les permissions du bot sur Discord

intents = discord.Intents.default()
intents.message_content = True


# Class principale
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        # Create a CommandTree instance
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This is called when the bot starts
        await self.tree.sync()  # Sync commands with Discord

# l'instanciation du bot
bot = MyBot()

# definir 2 commandes
@bot.event
async def on_ready():
    logger.info(f'{bot.user} est connecté à Discord!')

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
    """Dire bonjour à l'utilisateur"""
    await interaction.response.send_message(f"Bonjour {interaction.user.name}!")

# Lancer le bot
bot.run(TOKEN)