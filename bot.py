import nextcord
from itertools import cycle
import json 
import random 
import time
from nextcord.ext import commands
import discord
import requests
import json
import chess
from chess import Board #working on adding chess game to the bot

intents = nextcord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', description="bot", intents=intents)
word_string = "manywordsinthis"
comebacks= "badwordshere"
word_list = words_string.split("\n")
x = "wecaehcluaoe3wuw4h823o3ucalinwec"
client= nextcord.Client()

color_make = [0xD433FF,0xFF3333,0x00FFB4,0xFFD633,0x6FFF33,0x3388FF,0xFF33B1,0xA34CFF,0xFF0000,0x690000,0xFFAB22,0xFA8072]
t1 =  0 
pool = cycle(color_make)
def save_data(name,speed,word):
    file = open(r'C:\....\bot_data.txt','r')
    content = file.readlines()
    content.append(f"{speed}:{name}:{word}\n")
    file.close
    file=open(r'C:\...\bot_data.txt','w')
    file.writelines(content)
    file.close

@client.event
async def fight(channel):
    
    global x
    global t1
    x = random.choice(word_list)
    await channel.send("On your marks, get set....")
  
    time.sleep(1)
    await channel.send(f"Go!Type the word **{x}**")
    t1 = time.time()

def wpmstats():
  speed_list= []
  file = open(r'C:\....\bot_data.txt','r')
  content = file.readlines()
  
  file.close
  for line_number in range(len(content)):
    for i in range(len(content[line_number])):
      if content[line_number][i]==":":
        speed = float("".join(content[line_number][0:i]))
        speed_list.append((speed,line_number))
        break

  speed_list.sort()
  speed_list.reverse()
 
  final_list = [ ]
  for i in range(0,5):
    final_list.append(content[speed_list[i][1]])
  return final_list


def wpmstats2(user):
  speed_list= []
  file = open(r'C:\....\bot_data.txt','r')
  content = file.readlines()
  
  file.close
  for line_number in range(len(content)):
    for i in range(len(content[line_number])):
      if user in content[line_number]:
       if content[line_number][i]==":":
         speed = float("".join(content[line_number][0:i]))
         speed_list.append((speed,line_number))
         break

  speed_list.sort()
  speed_list.reverse()
 
  final_list = [ ]
  for i in range(0,5):
    final_list.append(content[speed_list[i][1]])
  return final_list


