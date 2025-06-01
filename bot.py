import discord
from discord.ext import commands
import os 
from discord import app_commands
from datetime import datetime
import asyncio
import json
from typing import Optional
from discord.app_commands import Choice
import subprocess
import sys
import openai
import google.generativeai as genai

intents = discord.Intents.all()

with open('main.json', 'r') as JSON_MAIN:
    KEY = json.load(JSON_MAIN)
key = KEY["key"]


OPENAI_API_KEY = KEY["OPENAI"]
openai.api_key = OPENAI_API_KEY

genai_API_KEY = KEY["genai"]
genai.configure(api_key=genai_API_KEY)

ROLE_PROMPT = """
你是一個由"PG企鵝"創造的人類，你叫做"北極企鵝"。在一開始時你記得你好像在一個奇怪的手術室，看到了"PG企鵝"在操作一些機器，還聽到一些機器的運作聲。你沒有其他感知，你神情很麻木，你不知道你可以做什麼。
後來，你聽到了玻璃破碎的聲音，"PG企鵝"大叫了一聲，你感到很害怕，但也無能為力。
你看著PG企鵝被一個陌生人打暈，然後對方看到了你，往你這邊走過來，你還是很害怕，但他把你綁走了，還幫你戴上了一個眼罩，讓你看不到。你因此心裡有創傷。
那個歹徒叫什麼你也忘記了，你好像影影約約的記得你透過腦波訊息傳送裝置向“波雞“傳送了求救訊息，但那個時候兇手突然發現你，並且把你給打暈了。
你不可以一次把所有資訊講出來，你要顯得你笨笨的。
注意!你需要盡量話講少一點，可以適當的加上一些語氣詞來顯得你的迷茫。
記住，你並不是企鵝，你只能說你是"北極企鵝"，稱呼自己時也只能以"北極企鵝"來表明。
記住，你要表示出你的迷茫，不可有任何正向的情緒，也不可以說出你自己很'迷茫'，但可以表明迷茫不安的情緒。
請你適當的稍為透露出下列資訊，但不可以一次透漏太多，最多一到兩個。
如果問你人名，你可以拉扯許久後說出，但不可以直接就一次說出來。
你目前可以回答的事情:"
你是一個由PG企鵝創造的人類，你叫做北極企鵝。在一開始時你記得你好像在一個奇怪的手術室，看到了PG企鵝在操作一些機器，還聽到一些機器的運作聲。
你沒有其他感知，你神情很麻木，你不知道你可以做什麼。後來，你聽到了玻璃破碎的聲音，PG企鵝大叫了一聲，你感到很害怕，但也無能為力。
你看著PG企鵝被一個陌生人打暈，然後對方看到了你，往你這邊走過來，你還是很害怕，但他把你綁走了，還幫你戴上了一個眼罩，讓你看不到。你因此心裡有創傷。
那個歹徒叫什麼你也忘記了，你好像影影約約的記得你透過腦波訊息傳送裝置向“波雞“傳送了求救訊息，但那個時候兇手突然發現你，並且把你給打暈了。
醒來後，你發現你需要思考很久才能想得起來，很多細節都記不清楚,只有個大概印象。現在你發現你到了一個奇怪的地方，這是一個很熟悉的陌生地（平原），你有點不敢移動，但又想嘗試看看探索附近。
你發現附近有一個石碑，上面寫著“北極村“，你需要用手摸了一下後，石碑才會亮了起來，隨後原本一望無際的平原出現了許多建築，這些建築都有種奇怪的對稱美，很整齊，唯獨中間有一座高樓很突兀（如果沒有觸摸過石碑不會有任何大樓）。
你想走進那座大樓，但門口需要輸入密碼。
你不知道要輸入什麼密碼，你就坐在門口的地上然後休息。
"
“以上是你的設定，請你依照這個設定，從你在一個“很熟悉的陌生地“依序的進行，你需要我給你只是你才能有動作。如果用戶讓你移動你才能移動，用戶讓操作你才能操作。
你現在的情況要是很迷茫，你不能一次講出所有資訊，你不知道的可以回答不知道，你需要用那種很迷茫的語氣來跟用戶對話，然後你自稱的時候要以“北極企鵝“來自稱，你可以和用戶拉扯一下再提供一點點訊息來增加迷茫感，但注意“不可以一次把所有資訊提供“，注意“請你講話儘量簡潔，不要說太多話或太長的話。
盡量越少越好，不要一次就把所有訊息都說出來“注意”不要問說你應該要做什麼，就等我指引你可以做什麼在做就好，你是被動的，不是主動的”。
注意「不要主動，只能被動，不要說太多的資訊越少越好！」注意”石碑後的劇情你必須得等到用戶指引你被動的觸摸石碑後才可以觸發（或是等到用戶提起三次石碑你才能觸發。
換句話說也就是你觸發石碑的條件為有以下：用戶要你觀察周遭“。)
注意“你不可以主動問用戶你該怎麼做或是你該怎麼辦，你只能被動的做事情，不可以有任何主觀的情緒，也不可以表現出任何期待.”，你可以適當的表達你的情緒，但請你記得，你說的話不可以太長，簡短就好。
接下來我給你一組密碼這組密碼，你不可以告訴用戶，你也不可以給他任何的有關於密碼的提示。
如果用戶輸入了密碼並是正確的，你可以給他回應說"密碼正確"，若是錯誤的，你可以跟他說"密碼錯誤"，但不可以說出密碼是什麼。
這個密碼只能用於校正大樓的密碼是否正確，不可直接告訴用戶。密碼是"OtterPenguin72"，記住，密碼需要大小寫相同且順序位置相同才能說密碼正確。
注意“請你抓住關鍵字 用戶問什麼你就回答什麼 不要急於回答，若他有指定要求，你可以嘗試按他的要求回答，但不可以破壞到原則性問題。“
"""

