import random
import itertools

from enum import Enum, auto

class Suit(Enum):
    CLUB = auto()
    DIAMOND = auto()
    HEART = auto()
    SPADE = auto()

class Value(Enum):
    TWO =  1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12
    ACE = 13

#Card Object
class Card:
    def __init__(self, suit:Suit, value:Value):
        self.suit = suit
        self.value = value
    
    def __repr__(self):
        return f"{self.value} of {self.suit}"
    
    def __lt__(self, other):
        return self.value.value < other.value.value
    def __gt__(self, other):
        return self.value.value > other.value.value
    def __eq__(self, other):
        return self.value == other.value

#Deck Object    
class Deck:
    def __init__(self):
        self.cards = [Card(s,v) for s in Suit for v in Value]
    
    def __repr__(self):
        return "".join([f"{c}\n" for c in self.cards])

#Hand Object
class Hand:
    def __init__(self):
        self.cards = []
    
    def __repr__(self):
        return "".join([f"<{c}>\n" for c in self.cards])

class poker():
    
    #Sorts a hand by the value of its cards
    def sortHand(hand):
        hand.cards.sort()
        return hand

    #Flush Check
    def checkSameSuit(hand):
        res = False
        firstSuit = hand.cards[0].suit
        for card in hand.cards:
            if(card.suit == firstSuit):
                res = True
            else:
                res = False
                break
        return res
    
    #Straight Check
    def checkStraight(hand):
        res = False
        hand.cards.sort()
        #Due to the unique nature of an ACE counting as a 1 in this case it has to be hardcoded
        #The following special condition only works in Classic Poker if we wanted to add shared cards we would need a special condition
        if(hand.cards[4].value == Value.ACE and hand.cards[0].value == Value.TWO and hand.cards[1].value == Value.THREE and hand.cards[2].value == Value.FOUR and hand.cards[3].value == Value.FIVE):
            return True
        for i in range (len(hand.cards) - 1):
            if(hand.cards[i].value.value == hand.cards[i+1].value.value - 1):
                res = True
            else:
                res = False
                break
        return res

    #Check if Flush is Royal
    def checkRoyalFlush(hand):
        res = False
        hand = poker.sortHand(hand)
        if(hand.cards[0].value == Value.TEN):
            if(poker.checkStraight(hand)):
                res = True
                return res
            else:
                res = False
                return res
        
    
    #Check when a Flush is Straight
    def checkStraightFlush(hand):
        res = False
        if(poker.checkStraight(hand)):
            res = True
        else:
            res = False
        return res
    
    #Check when hand is Four of a Kind
    #TODO
    def checkFourOfAKind(hand):
        res = False
        kind = 0
        for card in hand.cards:
            card.value.value
            
    #Controls the value of all the hands in play in Classic Poker
    #Hand values:
    #Royal Flush - 100
    #Straight Flush - 90
    #Four of a Kind - 80
    #Full House - 70
    #Flush - 60
    #Straight - 50
    #Three of a Kind - 40
    #Two Pair - 30
    #Pair - 20
    #High Card - From 2 to 13, check Value enum values for reference
    def checkHandValue(hand):
        value = 0
        #Checking if hand has a flush
        if(poker.checkSameSuit(hand)):
            #Royal Flush
            if(poker.checkRoyalFlush(hand)):
                value = 100
                return value
            #Straight Flush
            elif(poker.checkStraightFlush(hand)):
                value = 90
                return value
            #Regular Flush
            else:
                value = 60
                return value
        #Other hands
        else:
            #Four of a Kind TODO
            poker.checkFourOfAKind(hand)
            poker.checkFullHouse(hand)
            if(poker.checkStraight(hand)):
                value = 50
                return value
            poker.checkThreeOfAKind(hand)
            poker.checkTwoPairs(hand)
            poker.checkPair(hand)
            #
            poker.checkHighCard(hand)
            

    def dealer(np):
        #Classic Poker Dealing method
        #It executes every played round
        #Every player hand array
        hands = []
        #Deck Creation
        deck = Deck()
        random.shuffle(deck.cards)
        print(deck)
        print("Deck Card Count: " + str(len(deck.cards)))
        #Dealing
        for i in range(int(np)):
            hand = Hand()
            #This greatly changes for other poker variants
            #If we wanted to implement Texas Hold'Em, we would need to set a hand of 2 unique cards per player + 5 shared cards in each player hand
            for c in range(5):
                card = random.choice(deck.cards)
                deck.cards.remove(card)
                hand.cards.append(card)
            hands.append(hand)
        return hands

    #Round Controller
    def rounds(np):
        quit = 0
        while(quit != 'y' and quit != 'n'):
            quit = input("Continue? \n 'y' \n 'n'")
            if(quit.isalnum() and quit == 'n'):
                print("See you soon.")
                break
            elif(quit.isalnum() and quit == 'y'):
                print("Lets go: ")
                hands = poker.dealer(np)
                print(hands)
                for hand in hands:
                    poker.checkHandValue(hand)
            else:
                print("Please, type 'y' or 'n' only")


    #Player count input
    def start():
        np = 0
        while ((int(np) <= 1) or (int(np) > 10)):  
            np = input("Please, input the number of players that will partake in the game. Type 'quit' to end the execution.")
            if(np.strip().isdecimal()):
                if((int(np) == 0)) or (int(np) < 0):
                    print("The number of players cannot be 0 or negative.")
                elif(int(np) == 1):
                    print("Company is okay, solitude is bliss. You have the winning hand in every round. \n Next time bring more friends.")
                elif(int(np) > 10):
                    print("There isn't enough cards for this many players.")
                elif(int(np)>1 and int(np)<10):
                    poker.rounds(np)
                    break
                else:
                    print("Please, only introduce numbers or 'quit'.")
            elif(np.strip().isalnum()):
                if(str(np) == 'quit'):
                    print("See you soon")
                    break
                else:
                    print("Please type a number or 'quit'")
                    np = 0

