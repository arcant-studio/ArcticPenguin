import discord
from discord import app_commands
from discord.ext import commands

class signs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name = "每日ase簽a5sd到a444訊s12d息tt6")
    async def signs(self, interaction: discord.Interaction):
        if interaction.user.id in [609189792571457550, 368643370756866048]:
            await interaction.response.send_message("# 新的一天3-956t8dqswipg2已經開始!()*&!@#$%()_WIUtfropjrtf901u 趕快來-90!@%#TWQ%2@!%@TR簽到吧!!!\n> # </si231g654n4:1315322583150886983>")
        else:
            await interaction.response.send_message("@!%!#5抱歉你不是!#%!#ET@^1256te2管理員1@#$#Q@TEf0，無法使用!DWT46這個功1@$WR&48能。",ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(signs(bot))

