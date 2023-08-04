# Discord-Bot
Multipurpose discord bot with various features.
The bot is no longer hosted on any platform due to lack of extended free tier services from any platform (like heroku offered in the past). If you want to get it running, you can clone it and set up the env yourself, the collections used in the db are given below


## Mongo DB Collection Schemas  
The database bot_data contains the following collections:
1. accounts
2. scramble_stats
3. words
4. wpmstats


## Accounts
This collection contains the following fields:
1. discord_id (_id)
2. amount 

Example
```json
{
_id: 740931255599759XXX,
amount: 44750
}
```

## ScrambleStats
This collection contains the following fields:
1. discord_id (_id)
2. count 

Example
```json
{
_id: 740931255599759XXX,
count: 38
}
```

## Words
Words is a static collection. It basically contains all the words used (randomly) for the wpmrace or scramble game. The words are stored in the following format:
1. _id: (auto generated)
2. word_list_id : 1
3. words: [Array]


## wpmstats
This collection contains the following fields:
1. _id : (auto generated)
2. discord_id
3. guild_id
4. word 
5. speed 

Example 
```json
{
id : ObjectId('6160375af4248ea46bc64a1a'),
discord_id : 29769302956376XXXX,
guild_id : 82713138544495XXXX,
word : "soccer",
speed : 1.3877119961885351
}
```



the .env contains two variables : 

BOT_TOKEN = \<your bot token\>

CONNECTION_STRING = mongodb+srv://\<uname\>:\<password\>@\<dbname\>.si3ce.mongodb.net/?retryWrites=true&w=majority   // the mongo db atlas connection url
