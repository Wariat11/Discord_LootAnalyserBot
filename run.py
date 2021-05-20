from json import load
from discord.ext import commands
from analyst.raw_parse import LootAnalyser,pastebin_pattern
from discord import Embed
from setup import TOKEN


bot = commands.Bot(command_prefix='')

bot_analyst = LootAnalyser()

@bot.event
async def on_ready():
    print("Bot is loggin")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("https://pastebin.com"):
        if pastebin_pattern.match(message.content) != None:
            bot_analyst.parse_loot(message.content)
            monsters_count = 0
            for _ in bot_analyst.monsters:
                monsters_count += 1
            bot_analyst.add_to_json()
            await message.channel.send(f"Database updated, added {monsters_count} records")
            monsters_count = 0
        else:
            await message.channel.send("Error, incorrect pastebin")
        return  
            
    if message.content.startswith("!monster"):
        with open('loot.json') as file:
            data = load(file)
        message.content = message.content[9:]
        if message.content in data:
            embed = Embed(
            title = data[message.content]['monster_name'],
            color=0x00ff00
            )
            embed.add_field(name='Killed',value=f"{data[message.content]['killed']} pcs",inline=False)
            for i in data[message.content]['drop']:
                embed.add_field(name=i,value=f"{round(data[message.content]['drop'][i] / data[message.content]['killed'] * 100,1)} %" ,inline=True)
            await message.channel.send(embed=embed)

        else:
            if message.content not in data:
                embed = Embed(
                title = message.content,
                description='Not exists in database',
                color=0x00ff00
                )
                await message.channel.send(embed=embed)
        return
       
        
        
    if message.content.startswith("!item"):
        with open('loot.json') as file:
            data = load(file)
        message.content = message.content[6:]
        item_count = 0
        embed = Embed(
            title = message.content,
            color=0x00ff00
        )
        for monster in data:
            for item in data[monster]['drop']:
                if message.content == item:
                    embed.add_field(name=monster,value=f"{round(data[monster]['drop'][message.content] / data[monster]['killed'] * 100,1)} %",inline=True)
                    item_count += 1
                
        if item_count == 0:
            item_count = 0
            embed = Embed(
        title = message.content,
        description='Not exists in database',
        color=0x00ff00
    )
        await message.channel.send(embed=embed)
        return

    

bot.run(TOKEN)
