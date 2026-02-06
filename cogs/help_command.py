import discord
from discord.ext import commands
import logging

logger = logging.getLogger('generic_bot.help')

help_data = {
    "EN": {
        "title": "❓ Bot Commands",
        "description": "Here are the available commands:",
        "commands": {
            "!help": "Show this help message",
            "!stats": "Show network statistics",
            "!leaderboard": "View top members",
            "!rank": "Check your rank",
            "!propose": "Create a proposal (Admin)",
            "!proposals": "View active proposals",
            "!purge N": "Delete N messages (Admin)",
            "!slowmode N": "Set slowmode (Admin)",
        }
    },
    "EL": {
        "title": "❓ Εντολές Bot",
        "description": "Διαθέσιμες εντολές:",
        "commands": {
            "!help": "Εμφάνιση βοήθειας",
            "!stats": "Στατιστικά δικτύου",
            "!leaderboard": "Κατάταξη μελών",
            "!rank": "Η θέση σας",
        }
    }
}

class CustomHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.remove_command('help')
    
    def get_user_lang(self, member):
        if hasattr(member, 'roles'):
            role_names = [r.name.upper() for r in member.roles]
            for lang in ["EL", "ES", "RU", "JA"]:
                if lang in role_names:
                    return lang
        return "EN"
    
    @commands.hybrid_command(name="help", description="Show bot commands")
    async def help_command(self, ctx: commands.Context, command: str = None):
        lang = self.get_user_lang(ctx.author)
        text = help_data.get(lang, help_data["EN"])
        
        embed = discord.Embed(
            title=text["title"],
            description=text["description"],
            color=0x3498db
        )
        
        for cmd, desc in text.get("commands", {}).items():
            embed.add_field(name=cmd, value=desc, inline=True)
        
        await ctx.reply(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(CustomHelp(bot))
