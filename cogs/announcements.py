import discord
from discord.ext import commands
import logging

logger = logging.getLogger('generic_bot.announcements')

class Announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="announce", description="Make an announcement")
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx: commands.Context, *, message: str):
        channel = discord.utils.get(ctx.guild.text_channels, name="announcements")
        
        embed = discord.Embed(
            title="📢 Announcement",
            description=message,
            color=0xe74c3c
        )
        embed.set_footer(text=f"Posted by {ctx.author.display_name}")
        
        if channel:
            await channel.send(embed=embed)
            await ctx.reply(f"✅ Announcement posted in {channel.mention}")
        else:
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Announcements(bot))
