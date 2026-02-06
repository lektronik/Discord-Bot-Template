import discord
from discord.ext import commands
from discord import app_commands
import logging
import os

logger = logging.getLogger('generic_bot.info')

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.docs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'docs')
    
    @app_commands.command(name="roadmap", description="Get the project roadmap")
    async def roadmap(self, interaction: discord.Interaction):
        roadmap_file = os.path.join(self.docs_path, 'Roadmap.pdf')
        if os.path.exists(roadmap_file):
            await interaction.response.send_message("📋 Here's our roadmap:", file=discord.File(roadmap_file))
        else:
            await interaction.response.send_message("📋 Roadmap: Configure your roadmap document in the `docs/` folder")
    
    @app_commands.command(name="whitepaper", description="Get the project whitepaper")
    async def whitepaper(self, interaction: discord.Interaction):
        whitepaper_file = os.path.join(self.docs_path, 'Whitepaper.pdf')
        if os.path.exists(whitepaper_file):
            await interaction.response.send_message("📄 Here's our whitepaper:", file=discord.File(whitepaper_file))
        else:
            await interaction.response.send_message("📄 Whitepaper: Configure your whitepaper document in the `docs/` folder")
    
    @app_commands.command(name="website", description="Get the project website link")
    async def website(self, interaction: discord.Interaction):
        website_url = os.getenv('WEBSITE_URL', 'https://your-website.com')
        await interaction.response.send_message(f"🌐 Visit our website: {website_url}")

async def setup(bot):
    await bot.add_cog(Info(bot))
