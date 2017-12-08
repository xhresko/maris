#!/usr/bin/python3
# coding=utf-8

import cards
import random
import string

class Player(object):
    """ Basic player, which plays randomly. """

    def __init__(self, cards=None):
        self.name = "".join([random.choice(string.ascii_lowercase) for i in range(6)]).title()
        if cards is None:
            self.hand = []
        else:
            self.hand = cards

    def drop_card(self, card):
        """ Use card for play or for putting into talon """
            self.hand.remove(card)

    def add_cards(self, cards):
        """ Obtain cards from the dealer """
            self.hand += cards

    def select_talon(self, trumps):
        """ Won't throw away points or trumps if not necessary.
        Otherwise choses cards for talon randomly."""
        fortalon = [c for c in self.hand if c.val_game() < 6 and c.suit != trumps]
        if len(fortalon) < 2:
            fortalon = [c for c in self.hand if c.val_game() < 6]

        t_1 = random.choice(fortalon)
        t_2 = random.choice(fortalon)

        while t_2 == t_1:
            t_2 = random.choice(fortalon)

        talon = [t_1, t_2]

        self.drop_card(t_1)
        self.drop_card(t_2)

        return talon

    def select_trump(self):
        """ Count the values of the cards for each suit
        and select the one with highest sum to be trump"""
        scores = [0,0,0,0]
        for i, s in enumerate(cards.SUITS):
            for c in self.hand:
                if c.suit == s:
                    scores[i] += c.val_game()
        return cards.SUITS[scores.index(max(scores))]


    def play_card(self, table, trump):
        """ Play card from hand - by rules but randomly """
        playable = self.playable_cards(table, trump)
        return random.choice(playable)

    def playable_cards(self, table, trump):
        if not table:  # first player can choose whichever card he wants
            return hand
        suit = table[0].suit
        same_suit = [c for c in hand if c.suit == suit]
        trump_suit = [c for c in hand if c.suit == trump]
        trump_played = [c for c in table if c.suit == trump]

        if not same_suit and not trump_suit: # no card of same suit
            return hand
        elif not same_suit and trump_suit:
            values = [c.val_game() for c in table if c.suit == trump]
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


class MariasGame(object):
    """ One game of Marias. """

    def __init__(self):
        gamepack = cards.new_pack()

        self.p_1 = Player()
        self.p_2 = Player()
        self.p_3 = Player()

        self.p_1.add_cards(gamepack[0:7])

        self.trumps = self.p_1.select_trump()

        self.p_2.add_cards(gamepack[7:12])
        self.p_3.add_cards(gamepack[12:17])

        self.p_1.add_cards(gamepack[17:22])
        self.p_2.add_cards(gamepack[22:27])
        self.p_3.add_cards(gamepack[27:32])


        self.talon = self.p_1.select_talon(self.trumps)

        self.order = [self.p_1, self.p_2, self.p_3]

        self.solo_gain = []
        self.team_gain = []

        self.last_solo = 0
        self.last_team = 0

        self.table = []

    def beats(self, one, other):
        if self.trump:
            if one.suit == self.trump and other.suit != self.trump:
                return True
        if one.suit != other.suit:
            return False
        if one.suit == other.suit:
            return one > other

    def winner(self):
        if not self.beats(self.table[1], self.table[0], self.trump) and not self.beats(self.table[2], self.table[0], self.trump):
            return 0
        if not self.beats(self.table[2], self.table[1], self.trump):
            return 1
        return 2

    def play(self):
        for i in range(10):
            self.table = []
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


def main():

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


if __name__ == "__main__":
    main()

