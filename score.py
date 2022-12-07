class Score():
    def __init__(self):
        self.score = 0
        self.comboStreak = 0
        self.originalScoreIncrement = 75
        self.scoreIncrement = 75

    def returnScore(self):
        return self.score

    def incrementScore(self):
        if self.scoreIncrement <= 750:
            self.comboStreak += 1
            self.scoreIncrement = self.comboStreak*self.originalScoreIncrement
        self.score += self.scoreIncrement

    def resetScoreIncrement(self):
        self.scoreIncrement = 75

    def resetToDefault(self):
        self.score = 0
        self.comboStreak = 0
        self.scoreIncrement = 75