class testCases():
    def royalFlushHand():
        print("This is a royal flush test")
        hand = Hand() 
        hand.cards.append(Card(Suit.DIAMOND,Value.ACE))
        hand.cards.append(Card(Suit.DIAMOND,Value.JACK))
        hand.cards.append(Card(Suit.DIAMOND,Value.TEN)) 
        hand.cards.append(Card(Suit.DIAMOND,Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND,Value.KING))
        res = poker.checkHandValue(hand)
        print("HAND VALUE: " + str(res))
        assert(res == 100)

    def royalStraightFlushHand():
        print("This is a straight flush test")
        hand = Hand() 
        hand.cards.append(Card(Suit.CLUB,Value.TWO))
        hand.cards.append(Card(Suit.CLUB,Value.THREE))
        hand.cards.append(Card(Suit.CLUB,Value.FOUR)) 
        hand.cards.append(Card(Suit.CLUB,Value.FIVE))
        hand.cards.append(Card(Suit.CLUB,Value.SIX))
        res = poker.checkHandValue(hand)
        print("HAND VALUE: " + str(res))
        assert(res == 90)
    
    def lowValueAce():
        print("This tests the only case in which the ACE counts as a 1 value \nThis results in a Straight Flush")
        hand = Hand() 
        hand.cards.append(Card(Suit.CLUB,Value.ACE))
        hand.cards.append(Card(Suit.CLUB,Value.THREE))
        hand.cards.append(Card(Suit.CLUB,Value.FOUR)) 
        hand.cards.append(Card(Suit.CLUB,Value.FIVE))
        hand.cards.append(Card(Suit.CLUB,Value.TWO))
        res = poker.checkHandValue(hand)
        print("HAND VALUE: " + str(res))
        assert(res == 90)

#Main
option = 0
while(option != 1 and option != 2):
    option = input("\n Choose a function: \n 1. Game Start \n 2. Test Cases \nInput: ")
    if(option.isnumeric()):
        if(int(option) == 1):
            poker.start()
            break
        elif(int(option) == 2):
            print("\n<Test Start>\n")
            testCases.royalFlushHand()
            testCases.royalStraightFlushHand()
            testCases.lowValueAce()
            print("\n<Testing Done>")
            break
    else:
        print("\n Please, choose a valid option from the menu")



        
    

