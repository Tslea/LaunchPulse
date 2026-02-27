.PHONY: dev test lint format install

install:
	cd backend && pip install -e ".[dev]"

dev:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	cd backend && pytest -v

lint:
	cd backend && ruff check .

format:
	cd backend && ruff format .

# Dashboard
dashboard-dev:
	cd dashboard && npm run dev

dashboard-install:
	cd dashboard && npm install
