from Leaderboard import Leaderboard
from Leaderboard import ResetType
from Scoreboard import Scoreboard


class Guild:

    def __init__(self, guild_name, guild_id, guild_message=0, guild_leaderboards=[]):
        self.name = guild_name
        self.id = guild_id
        self.message = guild_message
        self.leaderboards = []
        if len(guild_leaderboards) == 0:
            for r_type in ResetType:
                self.leaderboards.append(Leaderboard(r_type.value))
        else:
            self.leaderboards = guild_leaderboards
        self.latest = None

    def check(self, score):
        return_value = False
        for leaderboard in self.leaderboards:
            if leaderboard.check(score.timeInSeconds):
                return_value = True
        return return_value

    def add(self, score):
        added_to = []
        for leaderboard in self.leaderboards:
            tmp = leaderboard.add(score)
            if tmp is not None:
                added_to.append(tmp)

        self.latest = (score, added_to)
        return len(added_to) > 0

    def to_json(self):
        tmp_leaderboards = []
        for leaderboard in self.leaderboards:
            tmp_leaderboards.append(leaderboard.to_json())
        return {"name": self.name, "id": self.id, "message": self.message, "leaderboards": tmp_leaderboards}

    @staticmethod
    def from_json(json):
        name = json['name']
        gid = json['id']
        message = json['message']
        tmp_leaderboards = []
        for json_leaderboard in json['leaderboards']:
            tmp_leaderboards.append(Leaderboard.from_json(json_leaderboard))

        return Guild(name, gid, message, tmp_leaderboards)
