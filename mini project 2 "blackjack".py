# Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
score = 0
outcome = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return "Hand contains " + ' '.join(str(h) for h in self.hand)
    
    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        hand_value = 0
        for h in self.hand:
            for key, value in VALUES.items():
                if Card.get_rank(h) == key:
                    hand_value += value
                    
        if ("AC" or "AS" or "AH" or "AD") not in self.hand:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
   
    def draw(self, canvas, pos):
        for c in self.hand:
            c.draw(canvas,[pos[0]+ self.hand.index(c)*100, pos[1]])
     
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for s in SUITS:
            for r in RANKS:
                self.deck.append(Card(s, r))
        
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return random.choice(self.deck)
    
    def __str__(self):
        return "Deck contains " + ' '.join(str(d) for d in self.deck) 

#define event handlers for buttons
def deal():
    global in_play, score, outcome, player_hand, dealer_hand, deck_card
    
    if in_play == True:
        outcome = "You have busted"
        score -= 1
        in_play = False
    else:
        in_play = True
        player_hand = Hand()
        dealer_hand = Hand()
        deck_card = Deck()
    
        player_hand.add_card(deck_card.deal_card())
        player_hand.add_card(deck_card.deal_card())
        dealer_hand.add_card(deck_card.deal_card())
        dealer_hand.add_card(deck_card.deal_card()) 
    
def hit():
    global score, in_play, outcome, player_hand, deck_card

    if player_hand.get_value() <= 21:
        in_play = True
        player_hand.add_card(deck_card.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted"
            score -= 1
            in_play = False         
    else:
        outcome = "You have busted"
        score -= 1
        in_play = False
        
def stand():
    global score, in_play, outcome, player_hand, dealer_hand, deck_card
    
    if player_hand.get_value() > 21:
        outcome = "You have busted"
    else:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck_card.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = "You have won"
            score += 1
        elif player_hand.get_value() > dealer_hand.get_value():
            outcome = "You have won"
            score += 1
        else:
            outcome = "You have busted"
            score -= 1
    in_play = False

# draw handler    
def draw(canvas):
    global in_play, score, player_hand, dealer_hand
    
    canvas.draw_text("Blackjack", [100, 100], 48, "Black")
    canvas.draw_text("Dealer", [100, 170], 30, "Black")
    canvas.draw_text("Player", [100, 420], 30, "Black")
    canvas.draw_text("Score: " + str(score), [450, 100], 30, "Black")

    dealer_hand.draw(canvas, [100, 200])
    player_hand.draw(canvas, [100, 450])
    
    if in_play:
        canvas.draw_text("Hit or stand?", [300, 420], 24, "Black")
        card_back_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [card_back_loc[0]+100, card_back_loc[1]+200] , CARD_BACK_SIZE)
    else:
        canvas.draw_text("New deal?", [300, 420], 24, "Black") 
        canvas.draw_text(outcome, [300, 170], 24, "Black")

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