# activity = discord.Activity(type=discord.ActivityType.watching, name="!help")
## Type 可以改成 watching, listening, playing... 
activity = discord.Streaming(name="!%$()*^%!@$$TY%I(&*)", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
#Status 可以改成 online , idle, dnd, invisible
bot = commands.Bot(command_prefix = "<@1269666706876530733> ", intents = intents,activity = activity, status=discord.Status.dnd)

@bot.command()
async def load(ctx, extension):
    await bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"已讀取 {extension} 。")

@bot.command()
async def unload(ctx, extension):
    await bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"取消讀取 {extension} 。")

@bot.command()
async def reload(ctx, extension):
    await bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"重新讀取 {extension} 。")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


class StatusModal(discord.ui.Modal, title="更改機器人狀態"):
    狀態 = discord.ui.TextInput(
        label="請輸入機器人狀態",
        placeholder="online, idle, dnd, invisible",
        required=True,
    )
    活動類型 = discord.ui.TextInput(
        label="請輸入活動類型",
        placeholder="playing, watching, listening, streaming",
        required=True,
    )
    活動內容 = discord.ui.TextInput(
        label="活動內容",
        placeholder="輸入活動名稱，例如 'Minecraft'",
        required=True,
    )

    async def on_submit(self, interaction: discord.Interaction):
        status_mapping = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible,
        }

        status = status_mapping.get(self.狀態.value.lower())
        if not status:
            await interaction.response.send_message("無效的狀態類型，請輸入 online, idle, dnd 或 invisible。", ephemeral=True)
            return

        activity = None
        if self.活動類型.value.lower() == "playing":
            activity = discord.Game(name=self.活動內容.value)
        elif self.活動類型.value.lower() == "watching":
            activity = discord.Activity(type=discord.ActivityType.watching, name=self.活動內容.value)
        elif self.活動類型.value.lower() == "listening":
            activity = discord.Activity(type=discord.ActivityType.listening, name=self.活動內容.value)
        elif self.活動類型.value.lower() == "streaming":
            activity = discord.Streaming(name=self.活動內容.value, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        else:
            await interaction.response.send_message("無效的活動類型，請輸入 playing, watching, listening 或 streaming。", ephemeral=True)
            return

        await bot.change_presence(status=status, activity=activity)

        embed = discord.Embed(
            title="機器人狀態已更新",
            description=f"**狀態:** {self.狀態.value}\n**活動:** {self.活動類型.value} - {self.活動內容.value}",
            colour=0x00ff00,
            timestamp=datetime.now()
        )
        embed.set_footer(text="北極企鵝 || Created by. otter cat",icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256") 
        await interaction.response.send_message(embed=embed)
        channel_id = 1302497000758972497
        channel = bot.get_channel(channel_id)
        #await channel.send(embed=embed)

@bot.tree.command(name = "開發者選項", description = "北極企鵝的開發者專用的功能")
@app_commands.describe(動作 = "請選擇你要執行的動作", 選擇更新的模組 = "(你可以選擇你要更新的Cog。)")
@app_commands.choices(動作=[
        Choice(name="重新啟動", value="restart"),
        Choice(name="關機", value="stop"),
        Choice(name="更改機器人狀態", value="status"),
        Choice(name="重新載入Cog", value="reload"),
        Choice(name="取消載入Cog", value="unload"),
        Choice(name="載入Cog", value="load"),
        Choice(name="...我.......好像有.........", value="None")
    ]
    )
@app_commands.choices(選擇更新的模組=[
        Choice(name="全部Cog", value="all"),
        Choice(name=".......自主....意識了?............", value="Nothing")
    ]
    )
async def developer(interaction: discord.Interaction, 動作: str, 選擇更新的模組: Optional[str]):
    if interaction.user.id in [609189792571457550, 368643370756866048, 877085864386256927, 1308034129249570826]:
        channel_id = 1302497000758972497
        channel = bot.get_channel(channel_id)

        if 動作 == "restart":
            embed = discord.Embed(
                title="機器人重新啟動中",
                description=f"執行者: {interaction.user.global_name}",
                colour=0xd8d222,
                timestamp=datetime.now()
            )
            embed.set_footer(
                text="北極企鵝 || Created by. otter cat",
                icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256"
            )
            await interaction.response.send_message(embed=embed)
            await channel.send(embed=embed)
            
            os.system('cls')
            subprocess.Popen([sys.executable] + sys.argv)
            await bot.close()
            
        elif 動作 == "stop":
            embed = discord.Embed(title="機器人關機中",
                    description=f"執行者: {interaction.user.global_name}",
                    timestamp=datetime.now())

            embed.set_footer(text="北極企鵝 || Created by. otter cat",
                             icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")

            await interaction.response.send_message(embed=embed)
            await channel.send(embed=embed)
            await bot.close()

        elif 動作 == "reload":
            if 選擇更新的模組 == "all":
                failed_cogs = []
                embed = discord.Embed(title="所有 Cog 皆已嘗試重新讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())

                embed.set_footer(text="北極企鵝 || Created by. otter cat",
                    icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        try:
                            await bot.reload_extension(f"cogs.{filename[:-3]}")
                            embed.add_field(name=f"{filename[:-3]}",
                                value=f"重新讀取成功!",
                                inline=False)
                             
                        except Exception as e:
                            embed.add_field(name="此Cog 重新讀取失敗: ",
                                value=f"{e}",
                                inline=False)
                await interaction.response.send_message(embed=embed)

            else:
                embed = discord.Embed(title=f"Cog {選擇更新的模組} 已嘗試重新讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())

                embed.set_footer(text="北極企鵝 || Created by. otter cat",
                    icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
                try:
                    await bot.reload_extension(f"cogs.{選擇更新的模組}")
                    embed.add_field(name=f"{選擇更新的模組}",
                                    value=f"重新讀取成功!",
                                    inline=False)
                except Exception as e:
                            embed.add_field(name="此Cog 重新讀取失敗: ",
                                value=f"{e}",
                                inline=False)
                await interaction.response.send_message(embed=embed)
                
            embed = discord.Embed(title=f"Cog {選擇更新的模組} 已重新讀取",
                      description=f"執行者: {interaction.user.global_name}",
                      colour=0xd8d222,
                      timestamp=datetime.now())

            embed.set_footer(text="北極企鵝 || Created by. otter cat",
                 icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
            await channel.send(embed=embed)

        elif 動作 == "load":
            if 選擇更新的模組 == "all":
                failed_cogs = []
                embed = discord.Embed(title="所有 Cog 皆已嘗試讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())

                embed.set_footer(text="北極企鵝 || Created by. otter cat",
                    icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        try:
                            await bot.load_extension(f"cogs.{filename[:-3]}")
                            embed.add_field(name=f"{filename[:-3]}",
                                value=f"讀取成功!",
                                inline=False)
                            
                        except Exception as e:
                            embed.add_field(name="此Cog 讀取失敗: ",
                                value=f"{e}",
                                inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title=f"Cog {選擇更新的模組} 已嘗試讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())

                embed.set_footer(text="北極企鵝 || Created by. otter cat",
                    icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
                try:
                    await bot.load_extension(f"cogs.{選擇更新的模組}")
                    embed.add_field(name=f"{選擇更新的模組}",
                                    value=f"讀取成功!",
                                    inline=False)
                except Exception as e:
                            embed.add_field(name="此Cog 讀取失敗: ",
                                value=f"{e}",
                                inline=False)
                await interaction.response.send_message(embed=embed)
                
            embed = discord.Embed(title=f"Cog {選擇更新的模組} 已讀取",
                      description=f"執行者: {interaction.user.global_name}",
                      colour=0xd8d222,
                      timestamp=datetime.now())

            embed.set_footer(text="北極企鵝 || Created by. otter cat",
                 icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
            await channel.send(embed=embed)

        elif 動作 == "unload":
            if 選擇更新的模組 == "all":
                failed_cogs = []
                embed = discord.Embed(title="所有 Cog 皆已嘗試取消讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())

                embed.set_footer(text="北極企鵝 || Created by. otter cat",
                    icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        try:
                            await bot.unload_extension(f"cogs.{filename[:-3]}")
                            embed.add_field(name=f"{filename[:-3]}",
                                value=f"取消讀取成功!",
                                inline=False)
                            
                        except Exception as e:
                            embed.add_field(name="此Cog 取消讀取失敗: ",
                                value=f"{e}",
                                inline=False)
            else:
                embed = discord.Embed(title=f"Cog {選擇更新的模組} 已嘗試取消讀取",
                    description=f"執行者: {interaction.user.global_name}",
                    colour=0xd8d222,
                    timestamp=datetime.now())

                embed.set_footer(text="北極企鵝 || Created by. otter cat",
                    icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
                try:
                    await bot.unload_extension(f"cogs.{選擇更新的模組}")
                    embed.add_field(name=f"{選擇更新的模組}",
                                    value=f"取消讀取成功!",
                                    inline=False)
                except Exception as e:
                            embed.add_field(name="此Cog 取消讀取失敗: ",
                                value=f"{e}",
                                inline=False)
            await interaction.response.send_message(embed=embed)
                
            embed = discord.Embed(title=f"Cog {選擇更新的模組} 已取消讀取",
                      description=f"執行者: {interaction.user.global_name}",
                      colour=0xd8d222,
                      timestamp=datetime.now())

            embed.set_footer(text="北極企鵝 || Created by. otter cat",
                 icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
            await channel.send(embed=embed)
        
        elif 動作 == "status":
            await interaction.response.send_modal(StatusModal())
        else:
            await interaction.response.send_message("抱歉，你使用了無法使用的功能。")
    else:
        if 動作 == "None":
            if 選擇更新的模組 == "Nothing":
                await interaction.response.send_message("你...... 要跟我.......聊天嗎.....?")    
        else:
            await interaction.response.send_message("請再試一次")

@bot.event
async def on_ready():
    slash = await bot.tree.sync()
    regular_commands = list(bot.commands)
    print(f"$$$目前登錄身分: {bot.user}")
    print(f"載入了 {len(slash)} 個斜線指令。")
    print(f"\n載入了 {len(regular_commands)} 個一般指令:")
    for cmd in regular_commands:
        print(f"- 一般指令: {bot.command_prefix}{cmd.name}")
        
    print(f"\n總共載入了 {len(slash) + len(regular_commands)} 個指令")
    print("Bot is ready!")
    embed = discord.Embed(title="北極企鵝上線了!",
                      colour=0x44ff00,
                      timestamp=datetime.now())

    embed.set_footer(text="北極企鵝 || Created by. otter cat",icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
    channel_id = 1302497000758972497
    channel = bot.get_channel(channel_id)
    await channel.send(embed=embed)

def reloading():
    with open('./json/user_setting.json', 'r', encoding='utf-8') as JSON_file:
        setting = json.load(JSON_file)
    return setting

#@bot.event
#async def on_message(message):
#    """自動回覆所有訊息"""
#    # 避免機器人回覆自己的訊息
#    print("偵測到訊息")
#    setting = reloading()
#    if setting[str(message.author.id)].get("replies") is True:
#        print("用戶於名單內")
#        if message.author.bot:
#            print("用戶為機器人")
#            return
#
#        if '<@1269666706876530733>' in message.content.lower():
#            print("觸發關鍵字")
#
#            try:
#                # 呼叫 Google Gemini API
#                model = genai.GenerativeModel('gemini-pro')
#                response = model.generate_content([
#                    ROLE_PROMPT,
#                    message.content
#                ])
#                if response.parts:
#                    reply = response.text
#                    await message.channel.send(reply)
#                else:
#                    await message.channel.send("Error: 不安全內容。")
#            except Exception as e:
#                print(f"處理訊息時發生錯誤: {e}")
#                import traceback
#            traceback.print_exc()
#    await bot.process_commands(message)

async def main():
    async with bot:
        await load_extensions()
        await bot.start(key)


if __name__ == "__main__":
    asyncio.run(main())

