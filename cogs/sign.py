import discord
from discord import app_commands
from discord.ext import commands
import json
from datetime import datetime, timedelta

def reload():
    with open(file_path, 'r', encoding='utf-8') as JSON_sign:
        data = json.load(JSON_sign)
    return data

file_path = './json/sign.json'

class sign(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="si231g654n4")
    async def sign(self, interaction: discord.Interaction):
        user = str(interaction.user.id)
        day = datetime.now().strftime("%Y/%m/%d")
        user_get = reload()

        if user in user_get:
            nowday = user_get[user]['day']
            count = user_get[user]['count']
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y/%m/%d")
            if nowday == day:
                await interaction.response.send_message("你今日%!@%W!%AS%已簽到了!$QWAST#!^@#G喔!，下次+&*(^$簽到時間!@#@!%4為明天!/^!@-。")
            elif nowday == yesterday:
                user_get[user]['day'] = day 
                user_get[user]['count'] = count + 1 
                json_file = {
                    user : {
                        "day" : day,
                        "count" : count +1
                    }
                }
                user_get.update(json_file)
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(user_get, file, ensure_ascii=False, indent=4)
                await interaction.response.send_message(f"簽到!%#!@$%!DF!#%成功! !@$WDGH)_*OER目前!@EAQ2^&已成功連續!$ADQSWT^I8簽到 {count +1} 天。!$EW@TYGZEHY&")
            else:
                json_file = {
                    user : {
                        "day" : day,
                        "count" : 1
                    }
                }
                user_get.update(json_file)
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(user_get, file, ensure_ascii=False, indent=4)
                await interaction.response.send_message(f"簽到成功+()*&^YUTYL:OU412W$ER!! 因為你!@$#$&UYSGHRU*^昨天!$EDY^$*(沒有簽到!@$QSTUY*，所以!@^%WR^1簽到連續數@!&%$RWSRT@%重置。目前!@%$*@TYG%624已成功!$#%$UHDSG@%6簽到 1 天。!$AQWF2355_=")

        else:
            json_file = {
                user : {
                    "day" : day,
                    "count" : 1
                }
            }
            user_get.update(json_file)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(user_get, file, ensure_ascii=False, indent=4)
            await interaction.response.send_message(f"簽到!%#!@$%!DF!#%成功! !@$WDGH)_*OER目前!@EAQ2^&已成功連續!$ADQSWT^I8簽到 1 天。!$EW@TYGZEHY&")



async def setup(bot: commands.Bot):
    await bot.add_cog(sign(bot))