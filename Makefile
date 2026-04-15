.PHONY: help install test validate pipeline clean clean-apply lint

PYTHON ?= python3
CLI    := $(PYTHON) -m cannabis_tax.cli

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install package in editable mode with dev deps
	$(PYTHON) -m pip install -e ".[dev]"

test: ## Run unit tests
	$(PYTHON) -m pytest tests/ -v --tb=short

test-cov: ## Run tests with coverage report
	$(PYTHON) -m pytest tests/ -v --tb=short --cov=cannabis_tax --cov-report=term-missing

validate: ## Validate target consistency (fail-fast)
	$(CLI) validate

pipeline: ## Run full pipeline: process → validate → consumption
	$(CLI) pipeline

clean: ## Dry-run: show artifacts that would be removed
	$(CLI) cleanup

clean-apply: ## Actually remove safe-to-delete artifacts
	$(CLI) cleanup --apply

lint: ## Run black + isort check (no changes)
	$(PYTHON) -m black --check src/ tests/
	$(PYTHON) -m isort --check src/ tests/

format: ## Auto-format with black + isort
	$(PYTHON) -m black src/ tests/
	$(PYTHON) -m isort src/ tests/
