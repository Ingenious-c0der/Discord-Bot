from discord.ext import commands
import random 
import time
import discord
import nums_from_string
from discord_components import Button,ButtonStyle,DiscordComponents 
from mongo_functions import ScrambleStats, WpmStats,Accounts,Words
import os
from dotenv import load_dotenv






intents = discord.Intents.default()
intents.members = True
bot = discord.ext.commands.Bot("$",intents = intents)
bot.remove_command("help")
DiscordComponents(bot)
@bot.event
async def on_ready():
  await bot.change_presence(activity=discord.Game('Wpm Races'))
  print('we have logged in as {0.user}'.format(bot))

class Bot(commands.Bot):


    pending_word = dict()
    pending_scramble_word = dict()
    context_scramble_word =dict()
    gamble_dict = dict()
   





    
    @bot.command()
    async def wpmrace(ctx):
      if ctx.channel in Bot.pending_word:#if that channel already has an ongoing wpmrace , a new instance won't be considered
        await ctx.channel.send(f"Hey <@{ctx.message.author.id}> slow down! A race is already in Progress!")
      else:
        def check(m):
            n = m.content.lower()  
            return n==word_lower and m.channel==ctx.channel

        word = await Words.get_word()
        word_lower = word.lower()
        Bot.pending_word[ctx.channel]= "occupied"
        await ctx.channel.send("On your marks, get set....")
        time.sleep(1)
        await ctx.channel.send(f"Go!Type the word **{word}**")
        time_1 = time.time()
        try: 
          Bot.pending_word[ctx.channel] = bot.wait_for('message', check=check,timeout=10)
          msg = await Bot.pending_word[ctx.channel]
          Bot.pending_word[ctx.channel].close()
          time_2 =time.time()
          delta_t = time_2-time_1
          speed = len(word)/delta_t
          await ctx.channel.send(f"<@{msg.author.id}> won!, at a typing speed of **{round(speed,3)}** characters per second")
          await WpmStats.add_stat(msg.author.id,ctx.guild.id,word,speed)
          Bot.pending_word.pop(ctx.channel,None)
          if speed>=3:
            await Accounts.manage_account(msg.author.id,500)
        except : #If the word expires an embed is sent indicating that the bot has stopped looking for that word
          Bot.pending_word[ctx.channel].close()
          embedVar = discord.Embed(title=f"**Word Expired**", color=0xFF0000)
          embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/895902833315041280/895961848426430475/clock.png")
          embedVar.add_field(name = "Timeout of 10 seconds",value=f"The word **{word}** has expired \n**Use $wpmrace for a new word** <(O.o)> ", inline=True)
          embedVar.add_field(name = "Info",value=f"You are seeing this message because the word {word} has expired.", inline=True)
          await ctx.channel.send(embed= embedVar)
          Bot.pending_word.pop(ctx.channel,None)
      


          

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
            
            if interaction.channel in Bot.pending_scramble_word:
              this_word =Bot.context_scramble_word[interaction.channel]
              await interaction.send(content=f"Ah dumb people ,The first half of the word is {this_word[0:int(len(this_word)/2)]}")
            else:
              await interaction.send(content = "Hmm , looks like this word has expired by now")
      def check(m):
        return m.content == word and m.channel == ctx.channel
      
      await ctx.send(f"Hmm , sort this word out **{scrambled_word}**", components=[Button(style = ButtonStyle.green,label="hint",custom_id="hint_button")])
      Bot.context_scramble_word[ctx.channel] = word
      try:
        Bot.pending_scramble_word[ctx.channel] = bot.wait_for('message', check=check,timeout=120)
        msg = await Bot.pending_scramble_word[ctx.channel]
        time_2 = time.time()
        await ctx.channel.send(f"<@{msg.author.id}> won!, Solved the scrambled word in **{round(time_2-time_1,3)}** seconds")
        await ScrambleStats.manage_stat(msg.author.id)
        await Accounts.manage_account(msg.author.id,200)
      except:
        await ctx.channel.send(f"Scramble Timeout : the word was {word}")
        Bot.pending_scramble_word[ctx.channel].close()
        Bot.pending_scramble_word.pop(ctx.channel,None)

    


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
    async def wpmstats(ctx,*args):
      try:
        
        id = int(nums_from_string.get_nums(args[0])[0])
        self_list = await WpmStats.get_self_wpm_stats(id)
        user =  await bot.fetch_user(id)
        
        embedVar = discord.Embed(title=f"** {user}'s Wpm Stats**", color=0xFFFF00)
        embedVar.add_field(name=f"**Highest So Far -**", value=f"**Speed**:{(self_list[0]['speed'])} char/S  **Word** :{self_list[0]['word']}", inline=False)
        embedVar.add_field(name=f"**Second best**", value=f"**Speed**:{(self_list[1]['speed'])} char/S  **Word** :{self_list[1]['word']}", inline=False)
        embedVar.add_field(name=f"**3.**", value=f"**Speed**:{(self_list[2]['speed'])} char/S  **Word** :{self_list[2]['word']}", inline=False)
        embedVar.add_field(name=f"**4.**", value=f"**Speed**:{(self_list[3]['speed'])} char/S  **Word** :{self_list[3]['word']}", inline=False)
        embedVar.add_field(name=f"**5.** ", value=f"**Speed**:{(self_list[4]['speed'])} char/S  **Word** :{self_list[4]['word']}", inline=False)
       
        embedVar.set_thumbnail(url=user.avatar_url)
        embedVar.set_footer(text='Bot developed by Ingenious#3023',icon_url="https://images-ext-2.discordapp.net/external/z00qs9F4naW67aIuZRooFryrXpeYrJJsDByJIX2yZok/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/297693029563760651/cb5e1f877f07cba43d0d6c459207bc46.webp") 
        await ctx.channel.send(embed=embedVar)

      except:
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
    async def wpmstatslocal(ctx):

      try:
        top_list = await WpmStats.get_wpm_leaderboard_local(ctx.guild.id)
        embedVar = discord.Embed(title=f"**WPM LEADERBOARD for {await bot.fetch_guild(ctx.guild.id)}**", color=0xFFFF00)
      
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/896066752193134655/896266321296248872/keyboard-burning-fire-concept-electronics-break-flames-67415324.png")
        embedVar.add_field(name=f"**1st 👑** **{ await bot.fetch_user(int(top_list[0]['discord_id']))}**", value=f"**Speed**:{(top_list[0]['speed'])} char/S  **Word** :{top_list[0]['word']}", inline=False)
        embedVar.add_field(name=f"**2nd 🥈** **{ await bot.fetch_user(int(top_list[1]['discord_id']))}**", value=f"**Speed**:{(top_list[1]['speed'])} char/S  **Word** :{top_list[1]['word']}", inline=False)
        embedVar.add_field(name=f"**3rd 🥉** **{ await bot.fetch_user(int(top_list[2]['discord_id']))}**", value=f"**Speed**:{(top_list[2]['speed'])} char/S  **Word** :{top_list[2]['word']}", inline=False)
        embedVar.add_field(name=f"**4th** **{ await bot.fetch_user(int(top_list[3]['discord_id']))}**", value=f"**Speed**:{(top_list[3]['speed'])} char/S  **Word** :{top_list[3]['word']}", inline=False)
        embedVar.add_field(name=f"**5th** **{ await bot.fetch_user(int(top_list[4]['discord_id']))}**", value=f"**Speed**:{(top_list[4]['speed'])} char/S  **Word** :{top_list[4]['word']}", inline=False)
        await ctx.channel.send(embed=embedVar)

      except:
        await ctx.channel.send(f"Looks like the server does not have enough stats yet.")


    @bot.command()
    async def scramblestats(ctx,*args):
      try:

        id = int(nums_from_string.get_nums(args[0])[0])
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


    @bot.command()
    async def gamble(ctx):
      def check(m):
          if m.channel == ctx.channel and m.author.id not in player_list and m.content.startswith("!bet")  and len(m.content.split(" "))==3 and len(nums_from_string.get_nums(m.content))==2:
              this = m.content.split(" ")
              player_list.append(m.author.id)
              net_list.append((m.author.id,int(this[1]),int(this[2])))
          return False
      player_list = []
      net_list = []
      gamble_number = random.randint(0,9)
      
      if ctx.channel not in Bot.gamble_dict:
        embedVar = discord.Embed(
        title = "Assemble Gamblers!",
        colour = 0x7CFC00)
        embedVar.add_field(name= "Players get ready to **Gamble**",value = 
          f"The one who wins gets all the betted money , and the participants lose the amount they had betted. If no one wins ,no one loses or gains money",inline = False)
        embedVar.add_field(name = "Instructions to set your bet :)",value= "You have **20 seconds** !Give your bets in the format !bet <amount to bet> <number on which you want to bet(0,9)>")
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/895902833315041280/896396326198181938/512x512bb.jpg")
        await ctx.channel.send(embed = embedVar)
        total_bet = 0
        someone_won = False 
        winner = None
        try:
          Bot.gamble_dict[ctx.channel]= "Occupied"
          _ = await bot.wait_for('message',check=check,timeout = 20)
        except:
          for bet in net_list:
            total_bet+= bet[1]
          for bet in net_list:
            if bet[2]==gamble_number:
              someone_won = True
              winner = bet
              break
          if someone_won:
            await ctx.channel.send(f"Wow <@{winner[0]}> won amount {total_bet}! The lucky number was {gamble_number} <a:blazesipp:898600460800364546>")
            await Accounts.manage_account(int(winner[0]),total_bet-winner[1])
            for bet in net_list:
              if bet[0]!= winner[0]:
                await Accounts.manage_account(int(bet[0]),-bet[1])
            Bot.gamble_dict.pop(ctx.channel,None)
            
          else:
            await ctx.channel.send(f"sigh , no one won . The lucky number was {gamble_number} ")
            Bot.gamble_dict.pop(ctx.channel,None)

      else:
         await ctx.channel.send(f"Hey <@{ctx.message.author.id}> slow down! A gamble is already in Progress! <a:blazesipp:898600460800364546>")

    
    @bot.command()
    async def donate(ctx,*arg):
      try:
        id = int(nums_from_string.get_nums(arg[0])[0])
        amount = int(arg[1])
        if amount>0:
          await Accounts.manage_account(ctx.author.id,-amount)
          await Accounts.manage_account(id,amount)
          await ctx.channel.send(f"<@{ctx.author.id}> transferred {amount} to <@{id}> , such a generous man.")
        else:
          await ctx.channel.send("Imagine trying to send negative money <a:blazesipp:898600460800364546>")
      except:
        await ctx.channel.send(f"Oops , Something went wrong. This is the format to donate \n```$donate <tag the person> <amount>```")
    
    @bot.command()
    async def balancestats(ctx):
       top_list = await Accounts.get_account_leaderboard_global()
       embedVar = discord.Embed(title=f"**Flamecoins Leaderboard**", color=0xFFFF00)
      
       embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/898553997810626620/898641846941659166/download-removebg-preview_1.png")
       embedVar.add_field(name=f"**Richie Rich 👑 : { await bot.fetch_user(int(top_list[0]['_id']))}** ", value=f"**balance** : {top_list[0]['amount']} flamecoins", inline=False)
       embedVar.add_field(name=f"**Mr almost Richie Rich 💎 : { await bot.fetch_user(int(top_list[1]['_id']))}** ", value=f"**balance** : {top_list[1]['amount']} flamecoins", inline=False)
       embedVar.add_field(name=f"**Rich 💸 :  { await bot.fetch_user(int(top_list[2]['_id']))}** ", value=f"**balance** : {top_list[2]['amount']} flamecoins", inline=False)
       embedVar.add_field(name=f"**Rich but 4th 💵 :  { await bot.fetch_user(int(top_list[3]['_id']))}** ", value=f"**balance** : {top_list[3]['amount']} flamecoins" , inline=False)
       embedVar.add_field(name=f"**Made it to the leaderboard 🌟 :{ await bot.fetch_user(int(top_list[4]['_id']))}** ",value=f"**balance** : {top_list[4]['amount']} flamecoins", inline=False)
       await ctx.channel.send(embed=embedVar)











    @bot.group(invoke_without_command = True)
    async def help(ctx):
      
      em = discord.Embed(title = "Help",description = "Use ```$help <command>``` for extended information about a particular command",color = 0x4e23c4)
      em.add_field(name = "Utility   ",value = "```•wpmrace\n•scramble\n•gamble\n•donate```",inline = True)
      em.add_field(name = "Information",value = "```•wpmstats\n•balancestats\n•balance\n•scramblestats```",inline = True )
      em.add_field(name = "Fun",value = "```•choice\n•toss```",inline = True)
      em.set_thumbnail(url="https://cdn.discordapp.com/avatars/827131558984810507/f2b9e7828a270b2f0f034b41dd073c60.png?size=1024")
      em.set_footer(text='Bot developed by Ingenious#3023',icon_url="https://cdn.discordapp.com/avatars/297693029563760651/55c5c4064de5e426076bafdcddee0dd9.png?size=1024") 
      await ctx.channel.send(embed =em )


    @help.command()
    async def wpmrace(ctx):
      em = discord.Embed(title= "Wpmrace",description= "Think you are an fast typer? Try wpm racing with your friends using this command.First one to type the given word out correctly wins!",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$wpmrace```",inline = False)
      em.add_field(name = "Reward",value = "You will be rewarded 500 flamecoins if your typing speed in 3+ characters per second",inline= False)
      await ctx.channel.send(embed =em )
    
    @help.command()
    async def scramble(ctx):
      em = discord.Embed(title= "Scramble",description= "You will be given a scrambled word to sort out, First to sort it out wins!",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$scramble```",inline = False)
      em.add_field(name = "Reward",value = "You will be rewarded 200 flamecoins for each scrambled word you sort out",inline= False)
      await ctx.channel.send(embed =em )

    @help.command()
    async def gamble(ctx):
      em = discord.Embed(title= "Gamble",description= "Wanna check your luck?? Bet the flamecoins with your friends , and know whose more lucky!",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "Invoking command: ```$gamble```\nbetting command: ```!bet <amount-to-bet> <number to bet on (0,9) inclusive>```",inline = False)
      em.add_field(name="Command example",value="```!bet 12000 4```",inline= False)
      em.add_field(name = "Reward",value = "If you win the gamble , you get all the flamecoins betted by eveyone.But if you lose you lose your betted amount.You have 20 seconds to make your bet once ```$gamble``` is invoked",inline= False)
      await ctx.channel.send(embed =em )

    @help.command()
    async def donate(ctx):
      em = discord.Embed(title= "Donate flamecoins",description= "Does your friend need help to pay his college fees? Please donate him!",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$donate <@user> <amount>```",inline = False)
      em.add_field(name = "Example",value = "```$donate @Ingenious 5000```",inline= False)
      await ctx.channel.send(embed =em )

    @help.command()
    async def balance(ctx):
      em = discord.Embed(title= "Check Balance",description= "Want to check your or someone's balance? ",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$balance(your own balance)\n$balance <@user>```",inline = False)
      em.add_field(name = "Example",value = "```$balance\n$balance @Ingenious```",inline= False)
      await ctx.channel.send(embed =em )

    @help.command()
    async def choice(ctx):
      em = discord.Embed(title= "Ask for a choice",description= "Do you want the answer to a yes/no type question the whole day? Now is your chance to ask it! ",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$choice <yes/no question>```",inline = False)
      em.add_field(name = "Example",value = "```$choice Should I go to university today?```",inline= False)
      em.add_field(name = "Warning",value = "The outcomes of this are random i.e. either yes/no .Please do not consider taking any important decisions based on this, neither the bot nor its owner will be responsible in such cases.")
      await ctx.channel.send(embed =em )




    @help.command()
    async def toss(ctx):
      em = discord.Embed(title= "Toss between two things",description= "Are you confused selecting in between two things? Here, use this.  ",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$toss Option 1 or Option 2```",inline = False)
      em.add_field(name = "Example",value = "```$toss Play football or Watch tv```",inline= False)
      em.add_field(name = "Warning",value = "Either Option 1 or Option 2 is selected randomly by the bot .Please do not consider taking any important decisions based on this, neither the bot nor its owner will be responsible in such cases.")
      await ctx.channel.send(embed =em )


    
    @help.command()
    async def wpmstats(ctx):
      em = discord.Embed(title= "Get Wpmstats",description= "Want to know info about the top wpmracers or your best wpm race events?",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$wpmstats(for checking global wpmstats)\n$wpmstatslocal (for checking wpmstats of your server)\n$wpmstats <@user>(to check the top 5 stats of only that user)```",inline = False)
      em.add_field(name = "Example",value = "```$wpmstats\n$wpmstatslocal\n$wpmstats @Ingenious```",inline=False)
      await ctx.channel.send(embed =em )

    @help.command()
    async def balancestats(ctx):
      em = discord.Embed(title= "Check Balance Leaderboard",description= "Want to see the richest people alive ? ",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$balancestats```",inline = False)
      em.add_field(name="Note",value = "```$help balance``` for individual balance information")
      await ctx.channel.send(embed =em )
      

    
    @help.command()
    async def scramblestats(ctx):
      em = discord.Embed(title= "Get Scramble Stats",description= "Want to know info about the top unscramblers or your sorted words count?",color = 0x4e23c4)
      em.add_field(name = "Syntax",value = "```$scramblestats\n$scramblestats <@user>(to check the stats of only that user)```",inline = False)
      em.add_field(name = "Example",value = "```$scramblestats\n$scramblestats @Ingenious```",inline=False)
      await ctx.channel.send(embed =em )



load_dotenv()
bot.run(os.environ.get("TOKEN"))


