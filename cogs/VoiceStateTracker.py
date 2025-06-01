import discord
import datetime
from discord.ext import commands
import discord.voice_state
import json
from random import choice

colors = [
    0xc97e4d, 0x8cbf5e, 0x6aa2d2, 0xe6a157, 0xb37ca1, 0x59a5a2, 0xde8579, 
    0x9289b8, 0xa2b872, 0xcb9763, 0x798ea4, 0xbf677a, 0x7aa861, 0x9a7a5c, 
    0x669f99, 0xb2a35c, 0xd17769, 0x7189c0, 0x9c8b77, 0x848f73
    ]

class VoiceStateTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    def create_base_embed(self, title: str, color: discord.Color, member: discord.Member, channel: discord.VoiceChannel) -> discord.Embed:
        timestamp = int(datetime.datetime.now().timestamp())
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        
        embed = discord.Embed(title=title, color=color)
        embed.add_field(
            name='',
            value=(
                f'時間：<t:{timestamp}:d> <t:{timestamp}:T> <t:{timestamp}:R>\n'
                f'用戶：{member.mention} ({member.name})\n'
                f'頻道：{channel.mention}'
            ),
            inline=False
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text="北極企鵝 || Created by. PGpenguin72 and IceBearowob",icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")
        return embed

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        with open("./json/Guild_setting.json",'r', encoding='utf-8') as file:
            Setting = json.load(file)
        guild_id = member.guild.id
        if Setting[str(guild_id)].get("Voice_State") == "True":
            if before.channel != after.channel:
                if not before.channel and after.channel:
                    embed = self.create_base_embed(
                        "> :inbox_tray: 加入語音頻道",
                        discord.Color.green(),
                        member,
                        after.channel
                    )
                    await after.channel.send(embed=embed, silent=True)

                elif before.channel and not after.channel:
                    embed = self.create_base_embed(
                        "> :outbox_tray: 離開語音頻道",
                        discord.Color.red(),
                        member,
                        before.channel
                    )
                    await before.channel.send(embed=embed, silent=True)

                elif before.channel and after.channel:
                    embed = self.create_base_embed(
                        "> :outbox_tray: 切換語音頻道 :inbox_tray:",
                        discord.Color.blue(),
                        member,
                        after.channel
                    )
                    embed.add_field(
                        name='',
                        value=f'來自：{before.channel.mention}',
                        inline=False
                    )
                    await after.channel.send(embed=embed, silent=True)
                if before.channel is None and after.channel:
                    if member.id == 613007318258548766:
                        channel_id = after.channel.id
                        channel = self.bot.get_channel(channel_id)
                        await channel.send("<@613007318258548766>唱歌!!!")
                    if member.voice.channel.name == "企鵝的小小小窩":
                        channel_id = after.channel.id
                        channel = self.bot.get_channel(channel_id)
                        embed = discord.Embed(title="歡迎你加入這個小小小窩，請查看下面的小小小窩規範喔!",
                          description="# 請看下面",
                          colour=choice(colors),
                          timestamp=datetime.datetime.now())

                        embed.set_author(name=f"哈囉! {member.name} ，歡迎來到企鵝的小小小窩!",
                                         icon_url=f"{member.display_avatar.url}")

                        embed.set_footer(text="北極企鵝 || Created by. otter cat",
                        icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256")

                        await channel.send(embed = embed)
                        await channel.send("https://discord.com/channels/1210593784128340028/1309097921756659716/1309099141854400544")

                        


            current_channel = after.channel
            if not current_channel:
                return

#            state_changes = [
#                (before.self_deaf, after.self_deaf, "> :headphones: 開啟拒聽", "> :headphones: 關閉拒聽"),
#                (before.self_mute, after.self_mute, "> :microphone2: 關閉麥克風", "> :microphone2: 開啟麥克風"),
#                (before.self_stream, after.self_stream, "> :desktop: 開啟直播", "> :desktop: 關閉直播"),
#                (before.self_video, after.self_video, "> :camera: 開啟鏡頭", "> :camera: 關閉鏡頭")
#            ]
#   
#            for before_state, after_state, enable_title, disable_title in state_changes:
#                if before_state != after_state:
#                    title = enable_title if after_state else disable_title
#                    embed = self.create_base_embed(
#                        title,
#                        member.top_role.color,
#                        member,
#                        current_channel
#                    )
#                    await current_channel.send(embed=embed, silent=True)

async def setup(bot):
    await bot.add_cog(VoiceStateTracker(bot))