import Board
import cardDeck

class EasyBoard(Board.Board):
    def __init__(self):
        super().__init__()
        self.trainLines.append(Board.TrainLine(10,3))
        self.trainLines[0].addStations(self.stations, 3)
        
        self.trainLines.append(Board.TrainLine(10,3))
        self.trainLines[1].addStations(self.stations, 12)
        
        self.trainLines.append(Board.TrainLine(2,3))
        self.trainLines[2].addStations(self.stations, 12)

def testRoutine():
    easyBoardTest = EasyBoard()
    cardDeckTest = cardDeck.CardDeck()
    print(easyBoardTest.getState())
    easyBoardTest.makeMove(0, '6')
    easyBoardTest.makeMove(1, 'c2')
    easyBoardTest.makeMove(2, 's')
    print(easyBoardTest)
    print(easyBoardTest.getState())
    print('Points: '+str(easyBoardTest.calculateScore()))
    print(easyBoardTest.getValidMoves())
    print(easyBoardTest.previewMove(1, '6'))
    print(easyBoardTest)
    print(easyBoardTest.getState()+cardDeckTest.getState())

#testRoutine()
