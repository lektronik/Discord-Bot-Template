import discord
from discord.ext import commands
import logging

logger = logging.getLogger('generic_bot.moderation')

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="purge", description="Delete messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int = 10):
        if amount < 1 or amount > 100:
            await ctx.reply("Please specify between 1-100 messages.")
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🗑️ Deleted {len(deleted) - 1} messages.", delete_after=5)
    
    @commands.hybrid_command(name="slowmode", description="Set channel slowmode")
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx: commands.Context, seconds: int = 0):
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds > 0:
            await ctx.reply(f"⏱️ Slowmode set to {seconds} seconds.")
        else:
            await ctx.reply("⏱️ Slowmode disabled.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
