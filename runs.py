import discord
import random
import time
import os

client = discord.Client()
player = [] #결과 저장
join = [] #플레이 하는 플레이어 hash 저장
hands = [] #join의 index 사용해서 플레이어 판별 + 플레이어의 카드 (0,1 인덱스에)
cards = [] #현재 남은 카드
start = 0 #시작했으면 1, 아니면 0
pick = "" #뽑은 카드 이름, 섯다 뽑기의 for문에서 사용
picker = 0 #뽑은 사람을 join 인덱스로 찾고 저장, 섯다 뽑기의 for문에서 사용

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
        await message.channel.send("!섯다 시작 : 섯다를 시작합니다.\n!섯다 뽑기 : 패를 뽑고 게임에 들어갑니다.\n!섯다 패까 : 현재 게임에 들어와있는 사람들의 패를 깝니다.")
    
    if message.content == "!섯다 시작":
        if start == 0:
            cards.clear()
            cards = ["1","2","3","4","5","6","7","8","9","10","**1**","**2**","**3**","**4**","**5**","**6**","**7**","**8**","**9**","**10**"]
            await message.channel.send("모든 카드 섞기 완료! !섯다 뽑기 로 패를 뽑아주세요!")
            start = 1
        else:
            await message.channel.send("이미 게임이 진행중입니다. 플레이어 수 : {}/{}".format(len(join),maxjoin))
    
    if message.content == "!섯다 뽑기":
        if start == 0:
            await message.channel.send("현재 게임이 시작되지 않았습니다. !섯다 시작")
            return
        if hash(message.author) in join:
            await message.channel.send("이미 패를 받으셨습니다. 플레이어 수 : {}/{}".format(len(join),maxjoin))
        elif len(join) >= maxjoin:
            await message.channel.send("플레이어가 꽉 찼습니다. 다음 게임에 참가해주세요.")
        else:
            join.append(hash(message.author))
            for i in range(2):
                pick = random.choice(cards)
                picker = join.index(hash(message.author))
                hands[picker][i] = pick
                cards.remove(pick)
            channel = await message.author.create_dm()
            picker = join.index(hash(message.author))
            await channel.send('{}, {} 패가 나왔습니다!'.format(hands[picker][0],hands[picker][1]))
            picker = join.index(hash(message.author))
            player.append("{}님은 {}, {}".format(message.author.display_name,hands[picker][0],hands[picker][1]))
            await message.channel.send("패 전송 완료! 플레이어 수 : {}/{}, 남은 카드 장수 : {}".format(len(join),maxjoin,len(cards)))
            
    
    if message.content == "!섯다 패까":
        if start == 0:
            await message.channel.send("현재 게임이 시작되지 않았습니다. !섯다 시작")
            return
        if len(join) <= 0:
            await message.channel.send("깔 패가 없습니다.")
        else:
            for say in player:
                await message.channel.send("{}".format(say))
                time.sleep(1)
            player.clear()
            join.clear()
            hands.clear()
            cards.clear()
            start=0

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
