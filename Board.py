import cardDeck
import copy

class Board():
    def __init__(self):
        self.stations = []
        self.trainLines = []

    def __str__(self):
        string = ''
        for trainLine in self.trainLines:
            string+=str(trainLine)+'\n'
        string += 'Score: ' + str(self.calculateScore())
        return string

    def getState(self):
        state = ''
        for trainLine in self.trainLines:
            state += trainLine.getState()
        for station in self.stations:
            state += station.getState()
        return state

    def getStateLen(self):
        stateLen = len(self.trainLines)
        stateLen += len(self.stations)
        return stateLen

    def getValidMoves(self):
        moves = []
        for i in range(len(self.trainLines)):
            if self.trainLines[i].maxCars > self.trainLines[i].cars:
                moves.append(i)
        return moves

    def makeMove(self, line, card):
        if card == '2':
            self.advanceLine(line, 2, 'normal')
        if card == '3':
            self.advanceLine(line, 2, 'normal')
        if card == '4':
            self.advanceLine(line, 4, 'normal')
        if card == '5':
            self.advanceLine(line, 5, 'normal')
        if card == '6':
            self.advanceLine(line, 6, 'normal')
        if card == 's':
            self.advanceLine(line, 1, 'star')
        if card == 'c2':
            self.advanceLine(line, 2, 'circle')
        if card == 'c3':
            self.advanceLine(line, 3, 'circle')

    def previewMove(self, line, card):
        copiedBoard = copy.deepcopy(self)
        copiedBoard.makeMove(line, card)
        return copiedBoard.getState()
        

    def advanceLine(self, line, number, cardType):
        if self.trainLines[line].maxCars > self.trainLines[line].cars:
            self.trainLines[line].advance(number, cardType)

    def gameOver(self):
        gameOver = False
        emptyStations = 0
        for trainLine in self.trainLines:
            emptyStations += trainLine.maxCars - trainLine.cars
        if emptyStations == 0:
            gameOver = True
        return gameOver
        
    def calculateScore(self):
        score = 0
        empty = 0
        for trainLine in self.trainLines:
            if trainLine.complete():
                score += trainLine.points
        for station in self.stations:
            if station.fill == 'Empty':
                empty += 1
            elif station.fill == 'Star':
                score += 2*station.connections
        return score + self.negativeScore(empty)

    def calculateReward(self):
        score = 0
        empty = 0
        for trainLine in self.trainLines:
            if trainLine.complete():
                score += trainLine.points
        for station in self.stations:
            if station.fill == 'Empty':
                empty += 1
            elif station.fill == 'Star':
                score += 2*station.connections
        return score - empty

    def negativeScore(self, empty):
        if empty >= 21:
            return -10
        if empty >= 19:
            return -9
        if empty >= 17:
            return -8
        if empty >= 15:
            return -7;
        if empty >= 13:
            return -6
        if empty >= 11:
            return -5
        if empty >= 9:
            return -4
        if empty >= 8:
            return -3
        if empty >= 7:
            return -2
        if empty >= 6:
            return -1
        else:
            return 0
        

class TrainLine():
    def __init__(self, cars, points):
        self.maxCars = cars
        self.cars = 0
        self.points = points
        self.stations = []

    def addStation(self, trainStation):
        self.stations.append(trainStation)
        trainStation.connections+=1

    def addStations(self, stationList, times):
        while times > 0:
            times-=1
            trainStation = TrainStation()
            stationList.append(trainStation)
            self.stations.append(trainStation)

    def __str__(self):
        printValue = 'Points: '+ str(self.points) + ' '
        printValue += '{'+str(self.maxCars-self.cars)+'} '
        for station in self.stations:
            if station.fill == 'Empty':
                printValue+='[ ]'
            elif station.fill == 'Star':
                printValue+='['+str(2*station.connections)+']'
            else:
                printValue+='[X]'
        return printValue

    def getState(self):
        state = str(self.cars)
        return state

    def advance(self, number, cardType):
        self.cars += 1
        advancesLeft = number
        startedAdvance = False
        for station in self.stations:
            if station.fill == 'Empty':
                startedAdvance = True
                advancesLeft-=1
                if cardType == 'star':
                    station.fill = 'Star'
                else:
                    station.fill = 'Filled'
                if advancesLeft == 0:
                    break
            else:
                if startedAdvance and cardType != 'circle':
                    break

    def complete(self):
        complete = True
        for station in self.stations:
            if station.fill == 'Empty':
                complete = False
                break
        return complete

class TrainStation():
    def __init__(self):
        self.fill = 'Empty'
        self.connections = 1
        
    def getState(self):
        state = '0'
        if self.fill == 'Filled':
            state = '1'
        elif self.fill == 'Star':
            state = '2'
        return state
