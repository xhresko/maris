#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from collections import OrderedDict

class Card(object):
    SUITS = ["♠", "♦", "♣", "♥"]
    CARD_NAMES = OrderedDict([
                  ("VII", (0, 0)),
                  ("VIII", (1, 1)),
                  ("IX", (2, 2)),
                  ("X", (3, 6)),
                  ("J", (4, 3)),
                  ("Q", (5, 4)),
                  ("K", (6, 5)),
                  ("A", (7, 7))])

    def __init__(self, value, suit):
        self.suit = self.SUITS[suit]
        self.value = list(self.CARD_NAMES.keys())[value]

    def val_base(self):
        return self.CARD_NAMES[self.value][0]

    def val_game(self):
        return self.CARD_NAMES[self.value][1]

    def __repr__(self):
        return "{} of {}".format(self.value, self.suit)

    def __lt__(self, other):
        #return self.SUITS.index(self.suit) < self.SUITS.index(other.suit) and self.val_game() < other.val_game()
        if self.suit == other.suit:
            return self.val_game() < other.val_game()
        return self.SUITS.index(self.suit) < self.SUITS.index(other.suit)
    def beats(self, other, trump):
        if self.suit == trump and other.suit != trump:
            return True
        if self.suit != other.suit:
            return False
        if self.suit == other.suit:
            return self > other

    def score(self):
        if self.value == "X" or self.value == "A":
            return 10
        else:
            return 0

def all_cards():
    for suit in range(4):
        for value in range(8):
            yield Card(value, suit)

def new_pack():
    pack = list(all_cards())
    random.shuffle(pack)
    return pack

def playable_cards(hand, table, trumps):
    if not table:  # first player can choose whichever card he wants
        return hand
    suit = table[0].suit
    same_suit = [c for c in hand if c.suit == suit]
    trump_suit = [c for c in hand if c.suit == trumps]
    trump_played = [c for c in table if c.suit == trumps]

    if not same_suit and not trump_suit: # no card of same suit
        return hand
    elif not same_suit and trump_suit:
        values = [c.val_game() for c in table if c.suit == trumps]
        higher_trumps = [c for c in trump_suit if not values or c.val_game() > max(values)]
        if higher_trumps:
            return higher_trumps
        else:
            return trump_suit
    elif trump_played and same_suit:
        return same_suit

    values = [c.val_game() for c in table if c.suit == suit]
    higher_suit = [c for c in same_suit if c.val_game() > max(values)]
    if higher_suit:
        return higher_suit
    return same_suit

def winner(table, trump):
    if not table[1].beats(table[0], trump) and not table[2].beats(table[0], trump):
        return 0
    if not table[2].beats(table[1], trump):
        return 1
    return 2

def select_trump(hand):
    scores = [0,0,0,0]
    for i, s in enumerate(Card.SUITS):
        for c in hand:
            if c.suit == s:
                scores[i] += c.val_game()
    return Card.SUITS[scores.index(max(scores))]

def select_talon(hand, trumps):
    fortalon = [c for c in hand if c.val_game() < 6 and c.suit != trumps]
    if len(fortalon) < 2:
        fortalon = [c for c in hand if c.val_game() < 6]

    t_1 = random.choice(fortalon)
    t_2 = random.choice(fortalon)

    while t_2 == t_1:
        t_2 = random.choice(fortalon)

    talon = [t_1, t_2]
    return talon

def game():
    gamepack = new_pack()

    p_1 = gamepack[0:7]

    trumps = select_trump(p_1)
    p_2 = gamepack[7:12]
    p_3 = gamepack[12:17]
    p_1 += gamepack[17:22]
    p_2 += gamepack[22:27]
    p_3 += gamepack[27:32]


    talon = select_talon(p_1, trumps)
    for c in talon:
        p_1.remove(c)


    order = [(p_1, "1"), (p_2, "2"), (p_3, "3")]

    solo_gain = []
    team_gain = []

    last_solo = 0
    last_team = 0

    for i in range(10):
        table = []
        for (hand, name) in order:
            pos_cards = playable_cards(hand, table, trumps)
            card = random.choice(pos_cards)
            table.append(card)
            hand.remove(card)

        win = winner(table, trumps)
        if order[win][1] == "1":
            solo_gain += table[:]
            last_solo, last_team = 10, 0
        else:
            team_gain += table[:]
            last_solo, last_team = 0, 10
        if win == 1:
            order = order[1:] + [order[0]]
        if win == 2:
            order = [order[2]] + order[:2]
    solo_score = sum([c.score() for c in solo_gain]) + last_solo
    team_score = sum([c.score() for c in team_gain]) + last_team
    return solo_score, team_score

sw, tw = 0.0, 0.0
gamnum = 10000
for i in range(gamnum):
    s, t = game()
    if s > t:
        sw +=1
    elif t > s:
        tw +=1

print ("Solo win percentage is", sw*100/gamnum)
print ("Team win percentage is", tw*100/gamnum)


def game_prints():
    gamepack = new_pack()

    p_1 = gamepack[0:7]

    trumps = random.choice(p_1).suit

    p_2 = gamepack[7:12]

    p_3 = gamepack[12:17]

    p_1 += gamepack[17:22]

    p_2 += gamepack[22:27]

    p_3 += gamepack[27:32]


    print ("Player One:")
    for c in sorted(p_1):
        print (c)

    print ("Player Two:")
    for c in sorted(p_2):
        print (c)

    print ("Player Three:")
    for c in sorted(p_3):
        print (c)

    talon = p_1[:2]
    p_1 = p_1[2:]

    #trumps = random.choice(p_1).suit
    print ("Player 1 picked {} as trumps".format(trumps))
    print ("Player 1 put {} into talon".format(talon))

    order = [(p_1, "1"), (p_2, "2"), (p_3, "3")]

    solo_gain = []
    team_gain = []

    last_solo = 0
    last_team = 0

    for i in range(10):
        print ("-"*15)
        print ("Round " + str(i+1))
        print ("-"*15)
        table = []
        for (hand, name) in order:

            print ("Player {} turn".format(name))
            pos_cards = playable_cards(hand, table, trumps)
            print (pos_cards)
            card = random.choice(pos_cards)
            table.append(card)
            print (card)
            hand.remove(card)

        win = winner(table, trumps)
        print ("Winner of round is player", order[win][1])
        if order[win][1] == "1":
            solo_gain += table[:]
            last_solo, last_team = 10, 0
        else:
            team_gain += table[:]
            last_solo, last_team = 0, 10
        if win == 1:
            order = order[1:] + [order[0]]
        if win == 2:
            order = [order[2]] + order[:2]


    print ("Solo gain: ", sum([c.score() for c in solo_gain]) + last_solo)
    print ("Team gain: ", sum([c.score() for c in team_gain]) + last_team)

