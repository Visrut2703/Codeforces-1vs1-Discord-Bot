import discord
import requests
from datetime import datetime
import os
import http
import hashlib
import time
import json
import random
from dotenv import load_dotenv
load_dotenv()
intents = discord.Intents.all()
contestId = 556
bot = discord.Client(intents=intents)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
apiKey = os.getenv("API")
secret = os.getenv("PASS")
rand = random.randint(000000, 999999)
timeValue = time.time()


@bot.event
async def on_ready():
    guild_count = 0
    for guild in bot.guilds:

        print(f"- {guild.id} (name: {guild.name})")

        guild_count = guild_count + 1

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    input1 = []
    input1 = message.content.split(" ")
    n = int(input1[3])
    rating = int(input1[4])
    # hashCode = hashlib.sha512()

    # hashCode.update(str(""+str(rand)+"/contest.list?apiKey="+apiKey+"&contestId="+str(contestId)+"&time="+str(timeValue)+"#"+secret).encode())

    # get = requests.get("https://codeforces.com/api/contest.hacks?contestId=566&apiKey="+apiKey+"&time="+time+"&apiSig="+rand+""+hashCode)

    try:
        get1 = requests.get(
            "https://codeforces.com/api/user.status?handle="+input1[1])
        get2 = requests.get(
            "https://codeforces.com/api/user.status?handle="+input1[2])
    except:
        await message.channel.send("User Not Found")
    getproblemset = requests.get(
        "https://codeforces.com/api/problemset.problems")

    data1 = get1.json()
    data2 = get2.json()
    dataproblemset = getproblemset.json()
    dict1 = {}
    dict2 = {}
    if (data1['status'] == 'FAILED'):
        await message.channel.send("User 1 is Invalid!!")
    elif (data2['status'] == 'FAILED'):
        await message.channel.send("User 2 is Invalid!!")
    elif message.content.startswith('/next'):
        # await message.channel.send("Next Contest is at")
        generatedProblems = []
        for i in range(0, len(data1['result'])):
            if data1['result'][i]['verdict'] == 'OK':
                a = str(data1['result'][i]['problem']['contestId'])
                b = data1['result'][i]['problem']['index']
                dict1[str(a)+b] = 1
        # print(dict1)
        for i in range(0, len(data2['result'])):
            if data2['result'][i]['verdict'] == 'OK':
                a = str(data2['result'][i]['problem']['contestId'])
                b = data2['result'][i]['problem']['index']
                dict2[str(a)+b] = 1
        ct = 0
        # print(len(dataproblemset['result']))
        for i in range(0, len(dataproblemset['result']['problems'])):
            try:
                x = dataproblemset['result']['problems'][i]['rating']
                if x != int(rating):
                    continue
                a = str(dataproblemset['result']['problems'][i]['contestId'])
                b = dataproblemset['result']['problems'][i]['index']
                if a+b in dict1.keys():
                    continue
                elif a+b in dict2.keys():
                    continue
                else:
                    generatedProblems.append(a+b)
                    ct = ct + 1
            except:
                continue
        if ct == 0:
            await message.channel.send("Kya re Babu Rao Thik se Rating Daal!")
            pass
        randomList = []
        while len(randomList) != n:
            r = random.randint(0, ct)
            if r not in randomList:
                randomList.append(r)
        for i in range(0, len(randomList)):
            siz = len(generatedProblems[randomList[i]])
            await message.channel.send("https://codeforces.com/problemset/problem/"+generatedProblems[randomList[i]][0:siz-1:1]+"/"+generatedProblems[randomList[i]][siz-1])
            

bot.run(DISCORD_TOKEN)
