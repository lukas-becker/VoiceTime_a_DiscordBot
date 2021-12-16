import time
from functools import total_ordering

@total_ordering
class Score:
    timeInSeconds = 0
    memberID = 0

    def __init__(self, time, id):
        self.timeInSeconds = time
        self.memberID = id

    @staticmethod
    def _is_valid_operand(other):
        return hasattr(other, "timeInSeconds") and hasattr(other, "memberID")

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.timeInSeconds, self.memberID) == (other.timeInSeconds, other.memberID)

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.timeInSeconds < other.timeInSeconds

    def __contains__(self, item):
        return

    def __str__(self):
        time_str = str(time.strftime('%H:%M:%S', time.gmtime(self.timeInSeconds)))
        return f"<@{self.memberID}> - " + time_str

    def toJson(self):
        return {self.memberID: self.timeInSeconds}


class Scoreboard:
    # FALSE = Shortest, TRUE = Longest

    def __init__(self, useType=False):
        self.scores = []
        self.scoreType = useType

    def check(self, newTime):
        if len(self.scores) < 5:
            return True
        for score in self.scores:
            if self.scoreType:
                if newTime > score.timeInSeconds:
                    return True
            else:
                if newTime < score.timeInSeconds:
                    return True

    def add(self, newScore):
        self.scores.append(newScore)
        self.scores.sort(reverse=self.scoreType)
        if len(self.scores) > 5:
            self.scores.pop()

    def __str__(self):
        printString = f"Leaderboard "
        if self.scoreType:
            printString = printString + f"längster Aufenthalt: \n"
        else:
            printString = printString + f"kürzester Aufenthalt: \n"

        for i in range(len(self.scores)):
            printString = printString + str(i+1) + ": " + str(self.scores[i]) + f"\n"
        return printString

    def toJson(self):
        tmpScoreboard = []
        for score in self.scores:
            tmpScoreboard.append(score.toJson())

        return {self.scoreType: tmpScoreboard}
