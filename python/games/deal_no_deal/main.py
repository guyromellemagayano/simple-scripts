from deal_no_deal import DealNoDeal

def main():
    while True:
        game_rounds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        game_round_cases_left = [6, 5, 4, 3, 2, 1, 1, 1, 1, 1]
        game_mechanics = dict(zip(game_rounds, game_round_cases_left))

        game = DealNoDeal()
        game.generate_briefcase_contents()
        game.choose_player_briefcase()

        for k, v in game_mechanics.items():
            game.simulate_round(k, v)
            if k < 10:
                game.banker_offer()

        if not game.replay_game():
            print('\n')
            break

if __name__ == "__main__":
    main()
