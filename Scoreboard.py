from Score import Score


class Scoreboard:
    # FALSE = Shortest, TRUE = Longest

    def __init__(self, use_type=False):
        self.scores = []
        self.scoreType = use_type

    def check(self, new_time):
        if len(self.scores) < 5:
            return True

        for score in self.scores:
            if self.scoreType:
                if new_time > score.timeInSeconds:
                    return True
            else:
                if new_time < score.timeInSeconds:
                    return True

    def add(self, new_score):
        self.scores.append(new_score)
        self.scores.sort(reverse=self.scoreType)

        user_found = False
        for score in self.scores:
            if score.memberID == new_score.memberID:
                if user_found:
                    self.remove(score)
                else:
                    user_found = True

        if len(self.scores) > 5:
            self.scores.pop()

        return new_score in self.scores

    def remove(self, old_score):
        if old_score in self.scores:
            self.scores.remove(old_score)

    def reset(self):
        self.scores = []

    def __str__(self):
        print_string = ""
        if len(self.scores) == 0:
            print_string = "-"
        else:
            for i in range(len(self.scores)):
                print_string = print_string + str(i + 1) + ": " + str(self.scores[i]) + f"\n"
        return print_string

    def to_json(self):
        tmp_scoreboard = []
        for score in self.scores:
            tmp_scoreboard.append(score.to_json())

        return {"type": self.scoreType, "board": tmp_scoreboard}

    @staticmethod
    def from_json(json):
        res_scoreboard = Scoreboard(json["type"])

        for score in json['board']:
            res_scoreboard.add(Score.from_json(score))

        return res_scoreboard
