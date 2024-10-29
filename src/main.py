import os
import random
import logging
import subprocess
import discord
from discord import app_commands
import openai

# le TOKEN

TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

@bot.tree.command(name="recipe")
async def recipe(interaction: discord.Interaction):
    """Generate a random recipe using ChatGPT."""
    try:
        # Set OpenAI API key
        openai.api_key = OPENAI_API_KEY

        # Prompt for the GPT model
        prompt = "Donne moi une recette au hasard ainsi qu'un lien."
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or any available model
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the recipe information from the response
        recipe_text = response['choices'][0]['message']['content']

        # Send the recipe back to the Discord channel
        await interaction.response.send_message(recipe_text)

    except Exception as e:
        logger.error(f"Error generating recipe: {e}")
        await interaction.response.send_message("Désolé, je ne peux pas générer de recette pour le moment.")

# Lancer le bot
bot.run(TOKEN)