import datetime
import discord
import score
import time
import json

client = discord.Client()
pretime_dict = {}


async def sendLeaderboardUpdate(message_text, leaderboard):
    for server in client.guilds:
        channel = discord.utils.find(lambda c: c.name == "voice-speedrun", server.channels)
        if leaderboard.message:
            message = await channel.fetch_message(leaderboard.message)
            await message.edit(content=message_text)
        else:
            message = await channel.send(message_text)
            await message.pin()
            leaderboard.message = message.id


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

        scoreboard = score.Scoreboard(type)
        for tmp_score in tmp[jsonType]:
            member = list(tmp_score.keys())[0]
            time = list(tmp_score.values())[0]
            newScore = score.Score(time, member)
            scoreboard.add(newScore)
        scoreboard.message = tmp["message"]
        print("Loaded Scoreboard")
        print(scoreboard)

        return scoreboard

    except:
        print("Error while loading Scoreboard!")
        return score.Scoreboard(type)

def storeLeaderboard(leaderboard):

    if leaderboard.scoreType:
        filename = "leaderboard_longest.json"
    else:
        filename = "leaderboard_shortest.json"

    f = open(filename, "w")
    f.write(json.dumps(leaderboard.toJson()))
    f.close()
    return


@client.event
async def on_voice_state_update(member, before, after):
    if (before.channel is None):
        pretime_dict[member] = datetime.datetime.now()
    elif (after.channel is None):
        duration_time = pretime_dict[member] - datetime.datetime.now()
        duration_time_adjust = int(duration_time.total_seconds()) * -1

        if leaderboard_shortest.check(duration_time_adjust):
            new_score = score.Score(duration_time_adjust, member.id)
            leaderboard_shortest.add(new_score)
            time_str = time.strftime('%H:%M:%S', time.gmtime(duration_time_adjust))
            message_text = ""
            message_text += f"<@{member.id}> " + " ist in das Leaderboard für kurze Aufenthalte mit einer Zeit von " + str(
                time_str) + "h in " + str(before.channel) + " aufgenommen worden! \n"
            message_text += str(leaderboard_shortest)
            message_text += "####"

            await sendLeaderboardUpdate(message_text, leaderboard_shortest)

            storeLeaderboard(leaderboard_shortest)

        if leaderboard_longest.check(duration_time_adjust):
            new_score = score.Score(duration_time_adjust, member.id)
            leaderboard_longest.add(new_score)
            time_str = time.strftime('%H:%M:%S', time.gmtime(duration_time_adjust))
            message_text = ""
            message_text += f"<@{member.id}> " + " ist in das Leaderboard für lange Aufenthalte mit einer Zeit von " + str(
                time_str) + "h in " + str(before.channel) + " aufgenommen worden! \n"
            message_text += str(leaderboard_longest)
            message_text += "####"

            await sendLeaderboardUpdate(message_text, leaderboard_longest)

            storeLeaderboard(leaderboard_longest)

leaderboard_longest = loadLeaderboard(True)
leaderboard_shortest = loadLeaderboard(False)
client.run("Token")  # Bot token of
