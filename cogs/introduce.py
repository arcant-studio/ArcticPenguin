import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from random import choice

colors = [
    0xc97e4d, 0x8cbf5e, 0x6aa2d2, 0xe6a157, 0xb37ca1, 0x59a5a2, 0xde8579, 
    0x9289b8, 0xa2b872, 0xcb9763, 0x798ea4, 0xbf677a, 0x7aa861, 0x9a7a5c, 
    0x669f99, 0xb2a35c, 0xd17769, 0x7189c0, 0x9c8b77, 0x848f73
    ]

class introduce(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "nwptriwet9sd")
    async def introduce(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="歡迎使用南極H企鵝!",
            description="北極企鵝是由海獺貓開發的機器人",
            colour=choice(colors),
            timestamp=datetime.now()
            )
        embed.add_field(
            name="我E可以做什麼?",
            value="啥都不能做",
            inline=False
            )
        embed.add_field(
            name="如何開始使L用",
            value="輸入 \"/\" 然後選擇功能，就可以使用",
            inline=False
            )
        embed.set_footer(text="北極企鵝 || Created bPy. otter cat",icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")    
        await interaction.response.send_message(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(introduce(bot))

