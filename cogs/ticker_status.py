import discord
from discord.ext import commands, tasks
import aiohttp
import logging
import os

logger = logging.getLogger('generic_bot.ticker')

class TickerStatus(commands.Cog):
    """Updates bot status with live price/stats."""
    
    def __init__(self, bot):
        self.bot = bot
        self.api_base = os.getenv('API_BASE_URL', 'https://your-api.com/api')
        self.update_status.start()
    
    def cog_unload(self):
        self.update_status.cancel()
    
    @tasks.loop(minutes=2)
    async def update_status(self):
        await self.bot.wait_until_ready()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base}/token/prices", timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if isinstance(data, dict):
                            price = data.get('price', 'N/A')
                            await self.bot.change_presence(
                                activity=discord.Activity(
                                    type=discord.ActivityType.watching,
                                    name=f"Price: ${price}"
                                )
                            )
                            return
        except Exception as e:
            logger.error(f"Status update error: {e}")
        
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="!help for commands"
            )
        )

async def setup(bot):
    await bot.add_cog(TickerStatus(bot))
