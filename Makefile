help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	
run-battleship-game: ## Run the `Battleship Game` in "games/battleship" folder
	python games/battleship/main.py
	
run-deal-no-deal-game: ## Run the `Deal or No Deal` in "games/deal-no-deal" folder
	python games/deal_no_deal/main.py