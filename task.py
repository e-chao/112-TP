class Task():
    def __init__(self, numTargets):
        self.numTargets = numTargets
        self.room = Cube(0,0,100,100)
        lookAngleX, lookAngleY = 0, 0
        oldX, oldY = sWidth/2, sHeight/2
        sixshotScore = Score()
        sixshotScores = []
        sixshotHits = 0
        sixshotShots = 0
        gameStarted = False
        targetLength = room.length/50
        accuracies = []
        totalHits = []
        sixshotMissedLeft = 0
        sixshotMissedRight = 0
        sixshotMissedUp = 0
        sixshotMissedDown = 0
        missedPointsL = []
        #time code inspired
        #from https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
        # start = pygame.time.get_ticks()
        start = time.time()
        lastTime = start
        timePast = 0
        gameTimePast = 0
        gameStarted = False
        #list of cube instances
        targets = []
        targetColor = (255,255,0)
        possibleTargetColors = set(['yellow', 'blue', 'green', 'red', 'black',
        'white'])
        drawnRoom = copy.deepcopy(room)
        getTargets(targets, drawnRoom, sWidth, sHeight, targetLength)
        #drawn objects are the rotated and actually drawn versions of the
        #original objects
        drawnTargets = copy.deepcopy(targets)