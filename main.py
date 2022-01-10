# Impports
import datetime
import discord
import DiscordMessages
from Guild import Guild
from GuildList import GuildList
from Score import Score
import json
import yaml


# Constants setup
settings = yaml.safe_load(open("settings.yml"))

# Variable setup
client = discord.Client()
pretime_dict = {}
message_handler = DiscordMessages.DiscordMessages(settings)


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
    if before.channel is None or before.channel == before.channel.guild.afk_channel:
        pretime_dict[member] = datetime.datetime.now()
    elif after.channel is None or after.channel == after.channel.guild.afk_channel:
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

        new_score = Score(duration_time_adjusted, member.id)
        if guild.check(new_score):
            if guild.add(new_score):
                await message_handler.send_or_update_leaderboard(guild, before.channel.guild)
                await message_handler.send_leaderboard_pm(member, guild)

        store_guild_data(guilds)


guilds = load_guild_data()
token_file = yaml.safe_load(open("./misc/token.yml"))
client.run(token_file['test'])