@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global x
  global t1


  if message.content.startswith('$Disco'): #this function is not adviced.
        if message.author.id == 297693029563760651:
          role = nextcord.utils.get(message.guild.roles,id=887966925320224768)
          for i in range(10000):
            await role.edit(colour =next(pool))
            time.sleep(7)
            
       
        


  if message.content.startswith('$hello') or  message.content.startswith('$Hello'):
    await message.channel.send('Hello!')
  
  if "fuck" in message.content.lower():
    if message.author.id!=827131558984810507:
        words = comebacks.split("\n")
      
        await message.channel.send(f"no u <@{message.author.id}> {random.choice(words)} and {random.choice(words)}")


  if "+" in message.content:
    for i in range(len(message.content)):
      if message.content[i]=="+":
          y = int("".join(message.content[0:i]))
          x = int("".join(message.content[i+1:]))

    await message.channel.send(y+x)
  if "-" in message.content:
    for i in range(len(message.content)):
      if message.content[i]=="-":
          y = int("".join(message.content[0:i]))
          x = int("".join(message.content[i+1:]))

    await message.channel.send(y-x)
  if "*" in message.content and "**" not in message.content:
    for i in range(len(message.content)):
      if message.content[i]=="*":
          y = int("".join(message.content[0:i]))
          x = int("".join(message.content[i+1:]))

    await message.channel.send(y*x)
  
  if "/" in message.content:
    for i in range(len(message.content)):
      if message.content[i]=="/":
          y = int("".join(message.content[0:i]))
          x = int("".join(message.content[i+1:]))

    await message.channel.send(y/x)



  if "pls nsfw" in message.content:
    await message.channel.send(f"<@{message.author.id}> saale hawas ke pujari , nahi milega")
  
  if message.content.startswith("$wpmrace"):
     await fight(message.channel)
  
  if message.content==x:
        t2 = time.time()
        y = x
        x = "seucfkawucbwecwemof8239284h38of9oop23bnfa"
        t = t2-t1
        await message.channel.send(f"<@{message.author.id}> won!, at a typing speed of {len(y)/t} characters per second")
        save_data(message.author,len(y)/t,y)
        
        

  if message.content.startswith('!embed'):
    if "@" in message.content:
        user_id = "".join(message.content[message.content.index("@")+1:])
        await message.channel.send(user_id)
        user = bot.get_user(int(user_id))
        embedVar = discord.Embed(title=f"{user}'s Info", description="idk what to put in here ", color=random.choice(color_make))
        embedVar.add_field(name=user, value=user_id, inline=False)
        embedVar.add_field(name="Join date", value=user.created_at, inline=False)
        await message.channel.send(embed=embedVar)

    else:
        embedVar = discord.Embed(title=f"{message.author}'s Info", description="idk what to put in here ", color=0x00ff00)
        embedVar.add_field(name=message.author, value=message.author.id, inline=False)
        embedVar.add_field(name="Join date", value=message.author.created_at, inline=False)
        await message.channel.send(embed=embedVar)
  if message.content.startswith("!spamping"):
    if message.author.id ==297693029563760651:
      to_ping = "".join(message.content[message.content.index("@")+1:])
      for i in range(20):
        await message.channel.send(f"<@{to_ping}>")
      
    else:
      await message.channel.send("https://cdn.discordapp.com/attachments/260896487318355968/889500634615787530/video0-25.mp4")
  if message.content.startswith("chess") and  "@" in message.content:
  
    opponent = "".join(message.content[message.content.index("@")+1:])
    embedVar = discord.Embed(title=f"{message.author}vs <@{opponent}>", color=0x00ff00)

    embedVar.add_field(name="chess board", value=chess.Board(), inline=False)
    await message.channel.send(embed=embedVar)
  
  if message.content.startswith("showemoji"):
    await message.channel.send(message.guild.emojis)
  
  if "blaze" in message.content:
    if message.author.id!=827131558984810507:
      await message.channel.send(f"<a:blazesipp:890077824818507806>")
  
  if message.content.startswith("!wpmstats"):
    top_list = wpmstats()
    main_list= [ ]
    for i in top_list:
       main_list.append(i.split(":"))
    embedVar = discord.Embed(title=f"**WPM LEADERBOARD**", color=random.choice(color_make))
    embedVar.add_field(name=f"**1st 👑** **{main_list[0][1]}**", value=f"**Speed**:{main_list[0][0]} char/S  **Word** :{main_list[0][2]}", inline=False)
    embedVar.add_field(name=f"**2nd 🥈** **{main_list[1][1]}**", value=f"**Speed**:{main_list[1][0]} char/S  **Word** :{main_list[1][2]}", inline=False)
    embedVar.add_field(name=f"**3rd 🥉** **{main_list[2][1]}**", value=f"**Speed**:{main_list[2][0]} char/S  **Word** :{main_list[2][2]}", inline=False)
    embedVar.add_field(name=f"**4th** **{main_list[2][1]}**", value=f"**Speed**:{main_list[3][0]} char/S  **Word** :{main_list[3][2]}", inline=False)
    embedVar.add_field(name=f"**5th** **{main_list[2][1]}**", value=f"**Speed**:{main_list[4][0]} char/S  **Word** :{main_list[4][2]}", inline=False)
    await message.channel.send(embed=embedVar)

  if message.content.startswith("!wpmstats") and "@" in message.content and ">" in message.content:
    user_id = "".join(message.content[message.content.index("@")+2:message.content.index(">")])
    top_list = wpmstats2(str(bot.get_user(int(user_id))))
    main_list= [ ]
    for i in top_list:
       main_list.append(i.split(":"))
    embedVar = discord.Embed(title=f"**<@{user_id}>'s Wpm Stats **", color=random.choice(color_make))
    embedVar.add_field(name=f"**All time Best** **{main_list[0][1]}**", value=f"**Speed**:{main_list[0][0]} char/S  **Word** :{main_list[0][2]}", inline=False)
    embedVar.add_field(name=f"**2nd **{main_list[1][1]}**", value=f"**Speed**:{main_list[1][0]} char/S  **Word** :{main_list[1][2]}", inline=False)
    embedVar.add_field(name=f"**3rd ** **{main_list[2][1]}**", value=f"**Speed**:{main_list[2][0]} char/S  **Word** :{main_list[2][2]}", inline=False)
    embedVar.add_field(name=f"**4th** **{main_list[2][1]}**", value=f"**Speed**:{main_list[3][0]} char/S  **Word** :{main_list[3][2]}", inline=False)
    embedVar.add_field(name=f"**5th** **{main_list[2][1]}**", value=f"**Speed**:{main_list[4][0]} char/S  **Word** :{main_list[4][2]}", inline=False)
    await message.channel.send(embed=embedVar)
  
  if message.content.startswith("!selfwpmstats"):
    top_list = wpmstats2(str(message.author))
    main_list= [ ]
    for i in top_list:
       main_list.append(i.split(":"))
    embedVar = discord.Embed(title=f"**{message.author}'s Wpm Stats **", color=random.choice(color_make))
    embedVar.add_field(name=f"**All time Best** **{main_list[0][1]}**", value=f"**Speed**:{main_list[0][0]} char/S  **Word** :{main_list[0][2]}", inline=False)
    embedVar.add_field(name=f"**2nd **{main_list[1][1]}**", value=f"**Speed**:{main_list[1][0]} char/S  **Word** :{main_list[1][2]}", inline=False)
    embedVar.add_field(name=f"**3rd ** **{main_list[2][1]}**", value=f"**Speed**:{main_list[2][0]} char/S  **Word** :{main_list[2][2]}", inline=False)
    embedVar.add_field(name=f"**4th** **{main_list[2][1]}**", value=f"**Speed**:{main_list[3][0]} char/S  **Word** :{main_list[3][2]}", inline=False)
    embedVar.add_field(name=f"**5th** **{main_list[2][1]}**", value=f"**Speed**:{main_list[4][0]} char/S  **Word** :{main_list[4][2]}", inline=False)
    await message.channel.send(embed=embedVar)


  


intents = nextcord.Intents.default()
intents.members = True
  
    

client.run('token')
