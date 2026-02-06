import discord
from discord.ext import commands
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# Setup logging
os.makedirs('logs', exist_ok=True)
logger = logging.getLogger('discord_bot')
logger.setLevel(logging.DEBUG)

file_handler = RotatingFileHandler(
    'logs/bot.log', maxBytes=10*1024*1024, backupCount=5
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Get token from environment
TOKEN = os.getenv('DISCORD_TOKEN')

class TemplateBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
    
    async def setup_hook(self):
        """Load all cogs on startup."""
        logger.info("Loading extensions...")
        
        cogs = [
            'cogs.server_setup',
            'cogs.verification',
            'cogs.language',
            'cogs.info',
            'cogs.network_stats',
            'cogs.help_command',
            'cogs.auto_sync',
            'cogs.welcome',
            'cogs.moderation',
            'cogs.announcements',
            'cogs.governance',
            'cogs.ticker_status',
            'cogs.leaderboard',
            'cogs.nft_gallery',
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded {cog}")
            except Exception as e:
                logger.error(f"Failed to load {cog}: {e}")
        
        await self.tree.sync()
        logger.info("Commands synced!")
    
    async def on_ready(self):
        logger.info(f'Logged in as {self.user} (ID: {self.user.id})')
        logger.info('Bot is ready!')

if __name__ == '__main__':
    if not TOKEN:
        print("ERROR: DISCORD_TOKEN not found in environment variables!")
        print("Create a .env file with: DISCORD_TOKEN=your_token_here")
        exit(1)
    
    bot = TemplateBot()
    bot.run(TOKEN)
