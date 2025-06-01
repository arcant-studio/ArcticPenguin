import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from random import choice
from discord.app_commands import Choice
from typing import Optional
import json

def reload():
    with open("./json/Guild_setting.json", "r", encoding='utf-8') as JSON_file:
        setting = json.load(JSON_file)
    return setting

class Guild_Setting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="伺服器設定", description="設定機器人的一些伺服器功能。")
    @app_commands.describe(選項="請選擇你要設定的內容:", 狀態="選擇狀態:")
    @app_commands.choices(
        選項=[
            Choice(name="語音頻道活動紀錄器", value="Voice_State")
        ],
        狀態=[
            Choice(name="True", value="True"),
            Choice(name="False", value="False")
        ]
    )
    async def Guild_Setting(self, interaction: discord.Interaction, 選項: str = None, 狀態: str = None):
        if interaction.user.guild_permissions.administrator:
            guild_id = str(interaction.guild.id)
            settings = reload()

            if guild_id not in settings:
                settings[guild_id] = {}

            settings[guild_id][選項] = 狀態
            with open('./json/Guild_setting.json', 'w', encoding='utf-8') as file:
                json.dump(settings, file, ensure_ascii=False, indent=8)
            
            await interaction.response.send_message(f"已成功更新 `{選項}` 為 `{狀態}`。")
        else:
            await interaction.response.send_message("抱歉，你並不是管理員，不可以進行設定。", ephemeral=True)    

async def setup(bot: commands.Bot):
    await bot.add_cog(Guild_Setting(bot))
