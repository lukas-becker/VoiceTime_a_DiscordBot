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

    def __str__(self):
        time_str = str(time.strftime('%H:%M:%S', time.gmtime(self.timeInSeconds)))
        return f"<@{self.memberID}> - " + time_str

    def to_json(self):
        return {"time": self.timeInSeconds, "member": self.memberID}

    @staticmethod
    def from_json(json):
        return Score(json['time'], json['member'])
