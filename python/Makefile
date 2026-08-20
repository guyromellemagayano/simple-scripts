help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run-battleship-game: ## Run the `Battleship Game` in "games/battleship" folder
	python3 games/battleship/main.py

run-deal-no-deal-game: ## Run the `Deal or No Deal` in "games/deal-no-deal" folder
	python3 games/deal_no_deal/main.py

run-password-generator: ## Run the password generator utility
	python3 utils/password_generator.py

test: ## Run the Python test suite
	PYTHONPATH=.. python3 -m unittest discover -s tests -v
