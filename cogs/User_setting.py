import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from random import choice
from discord.app_commands import Choice
from typing import Optional
import json

def reload():
    with open("./json/user_setting.json", "r", encoding='utf-8') as JSON_file:
        setting = json.load(JSON_file)
    return setting

class User_Setting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="用戶設定", description="設定用戶功能。")
    @app_commands.describe(選項="開啟ping我+內容後來跟我對話。", 狀態="狀態:")
    @app_commands.choices(
        選項=[
            Choice(name="ERRRRRRRRRRRRRORRRRRRR", value="replies")
        ],
        狀態=[
            Choice(name="TRUEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE", value="True"),
            Choice(name="FALSEEEEEEEEEEEEEEEEEEEEEEEEEE", value="False")
        ]
    )
    async def User_Setting(self, interaction: discord.Interaction, 選項: str = None, 狀態: str = None):
        user_id = str(interaction.user.id)
        settings = reload()

        if user_id not in settings:
            settings[user_id] = {}

        settings[user_id][選項] = True if 狀態 == "True" else False
        with open('./json/user_setting.json', 'w', encoding='utf-8') as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)
        
        await interaction.response.send_message(f"成功更新 `{選項}` 為 `{狀態}`。")

async def setup(bot: commands.Bot):
    await bot.add_cog(User_Setting(bot))
