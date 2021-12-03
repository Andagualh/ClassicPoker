import random
import itertools

from enum import Enum, auto
from collections import Counter

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
        return f"{self.value.name} of {self.suit.name}"
    
    def __lt__(self, other):
        return self.value.value < other.value.value
    def __gt__(self, other):
        return self.value.value > other.value.value
    def __eq__(self, other):
        return self.value == other.value and self.suit == other.suit

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
                return True
            else:
                return False
        
    
    #Check when a Flush is Straight
    def checkStraightFlush(hand):
        return poker.checkStraight(hand)
    
    #Check when hand is Four of a Kind
    def checkFourOfAKind(count):
        return count == (4,1)
    
    #Check when hand is Full House
    def checkFullHouse(count):
        return count == (3,2)
    
    #Check when hand is Two Pairs
    def checkTwoPairs(count):
        return count == (2,2)
    
    #Check when hand is Three of a Kind
    def checkThreeOfAKind(count):
        return count == (3,1)
    
    #Check when hand is Pair
    def checkPair(count):
        return count == (2,1)

    def checkHighCard(hand):
        highest = hand.cards[0]
        for card in hand.cards:
            if(highest < card):
                highest = card
        return highest.value.value

    #Counts how common a value is in a hand
    def countCards(hand):
        handvalues = []
        for cardvalues in hand.cards:
            handvalues.append(cardvalues.value.value)
        counting_cards = Counter(handvalues)
        #Count Structure: (Number of Repeated Values, Amount of Sets with repeated values)
        most_common_values, count = zip(*counting_cards.most_common(2))
        return count
           
    #Controls the value of all the hands in play in Classic Poker
    #Hand values:
    #Royal Flush - 1000
    #Straight Flush - 900 + highest card
    #Four of a Kind - 800 
    #Full House - 700 
    #Flush - 600 
    #Straight - 500 + highest card
    #Three of a Kind - 400 
    #Two Pair - 300 
    #Pair - 200 
    #High Card - From 2 to 13 (ACE), check Value enum values for reference
    def checkHandValue(hand):
        value = 0
        for card in hand.cards:
            value += card.value.value
        #Checking if hand has a flush
        if(poker.checkSameSuit(hand)):
            #Royal Flush
            if(poker.checkRoyalFlush(hand)):
                return 1000
            #Straight Flush
            elif(poker.checkStraightFlush(hand)):
                return 900 + poker.checkHighCard(hand)
            #Regular Flush
            else:
                return 600
        #Other hands
        else:
            #Counting if hand is repeated
            #Most of these checks could be added here, but this allows for modularity
            count = poker.countCards(hand)
            #Four of a Kind
            if(poker.checkFourOfAKind(count)):
                return 800
            #Full House    
            elif(poker.checkFullHouse(count)):
                return 700
            #Straight + 
            elif(poker.checkStraight(hand)):
                return 500 + poker.checkHighCard(hand)
            #Three of a Kind
            elif(poker.checkThreeOfAKind(count)):
                return 400
            #Two Pairs
            elif(poker.checkTwoPairs(count)):
                return 300
            #Single Pair
            elif(poker.checkPair(count)):
                return 200
            else:
                return poker.checkHighCard(hand)
            

    def dealer(np):
        #Classic Poker Dealing method
        #It executes every played round
        #Every player hand array
        hands = []
        #Deck Creation
        deck = Deck()
        random.shuffle(deck.cards)
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

    #Round Resolver
    #To prevent Tests from requesting additional rounds an extra parameter is thrown in
    def roundResolver(hands, isTest):
        storedHandValues = []
        tie = False
        for hand in hands:
            storedHandValues.append(poker.checkHandValue(hand))
        
        highestValue = 0
        winner = 0
        for i in range (len(hands)):
            #A hand just overtook one as the winner by its bare value
            if(storedHandValues[i] > highestValue):
                highestHand = hands[i]
                highestValue = storedHandValues[i]
                winner = i
                tie = False
            elif(storedHandValues[i] == highestValue):
                oneValue = poker.mostCommonOccurrence(highestHand)
                twoValue = poker.mostCommonOccurrence(hands[i])
                if(oneValue < twoValue):
                    highestHand = hands[i]
                    highestValue = storedHandValues[i]
                    winner = i
                    tie = False
                elif(oneValue == twoValue):
                    tiedwinner = i
                    tiedhand = hands[i]
                    tie = True
        if(tie == False):
            print("The Player Number " + str(winner + 1) + " with the following hand:\n" + str(highestHand) + "\nis the winner of the round with " + poker.handValueToString(storedHandValues[winner]))
        elif(tie == True):
            print("It's a tie between Player Number " + str(tiedwinner+1) + " and Player Number " + str(winner+1) + " with both having " + poker.handValueToString(highestValue))
            print("Player " + str(tiedwinner+1) + " hand: \n" + str(tiedhand))
            print("Player " + str(winner + i) + " hand: \n" + str(highestHand))
        
        if(isTest == False):
            poker.rounds(len(storedHandValues))

    #Find which are the repeated values in a hand to determine Pair, Three of a Kind and Four of a Kind values
    def mostCommonOccurrence(hand):
        handvalues = []
        setValue = 0
        for cardvalues in hand.cards:
            handvalues.append(cardvalues.value.value)
        counting_cards = Counter(handvalues)
        most_common_values = counting_cards.most_common(2)
        print(most_common_values)
        for set in most_common_values:
            if(set[1] > 1):
                setValue += set[0]
        return setValue

    #HandValue to String Auxiliary Function
    def handValueToString(handValue):
        #check straights
        if(handValue in range(900,999)):
            handValue = 900
        elif(handValue in range(500,599)):
            handValue = 500
        
        possibleHands = {
        1000 : "a Royal Flush",
        900 : "a Straight Flush",
        800 : "a Four of a Kind",
        700 : "a Full House",
        600 : "a Flush",
        500 : "a Straight",
        400 : "a Three of a Kind",
        300 : "a Two Pair",
        200 : "a Pair",
        13 : "an Ace as the highest card",
        12 : "a King as the highest card",
        11 : "a Queen as the highest card",
        10 : "a Jack as the highest card",
        9 : "a Ten as the highest card",
        8 : "a Nine as the highest card",
        7 : "a Eight as the highest card",
        6 : "a Seven as the highest card",
        5 : "a Six as the highest card",
        4 : "a Five as the highest card",
        3 : "a Four as the highest card",
        2 : "a Three as the highest card",
        1 : "a Two as the highest card"
        }                                       
        return possibleHands[handValue]

    #Round Controller
    def rounds(np):
        quit = 0
        while(quit != 'y' and quit != 'n'):
            quit = input("Start next round? \n 'y' \n 'n'")
            if(quit.isalnum() and quit == 'n'):
                print("See you soon.")
                break
            elif(quit.isalnum() and quit == 'y'):
                print("Lets go: ")
                hands = poker.dealer(np)
                poker.roundResolver(hands, False)
            else:
                print("Please, type 'y' or 'n' only")


    #Player count input
    def start():
        np = 0
        while ((int(np) <= 1) or (int(np) > 10)):  
            np = input("Please, input the number of players that will partake in the game. Type 'quit' to end the execution.\n Input: ")
            if(np.isnumeric()):
                if((int(np) == 0)) or (int(np) < 0):
                    print("The number of players cannot be 0 or negative.")
                elif(int(np) == 1):
                    print("Company is okay, solitude is bliss. You have the winning hand in every round. \n Next time bring more friends.")
                elif(int(np) > 10):
                    print("There isn't enough cards for this many players.")
                elif(int(np)>1 and int(np)<=10):
                    poker.rounds(np)
                    break
                else:
                    print("Please, only introduce integers or 'quit'.")
            elif(np.strip().isalnum()):
                if(str(np) == 'quit'):
                    print("See you soon")
                    break
                else:
                    print("Please type an integer or 'quit'.")
                    np = 0
            else:
                print("Please type an integer or 'quit'.")
                np = 0

