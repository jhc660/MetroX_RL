import random
import copy

class CardDeck():
    def __init__(self):
        self.deck = []
        self.discard = []
        self.currentCard = ''
        self.initDeck()
        self.nextCard()

    def nextCard(self):
        if self.currentCard != '':
            self.discard.append(self.currentCard)
            if self.currentCard == '6':
                self.deck.extend(self.discard)
                self.discard = []   
        self.currentCard = random.choice(self.deck)
        self.deck.remove(self.currentCard)

    def getState(self):
        card = self.currentCard
        if card == 'c2':
            card = '7'
        elif card == 'c3':
            card = '8'
        elif card == 's':
            card = '1'
        state = card
        #state += str(self.deck.count('2'))
        #state += str(self.deck.count('3'))
        #state += str(self.deck.count('4'))
        #state += str(self.deck.count('5'))
        #state += str(self.deck.count('6'))
        #state += str(self.deck.count('s'))
        #state += str(self.deck.count('c2'))
        #state += str(self.deck.count('c3'))
        return state

    def previewNextCard(self):
        copiedDeck = copy.deepcopy(self)
        copiedDeck.nextCard()
        return copiedDeck.getState()

    def initDeck(self):
        self.deck = []
        self.deck.append('2')
        self.deck.append('2')
        self.deck.append('3')
        self.deck.append('3')
        self.deck.append('3')
        self.deck.append('3')
        self.deck.append('4')
        self.deck.append('4')
        self.deck.append('4')
        self.deck.append('4')
        self.deck.append('4')
        self.deck.append('5')
        self.deck.append('5')
        self.deck.append('6')
        self.deck.append('s')
        self.deck.append('s')
        self.deck.append('s')
        self.deck.append('c2')
        self.deck.append('c2')
        self.deck.append('c3')


