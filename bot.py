import nextcord
from itertools import cycle
import random 
import time
from nextcord.ext import commands
import discord
import requests
import json
import chess
import chess.svg

betting_list = []
gambling_on = False   
board = chess.Board()
pathe = "C:/.../disco_bot/disco.py"
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', description="coolbot", intents=intents)
in_process = False
chess_in_play = False
comebacks = """_"""





x = "wecaehcluaoe3wuw4h823o3ucalinwec"
client= nextcord.Client()

sad_words=["depressed","unhappy","angry","miserable",'depressing']
starter_encouragements=["cheerup","hang in there","you are a great person "]
file = open(r'C:\Users\sagar\Desktop\disco_bot\words.txt','r')

word_list_2= file.readlines()
word_string_2 = "".join(word_list_2)
word_list_3 = word_string_2.split("\n")
file.close

color_make = [0xD433FF,0xFF3333,0x00FFB4,0xFFD633,0x6FFF33,0x3388FF,0xFF33B1,0xA34CFF,0xFF0000,0x690000,0xFFAB22,0xFA8072]
t1 =  0 
pool = cycle(color_make)
def save_data(name,speed,word):
    file = open(r'C:\Users\sagar\Desktop\disco_bot\bot_data.txt','r')
    content = file.readlines()
    content.append(f"{speed}:{name}:{word}\n")
    file.close
    file=open(r'C:\Users\sagar\Desktop\disco_bot\bot_data.txt','w')
    file.writelines(content)
    file.close

@client.event
async def fight(channel):
    global in_process
    in_process = True
    global x
    global t1
    x = random.choice(word_list_3)
    await channel.send("On your marks, get set....")
    time.sleep(1)
    await channel.send(f"Go!Type the word **{x}**")
    t1 = time.time()

def wpmstats():
  speed_list= []
  file = open(r'C:\Users\sagar\Desktop\disco_bot\bot_data.txt','r')
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
  file = open(r'C:\...\disco_bot\bot_data.txt','r')
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

#betting_list.append((message.author,amount,bet))
def gamble(users,bets):
  gambling_number = random.randint(0,9)
  win =False
 
  file = open(r'C:\....\disco_bot\account.txt','r')
  content = file.readlines()
  file.close
  
  for i in range(len(bets)):
    if bets[i][0] not in "".join(content):
        content.append((f"{bets[i][0]}:{1000};\n"))
      
  winner= ["No one"]
  

  #making sure everyone has an account and can play
  file = open(r'C:\Users\sagar\Desktop\disco_bot\account.txt','w')
  file.writelines(content)
  file.close
  total_bet = sum([i[1] for i in bets])
  #checking if atleast one person has won
  for j in range(len(bets)):
    if gambling_number == bets[j][2]:
        win=True
        break



  #finding the winner
  if win:
    for h in range(len(bets)):
      if gambling_number == bets[h][2]:
        winner = bets[h]
        for line in range(len(content)):
          if winner[0] in content[line]:
             #and giving him the total amount 
            initial_amt = int("".join(content[line][content[line].index(":")+1:content[line].index(";")]))
            content[line] = f"{bets[h][0]}:{initial_amt+total_bet-bets[h][1]};\n"

          #subtracting the amounts lost for participants
      else:
        for line in range(len(content)):
          if bets[h][0] in content[line]:
            initial_amt = int("".join(content[line][content[line].index(":")+1:content[line].index(";")]))
            content[line] = f"{bets[h][0]}:{initial_amt-bets[h][1]};\n"
    
  file = open(r'C:\Users\sagar\Desktop\disco_bot\account.txt','w')
  file.writelines(content)
  file.close
  return (winner[0],total_bet,gambling_number)


def check_balance(username):
   file = open(r'C:\....\disco_bot\account.txt','r')
   content = file.readlines()
   file.close
   for line in content:
     if username in line:
       amount = int("".join(line[line.index(":")+1:line.index(";")]))
       return (amount)





@client.event
async def on_ready():
  print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global x
  global t1
  global board
  global chess_in_play
  global gambling_on
  global betting_list


  if message.content.startswith('$Disco'):
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
    global in_process
    if not in_process:
     await fight(message.channel)
     in_process = False
  
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
    
    to_ping = "".join(message.content[message.content.index("@")+1:])
    if to_ping!=297693029563760651 and message.author.id !=740931255599759450:    
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
  
  if message.content.startswith("!wpmstats") and "@" not in message.content:
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
    
    top_list = wpmstats2(str(message.mentions[0]))
    main_list= [ ]
    for i in top_list:
       main_list.append(i.split(":"))
    embedVar = discord.Embed(title=f"**{message.mentions[0]}'s Wpm Stats **", color=random.choice(color_make))
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

  if message.content.startswith("!chess"):
    embedVar = discord.Embed(title=f"chessboard", color=random.choice(color_make))
    chess_in_play = True
  
    embedVar.add_field(name=f"chess", value=board  , inline=False)
    
    await message.channel.send(embed=embedVar)
  
  if len(message.content)==2 or len(message.content)==3 or len(message.content)==4:
    if chess_in_play:
      board.push_san(message.content)
      embedVar = discord.Embed(title=f"chessboard", color=random.choice(color_make))
      
      embedVar.add_field(name=f"a b c d e f g h", value=board  , inline=False)
      
    
      await message.channel.send(embed=embedVar)
      await message.delete()


  if message.content.startswith("$gamble") and not gambling_on:
    global playing_users
    playing_users=[]
    
    if len(message.mentions)>=2:
      for i in range(len(message.mentions)):
        playing_users.append(str(message.mentions[i]))
      gambling_on = True
      await message.channel.send(f"Awaiting bets from {playing_users}")
         
    else:
       await message.channel.send("You need atleast 2 or more members to start gambling")
    
  if message.content.startswith("$bet") and gambling_on:
    
    if str(message.author) in playing_users:
      
      amount,bet = int(message.content.split(" ")[1]),int(message.content.split(" ")[2])
      betting_list.append((str(message.author),amount,bet))
    if len(playing_users)==len(betting_list):
      await message.channel.send("All bets have been noted , starting to gamble")
      gambling_on=False
      result_tuple = gamble(playing_users,betting_list)
      await message.channel.send(f"**{result_tuple[0]}** won amount {result_tuple[1]} jeez ..the number was {result_tuple[2]}, nice. ")
      betting_list=[]
      playing_users=[]

  if message.content.startswith("$balance"):
    x = check_balance(str(message.author))
    await message.channel.send(f"{str(message.author)}'s balance is {x}")



  


intents = discord.Intents.default()
intents.members = True
  
    

client.run("token")
