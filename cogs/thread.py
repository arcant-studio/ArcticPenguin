import discord
from discord.ext import commands
from discord import app_commands

class Thread(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cthread", description="創建一個討論串")
    async def create_thread(self, interaction: discord.Interaction, channel: discord.TextChannel, name: str):
        # 創建討論串
        for i in range(1,11):
            fname = f"{name}{i:02d}"
            thread = await channel.create_thread(name=fname, type=discord.ChannelType.public_thread)
        
        # 回覆用戶
        await interaction.response.send_message(f"已成功創建！", ephemeral=True)

# 加載 cog
async def setup(bot):
    await bot.add_cog(Thread(bot))