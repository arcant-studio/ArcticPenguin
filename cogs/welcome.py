import discord
from discord.ext import commands
from datetime import datetime
import json
from random import choice

colors = [
    0xc97e4d, 0x8cbf5e, 0x6aa2d2, 0xe6a157, 0xb37ca1, 0x59a5a2, 0xde8579, 
    0x9289b8, 0xa2b872, 0xcb9763, 0x798ea4, 0xbf677a, 0x7aa861, 0x9a7a5c, 
    0x669f99, 0xb2a35c, 0xd17769, 0x7189c0, 0x9c8b77, 0x848f73
]



class Welcome(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def format_welcome_message(self, member, welcome_MSG):
        count = member.guild.member_count
        guild = member.guild.name
        user = member.display_name
        title = welcome_MSG["title"].replace("{user}", user)
        author_name = welcome_MSG["author"]["name"]
        author_name = author_name.replace("{guild}", guild)
        author_name = author_name.replace("{count}", str(count))
        
        return title, author_name

    async def send_welcome_embed(self, channel, member, welcome_MSG, title, author_name):
        embed = discord.Embed(
            title=title,
            description=welcome_MSG["description"],
            colour=choice(colors),
            timestamp=datetime.now()
        )

        embed.set_author(
            name=author_name,
            icon_url = member.guild.icon
        )

        if welcome_MSG.get("images"):
            embed.set_image(url=welcome_MSG["images"])
            
        embed.set_thumbnail(url=member.display_avatar)
        embed.set_footer(
            text="北極企鵝 || Created by. otter cat", 
            icon_url="https://cdn.discordapp.com/app-icons/1269666706876530733/e185878d40272a50720334434811b71a.png?size=256"
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        with open('./json/welcome.json', 'r', encoding='utf-8') as JSON_welcome:
            data = json.load(JSON_welcome)
        if guild_id not in data:
            return

        group = data[guild_id]
        welcome_MSG = group["welcome_MSG"]

        channel_id = int(group["CH_welcome"])
        channel = self.bot.get_channel(channel_id)

        if not channel:
            return

        title, author_name = self.format_welcome_message(member, welcome_MSG)

        await self.send_welcome_embed(channel, member, welcome_MSG, title, author_name)

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))