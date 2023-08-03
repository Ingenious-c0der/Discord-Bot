import ssl
import motor 
import motor.motor_asyncio
import random 
from dotenv import load_dotenv
import os 
load_dotenv()
Mongo_Client =motor.motor_asyncio.AsyncIOMotorClient(fr"{os.environ.get('CONNECTION_STRING')}", serverSelectionTimeoutMS=5000)
db = Mongo_Client.get_database('Bot_data')



class Accounts:
    account =db.accounts


    async def manage_account(user_id,amount=1000)->None:
        """All in one function to create and update accounts. Creates an account if it does not exist already ,else updates it
        Parameters :  user_id,amount=1000
        Returns :None """
        await Accounts.account.update_one({"_id":user_id},{"$inc":{"amount":amount}},upsert=True)

    async def get_balance(user_id)->tuple:
        """Function to return the account balance of the given user_id.To be called only if user_id has an account. 
        Parameters : user_id
        Returns : tuple containing ((Int)account balance,str(username))
                  None if the user does not have an account"""

        acc =   await Accounts.account.find_one({"_id":user_id })
        return (acc["amount"])

    async def get_account_leaderboard_global()->list:
        """Function to return the account balance of the top wealthy accounts. 
        Parameters : None
        Returns : list of dicts containing [{(Int)account balance,int(user_id)}]
                  None if there is no account at all (not very probable)"""

        top_cursor = Accounts.account.find().sort("amount",-1)
        top_list =  [i async for i in top_cursor][0:5]
        return top_list






class WpmStats:
    wpmstat = db.wpmstats

    async def add_stat(user_id,guild_id,word,speed)->None:
        """Adds a wpm stat corresponding to the passed parameters 
        parameters : user_id , guild_id,word,speed
        returns :None"""
        await WpmStats.wpmstat.insert_one({"discord_id":user_id,"guild_id":guild_id,"word":word,"speed":speed})

    async def get_wpm_leaderboard()->list:
        """
        Function to get global leaderboard of WpmStats

        Parameters : None
       
        Returns : list of dicts (Attributes : _id, speed,word,guild_id)(top 5 wpmracers info)
       
       """
        top_cursor = WpmStats.wpmstat.find().sort("speed",-1)
        top_list =  [i async for i in top_cursor][0:5]
        return top_list
    
    async def get_wpm_leaderboard_local(guild_id)->list:
        """
        Function to get local (server) leaderboard of WpmStats

        Parameters : Guild_id
       
        Returns : list of dicts (Attributes : _id, speed,word,guild_id) (top 5 wpmrace events info)
       
       """
        top_cursor =  WpmStats.wpmstat.find({"guild_id":guild_id}).sort("speed",-1)
        top_list = [i async for i in top_cursor][0:5]
        return top_list

    async def get_self_wpm_stats(user_id)->list:
        """
        Function to get self WpmStats

        Parameters : user id
       
        Returns : list of dicts (Attributes : _id, speed,word,guild_id) (top 5 wpmrace events info)
        """
        top_cursor =  WpmStats.wpmstat.find({"discord_id":user_id}).sort("speed",-1)
        top_list = [i async for i in top_cursor][0:5]
        return top_list

class ScrambleStats:
    scramble = db.scramble_stats
    
    async def manage_stat(user_id)->None:

        await ScrambleStats.scramble.update_one({"_id":user_id},{"$inc":{"count":1}},upsert=True)
    
    async def get_scramble_leaderboard():
        top_cursor = ScrambleStats.scramble.find().sort("count",-1)
        top_list = [i async for i in top_cursor][0:5]
        return top_list

    async def get_self_scramble_stats(user_id):
        top_cursor = ScrambleStats.scramble.find({"_id":user_id}).sort("count",-1)
        top_list = [i async for i in top_cursor]
        return top_list


class Words:
    words = db.words
    word_list = None

    
    
    async def get_word()->str:
       
        """Returns a random word from the word list
        Parameters : None
        Returns :str word
        """
        # words_raw = await Words.words.find_one({"word_list_id":1})
        # word_list = words_raw["words"]
        if Words.word_list is None:
            words_raw = await Words.words.find_one({"word_list_id":1})
            Words.word_list = words_raw["words"]
        return random.choice(Words.word_list)


