import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import json

with open('main.json', 'r', encoding='utf-8') as file:
    admin_chack = json.load(file)

class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "〇")

    async def Say(self, interaction: discord.Interaction, 〇: str):
        channel_id = interaction.channel_id
        channel = self.bot.get_channel(int(channel_id))
        if interaction.user.id in admin_chack.get("admin", []):
            await interaction.response.send_message(〇, ephemeral=True)
            await channel.send(〇)

async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))