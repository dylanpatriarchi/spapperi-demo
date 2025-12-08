.PHONY: help build up down restart logs clean test health stats

help:
	@echo "Spapperi RAG Agent - Available commands:"
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make clean       - Remove all containers and volumes"
	@echo "  make test        - Run test queries"
	@echo "  make health      - Check system health"
	@echo "  make stats       - Show knowledge base statistics"
	@echo "  make reload      - Reload documents"

build:
	docker compose build

up:
	docker compose up -d
	@echo "✓ Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

clean:
	docker compose down -v
	@echo "✓ All containers and volumes removed"

test:
	@echo "Testing English query..."
	@curl -X POST http://localhost:8000/query \
		-H "Content-Type: application/json" \
		-d '{"question": "What products does Spapperi offer?"}' \
		2>/dev/null | python3 -m json.tool
	@echo "\nTesting Italian query..."
	@curl -X POST http://localhost:8000/query \
		-H "Content-Type: application/json" \
		-d '{"question": "Quali prodotti offre Spapperi?"}' \
		2>/dev/null | python3 -m json.tool

health:
	@curl http://localhost:8000/health 2>/dev/null | python3 -m json.tool

stats:
	@curl http://localhost:8000/stats 2>/dev/null | python3 -m json.tool

reload:
	@curl -X POST http://localhost:8000/reload-documents 2>/dev/null | python3 -m json.tool


