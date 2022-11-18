from cmu_112_graphics import *

class Score():
    def __init__(self):
        self.score = 0
        self.comboStreak = 0
        self.scoreIncrement = 75

    def returnScore(self):
        return self.score

    def increaseCombo(self):
        self.comboStreak += 1

    def incrementScore(self):
        if self.scoreIncrement <= 1000:
            self.scoreIncrement *= self.comboStreak

    def resetScoreIncrement(self):
        self.scoreIncrement = 75

    def resetToDefault(self):
        self.score = 0
        self.comboStreak = 0
        self.scoreIncrement = 75