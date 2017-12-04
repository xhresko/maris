#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random

def playable_cards(hand, table, trumps):
    if not table:  # first player can choose whichever card he wants
        return hand
    suit = table[0][1]
    same_suit = [c for c in hand if c[1] == suit]
    trump_suit = [c for c in hand if c[1] == trumps]
    trump_played = [c for c in table if c[1] == trumps]

    if not same_suit and not trump_suit: # no card of same suit
        return hand
    elif not same_suit and trump_suit:
        values = [c[0] for c in table if c[1] == trumps]
        higher_trumps = [c for c in trump_suit if not values or c[0] > max(values)]
        if higher_trumps:
            return higher_trumps
        else:
            return trump_suit
    elif trump_played and same_suit:
        return same_suit

    values = [c[0] for c in table if c[1] == suit]
    higher_suit = [c for c in same_suit if c[0] > max(values)]
    if higher_suit:
        return higher_suit
    return same_suit


SUITS = ["♠", "♣", "♥", "♦"]

CARD_VALS_NAMES = ["VII", "VIII", "IX", "X", "J", "Q", "K", "A"]
CARD_VALS = [0, 1, 2, 3, 4, 5, 6, 7]

CARDS = [(v, s) for s in SUITS for v in CARD_VALS]

print(CARDS)

random.shuffle(CARDS)

p_1 = CARDS[0:7]

p_2 = CARDS[7:12]

p_3 = CARDS[12:17]

p_1 += CARDS[17:22]

p_2 += CARDS[22:27]

p_3 += CARDS[27:32]


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

trumps = random.choice(p_1)[1]
print ("Player 1 picked {} as trumps".format(trumps))
print ("Player 1 put {} into talon".format(talon))

order = [(p_1, "1"), (p_2, "2"), (p_3, "3")]

for i in range(10):
    print ("Round " + str(i))
    table = []
    for (hand, name) in order:
        print ("Player {} turn".format(name))
        pos_cards = playable_cards(hand, table, trumps)
        print (pos_cards)
        card = random.choice(pos_cards)
        table.append(card)
        print (CARD_VALS_NAMES[card[0]] + " of " + card[1])
        hand.remove(card)







