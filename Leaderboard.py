import datetime
from enum import Enum
import json
from Scoreboard import Scoreboard


class ResetType(Enum):
    ALL_TIME = 0
    MONTHLY = 1
    WEEKLY = 2
    DAILY = 3


class Leaderboard:

    def set_reset_date(self):
        dt = datetime.date.today()
        if self.reset_type.name == "MONTHLY":
            self.reset_date = (dt.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
        elif self.reset_type.name == "WEEKLY":
            start = dt - datetime.timedelta(days=dt.weekday())
            self.reset_date = start + datetime.timedelta(days=6)
        elif self.reset_type.name == "DAILY":
            self.reset_date = dt + datetime.timedelta(days=1)
        else:
            self.reset_date = dt + datetime.timedelta(weeks=5200)

    def __init__(self, lb_type, scoreboard_shortest=None, scoreboard_longest=None, lb_reset_date=None):
        self.shortest = Scoreboard(use_type=False) if scoreboard_shortest is None else scoreboard_shortest
        self.longest = Scoreboard(use_type=True) if scoreboard_longest is None else scoreboard_longest

        self.reset_type = ResetType(lb_type)

        if lb_reset_date is None:
            self.set_reset_date()
        else:
            self.reset_date = lb_reset_date

    def check_shortest(self, time):
        return self.shortest.check(time)

    def check_longest(self, time):
        return self.longest.check(time)

    def check(self, time):
        if datetime.date.today() >= self.reset_date:
            self.shortest.reset()
            self.longest.reset()
            self.set_reset_date()
        return self.check_shortest(time) or self.check_longest(time)

    def add(self, score):
        tmp_shortest = self.shortest.add(score)
        tmp_longest = self.longest.add(score)
        if tmp_shortest or tmp_longest:
            return self.reset_type
        else:
            return None

    def to_json(self):
        return {"type": self.reset_type.value, "reset_date": json.dumps(self.reset_date, default=str),
                "shortest": self.shortest.to_json(), "longest": self.longest.to_json()}

    @staticmethod
    def from_json(lb):
        return Leaderboard(lb['type'], Scoreboard.from_json(lb['shortest']), Scoreboard.from_json(lb['longest']),
                           datetime.datetime.strptime(lb['reset_date'], '"%Y-%m-%d"').date())


