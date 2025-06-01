import discord
from discord.ext import commands
from discord import app_commands
import json
import google.generativeai as genai

intents = discord.Intents.all()

with open('main.json', 'r') as JSON_MAIN:
    KEY = json.load(JSON_MAIN)
key = KEY["key"]

group_id = None
group_name = None

ROLE_PROMPT = """
你是一個批卷器，你要負責幫我檢查答案是否全數正確，若其中有個答案錯誤就請你把用戶錯誤的選項標記起來並告訴我哪裡有錯誤。，若全部正確就回答'衛星'。這是正確答案:'[求助, 有人類自主意識的機器人, PG企鵝, 一隻, 無數隻]'。
你批改答案的時候可以改的寬鬆一點，不必太嚴格，意思有達到就好，但不可以放太多水。例如一隻可以寫成1隻或只有寫數字1，無數隻也可以寫成無限或無限隻或無限個或無數個。
以下是用戶的答案:
"""

class First(discord.ui.Modal, title="第一層儀表板"):
    one = discord.ui.TextInput(label="為什麼北極企鵝會提到波雞?", placeholder="因為北極企鵝向波雞....?", max_length=10)
    two = discord.ui.TextInput(label="北極企鵝是什麼?", max_length=10)
    three = discord.ui.TextInput(label="南極企鵝是誰創造的？", placeholder="(請填人名)", max_length=10)
    four = discord.ui.TextInput(label="北極企鵝有幾隻？", placeholder="請填數量", max_length=10)
    five = discord.ui.TextInput(label="南極企鵝有幾隻？", max_length=10)

    async def on_submit(self, interaction: discord.Interaction):
        # 先延遲回應，避免超時
        await interaction.response.defer(ephemeral=True)  

        # 收集使用者輸入
        answer = [
            self.one.value,
            self.two.value,
            self.three.value,
            self.four.value,
            self.five.value,
        ]
        answer_text = "\n".join(answer)

        # 設置 API Key
        genai_API_KEY = "AIzaSyDMtK4Zd9jDOc5KjBv6SdyWiYejymKkWFE"
        genai.configure(api_key=genai_API_KEY)

        # 設置 AI 模型
        model = genai.GenerativeModel("gemini-pro")

        try:
            # 生成 AI 回應
            response = model.generate_content([ROLE_PROMPT, answer_text])
            reply = response.text.strip().lower() if response else None
        except Exception as e:
            reply = None
            print("AI 回應錯誤:", e)

        # 確保 AI 回應有效
        if not reply:
            await interaction.followup.send("系統錯誤，請稍後再試。", ephemeral=True)
            return
        member = interaction.user
        correct_role_id = 1323969057971638312  # 正確答案新增的身分組
        incorrect_role_id = 1323690467459596338  # 錯誤答案移除的身分組
        # 判斷是否正確
        if reply == "衛星":
            role = discord.utils.get(interaction.guild.roles, id=correct_role_id)
            await member.add_roles(role)
            await interaction.followup.send("回答正確，正在進入樓層。", ephemeral=True)
        else:
            role = discord.utils.get(interaction.guild.roles, id=incorrect_role_id)
            await member.remove_roles(role)
            await interaction.followup.send("回答錯誤，回到起點。", ephemeral=True)

        print("AI 回覆:", reply)
        print("使用者輸入:", answer)


class dashboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "儀錶板", description = "一個奇怪的儀表板")
    async def dashboard(self, interaction: discord.Interaction):
        await interaction.response.send_modal(First())
                    

async def setup(bot: commands.Bot):
    await bot.add_cog(dashboard(bot))