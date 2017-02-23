"""
Deal or No Deal

A Python script simulating the popular game show, Deal or No Deal.
"""

import random, sys

# Global variables
briefcaseStack = {}
briefcaseAmount = []
expectedValueSmall = []
expectedValueBig = []
briefcaseNumber = 0
briefcaseValue = 0
briefcaseJackpot = 0

class DealNoDeal(object):
    def __init__(self):
        print(end='\n\n')
        print('*' * 30, end='\n\n')
        print(('Welcome to Deal or No Deal!').upper(), end='\n\n')
        print('*' * 30, end='\n\n')

    # Method that populates the briefcases with an random amount from 125 to 1,000,000
    def generateBriefcaseContents(self):
        global briefcaseStack
        global briefcaseAmount
        global briefcaseValue
        global briefcaseJackpot

        # First delete the list contents from the previous game session to prevent stacking
        briefcaseStack.clear()
        briefcase = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
        briefcaseContent = [0, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000, 25000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 750000, 1000000]
        briefcaseAmount = sorted(briefcaseContent)
        # Randomly shuffles the briefcase list everytime the game is played
        random.shuffle(briefcaseContent)
        briefcaseStack = dict(zip(briefcase, briefcaseContent))
        # Store the winning briefcase in a global variable
        for k, v in briefcaseStack.items():
            if v == 1000000:
                briefcaseJackpot = k
            else: 
                continue
        return briefcaseStack
        
    # Method that prompts player to select a briefcase
    def choosePlayerBriefcase(self, casesContent):
        global briefcaseNumber
        global briefcaseStack
        global briefcaseValue
        self.casesContent = casesContent

        while True:
            try:
                choice = int(input('Select your briefcase (1-26): ')) - 1
                # Checking the inputted number is within the range of 26 briefcases
                if choice >= 0 and choice <= 25:
                    print('You\'ve chosen briefcase no. {0}'.format(choice + 1), end='\n')
                    print('Let\'s start the first round', end='\n')
                    briefcaseNumber = choice + 1
                    briefcaseValue = briefcaseStack[briefcaseNumber]
                    # Delete the chosen briefcase in the list of all the briefcases
                    del briefcaseStack[briefcaseNumber]
                    return briefcaseNumber
                else:
                    print('ERROR! Out of range', end='\n\n')
                    continue
            except ValueError:
                print('ERROR! Wrong input', end='\n\n')
                continue
            else: 
                break

    # Method that counts the total number of briefcases remaining in each round
    def briefcaseCount(self):
        global briefcaseStack
        return len(briefcaseStack)

    # Method that simulates each round of the game. Accepts an integer representing the number of suitcases the player has to open for each round.
    def simulateRound(self, gameRound, openCase, selectedCase):
        global briefcaseStack
        global briefcaseNumber
        global briefcaseValue
        global briefcaseAmount
        self.gameRound = gameRound
        self.openCase = openCase
        self.selectedCase = selectedCase
        choice = 0
        openPrompt = ''

        if self.gameRound == 10:
            print(end='\n')
            print('-' * 45, end='\n\n')
            print('Final Round: Let\'s open your briefcase', end='\n\n')
            print('-' * 45, end='\n\n')
            print('Amounts left: ', end='\n\n')
            for x in briefcaseAmount:
                print(x, end=' ')
            print(end='\n\n')

            # Prompt player to open his/her briefcase
            while not openPrompt == 'y' or openPrompt == 'n':
                openPrompt = input('Are you ready check out your briefcase (y/n)? ').lower()
                if openPrompt == 'y':
                    if briefcaseValue == 1000000:
                        print(end='\n\n')
                        print('Congratulations! Your briefcase no. {0} has the jackpot prize of PHP {1}! Thanks for playing.'.format(briefcaseNumber, briefcaseValue), end='\n')
                    else:
                        print(end='\n')
                        print('Congratulations! Your briefcase no. {0} has PHP {1}! Thanks for playing.'.format(briefcaseNumber, briefcaseValue), end='\n')
                else:
                    continue
        else:
            print(end='\n')
            print('-' * 45, end='\n\n')
            print(('Round {0}: You have {1} suitcase/s to open'.format(self.gameRound, self.openCase)), end='\n\n')
            print('-' * 45, end='\n\n')

            while True:
                try:
                    for y in range(openCase, 0, -1):
                        print('Amounts left: ', end='\n\n')
                        # Display a loop of amounts available
                        for x in briefcaseAmount:
                            print(x, end=' ')
                        print(end='\n\n')

                        # Display remaining briefcases
                        print('Remaining briefcases:', end='\n\n')
                        for k, v in briefcaseStack.items():
                            print(k, end=' ')
                        print(end='\n\n')
                        print('Cases to open for this round: {0}'.format(y), end='\n\n')
                        
                        choice = int(input('Select briefcase to open: '))

                        print('You\'ve chosen briefcase no. {0}'.format(choice), end='\n')
                        print('Briefcase no. {0} contains PHP {1}'.format(choice, briefcaseStack.get(choice)), end='\n\n')
                        print('+' * 45, end='\n\n')

                        # Delete amount based from the selected briefcase in list 
                        for a in briefcaseAmount:
                            if a == briefcaseStack.get(choice):
                                briefcaseAmount.remove(a)
                        # Delete the selected briefcase in the list
                        del briefcaseStack[choice]
                except ValueError:
                    print('ERROR! Wrong input', end='\n\n')
                    continue
                else: 
                    break

    # Method that calculates the expected value of smaller amounts (maximum of 75,000)
    def expectedValueSmall(self):
        global briefcaseStack
        global expectedValueSmall

        for k, v in briefcaseStack.items():
            if v < 75000:
                expectedValueSmall.append(v)
        result = int(sum(expectedValueSmall) / len(expectedValueSmall))
        return result

    # Method that calculates the expected value of bigger amounts (starting from 100,000 to the maximum amount of 1,000,000)
    def expectedValueBig(self):
        global briefcaseStack
        global expectedValueBig

        for k, v in briefcaseStack.items():
            if v > 75000:
                expectedValueBig.append(v)
        result = int(sum(expectedValueBig) / len(expectedValueBig))
        return result

    # Method that calls the "banker" after each round. The "banker" will offer the player an initial amount which will convince the player to end the game and go home with the amount offered. If the player decides to continue playing, the game would continue and this method terminates. The algorithm for the calculation of the amount can be found here: http://www.davegentile.com/stuff/Deal_or_no_deal.html
    def bankerOffer(self, caseCount, small, big):
        global briefcaseNumber
        global briefcaseValue
        global briefcaseJackpot
        self.caseCount = caseCount
        self.small = small
        self.big = big
        response = ''
        askPlayer = ''
        offer = 0

        # If 20 briefcases are left unopened
        if self.caseCount == 19:
            bigValue = float(0.154 * (random.uniform(0.2, 0.35) * self.big)) 
            smallValue = float(1.4 * (random.uniform(0.2, 0.35) * self.small))
        # If 15 briefcases are left unopened
        elif self.caseCount == 14:
            bigValue = float(0.216 * (random.uniform(0.2, 0.35) * self.big))
            smallValue = float(1.35 * (random.uniform(0.2, 0.35) * self.small))
        # If 11 briefcases are left unopened
        elif self.caseCount == 10:
            bigValue = float(0.3003 * (random.uniform(0.2, 0.35) * self.big))
            smallValue = float(1.43 * (random.uniform(0.2, 0.35) * self.small))
        # If 8 briefcases are left unopened
        elif self.caseCount == 7:
            bigValue = float(0.3536 * (random.uniform(0.2, 0.35) * self.big))
            smallValue = float(1.36 * (random.uniform(0.2, 0.35) * self.small))
        # If 6 briefcases are left unopened
        elif self.caseCount == 5:
            bigValue = float(0.372 * (random.uniform(0.2, 0.35) * self.big))
            smallValue = float(1.2 * (random.uniform(0.2, 0.35) * self.small))
        # If 5 briefcases are left unopened
        elif self.caseCount == 4:
            bigValue = float(0.5125 * (random.uniform(0.3, 0.45) * self.big))
            smallValue = float(1.25 * (random.uniform(0.3, 0.45) * self.small))
        # If 4 briefcases are left unopened
        elif self.caseCount == 3:
            bigValue = float(0.6732 * (random.uniform(0.4, 0.55) * self.big))
            smallValue = float(1.32 * (random.uniform(0.4, 0.55) * self.small))
        # If 3 briefcases are left unopened
        elif self.caseCount == 2:
            bigValue = float(0.915 * (random.uniform(0.5, 0.65) * self.big))
            smallValue = float(1.5 * (random.uniform(0.5, 0.65) * self.small))
        # If 2 briefcases are left unopened
        else:
            bigValue = float(0.71 * (random.uniform(0.6, 0.75) * self.big))
            smallValue = float(1 * (random.uniform(0.6, 0.75) * self.small))

        # Calculate the banker's final offer
        offer = round(float(bigValue) + float(smallValue))
        # Declare end of round
        print('End of Round.', end='\n\n')

        while not askPlayer == 'y' or askPlayer == 'n':
            askPlayer = input('Banker\'s offer received. Do you want to know how much did he offer (y/n)? ').lower()
            if askPlayer == 'y':
                print(end='\n')
                print('~' * 45, end='\n\n')
                print('Banker\'s initial offer is worth PHP {0}'.format(offer), end='\n\n')
                print('~' * 45, end='\n\n')

                # Prompt player whether to accept the banker's offer or continue playing 
                while not response == 'y' or response == 'n':
                    response = input('Accept banker\'s offer (y/n)? ').lower()
                    if response == 'y':
                        print(end='\n\n')
                        print('#' * 45, end='\n\n')
                        print(('Game Results: ').upper(), end='\n\n')
                        print('Your chosen briefcase, no. {0} has an amount value of {1}'.format(briefcaseNumber, briefcaseValue), end='\n')
                        print('The briefcase that contains the PHP {0} jackpot prize is inside no. {1}'.format("1,000,000", briefcaseJackpot), end='\n\n')
                        print('#' * 45, end='\n\n')
                        print('Congratulations! You go home with PHP {0}. Thanks for playing.'.format(offer), end='\n\n')
                        sys.exit()
                    else:
                        return True
            else:
                continue

    # Method that prompts the player whether to play again to not. Returns True and repeats the game all over again if the player selects yes; Otherwise False and the entire program terminates immediately
    def replayGame(self):
        print(end='\n')
        return input('Do you want to play again (y/n)? ').lower().startswith('y')

# Start program execution
while True:
    # Merge game rounds and the number of briefcases remaining for each round
    gameRounds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    gameRoundCasesLeft = [6, 5, 4, 3, 2, 1, 1, 1, 1, 1]
    gameMechanics = dict(zip(gameRounds, gameRoundCasesLeft))

    # Class Instantiation
    game = DealNoDeal()

    # The player chooses his/her briefcase
    game.choosePlayerBriefcase(game.generateBriefcaseContents())

    # Simulate the game rounds in a loop
    for k, v in gameMechanics.items():
        if k < 10:
            # Simulate each round
            game.simulateRound(k, v, briefcaseNumber)
            # Simulate banker's offer
            game.bankerOffer(game.briefcaseCount(), game.expectedValueSmall(), game.expectedValueBig())
        else: 
            game.simulateRound(k, v, briefcaseNumber)

    # Terminates game
    if not game.replayGame():
        print(end='\n')
        break