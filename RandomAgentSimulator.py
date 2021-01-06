import EasyBoard
import TokyoBoard
import cardDeck
import random

def simulate(times = 1000):
    timesLeft = times
    score = 0
    reward = 0
    while (timesLeft > 0):
        timesLeft -= 1
        board = EasyBoard.EasyBoard()
        deck = cardDeck.CardDeck()
        while board.gameOver() == False:
            move = random.choice(board.getValidMoves())
            board.makeMove(move, deck.currentCard)
            deck.nextCard()
            if board.gameOver() == True:
                score += board.calculateScore()
                reward += board.calculateReward()
        print('Game '+str(times-timesLeft))
    print('Avg Score: ' + str(score/times))
    print('Avg Score: ' + str(reward/times))

simulate()
