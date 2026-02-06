import discord
from discord.ext import commands
import logging
from database import create_proposal, get_proposals, record_vote, has_voted

logger = logging.getLogger('generic_bot.governance')

class VoteView(discord.ui.View):
    def __init__(self, proposal_id):
        super().__init__(timeout=None)
        self.proposal_id = proposal_id
    
    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="vote_yes")
    async def vote_yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if has_voted(self.proposal_id, interaction.user.id):
            await interaction.response.send_message("You already voted!", ephemeral=True)
            return
        record_vote(self.proposal_id, interaction.user.id, 'yes')
        await interaction.response.send_message("✅ Voted Yes!", ephemeral=True)
    
    @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="vote_no")
    async def vote_no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if has_voted(self.proposal_id, interaction.user.id):
            await interaction.response.send_message("You already voted!", ephemeral=True)
            return
        record_vote(self.proposal_id, interaction.user.id, 'no')
        await interaction.response.send_message("❌ Voted No!", ephemeral=True)

class Governance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="propose", description="Create a proposal")
    @commands.has_permissions(administrator=True)
    async def propose(self, ctx: commands.Context, title: str, *, description: str = ""):
        proposal_id = create_proposal(title, description, ctx.author.id, str(ctx.author))
        
        embed = discord.Embed(
            title=f"📋 Proposal #{proposal_id}: {title}",
            description=description or "No description",
            color=0x9b59b6
        )
        embed.set_footer(text=f"Proposed by {ctx.author.display_name}")
        
        view = VoteView(proposal_id)
        await ctx.reply(embed=embed, view=view)
    
    @commands.hybrid_command(name="proposals", description="List active proposals")
    async def proposals_cmd(self, ctx: commands.Context):
        proposals = get_proposals()
        
        if not proposals:
            await ctx.reply("No active proposals.")
            return
        
        embed = discord.Embed(
            title="📋 Active Proposals",
            color=0x9b59b6
        )
        
        for p in proposals[:10]:
            embed.add_field(
                name=f"#{p[0]}: {p[1]}",
                value=f"Yes: {p[8]} | No: {p[9]}",
                inline=False
            )
        
        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Governance(bot))
