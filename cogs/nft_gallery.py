import discord
from discord.ext import commands
import aiohttp
import logging
import os

logger = logging.getLogger('generic_bot.nft_gallery')

class NFTGallery(commands.Cog):
    """Display tokens/NFTs from your network."""
    
    def __init__(self, bot):
        self.bot = bot
        self.api_base = os.getenv('API_BASE_URL', 'https://your-api.com/api')
    
    @commands.hybrid_command(name="tokens", description="Show all tokens on the network")
    async def tokens_command(self, ctx: commands.Context):
        await ctx.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base}/tokens/list", timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        tokens = data if isinstance(data, list) else data.get('tokens', [])
                        
                        embed = discord.Embed(
                            title="🪙 Token Gallery",
                            description=f"Found {len(tokens)} tokens",
                            color=0xf1c40f
                        )
                        
                        for token in tokens[:10]:
                            name = token.get('name', 'Unknown')
                            symbol = token.get('symbol', '???')
                            supply = token.get('total_supply', 'N/A')
                            embed.add_field(
                                name=f"{symbol}",
                                value=f"**{name}**\nSupply: {supply}",
                                inline=True
                            )
                        
                        await ctx.reply(embed=embed)
                        return
            await ctx.reply("Could not fetch token data.")
        except Exception as e:
            logger.error(f"Tokens command error: {e}")
            await ctx.reply("Error fetching tokens.")
    
    @commands.hybrid_command(name="token", description="Show details for a specific token")
    async def token_command(self, ctx: commands.Context, symbol: str):
        await ctx.defer()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_base}/tokens/stats", timeout=10) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        tokens = data if isinstance(data, list) else data.get('tokens', [])
                        
                        for token in tokens:
                            if token.get('symbol', '').upper() == symbol.upper():
                                embed = discord.Embed(
                                    title=f"🪙 {token.get('name', symbol)}",
                                    color=0x3498db
                                )
                                embed.add_field(name="Symbol", value=token.get('symbol', 'N/A'), inline=True)
                                embed.add_field(name="Supply", value=token.get('total_supply', 'N/A'), inline=True)
                                embed.add_field(name="Holders", value=token.get('holders', 'N/A'), inline=True)
                                await ctx.reply(embed=embed)
                                return
                        
                        await ctx.reply(f"Token `{symbol}` not found.")
                        return
            await ctx.reply("Could not fetch token data.")
        except Exception as e:
            logger.error(f"Token command error: {e}")
            await ctx.reply("Error fetching token details.")

async def setup(bot):
    await bot.add_cog(NFTGallery(bot))
