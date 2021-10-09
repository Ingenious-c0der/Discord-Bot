from discord.ext import commands
import random 
import time
from nextcord.ext import commands
import discord
import nums_from_string
from discord_components import Button,ButtonStyle,DiscordComponents 
from mongo_functions import ScrambleStats, WpmStats,Accounts,Words


intents = discord.Intents.default()
intents.members = True
bot = discord.ext.commands.Bot("$",intents = intents)
DiscordComponents(bot)
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game('Wpm Races'))
  print('we have logged in as {0.user}'.format(bot))

class Bot(commands.Bot):
   
    pending_word = dict()
    pending_scramble_word = dict()


    @bot.command()
    async def wpmrace(ctx):
      if ctx.message.author in Bot.pending_word:
          print("this executed")
          Bot.pending_word[ctx.channel].close()
      
      not_skipped = True
      def check(m):
          return m.content==word and m.channel==ctx.channel

      word = await Words.get_word()
      await ctx.channel.send("On your marks, get set....")
      time.sleep(1)
      await ctx.channel.send(f"Go!Type the word **{word}**")
      time_1 = time.time()
      

      try:
        Bot.pending_word[ctx.channel] = bot.wait_for('message', check=check,timeout=10)
      
        msg = await Bot.pending_word[ctx.channel]
        Bot.pending_word[ctx.channel].close()
      except :
        Bot.pending_word[ctx.channel].close()
        embedVar = discord.Embed(title=f"**Word Expired**", color=0xFF0000)
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/895902833315041280/895961848426430475/clock.png")
        embedVar.add_field(name = "Timeout/wpmrace was spammed.",value=f"The word **{word}** has expired \n**Use $wpmrace for a new word** <(O.o)> ", inline=True)
        embedVar.add_field(name = "Info",value=f"You might be seeing this messasge either if the 10sec limit was crossed or someone used the $wpmrace more than once.Only one word will be validated in such cases ", inline=True)
        await ctx.channel.send(embed= embedVar)
        not_skipped = False
      if not_skipped:
        if ctx.channel in Bot.pending_word:
              Bot.pending_word[ctx.channel].close()
        time_2 =time.time()
        delta_t = time_2-time_1
        speed = len(word)/delta_t
        await ctx.channel.send(f"<@{msg.author.id}> won!, at a typing speed of **{round(speed,3)}** characters per second")
        await WpmStats.add_stat(msg.author.id,ctx.guild.id,word,speed)
        if speed>=3:
          await Accounts.manage_account(msg.author.id,50)

    @bot.command()
    async def scramble(ctx):
     
      Bot.scrambling = True
      if ctx.channel in Bot.pending_scramble_word:
         Bot.pending_scramble_word[ctx.channel].close()
      word = await  Words.get_word()
      print(word)
      Bot.scramble_solution = word
      scramble_list = list(word)
      random.shuffle(scramble_list)
      scrambled_word = "".join(scramble_list)
      if scrambled_word == word:
        random.shuffle(scramble_list)
        scrambled_word = "".join(scramble_list)
      
      time_1 = time.time()
      @bot.event
      async def on_button_click(interaction):
            await interaction.send(content=f"Ah dumb people ,The first half of the word is {word[0:int(len(word)/2)]}")
      def check(m):
        return m.content == word and m.channel == ctx.channel
      
      await ctx.send(f"Hmm , sort this word out **{scrambled_word}**", components=[Button(style = ButtonStyle.green,label="hint",custom_id="hint_button")])

      Bot.pending_scramble_word[ctx.channel] = bot.wait_for('message', check=check)
      msg = await Bot.pending_scramble_word[ctx.channel]

      
 
      time_2 = time.time()
      await ctx.channel.send(f"<@{msg.author.id}> won!, Solved the scrambled word in **{round(time_2-time_1,3)}** seconds")
      await ScrambleStats.manage_stat(msg.author.id)
      await Accounts.manage_account(msg.author.id,20)
      Bot.scrambling = False



    @bot.command()
    async def choice(ctx,arg):
      choice = random.choice(["yes","no","Ofcourse YES!","Really are you gonna ask me this now? You know the answer its ..YES","NO PLEASE DON'T","Nope","Yups Yups","Affirmative","Negative"])
      await ctx.channel.send(f"{choice}")

    @bot.command()
    async def toss(ctx,*arg):
      or_n = arg.index("or")
      options = [arg[0:or_n],arg[or_n+1:]]
      starters = ["If it were up to me I would select ","I would say ","Go ahead with ","Definitely ","Give priority to ","The other option is so trash , I would obviously select "]
      await ctx.channel.send(f"{random.choice(starters)}{' '.join(random.choice(options))}")


    
    @bot.command()
    async def balance(ctx,*arg):
      
      try:
      
        id = int(nums_from_string.get_nums(arg[0])[0])

      except:
        id = ctx.author.id

      await Accounts.manage_account(id,0)
      user = await bot.fetch_user(id)
      embedVar = discord.Embed(title= "Balance")
      embedVar.set_thumbnail(url=user.avatar_url)
      embedVar.set_footer(text='Bot developed by Ingenious#3023',icon_url="https://images-ext-2.discordapp.net/external/z00qs9F4naW67aIuZRooFryrXpeYrJJsDByJIX2yZok/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/297693029563760651/cb5e1f877f07cba43d0d6c459207bc46.webp") 
      embedVar.add_field(name = f"Account Stats of {await bot.fetch_user(id)}",value=f"The current balance of the user is **{await Accounts.get_balance(id)}** flame coins ", inline=False)
      await ctx.channel.send(embed=embedVar)



    @bot.command()
    async def wpmstats(ctx):
        top_list = await WpmStats.get_wpm_leaderboard()
        embedVar = discord.Embed(title=f"**WPM LEADERBOARD**", color=0xFFFF00)
      
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/896066752193134655/896266321296248872/keyboard-burning-fire-concept-electronics-break-flames-67415324.png")
        embedVar.add_field(name=f"**1st 👑** **{ await bot.fetch_user(int(top_list[0]['discord_id']))}**", value=f"**Speed**:{(top_list[0]['speed'])} char/S  **Word** :{top_list[0]['word']}", inline=False)
        embedVar.add_field(name=f"**2nd 🥈** **{ await bot.fetch_user(int(top_list[1]['discord_id']))}**", value=f"**Speed**:{(top_list[1]['speed'])} char/S  **Word** :{top_list[1]['word']}", inline=False)
        embedVar.add_field(name=f"**3rd 🥉** **{ await bot.fetch_user(int(top_list[2]['discord_id']))}**", value=f"**Speed**:{(top_list[2]['speed'])} char/S  **Word** :{top_list[2]['word']}", inline=False)
        embedVar.add_field(name=f"**4th** **{ await bot.fetch_user(int(top_list[3]['discord_id']))}**", value=f"**Speed**:{(top_list[3]['speed'])} char/S  **Word** :{top_list[3]['word']}", inline=False)
        embedVar.add_field(name=f"**5th** **{ await bot.fetch_user(int(top_list[4]['discord_id']))}**", value=f"**Speed**:{(top_list[4]['speed'])} char/S  **Word** :{top_list[4]['word']}", inline=False)
        await ctx.channel.send(embed=embedVar)

    @bot.command()
    async def scramblestats(ctx,*arg):
      try:
        id = int(nums_from_string.get_nums(arg[0])[0])
        
        self_list = await ScrambleStats.get_self_scramble_stats(id)
        user =  await bot.fetch_user(id)
        
        embedVar = discord.Embed(title=f"** {user}'s Scramble Stats**", color=0xFFFF00)
        embedVar.add_field(name="Stats",value=f"{user} has solved **{self_list[0]['count']}** scrambled words till now.")
        embedVar.set_thumbnail(url=user.avatar_url)
        embedVar.set_footer(text='Bot developed by Ingenious#3023',icon_url="https://images-ext-2.discordapp.net/external/z00qs9F4naW67aIuZRooFryrXpeYrJJsDByJIX2yZok/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/297693029563760651/cb5e1f877f07cba43d0d6c459207bc46.webp") 
        await ctx.channel.send(embed=embedVar)

      except:
       top_list = await ScrambleStats.get_scramble_leaderboard()
       embedVar = discord.Embed(title=f"**SCRAMBLE LEADERBOARD**", color=0xFFFF00)
      
       embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/896066752193134655/896268632349376552/46-467980_brain-brains-clipart-animated-transparent-png-transparent-background.png")
       embedVar.add_field(name=f"**1st 👑** **{ await bot.fetch_user(int(top_list[0]['_id']))}**", value=f"**Total solved**:{(top_list[0]['count'])} ", inline=False)
       embedVar.add_field(name=f"**2nd 🥈** **{ await bot.fetch_user(int(top_list[1]['_id']))}**", value=f"**Total solved**:{(top_list[1]['count'])} ", inline=False)
       embedVar.add_field(name=f"**3rd 🥉** **{ await bot.fetch_user(int(top_list[2]['_id']))}**", value=f"**Total solved**:{(top_list[2]['count'])} ", inline=False)
       embedVar.add_field(name=f"**4th** **{ await bot.fetch_user(int(top_list[3]['_id']))}**", value=f"**Total solved**:{(top_list[3]['count'])} ", inline=False)
       embedVar.add_field(name=f"**5th** **{ await bot.fetch_user(int(top_list[4]['_id']))}**", value=f"**Total solved**:{(top_list[4]['count'])} ", inline=False)
       await ctx.channel.send(embed=embedVar)
    


      

  



    
    # @bot.command()
    # async def gamble(ctx):
    #   mentions_list = ctx.message.mentions 

    








      




bot.run("token")




