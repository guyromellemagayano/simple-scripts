"""
Deal or No Deal

A Python script simulating the popular game show, Deal or No Deal.
"""

import random
import sys


class DealNoDeal:
    def __init__(self):
        self.briefcase_stack = {}
        self.briefcase_amount = []
        self.briefcase_number = 0
        self.briefcase_value = 0
        self.briefcase_jackpot = 0
        self.expected_value_small_list = []
        self.expected_value_big_list = []

        print('\n\n' + '*' * 30 + '\n\n')
        print('WELCOME TO DEAL OR NO DEAL!\n\n')
        print('*' * 30 + '\n\n')

    def generate_briefcase_contents(self):
        briefcases = list(range(1, 27))
        amounts = [0, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000,
                   25000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 750000, 1000000]
        self.briefcase_amount = sorted(amounts)
        random.shuffle(amounts)
        self.briefcase_stack = dict(zip(briefcases, amounts))
        self.briefcase_jackpot = next(
            k for k, v in self.briefcase_stack.items() if v == 1000000)

    def choose_player_briefcase(self):
        while True:
            try:
                choice = int(input('Select your briefcase (1-26): '))
                if 1 <= choice <= 26:
                    self.briefcase_number = choice
                    self.briefcase_value = self.briefcase_stack.pop(choice)
                    print(f"You've chosen briefcase no. {
                          choice}\n\nLet's start the first round")
                    return
                else:
                    print('ERROR! Out of range\n')
            except ValueError:
                print('ERROR! Wrong input\n')

    def briefcase_count(self):
        return len(self.briefcase_stack)

    def simulate_round(self, game_round, open_case):
        if game_round == 10:
            self.final_round()
        else:
            print('\n' + '-' * 45 + f'\n\nRound {game_round}: You have {
                  open_case} suitcase/s to open\n\n' + '-' * 45 + '\n')
            for _ in range(open_case):
                self.display_briefcases_and_amounts()
                while True:
                    try:
                        choice = int(input('Select briefcase to open: '))
                        if choice in self.briefcase_stack:
                            print(f"You've chosen briefcase no. {choice}\nBriefcase no. {
                                  choice} contains PHP {self.briefcase_stack[choice]}\n")
                            self.briefcase_amount.remove(
                                self.briefcase_stack[choice])
                            del self.briefcase_stack[choice]
                            print('+' * 45 + '\n')
                            break
                        else:
                            print(
                                'ERROR! Briefcase already opened or out of range\n')
                    except ValueError:
                        print('ERROR! Wrong input\n')

    def final_round(self):
        print('\n' + '-' * 45 +
              '\n\nFinal Round: Let\'s open your briefcase\n\n' + '-' * 45 + '\n')
        self.display_briefcases_and_amounts()
        while True:
            open_prompt = input(
                'Are you ready to check your briefcase (y/n)? ').lower()
            if open_prompt == 'y':
                if self.briefcase_value == 1000000:
                    print(f'\n\nCongratulations! Your briefcase no. {
                          self.briefcase_number} has the jackpot prize of PHP {self.briefcase_value}! Thanks for playing.')
                else:
                    print(f'\n\nCongratulations! Your briefcase no. {
                          self.briefcase_number} has PHP {self.briefcase_value}! Thanks for playing.')
                break

    def display_briefcases_and_amounts(self):
        print('Amounts left:\n')
        print(' '.join(map(str, self.briefcase_amount)) + '\n')
        print('Remaining briefcases:\n')
        print(' '.join(map(str, self.briefcase_stack.keys())) + '\n')

    def expected_value_small(self):
        self.expected_value_small_list = [
            v for v in self.briefcase_stack.values() if v < 75000]
        if not self.expected_value_small_list:
            return 0
        return sum(self.expected_value_small_list) // len(self.expected_value_small_list)

    def expected_value_big(self):
        self.expected_value_big_list = [
            v for v in self.briefcase_stack.values() if v >= 75000]
        if not self.expected_value_big_list:
            return 0
        return sum(self.expected_value_big_list) // len(self.expected_value_big_list)

    def banker_offer(self):
        case_count = self.briefcase_count()
        small = self.expected_value_small()
        big = self.expected_value_big()

        offer = 0
        if case_count >= 20:
            big_value = 0.154 * (random.uniform(0.2, 0.35) * big)
            small_value = 1.4 * (random.uniform(0.2, 0.35) * small)
        elif case_count >= 15:
            big_value = 0.216 * (random.uniform(0.2, 0.35) * big)
            small_value = 1.35 * (random.uniform(0.2, 0.35) * small)
        elif case_count >= 10:
            big_value = 0.3003 * (random.uniform(0.2, 0.35) * big)
            small_value = 1.43 * (random.uniform(0.2, 0.35) * small)
        elif case_count >= 7:
            big_value = 0.3536 * (random.uniform(0.2, 0.35) * big)
            small_value = 1.36 * (random.uniform(0.2, 0.35) * small)
        elif case_count >= 5:
            big_value = 0.372 * (random.uniform(0.2, 0.35) * big)
            small_value = 1.2 * (random.uniform(0.2, 0.35) * small)
        elif case_count >= 4:
            big_value = 0.5125 * (random.uniform(0.3, 0.45) * big)
            small_value = 1.25 * (random.uniform(0.3, 0.45) * small)
        elif case_count >= 3:
            big_value = 0.6732 * (random.uniform(0.4, 0.55) * big)
            small_value = 1.32 * (random.uniform(0.4, 0.55) * small)
        elif case_count >= 2:
            big_value = 0.915 * (random.uniform(0.5, 0.65) * big)
            small_value = 1.5 * (random.uniform(0.5, 0.65) * small)
        else:
            big_value = 0.71 * (random.uniform(0.6, 0.75) * big)
            small_value = 1.0 * (random.uniform(0.6, 0.75) * small)

        offer = round(big_value + small_value)
        print('End of Round.\n')
        while True:
            ask_player = input(
                'Banker\'s offer received. Do you want to know how much he offered (y/n)? ').lower()
            if ask_player == 'y':
                print(
                    '\n' + '~' * 45 + f'\n\nBanker\'s initial offer is worth PHP {offer}\n\n' + '~' * 45 + '\n')
                while True:
                    response = input('Deal or No Deal? ').lower()
                    if response == 'deal':
                        print('\n\n' + '#' * 45 + f'\n\nGAME RESULTS:\n\nYour chosen briefcase, no. {
                              self.briefcase_number} has an amount value of {self.briefcase_value}')
                        print(f'The briefcase that contains the PHP 1,000,000 jackpot prize is inside no. {
                              self.briefcase_jackpot}\n\n' + '#' * 45 + f'\n\nCongratulations! You go home with PHP {offer}. Thanks for playing.\n\n')
                        sys.exit()
                    elif response == 'no deal':
                        return
                    else:
                        print('ERROR! Invalid input\n')
            elif ask_player == 'n':
                break
            else:
                print('ERROR! Invalid input\n')

    def replay_game(self):
        return input('Do you want to play again (y/n)? ').lower().startswith('y')
