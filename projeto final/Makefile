help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up: ## Build and start containers
	docker compose up --build --force-recreate

down: ## Stop containers
	docker compose down

restart: ## Restart containers
	$(MAKE) down
	$(MAKE) up

crud:
	uvicorn main:app --reload