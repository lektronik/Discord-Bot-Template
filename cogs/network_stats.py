import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import logging
import os

logger = logging.getLogger('generic_bot.network_stats')

class NetworkStats(commands.Cog):
    """Fetches and displays real-time network statistics from your API."""
    
    def __init__(self, bot):
        self.bot = bot
        self.api_base = os.getenv('API_BASE_URL', 'https://your-api.com/api')
        self.update_stats.start()
    
    def cog_unload(self):
        self.update_stats.cancel()
    
    async def fetch_json(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        return await resp.json()
        except Exception as e:
            logger.error(f"API fetch error: {e}")
        return None
    
    async def generate_stats_embed(self):
        network_data = await self.fetch_json(f"{self.api_base}/network_stats")
        prices_data = await self.fetch_json(f"{self.api_base}/token/prices")
        health_data = await self.fetch_json(f"{self.api_base}/health")
        
        embed = discord.Embed(
            title="📊 Network Statistics",
            description="Real-time data from your network",
            color=0x3498db
        )
        
        if isinstance(network_data, dict):
            embed.add_field(
                name="🔗 Network",
                value=f"Transactions: {network_data.get('total_transactions', 'N/A')}\n"
                      f"Tokens: {network_data.get('total_tokens', 'N/A')}\n"
                      f"Pledges: {network_data.get('total_pledges', 'N/A')}",
                inline=True
            )
        
        if isinstance(prices_data, dict):
            price = prices_data.get('price', 'N/A')
            embed.add_field(
                name="💰 Token Price",
                value=f"${price}",
                inline=True
            )
        
        if isinstance(health_data, dict):
            status = "🟢 Online" if health_data.get('status') == 'ok' else "🔴 Issues"
            embed.add_field(name="🖥️ API Status", value=status, inline=True)
        
        embed.set_footer(text="Updates every 5 minutes")
        return embed
    
    @tasks.loop(minutes=5)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name="network-stats")
            if channel:
                try:
                    embed = await self.generate_stats_embed()
                    async for msg in channel.history(limit=5):
                        if msg.author == self.bot.user and msg.embeds:
                            await msg.edit(embed=embed)
                            return
                    await channel.send(embed=embed)
                except Exception as e:
                    logger.error(f"Stats update error: {e}")
    
    @commands.hybrid_command(name="stats", description="Show live network statistics")
    async def stats_command(self, ctx: commands.Context):
        await ctx.defer()
        try:
            embed = await self.generate_stats_embed()
            await ctx.reply(embed=embed)
        except Exception as e:
            logger.error(f"Stats command error: {e}")
            await ctx.reply("Unable to fetch stats at this time.")

async def setup(bot):
    await bot.add_cog(NetworkStats(bot))
