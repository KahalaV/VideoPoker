# TIE-02100 Johdatus ohjelmointiin
# Väinö Kahala
# Videopokeri tkinterillä

"""
Tämä on tkinterillä skaalautuvasti toteutettu Jacks or Better-videopokeriin
pohjautuva yhden hengen pokeripeli. Pelissä pelaaja voi valita panoksensa
väliltä 1-5 tai 10. Jokaisella pelikierroksella pelaajalla on käytettävissä
yksi korttien vaihto. Pelaaja voi vaihtaa haluamansa määrän kortteja, jonka
jälkeen pelaajalle maksetaan mahdollinen voitto muodostetun pokerikäden ja
voittotaulukon mukaan.
Mikäli pelaajan rahat loppuvat, peli päättyy.

DEAL-nappi pelitilanteesta riippuen joko jakaa uuden käden, vaihtaa
lukitsemattomat kortit tai lopettaa kierroksen ja maksaa pelaajalle voitot.

BET-napista pelaaja pystyy vaihtamaan panostaan.

KEEP-napeilla pelaaja voi lukita haluamansa kortit, jolloin niitä ei vaihdeta.
"""



from random import randint
from tkinter import *


CARDS = ["1S.gif", "2S.gif", "3S.gif", "4S.gif", "5S.gif", "6S.gif", "7S.gif",
         "8S.gif", "9S.gif", "10S.gif", "11S.gif", "12S.gif", "13S.gif",
         "1H.gif", "2H.gif", "3H.gif", "4H.gif", "5H.gif", "6H.gif", "7H.gif",
         "8H.gif", "9H.gif", "10H.gif", "11H.gif", "12H.gif", "13H.gif",
         "1C.gif", "2C.gif", "3C.gif", "4C.gif", "5C.gif", "6C.gif", "7C.gif",
         "8C.gif", "9C.gif", "10C.gif", "11C.gif", "12C.gif", "13C.gif",
         "1D.gif", "2D.gif", "3D.gif", "4D.gif", "5D.gif", "6D.gif", "7D.gif",
         "8D.gif", "9D.gif", "10D.gif", "11D.gif", "12D.gif", "13D.gif",
         "red_back.gif"]
# includes all filenames of the pictures used in the game

CARD_NAMES = ["1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S",
              "11S", "12S", "13S",
              "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H",
              "11H", "12H", "13H",
              "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C",
              "11C", "12C", "13C",
              "1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D",
              "11D", "12D", "13D"]
# contains the name of every playing card
# names are used to handle information about cards in hand and deck

WIN_FACTORS = [1, 2, 3, 4, 6, 9, 25, 50, 250]
# these are used to calculate the payout for different winning hands

def return_values(hand):
    """
    :param hand: list that contains the card names of a hand
    :return: a sorted list of card values (1-13) in given hand as integers
    """

    values = []
    for card in hand:
        values.append(int(card[:-1]))

    values.sort(key=int)
    return values


def is_straight(hand):
    """
    Checks if hand contains a series of values that form a straight

    :param hand: list that contains the card names of a hand
    :return: boolean
    """
    values = return_values(hand)

    if values[4] - values[3] == 1:
        if values[3] - values[2] == 1:
            if values[2] - values[1] == 1:
                if values[1] - values[0] == 1:
                    return True
    else:
        return False

def is_flush(hand):
    """
    Checks if all the cards of a hand have the same suit

    :param hand: list that contains the card names of a hand
    :return: boolean
    """

    suits = []
    for card in hand:
        suits.append(card[-1:])
    if suits[0] == suits[1] == suits[2] == suits[3] == suits[4]:
        return True
    else:
        return False

def has_4_same(hand):
    """
    Checks if hand contains 4 cards of the same value

    :param hand: list that contains the card names of a hand
    :return: boolean
    """

    values = return_values(hand)

    if values[0] == values[1] == values[2] == values[3]:
        return True
    elif values[1] == values[2] == values[3] == values[4]:
        return True
    else:
        return False

