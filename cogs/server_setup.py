import discord
from discord.ext import commands
from discord import app_commands
import logging
import os

logger = logging.getLogger('generic_bot.server_setup')

class ServerSetup(commands.Cog):
    """Auto-configure server channels and structure."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="setup_server", description="Auto-configure server channels")
    @commands.has_permissions(administrator=True)
    async def setup_server(self, ctx: commands.Context):
        await ctx.defer()
        
        guild = ctx.guild
        created = []
        
        categories = {
            "📢 Information": ["announcements", "rules", "faq"],
            "💬 Community": ["general", "introductions", "off-topic"],
            "📊 Network": ["network-stats", "governance"],
            "🛠️ Support": ["help", "feedback"],
        }
        
        for cat_name, channels in categories.items():
            category = discord.utils.get(guild.categories, name=cat_name)
            if not category:
                category = await guild.create_category(cat_name)
                created.append(f"Category: {cat_name}")
            
            for channel_name in channels:
                channel = discord.utils.get(guild.text_channels, name=channel_name)
                if not channel:
                    await guild.create_text_channel(channel_name, category=category)
                    created.append(f"Channel: #{channel_name}")
        
        if created:
            embed = discord.Embed(
                title="✅ Server Setup Complete",
                description=f"Created {len(created)} items",
                color=0x2ecc71
            )
            embed.add_field(name="Created", value="\n".join(created[:15]) or "None")
        else:
            embed = discord.Embed(
                title="ℹ️ Server Already Configured",
                description="All channels already exist",
                color=0x3498db
            )
        
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerSetup(bot))
