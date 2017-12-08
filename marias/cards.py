#!/usr/bin/python3
# coding=utf-8
from collections import OrderedDict
import random


SUITS = ["♠", "♦", "♣", "♥"]

CARD_NAMES = OrderedDict([("VII", (0, 0)),
                          ("VIII", (1, 1)),
                          ("IX", (2, 2)),
                          ("X", (3, 6)),
                          ("J", (4, 3)),
                          ("Q", (5, 4)),
                          ("K", (6, 5)),
                          ("A", (7, 7))])


class Card(object):
    """ One card from the classic 32 cards pack"""

    def __init__(self, value, suit):
        self.suit = SUITS[suit]
        self.value = list(CARD_NAMES.keys())[value]

    def val_base(self):
        """
        Returns value of the card in 'regular' order.
        Used in 'betl' and 'durch' variants of game.
        """
        return CARD_NAMES[self.value][0]

    def val_game(self):
        """ Returns value of the card in 'classic game' order.
        The X is in this case between K and A."""
        return CARD_NAMES[self.value][1]

    def __repr__(self):
        """ String representation of card (e.g. 'K of ♥') """
        return "{} of {}".format(self.value, self.suit)

    def __lt__(self, other):
        if self.suit == other.suit:
            return self.val_game() < other.val_game()
        return SUITS.index(self.suit) < SUITS.index(other.suit)

    def score(self):
        """ Scoring value of the card for 'classic game' """
        if self.value == "X" or self.value == "A":
            return 10
        else:
            return 0

def all_cards():
    """Generate whole ordered pack of cards"""
    for suit in range(len(SUITS)):
        for value in range(len(CARD_NAMES)):
            yield Card(value, suit)

def new_pack():
    """ Create list of all cards in random order (shuffled)"""
    pack = list(all_cards())
    random.shuffle(pack)
    return pack

