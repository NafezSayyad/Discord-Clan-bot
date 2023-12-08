from discord.ext import commands
from discord import ui
import discord
import asyncio



def setup(bot):
    bot.add_cog(PollCog(bot))

class PollQuestionnaire(ui.View):
    def __init__(self, timeout: int = 60):
        super().__init__(timeout=timeout)
        self.poll_question = None

    @ui.button(label='✅', custom_id='poll_yes', style=discord.ButtonStyle.success)
    async def yes_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.poll_question = True
        self.stop()

    @ui.button(label='❌', custom_id='poll_no', style=discord.ButtonStyle.danger)
    async def no_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        self.poll_question = False
        self.stop()

class PollCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='poll')
    async def poll(self, ctx):
        # Ask the user to initiate the poll
        await ctx.send("Please initiate the poll by clicking on the buttons below:")
        
        questionnaire = PollQuestionnaire()
        await ctx.send("Poll initiated!", view=questionnaire)

        try:
            await asyncio.wait_for(questionnaire.wait(), timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("Poll creation timed out. Please try again.")
            return

        if questionnaire.poll_question is not None:
            await ctx.send(f"Poll question: {questionnaire.poll_question}")
            # Continue with the rest of your poll logic
        else:
            await ctx.send("Poll creation canceled.")

async def setup(bot):
    await bot.add_cog(PollCog(bot))
