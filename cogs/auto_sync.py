import discord
from discord.ext import commands, tasks
import logging

logger = logging.getLogger('generic_bot.auto_sync')

class AutoSync(commands.Cog):
    """Automatically sync content every 24 hours."""
    
    def __init__(self, bot):
        self.bot = bot
        self.auto_sync.start()
    
    def cog_unload(self):
        self.auto_sync.cancel()
    
    @tasks.loop(hours=24)
    async def auto_sync(self):
        await self.bot.wait_until_ready()
        logger.info("Running automatic content sync...")
        # Add your sync logic here
    
    @commands.hybrid_command(name="sync_now", description="Force content sync")
    @commands.has_permissions(administrator=True)
    async def sync_now(self, ctx: commands.Context):
        await ctx.defer()
        await ctx.reply("✅ Content synced!")

async def setup(bot):
    await bot.add_cog(AutoSync(bot))
