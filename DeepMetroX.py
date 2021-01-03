import random
import csv
import os
from pathlib import Path
from tabulate import tabulate
from abc import abstractmethod
import keras.layers as Kl
import keras.models as Km
import numpy as np
import matplotlib.pyplot as plt
import TokyoBoard
import cardDeck

class MetroX():

    def __init__(self, player1, deckType, exp1=1):
        player1 = globals()[player1]
        self.player1 = player1(exploration_factor=exp1)
        self.deckType = deckType
        self.init_game()

    def play_game(self):
        self.print_game()
        while self.gameEnd is False:
            self.state = self.play_move()
            self.print_game()

    def play_to_learn(self, episodes):
        avgScore = 0
        
        try:
            os.remove("results.txt")
        except:
            pass
        
        for i in range(episodes):
            print('Episode number: ' + str(i))

            while self.gameEnd is False:
                self.state = self.play_move(learn=True)

            score = self.board.calculateScore()
            avgScore = (avgScore*0.95) + (score*0.05)
                
            print('Score: ' + str(score))
            print('Weighted Average Score: ' + str(avgScore))

            log = open("results.txt", "a")
            log.write('Weighted Average Score: ' + str(avgScore))
            log.close()

            # update last state
            self.state = self.play_move(learn=True)
            # update winning state
            self.state = self.play_move(learn=True)

            self.init_game()
        
        self.player1.save_values()

    def play_move(self, learn=False):
        if learn is True:
            board_state = self.player1.make_move_and_learn(self.board, self.cardDeck, self.gameEnd)
        else:
            board_state = self.player1.make_move(self.board, self.cardDeck, self.gameEnd)
        card_state = self.turnEnd()
        return board_state+card_state

    def print_game(self):
        print(self.board)
        print('Card:' + self.cardDeck.currentCard)

    def turnEnd(self):
        if self.board.gameOver():
            self.gameEnd = True
        else:
            self.cardDeck.nextCard();
        return self.cardDeck.getState()

    def init_game(self):
        self.board = TokyoBoard.TokyoBoard()
        self.gameEnd = False
        self.cardDeck = cardDeck.CardDeck()


class Player():

    def __init__(self, exploration_factor=1):
        self.print_value = False
        self.exp_factor = exploration_factor

    def make_move(self, board, cardDeck, gameEnd):
        idx = int(input('Choose station number: '))
        board.makeMove(idx, cardDeck.currentCard)
        return board.getState()+cardDeck.getState()


class Agent(Player):

    def __init__(self, exploration_factor=1):
        super().__init__(exploration_factor)
        self.epsilon = 0.1
        self.alpha = 0.5
        self.prev_state = TokyoBoard.TokyoBoard().getState() + cardDeck.CardDeck().getState()
        self.state = None
        self.print_value = False

    @abstractmethod
    def calc_value(self, board, cardDeck):
        pass

    @abstractmethod
    def learn_state(self, board, cardDeck, gameEnd):
        pass

    def make_move(self, board, cardDeck, gameEnd):
        self.state = board.getState()+cardDeck.getState()

        if gameEnd:
            new_state = board.getState()+cardDeck.getState()
            return new_state

        p = random.uniform(0, 1)
        if p < self.exp_factor:
            new_state = self.make_optimal_move(board, cardDeck)
        else:
            moves = board.getValidMoves()
            idx = random.choice(moves)
            board.makeMove(idx, cardDeck.currentCard)
            new_state = board.getState()+cardDeck.getState()
        return new_state

    def make_move_and_learn(self, board, cardDeck, gameEnd):

        self.learn_state(board, cardDeck, gameEnd)

        return self.make_move(board, cardDeck, gameEnd)

    def make_optimal_move(self, board, cardDeck):
        moves = board.getValidMoves()
        if len(moves) == 1:
            board.makeMove(moves[0], cardDeck)
            return board.getState()+cardDeck.getState()

        temp_move_list = []
        v = -float('Inf')

        for idx in moves:

            v_temp = []
            temp_state = board.previewMove(idx, cardDeck.currentCard)

            simCardDraws = 10
            while simCardDraws > 0:
                simCardDraws-=1
                temp_state_op = temp_state+cardDeck.previewNextCard()
                v_temp.append(self.calc_value(temp_state_op))

            # deletes Nones
            v_temp = list(filter(None.__ne__, v_temp))

            if len(v_temp) != 0:
                v_temp = np.average(v_temp)
            else:
                # encourage exploration
                v_temp = 1

            if v_temp > v:
                temp_move_list = [idx]
                v = v_temp
            elif v_temp == v:
                temp_move_list.append(idx)

        try:
            board.makeMove(random.choice(temp_move_list), cardDeck)
        except ValueError:
            print('temp state:', temp_state_list)
            raise Exception('temp state empty')

        return board.getState()+cardDeck.getState()

    def reward(self, board):
        score = board.calculateScore()
        reward = (score+6)/90
        if reward > 1:
            reward = 1
        return reward

class DeepAgent(Agent):

    def __init__(self, exploration_factor=1):
        super().__init__(exploration_factor)
        self.value_model = self.load_model()

    @staticmethod
    def state2array(state):
        num_state = []
        for s in state:
            num_state.append(int(s))
        num_state = np.array([num_state])
        return num_state

    def learn_state(self, board, cardDeck, gameEnd):

        state = board.getState()+cardDeck.getState()

        target = self.calc_target(board, cardDeck, gameEnd)

        self.train_model(target, 10)

        self.prev_state = state

    def load_model(self):
        s = 'model_values_metroX.h5'
        model_file = Path(s)
        if model_file.is_file():
            model = Km.load_model(s)
            print('load model: ' + s)
        else:
            print('new model')
            model = Km.Sequential()
            model.add(Kl.Dense(64, activation='relu', input_dim=95))
            model.add(Kl.Dense(64, activation='relu'))
            model.add(Kl.Dense(1, activation='linear'))
            model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'])

        model.summary()
        return model

    def calc_value(self, state):
        return self.value_model.predict(self.state2array(state))

    def calc_target(self, board, cardDeck, gameEnd):
        v_s = self.calc_value(self.prev_state)

        R = self.reward(board)

        if gameEnd:
            v_s_tag = 0
        else:
            v_s_tag = self.calc_value(board.getState()+cardDeck.getState())

        target = np.array(v_s + self.alpha * (R + v_s_tag - v_s))

        return target

    def train_model(self, target, epochs):

        X_train = self.state2array(self.prev_state)

        if target is not None:
            self.value_model.fit(X_train, target, epochs=epochs, verbose=0)

    def save_values(self):
        s = 'model_values_metroX.h5'
        try:
            os.remove(s)
        except:
            pass
        self.value_model.save(s)


def check_player():
    #print('DeepAgent X 0.8 and DeepAgent 0.8')
    game = MetroX('DeepAgent', 'Random', 0.8)
    game.play_to_learn(10000)
    game = MetroX('DeepAgent', 'Random', 1)
    game.play_game()


check_player()