def has_3_same(hand):
    """
    Checks if hand contains 3 cards of the same value

    :param hand: list that contains the card names of a hand
    :return: boolean
    """

    values = return_values(hand)

    if values.count(values[0]) == 3:
        return True
    elif values.count(values[2]) == 3:
        return True
    elif values.count(values[4]) == 3:
        return True
    else:
        return False

def has_2_same(hand):
    """
    Checks if hand has any pairs and if so, how many

    :param hand: list that contains the card names of a hand
    :return: amount of pairs in a hand as integer
    """


    values = return_values(hand)

    if values.count(values[0]) == 2:
        if values.count(values[2]) == 2:
            return 2

    if values.count(values[0]) == 2:
        if values.count(values[4]) == 2:
            return 2

    if values.count(values[2]) == 2:
        if values.count(values[4]) == 2:
            return 2

    if values.count(values[0]) == 2:
        return 1
    if values.count(values[2]) == 2:
        return 1
    if values.count(values[4]) == 2:
        return 1
    else:
        return 0

def has_jacksorbetter(hand):
    """
    Checks if hand contains a pair of Jacks, Queens, Kings or Aces

    :param hand: list that contains the card names of a hand
    :return: boolean
    """

    values = return_values(hand)

    for value in values:
        if value >= 11:
            if values.count(value) == 2:
                return True
        elif value == 1:
            if values.count(value) == 2:
                return True
    return False


def check_win(hand):
    """
    Returns an key number that represents a certain poker hand

    :param hand: list that contains the card names of a hand
    :return: an integer indicating certain poker hand
    """


    # ROYAL FLUSH
    if is_flush(hand):
        values = return_values(hand)
        if values[0] == 1:
            if values[1] == 10:
                if values[2] == 11:
                    if values[3] == 12:
                        if values[4] == 13:
                            return 9

    # STRAIGHT FLUSH
    if is_straight(hand):
        if is_flush(hand):
            return 8

    # 4 OF A KIND
    if has_4_same(hand):
        return 7

    # FULL HOUSE
    if has_3_same(hand):
        if has_2_same(hand) == 1:
            return 6

    # FLUSH
    if is_flush(hand):
        return 5

    # STRAIGHT
    if is_straight(hand):
        return 4
    values = return_values(hand)
    if values[0] == 1:
        if values[1] == 10:
            if values[2] == 11:
                if values[3] == 12:
                    if values[4] == 13:
                        return 4

    # 3 OF A KIND
    if has_3_same(hand):
        return 3

    # 2 PAIR
    if has_2_same(hand) == 2:
        return 2

    # JACKS OR BETTER
    if has_jacksorbetter(hand):
        return 1

    # NO WIN
    else:
        return 0

def return_win_text(win):
    """
    Returns the name of a poker hand as a string

    :param win: key number that represents certain poker hand
    :return: name of the poker hand
    """

    if win == 9:
        return "ROYAL FLUSH"
    elif win == 8:
        return "STRAIGHT FLUSH"
    elif win == 7:
        return"4 OF A KIND"
    elif win == 6:
        return "FULL HOUSE"
    elif win == 5:
        return "FLUSH"
    elif win == 4:
        return "STRAIGHT"
    elif win == 3:
        return "3 OF A KIND"
    elif win == 2:
        return "2 PAIR"
    elif win == 1:
        return "JACKS OR BETTER"
    elif win == 0:
        pass



