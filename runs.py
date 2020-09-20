import discord
import random
import time

client = discord.Client()

player = [] #결과 저장
join = [] #플레이 하는 플레이어 hash 저장
maxjoin = 10
hands = [] #join의 index 사용해서 플레이어 판별 + 플레이어의 카드 (0,1 인덱스에)
cards = [] #현재 남은 카드
start = [] #시작했으면 1, 아니면 0
server = [] #섯다를 하는 서버, 여러 서버에서 동시에 섯다를 칠 수 있게 해줌

# (지) pick : 뽑은 카드 이름, 섯다 뽑기의 for문에서 사용
# (지) picker : 뽑은 사람을 join 인덱스로 찾고 저장, 섯다 뽑기의 for문에서 사용
# (지) pickinfo : 카드를 뽑을 때 남은 플레이어 수, 카드 남은 장수 저장하여 겹치기 방지

@client.event
async def on_ready():
    print('{0.user}봇이 작동되기 시작했습니다.'.format(client))

@client.event
async def on_message(message):
    global start
    global player
    global join
    global hands
    global cards
    global maxjoin
    global server
    
    if message.author == client.user:
        return

    if message.author.bot:
        return
    
    if message.content == "!섯다":
        await message.channel.send("!섯다 시작 : 섯다를 시작합니다.\n!섯다 뽑기 : 패를 뽑고 게임에 들어갑니다.\n!섯다 패까 : 현재 게임에 들어와있는 사람들의 패를 깝니다.")
    
    if message.content == "!테스트":
        await message.channel.send(f"{server}")
        await message.channel.send(f"이 디스코드 길드 hash : {hash(message.guild)}")
        if hash(message.guild) in server:
            await message.channel.send(f"{cards[server.index(hash(message.guild))]}")
    
    if message.content == "!섯다 시작":
        if not hash(message.guild) in server:
            server.append(hash(message.guild))
            cards.insert(server.index(hash(message.guild)),[])
            player.insert(server.index(hash(message.guild)),[])
            join.insert(server.index(hash(message.guild)),[])
            hands.insert(server.index(hash(message.guild)),[])
            for i in range(1,11):
                cards[server.index(hash(message.guild))].append(f"{i}")
            for i in range(1,11):
                cards[server.index(hash(message.guild))].append("__"+f"{i}"+"__")
            await message.channel.send("모든 카드 섞기 완료! !섯다 뽑기 로 패를 뽑아주세요!")
        else:
            await message.channel.send("이미 게임이 진행중입니다. 플레이어 수 : {}/{}".format(len(join[server.index(hash(message.guild))]),maxjoin))
    
    if message.content == "!섯다 뽑기":
        if not hash(message.guild) in server:
            await message.channel.send("현재 게임이 시작되지 않았습니다. !섯다 시작")
            return
        if hash(message.author) in join[server.index(hash(message.guild))]:
            await message.channel.send("이미 패를 받으셨습니다. 플레이어 수 : {}/{}".format(len(join[server.index(hash(message.guild))]),maxjoin))
        elif len(join[server.index(hash(message.guild))]) >= maxjoin:
            await message.channel.send("플레이어가 꽉 찼습니다. 다음 게임에 참가해주세요.")
        else:
            join[server.index(hash(message.guild))].append(hash(message.author))
            for i in range(2):
                pick = random.choice(cards[server.index(hash(message.guild))])
                picker = join[server.index(hash(message.guild))].index(hash(message.author))*10
                hands[server.index(hash(message.guild))].insert(picker+i,pick)
                cards[server.index(hash(message.guild))].remove(pick)
            
            channel = await message.author.create_dm()
            picker = join[server.index(hash(message.guild))].index(hash(message.author))*10
            await channel.send('{}, {} 패가 나왔습니다!'.format(hands[server.index(hash(message.guild))][picker],hands[server.index(hash(message.guild))][picker+1]))
            picker = join[server.index(hash(message.guild))].index(hash(message.author))*10
            player[server.index(hash(message.guild))].append("{}님은 {}, {}".format(message.author.display_name,hands[server.index(hash(message.guild))][picker],hands[server.index(hash(message.guild))][picker+1]))
            await message.channel.send("패 전송 완료! 플레이어 수 : {}/{}, 남은 카드 장수 : {}".format(len(join[server.index(hash(message.guild))]),maxjoin,len(cards[server.index(hash(message.guild))])))
            
    
    if message.content == "!섯다 패까":
        if not hash(message.guild) in server:
            await message.channel.send("현재 게임이 시작되지 않았습니다. !섯다 시작")
        elif len(join[server.index(hash(message.guild))]) <= 0:
            await message.channel.send("깔 패가 없습니다.")
        else:
            for say in player[server.index(hash(message.guild))]:
                await message.channel.send("{}".format(say))
                time.sleep(1)
            player[server.index(hash(message.guild))].clear()
            join[server.index(hash(message.guild))].clear()
            hands[server.index(hash(message.guild))].clear()
            cards[server.index(hash(message.guild))].clear()
            server[server.index(hash(message.guild))]=-1

    if message.content == "!섯다 종료":
        if not hash(message.guild) in server:
            await message.channel.send("현재 게임이 시작되지 않았습니다. !섯다 시작")
        else:
            player[server.index(hash(message.guild))].clear()
            join[server.index(hash(message.guild))].clear()
            hands[server.index(hash(message.guild))].clear()
            cards[server.index(hash(message.guild))].clear()
            server[server.index(hash(message.guild))]=-1
            await message.channel.send("정상적으로 종료되었습니다.")

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
