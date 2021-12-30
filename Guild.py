from Scoreboard import Scoreboard


class Guild:

    def __init__(self, guild_name, guild_id, scoreboard_shortest=None, scoreboard_longest=None):
        self.g_name = guild_name
        self.g_id = guild_id
        self.shortest = Scoreboard(use_type=False) if scoreboard_shortest is None else scoreboard_shortest
        self.longest = Scoreboard(use_type=True) if scoreboard_longest is None else scoreboard_longest

    def check_shortest(self, time):
        return self.shortest.check(time)

    def check_longest(self, time):
        return self.longest.check(time)

    def add_shortest(self, score):
        return self.shortest.add(score)

    def add_longest(self, score):
        return self.longest.add(score)

    def to_json(self):
        return {"name": self.g_name, "id": self.g_id, "shortest": self.shortest.to_json(), "longest": self.longest.to_json()}

    @staticmethod
    def from_json(json):
        name = json['name']
        id = json['id']
        shortest = Scoreboard.from_json(json['shortest'])
        longest = Scoreboard.from_json(json['longest'])

        return Guild(name, id, shortest, longest)
