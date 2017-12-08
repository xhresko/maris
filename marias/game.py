#!/usr/bin/python3
# coding=utf-8

import cards
import random
import string


class Player(object):
    """ Basic player, which plays randomly. """

    def __init__(self, is_solo=False, cards=None):
        self.name = "".join([random.choice(string.ascii_lowercase) for i in range(6)]).title()
        self.is_solo = is_solo
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

    def select_talon(self, trump):
        """ Won't throw away points or trump if not necessary.
        Otherwise choses cards for talon randomly."""
        fortalon = [c for c in self.hand if c.val_game() < 6 and c.suit != trump]
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
        choice = random.choice(playable)
        self.drop_card(choice)
        return choice

    def playable_cards(self, table, trump):
        if not table:  # first player can choose whichever card he wants
            return self.hand
        suit = table[0].suit
        same_suit = [c for c in self.hand if c.suit == suit]
        trump_suit = [c for c in self.hand if c.suit == trump]
        trump_played = [c for c in table if c.suit == trump]

        if not same_suit and not trump_suit: # no card of same suit
            return self.hand
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


class HumanPlayer(Player):
    """ Human player that expect input and provide info about status. """

    def __init__(self, is_solo=False, cards=None):
        self.name = "".join([random.choice(string.ascii_lowercase) for i in range(6)]).title()
        print ("Your name will be {}".format(self.name))
        self.is_solo = is_solo
        if cards is None:
            self.hand = []
        else:
            self.hand = cards

    def print_hand(self, marked=None):
        if not marked:
            marked = []
        print ("You have following cards:")
        for i, c in enumerate(sorted(self.hand)):
            mark = "*" if c in marked else ""
            print("({}) - {}  {}".format(i, c, mark))

    def select_talon(self, trump):
        self.print_hand()
        t_1 = input("Please choose first talon card: ")
        t_2 = input("Please choose second talon card: ")

        talon = [sorted(self.hand)[int(t_1)], sorted(self.hand)[int(t_2)]]

        self.drop_card(talon[0])
        self.drop_card(talon[1])

        print ("You dropped {} and {} in talon.".format(talon[0], talon[1]))
        return talon

    def select_trump(self):
        self.print_hand()
        trump_num = input("Pick a trump by selecting card from your hand: ")
        trump = sorted(self.hand)[int(trump_num)].suit
        return trump

    def play_card(self, table, trump):
        playable = self.playable_cards(table, trump)
        self.print_hand(playable)
        card_num = input("Choose which card you want to play: ")
        choice = sorted(self.hand)[int(card_num)]
        self.drop_card(choice)
        return choice


class MariasGame(object):
    """ One game of Marias. """

    def __init__(self, human=0, prints=False):

        if not prints:
            self.report = lambda x: None
        else:
            self.report = print

        gamepack = cards.new_pack()

        self.p_1 = Player(is_solo=True)
        self.p_2 = Player()
        self.p_3 = Player()


        if human == 1:
            self.p_1 = HumanPlayer(is_solo=True)
        elif human == 2:
            self.p_2 = HumanPlayer()
        elif human == 3:
            self.p_3 = HumanPlayer()

        self.p_1.add_cards(gamepack[0:7])

        self.trump = self.p_1.select_trump()

        self.report("{} has been selected as trump".format(self.trump))

        self.p_2.add_cards(gamepack[7:12])
        self.p_3.add_cards(gamepack[12:17])

        self.p_1.add_cards(gamepack[17:22])
        self.p_2.add_cards(gamepack[22:27])
        self.p_3.add_cards(gamepack[27:32])


        self.talon = self.p_1.select_talon(self.trump)

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
        if not self.beats(self.table[1], self.table[0]) and not self.beats(self.table[2], self.table[0]):
            return 0
        if not self.beats(self.table[2], self.table[1]):
            return 1
        return 2

    def play(self):
        for i in range(10):
            self.report("-------------")
            self.report("Round no. {}".format(i + 1))
            self.report("-------------")
            self.table = []
            for player in self.order:
                card = player.play_card(self.table, self.trump)
                self.table.append(card)
                self.report("{} played {}".format(player.name, card))

            win = self.winner()
            if self.order[win].is_solo:
                self.solo_gain += self.table[:]
                self.last_solo, self.last_team = 10, 0
            else:
                self.team_gain += self.table[:]
                self.last_solo, self.last_team = 0, 10
            if win == 1:
                self.order = self.order[1:] + [self.order[0]]
            if win == 2:
                self.order = [self.order[2]] + self.order[:2]

        solo_score = sum([c.score() for c in self.solo_gain]) + self.last_solo
        team_score = sum([c.score() for c in self.team_gain]) + self.last_team

        self.report("Solo player score: {}".format(solo_score))
        self.report("Team score: {}".format(team_score))
        return solo_score, team_score


def main():

    sw, tw = 0.0, 0.0
    gamnum = 1000
    for i in range(gamnum):
        game = MariasGame(human=(i % 3) + 1, prints=True)
        s, t = game.play()
        print ("")
        print ("==========================")
        print ("")
        if s > t:
            sw +=1
        elif t > s:
            tw +=1
    print ("------------------------------")
    print ("Solo win percentage is", sw*100/gamnum, "with total wins", int(sw))
    print ("Team win percentage is", tw*100/gamnum, "with total wins", int(tw))


if __name__ == "__main__":
    main()

