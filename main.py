# Impports
import datetime
import discord
from Guild import Guild
from GuildList import GuildList
from Score import Score
from Scoreboard import Scoreboard
import time
import json
import yaml

# Variable setup
client = discord.Client()
pretime_dict = {}

# Constants setup
settings = yaml.safe_load(open("settings.yml"))
messages = {}
try:
    f = open("localization.json", encoding='UTF-8')
    tmp = json.loads(f.read())
    f.close()
    messages = tmp[settings['language']]
except:
    exit(0)

# Send or edit message
async def send_leaderboard_update(embed_message, leaderboard):
    for server in client.guilds:
        channel = discord.utils.find(lambda c: c.name == "voice-speedrun", server.channels)
        try:
            message = await channel.fetch_message(leaderboard.message)
            await message.edit(embed=embed_message)
        except discord.NotFound:
            message = await channel.send(embed=embed_message)
            await message.pin()
            leaderboard.message = message.id

'''
# load stored leaderboard from file
def loadLeaderboard(type):
    try:
        if type:
            filename = "leaderboard_longest.json"
            jsonType = "true"
        else:
            filename = "leaderboard_shortest.json"
            jsonType = "false"

        f = open(filename, "r")
        tmp = json.loads(f.read())
        f.close()

        scoreboard = Scoreboard(type)
        for tmp_score in tmp[jsonType]:
            member = list(tmp_score.keys())[0]
            time = list(tmp_score.values())[0]
            newScore = Score(time, member)
            scoreboard.add(newScore)
        scoreboard.message = tmp["message"]
        print("Loaded Scoreboard")
        print(scoreboard)

        return scoreboard

    except:
        print("Error while loading Scoreboard!")
        return Scoreboard(type)
        
    
    # store current leaderboard to file
    def storeLeaderboard(leaderboard):
    
        if leaderboard.scoreType:
            filename = "leaderboard_longest.json"
        else:
            filename = "leaderboard_shortest.json"
    
        f = open(filename, "w")
        f.write(json.dumps(leaderboard.toJson()))
        f.close()
        return
'''


# load Guilds from file
def load_guild_data():
    try:
        f = open(settings['filename'], "r")
        tmp = json.loads(f.read())
        f.close()

        guilds = GuildList.from_json(tmp)
        print("Loaded Guilds")

        return guilds

    except:
        print("Error while loading Guild data!")
        return GuildList()


# store current leaderboard to file
def store_guild_data(guilds):
    buffer = json.dumps(guilds.to_json())

    f = open(settings['filename'], "w")
    f.write(buffer)
    f.close()
    return


# Act on people joining or leaving a voice channel
@client.event
async def on_voice_state_update(member, before, after):

    if before.channel is None:
        pretime_dict[member] = datetime.datetime.now()
    elif after.channel is None:
        if member not in pretime_dict:
            return

        guild_id = before.channel.guild.id
        guild_name = before.channel.guild.name

        if guilds.check_guild(guild_id):
            guild = guilds.get_by_id(guild_id)
        else:
            guild = Guild(guild_name, guild_id)
            guilds.add(guild)


        duration_time = pretime_dict[member] - datetime.datetime.now()
        duration_time_adjusted = int(duration_time.total_seconds()) * -1

        if guild.check_shortest(duration_time_adjusted):
            new_score = Score(duration_time_adjusted, member.id)
            guild.add_shortest(new_score)

            time_str = time.strftime('%H:%M:%S', time.gmtime(duration_time_adjusted))
            message_text = messages['new_entry_shortest'].format(member.id, str(time_str), str(before.channel))
            embed_msg = discord.Embed(title=messages['title_shortest'], description=message_text)
            embed_msg.add_field(name=messages['lb_type_all_time'], value=str(guild.shortest))
            embed_msg.set_footer(text=messages['server'] + f"{guild_name}")
            await send_leaderboard_update(embed_msg, guild.shortest)

        if guild.check_longest(duration_time_adjusted):
            new_score = Score(duration_time_adjusted, member.id)
            guild.add_longest(new_score)

            time_str = time.strftime('%H:%M:%S', time.gmtime(duration_time_adjusted))
            message_text = messages['new_entry_longest'].format(member.id, str(time_str), str(before.channel))
            embed_msg = discord.Embed(title=messages['title_longest'], description=message_text)
            embed_msg.add_field(name=messages['lb_type_all_time'], value=str(guild.longest))
            embed_msg.set_footer(text=messages['server'] + f"{before.channel.guild.name}")
            await send_leaderboard_update(embed_msg, guild.longest)

        store_guild_data(guilds)

guilds = load_guild_data()
client.run("Token")
