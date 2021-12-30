import discord
import json
import time


class DiscordMessages:
    def __init__(self, settings):
        self.messages = {}
        try:
            f = open("localization.json", encoding='UTF-8')
            tmp = json.loads(f.read())
            f.close()
            self.messages = tmp[settings['language']]
        except:
            exit(0)

    # Send or edit message
    async def send_or_update_leaderboard(self, guild, discord_guild):
        embed_message = self.create_embed(guild)

        channel = discord.utils.find(lambda c: c.name == "voice-speedrun", discord_guild.channels)
        if channel is None:
            channel = await discord_guild.create_text_channel("voice-speedrun")
        try:
            message = await channel.fetch_message(guild.message)
            await message.edit(embed=embed_message)
        except discord.NotFound:
            message = await channel.send(embed=embed_message)
            await message.pin()
            guild.message = message.id

    def create_embed(self, guild):

        embed_msg = discord.Embed(title=self.messages['embed_title'])
        for leaderboard in guild.leaderboards:
            embed_msg.add_field(name=self.messages['title_shortest'] + " " + str(leaderboard.reset_type.name),
                                value=str(leaderboard.shortest),
                                inline=False)
            embed_msg.add_field(name=self.messages['title_longest'] + " " + str(leaderboard.reset_type.name),
                                value=str(leaderboard.longest),
                                inline=False)

        score, boards = guild.latest
        time_str = time.strftime('%H:%M:%S', time.gmtime(score.timeInSeconds))
        tmp_board_str = ""
        for i in range(len(boards)):
            if i == 0:
                tmp_board_str = str(boards[i].name)
            else:
                tmp_board_str = tmp_board_str + ", " + str(boards[i].name)

        embed_msg.add_field(name=self.messages['newest_entry_title'],
                            value=self.messages['newest_entry_body'].format(score.memberID, time_str, tmp_board_str))

        embed_msg.set_footer(text=self.messages['server'] + f"{guild.name}")

        return embed_msg

    async def send_leaderboard_pm(self, member, guild):
        score, boards = guild.latest
        time_str = time.strftime('%H:%M:%S', time.gmtime(score.timeInSeconds))
        await member.send(self.messages['new_entry_pm'].format(score.memberID, time_str, guild.name))
