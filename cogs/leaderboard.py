import discord
from discord.ext import commands
import logging
from database import update_user_stats, get_leaderboard, get_user_rank

logger = logging.getLogger('generic_bot.leaderboard')

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        update_user_stats(message.author.id, str(message.author), messages=1)
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        update_user_stats(user.id, str(user), reactions=1)
    
    @commands.hybrid_command(name="leaderboard", description="Show top members by XP")
    async def leaderboard_cmd(self, ctx: commands.Context):
        users = get_leaderboard(10)
        
        embed = discord.Embed(
            title="🏆 Leaderboard",
            description="Top members by XP",
            color=0xf1c40f
        )
        
        medals = ["🥇", "🥈", "🥉"]
        for i, user in enumerate(users):
            medal = medals[i] if i < 3 else f"#{i+1}"
            embed.add_field(
                name=f"{medal} {user[1]}",
                value=f"XP: {user[2]} | Messages: {user[3]}",
                inline=False
            )
        
        await ctx.reply(embed=embed)
    
    @commands.hybrid_command(name="rank", description="Check your rank")
    async def rank_cmd(self, ctx: commands.Context):
        rank, user = get_user_rank(ctx.author.id)
        
        if user:
            embed = discord.Embed(
                title=f"📊 {ctx.author.display_name}'s Stats",
                color=0x3498db
            )
            embed.add_field(name="Rank", value=f"#{rank}", inline=True)
            embed.add_field(name="XP", value=str(user[5]), inline=True)
            embed.add_field(name="Messages", value=str(user[2]), inline=True)
            embed.add_field(name="Reactions", value=str(user[3]), inline=True)
        else:
            embed = discord.Embed(
                title="No Data Yet",
                description="Start chatting to earn XP!",
                color=0xe74c3c
            )
        
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))
