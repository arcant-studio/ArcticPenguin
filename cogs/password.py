import discord
from discord import app_commands
from discord.ext import commands
import json
from discord.utils import get

# 讀取密碼設定
with open("./json/password.json", 'r', encoding='utf-8') as file:
    passwords = json.load(file)

def user_setting():
    # 讀取已輸入的密碼設定
    try:
        with open('./json/entered_password.json', 'r', encoding="utf-8") as file_2:
            passwords_entered = json.load(file_2)
    except FileNotFoundError:
        # 如果檔案不存在，初始化為空字典
        passwords_entered = {}
    return passwords_entered

colors = [
    0xc97e4d, 0x8cbf5e, 0x6aa2d2, 0xe6a157, 0xb37ca1, 0x59a5a2, 0xde8579, 
    0x9289b8, 0xa2b872, 0xcb9763, 0x798ea4, 0xbf677a, 0x7aa861, 0x9a7a5c, 
    0x669f99, 0xb2a35c, 0xd17769, 0x7189c0, 0x9c8b77, 0x848f73
]

class password(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="密碼", description="一個密碼系統，不知道可以拿來幹啥用的。")
    @app_commands.describe(密碼="請在這個地方輸入密碼(大小寫有分)")
    async def password(self, interaction: discord.Interaction, 密碼: str = None):
        if 密碼 is None:
            await interaction.response.send_message("請輸入密碼!", ephemeral=True)
        elif 密碼 in passwords:
            # 密碼正確，進行後續處理
            passwords_entered = user_setting()  # 加載現有數據
            passwords_entered[str(interaction.user.id)] = 密碼
            
            role_id = 1323690467459596338
            role = get(interaction.guild.roles, id=role_id)

            if role:
                # 給用戶加上身分組
                await interaction.user.add_roles(role)
                await interaction.response.send_message("密碼正確，正在進入樓層。",ephemeral=True)
            else:
                await interaction.response.send_message('產生了一些問題，請稍後再嘗試。', ephemeral=True)

            # 更新密碼設定並寫回文件
            with open('./json/entered_password.json', 'w', encoding='utf-8') as file:
                json.dump(passwords_entered, file, ensure_ascii=False, indent=4)

        else:
            await interaction.response.send_message("密碼錯誤，請重新輸入", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(password(bot))
