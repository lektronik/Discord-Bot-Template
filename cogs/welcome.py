import discord
from discord.ext import commands
import logging

logger = logging.getLogger('generic_bot.welcome')

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            welcome_embed = discord.Embed(
                title=f"Welcome to {member.guild.name}! 🎉",
                description=(
                    f"Hey {member.mention}!\n\n"
                    "We're excited to have you here. Here's how to get started:\n\n"
                    "1️⃣ Read the rules in #rules\n"
                    "2️⃣ Introduce yourself in #introductions\n"
                    "3️⃣ Check out #announcements for updates\n\n"
                    "Have fun! 🚀"
                ),
                color=0x2ecc71
            )
            welcome_embed.set_thumbnail(url=member.display_avatar.url)
            await member.send(embed=welcome_embed)
            logger.info(f"Sent welcome DM to {member.name}")
        except discord.Forbidden:
            logger.warning(f"Could not DM {member.name}")
        except Exception as e:
            logger.error(f"Welcome error: {e}")

async def setup(bot):
    await bot.add_cog(Welcome(bot))