class testCases():
    def royalFlushHand():
        print("\n1 - This is a royal flush test")
        hand = Hand() 
        hand.cards.append(Card(Suit.DIAMOND,Value.ACE))
        hand.cards.append(Card(Suit.DIAMOND,Value.JACK))
        hand.cards.append(Card(Suit.DIAMOND,Value.TEN)) 
        hand.cards.append(Card(Suit.DIAMOND,Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND,Value.KING))
        res = poker.checkHandValue(hand)
        #print("1 - HAND VALUE: " + poker.handValueToString(res))
        assert(res == 1000)

    def royalStraightFlushHand():
        print("\n2 - This is a straight flush test")
        hand = Hand() 
        hand.cards.append(Card(Suit.CLUB,Value.TWO))
        hand.cards.append(Card(Suit.CLUB,Value.THREE))
        hand.cards.append(Card(Suit.CLUB,Value.FOUR)) 
        hand.cards.append(Card(Suit.CLUB,Value.FIVE))
        hand.cards.append(Card(Suit.CLUB,Value.SIX))
        res = poker.checkHandValue(hand)
        print("2 - HAND VALUE: " + poker.handValueToString(res))
        assert(res == 905)
    
    def lowValueAce():
        print("\n3 - This tests the only case in which the ACE counts as a 1 value \nThis results in a Straight Flush")
        hand = Hand() 
        hand.cards.append(Card(Suit.CLUB,Value.ACE))
        hand.cards.append(Card(Suit.CLUB,Value.THREE))
        hand.cards.append(Card(Suit.CLUB,Value.FOUR)) 
        hand.cards.append(Card(Suit.CLUB,Value.FIVE))
        hand.cards.append(Card(Suit.CLUB,Value.TWO))
        res = poker.checkHandValue(hand)
        print("3 - HAND VALUE: " + poker.handValueToString(res))
        assert(res == 913)
    
    def regularStraight():
        print("\n4 - This is a straight test")
        hand = Hand() 
        hand.cards.append(Card(Suit.DIAMOND,Value.TWO))
        hand.cards.append(Card(Suit.CLUB,Value.THREE))
        hand.cards.append(Card(Suit.CLUB,Value.FOUR)) 
        hand.cards.append(Card(Suit.CLUB,Value.FIVE))
        hand.cards.append(Card(Suit.CLUB,Value.SIX))
        res = poker.checkHandValue(hand)
        print("4 - HAND VALUE: " + poker.handValueToString(res))
        assert(res == 505)
    
    def pairHand():
        print("\n5 - Tests a Hand with a Pair")
        hand = Hand()
        hand.cards.append(Card(Suit.CLUB, Value.ACE))
        hand.cards.append(Card(Suit.DIAMOND, Value.ACE))
        hand.cards.append(Card(Suit.DIAMOND, Value.TWO))
        hand.cards.append(Card(Suit.SPADE, Value.FIVE))
        hand.cards.append(Card(Suit.HEART, Value.TEN))
        res = poker.checkHandValue(hand)
        print("5 - HAND VALUE: " + poker.handValueToString(res))
        assert(res == 200)

    def threeOfAKind():
        print("\n6 - Tests a Hand with a Three of a Kind")
        hand = Hand()
        hand.cards.append(Card(Suit.CLUB, Value.ACE))
        hand.cards.append(Card(Suit.DIAMOND, Value.ACE))
        hand.cards.append(Card(Suit.DIAMOND, Value.TWO))
        hand.cards.append(Card(Suit.SPADE, Value.ACE))
        hand.cards.append(Card(Suit.HEART, Value.TEN))
        res = poker.checkHandValue(hand)
        print("6 - HAND VALUE: " + poker.handValueToString(res))
        assert(res == 400)

    def highCard():
        print("\n7 - Tests a Hand with only a high card\n Highest Card is QUEEN")
        hand = Hand()
        hand.cards.append(Card(Suit.CLUB, Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND, Value.FIVE))
        hand.cards.append(Card(Suit.DIAMOND, Value.TWO))
        hand.cards.append(Card(Suit.SPADE, Value.SIX))
        hand.cards.append(Card(Suit.HEART, Value.TEN))
        res = poker.checkHandValue(hand)
        print("7 - HAND VALUE: " + poker.handValueToString(res))
        assert(res == 11)
    
    def mostCommonOcurrenceTest():
        print("\n8 - Tests a Hand to find its most common value")
        hand = Hand()
        hand.cards.append(Card(Suit.CLUB, Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND, Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND, Value.TWO))
        hand.cards.append(Card(Suit.SPADE, Value.TWO))
        hand.cards.append(Card(Suit.HEART, Value.TWO))
        res = poker.mostCommonOccurrence(hand)
        print("8 - MOST COMMON OCURRENCE: " + str(res))
    
    #Suits will be ignored in RoundResolver-like Tests
    def testRoundResolver1():
        print("9 - Two Full House hands tiebreaking test")
        hand = Hand()
        hand.cards.append(Card(Suit.CLUB, Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND, Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND, Value.THREE))
        hand.cards.append(Card(Suit.SPADE, Value.THREE))
        hand.cards.append(Card(Suit.HEART, Value.THREE))

        hand2 = Hand()
        hand2.cards.append(Card(Suit.CLUB, Value.QUEEN))
        hand2.cards.append(Card(Suit.DIAMOND, Value.QUEEN))
        hand2.cards.append(Card(Suit.DIAMOND, Value.TWO))
        hand2.cards.append(Card(Suit.SPADE, Value.TWO))
        hand2.cards.append(Card(Suit.HEART, Value.TWO))

        hands = []
        hands.append(hand)
        hands.append(hand2)
        poker.roundResolver(hands, True)

    def testRoundResolver2():
        print("10 - Two Pair hands tiebreaking test")
        hand = Hand()
        hand.cards.append(Card(Suit.CLUB, Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND, Value.QUEEN))
        hand.cards.append(Card(Suit.DIAMOND, Value.THREE))
        hand.cards.append(Card(Suit.SPADE, Value.THREE))
        hand.cards.append(Card(Suit.HEART, Value.ACE))

        hand2 = Hand()
        hand2.cards.append(Card(Suit.CLUB, Value.QUEEN))
        hand2.cards.append(Card(Suit.DIAMOND, Value.QUEEN))
        hand2.cards.append(Card(Suit.DIAMOND, Value.THREE))
        hand2.cards.append(Card(Suit.SPADE, Value.THREE))
        hand2.cards.append(Card(Suit.HEART, Value.ACE))

        hands = []
        hands.append(hand)
        hands.append(hand2)
        poker.roundResolver(hands, True)
        

        

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
            testCases.pairHand()
            testCases.regularStraight()
            testCases.threeOfAKind()
            testCases.highCard()
            testCases.mostCommonOcurrenceTest()
            testCases.testRoundResolver1()
            testCases.testRoundResolver2()
            print("\n<Testing Done>")
            break
    else:
        print("\n Please, choose a valid option from the menu")



        
    

