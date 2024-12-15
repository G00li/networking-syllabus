help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up: ## Builda e inicia os containers
	docker compose up --build --force-recreate

down: ## Para os containers em execução
	docker compose down

restart: ## Faz restart nos containers
	$(MAKE) down
	$(MAKE) up

crud: ## Realiza o crud 
	uvicorn main:app --reload

netls: ## Verifica as networks existentes
	docker network ls

stats: ## Verifica se o balanceamento de carga está funcionando 
	docker stats

depends:
	pip install -r requirements.txt
