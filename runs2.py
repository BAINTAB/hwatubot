import discord
import random
import os

client = discord.Client()
rand = []
player = []
join = []
maxjoin = 10

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.bot:
        return
    
    if message.content == "!섯다":
        if hash(message.author) in join:
            await message.channel.send("이미 패를 받으셨습니다. 플레이어 수 : {}/{}".format(len(join),maxjoin))
        elif len(join) >= maxjoin:
            await message.channel.send("플레이어가 꽉 찼습니다. 다음 게임에 참가해주세요.")
        else:
            rand.clear()
            rand.append(random.randint(1,10))
            rand.append(random.randint(0,1))
            rand.append(random.randint(1,10))
            rand.append(random.randint(0,1))
            channel = await message.author.create_dm()
            await channel.send('{}({}), {}({}) 패가 나왔습니다!'.format(rand[0],rand[1],rand[2],rand[3]))
            player.append("{}님은 {}({}), {}({})".format(message.author,rand[0],rand[1],rand[2],rand[3]))
            join.append(hash(message.author))
            await message.channel.send("패 전송 완료! 플레이어 수 : {}/{}".format(len(join),maxjoin))
            
    
    if message.content == "!패까":
        for say in player:
            await message.channel.send("{}".format(say))
        player.clear()
        join.clear()

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