class VideoPoker:
    def __init__(self):
        self.__window = Tk()
        self.__window.title("Video Poker")
        self.__cardpics = []
        self.__cardstatuses = [0, 0, 0, 0, 0]
        # 0 = card is unlocked, 1 = card is locked
        self.__game_phase = 0
        # set game phase to 0
        self.__hand = ["n", "n", "n", "n", "n"]
        # contains cards that are in hand
        self.__winnings = 0
        # winnings of current hand
        self.__cash = 100
        # player's bankroll
        self.__bet = 1
        # bet


        for filename in CARDS:
            picture = PhotoImage(file=filename)
            self.__cardpics.append(picture)
        # save the card images to list

        self.__cardlabels = []
        for i in range(5):
            card_label = Label(self.__window)
            card_label.configure(image=self.__cardpics[52])
            card_label.grid(row=1, column=i)
            self.__cardlabels.append(card_label)
        # set all card labels to card back side

        self.__lockbuttons = []
        for i in range(5):
            lock_button = Button(self.__window, text="KEEP", height=2, width=12,
                                 background="yellow",
                                 command=lambda x=i: self.lock(x))

            lock_button.grid(row=2, column=i)
            self.__lockbuttons.append(lock_button)
        # create lock buttons

        dealbutton = Button(self.__window, text="DEAL", height=4, width=12,
                            background="green", command=self.deal)
        dealbutton.grid(row=3, column=0)
        # create deal button

        betbutton = Button(self.__window, text="BET", height=4, width=12,
                           background="dark blue", foreground="yellow",
                           command=self.bet)
        betbutton.grid(row=3, column=1)
        # create bet button

        self.__infolabel = Label(self.__window, text="CHOOSE YOUR BET",
                                 font=("", 20), background="green",
                                 foreground="white")
        self.__infolabel.grid(row=0, column=0, rowspan=1, columnspan=3)
        # info label shows game instructions and names winning hands

        self.__betlabel = Label(self.__window, text="BET\n"+str(self.__bet),
                                font=("", 20))
        self.__betlabel.grid(row=3, column=2)
        # shows current bet

        self.__winlabel = Label(self.__window, text="WIN\n"+str(self.__winnings),
                                font=("", 20))
        self.__winlabel.grid(row=3, column=3)
        # shows current winnings

        self.__cashlabel = Label(self.__window, text="CASH\n"+str(self.__cash),
                                 font=("", 20))
        self.__cashlabel.grid(row=3, column=4)
        # shows the amount of money player has

        paytable = Label(self.__window, text="{:<20}\n{:<20}\n{:<20}\n{:<20}"
                                             "\n{:<20}\n{:<20}\n{:<20}\n{:<20}"
                                             "\n{:<20}\n{:<20}"
                                             .format("PAYTABLE", "Royal Flush",
                                             "Straight Flush", "4 of a Kind",
                                             "Full House", "Flush", "Sraight",
                                             "3 of a Kind", "2 Pair",
                                             "Jacks or Better")
                                             , font=("", 11))



        paytable.grid(row=0, column=3)
        # list of possible winning combinations

        self.__paytable_values = Label(self.__window, text="\n{:<30}\n{:<30}\n{:<30}\n"
                                                    "{:<30}\n{:<30}\n{:<30}\n"
                                                    "{:<30}\n{:<30}\n{:<30}"
                                                    .format(250*self.__bet,
                                                            50*self.__bet,
                                                            25*self.__bet,
                                                            9*self.__bet,
                                                            6*self.__bet,
                                                            4 * self.__bet,
                                                            3 * self.__bet,
                                                            2 * self.__bet,
                                                            1 * self.__bet)
                                                    , font=("", 11))

        self.__paytable_values.grid(row=0, column=4)
        # list of possible wins with current bet

    def reset_all(self):
        # resets all in-game variables to zero/none
        self.__cardstatuses = [0, 0, 0, 0, 0]
        self.__hand = ["n", "n", "n", "n", "n"]
        self.__winlabel.configure(text="WIN\n0")
        self.__winnings = 0
        self.__infolabel.configure(text="")
        self.__game_phase = 0

        for lockbutton in self.__lockbuttons:
            lockbutton.configure(background="yellow", foreground="black")

        for card_label in self.__cardlabels:
            card_label.configure(image=self.__cardpics[52])

    def deal_new_hand(self):
        # deals a completely new hand at the start of a game round
        self.reset_all()
        card_indexes = []

        for i in range(5):
            while len(card_indexes) != 5:
                index = randint(0, 51)
                if index not in card_indexes:
                    card_indexes.append(index)

        for i in range(5):
            self.__hand[i] = CARD_NAMES[card_indexes[i]]
            self.__cardlabels[i].configure(image=self.__cardpics[card_indexes[i]])

        self.__infolabel.configure(text="CHOOSE CARDS TO KEEP")

    def deal_unlocked(self):
        # deals new cards to card slots that are unlocked in the second phase
        # of the game round
        for i in range(5):
            if self.__cardstatuses[i] == 0:
                index = randint(0, 51)
                while CARD_NAMES[index] in self.__hand:
                    index = randint(0, 51)
                self.__cardlabels[i].configure(image=self.__cardpics[index])
                self.__hand[i] = CARD_NAMES[index]

            elif self.__cardstatuses[i] == 1:
                pass

    def deal(self):
        # deal button command
        if self.__game_phase == 0:
            # start of a new game round
            if self.__cash == 0:
                return
                # the game can't be played if player has no money left

            elif self.__bet > self.__cash:
                self.__infolabel.configure(text="NOT ENOUGH MONEY")
                return
                # prevents betting more than the available cash allows

            else:
                self.__cash -= self.__bet
                self.__cashlabel.configure(text="CASH\n"+str(self.__cash))
                # substract bet from player's cash

            self.deal_new_hand()
            self.__game_phase = 1

        elif self.__game_phase == 1:
            # the changing of cards phase of a game round

            self.deal_unlocked()
            win = check_win(self.__hand)
            if win != 0:
                self.__winnings = WIN_FACTORS[win-1] * self.__bet
                self.__winlabel.configure(text="WIN\n"+str(self.__winnings))
                self.__infolabel.configure(text=return_win_text(win)+"!")
            else:
                self.__infolabel.configure(text="YOU LOSE")

            self.__game_phase = 2

        elif self.__game_phase == 2:
            # end of a game round

            self.add_winnings()
            self.reset_all()
            self.__game_phase = 0

            if self.__cash == 0:
                self.__infolabel.configure(text="YOU DON'T HAVE ANY CASH\n"
                                                 "GAME ENDS")

            else:
                self.__infolabel.configure(text="CHOOSE YOUR BET")

    def lock(self, index):
        # locks the card above the lock button

        lockbutton = self.__lockbuttons[index]
        if self.__game_phase == 1:
            if self.__cardstatuses[index] == 0:
                lockbutton.configure(background="red", foreground="white")
                self.__cardstatuses[index] = 1

            elif self.__cardstatuses[index] == 1:
                lockbutton.configure(background="yellow", foreground="black")
                self.__cardstatuses[index] = 0
        else:
            pass

    def add_winnings(self):
        # adds current winnings to players bankroll
        self.__cash += self.__winnings
        self.__cashlabel.configure(text="CASH\n"+str(self.__cash))

    def bet(self):
        # changes the bet, clicking the button raises the bet by 1
        # except to 10 if current bet is 5
        # and to 1 if current bet is 10
        if self.__game_phase == 0:
            if self.__bet < 5:
                self.__bet += 1
                self.__betlabel.configure(text="BET\n"+str(self.__bet))

            elif self.__bet == 5:
                self.__bet = 10
                self.__betlabel.configure(text="BET\n" + str(self.__bet))

            else:
                self.__bet = 1
                self.__betlabel.configure(text="BET\n"+str(self.__bet))

        self.__paytable_values.configure(text="\n{:<30}\n{:<30}\n{:<30}\n"
                                                    "{:<30}\n{:<30}\n{:<30}\n"
                                                    "{:<30}\n{:<30}\n{:<30}"
                                                    .format(250*self.__bet,
                                                            50*self.__bet,
                                                            25*self.__bet,
                                                            9*self.__bet,
                                                            6*self.__bet,
                                                            4 * self.__bet,
                                                            3 * self.__bet,
                                                            2 * self.__bet,
                                                            1 * self.__bet))

    def start(self):
        self.__window.mainloop()


def main():
    ui = VideoPoker()
    ui.start()


main()
