.DEFAULT_GOAL := all

.PHONY: .uv
.uv: ## Check that uv is installed
	@uv --version || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'


.PHONY: install
install: .uv  ## Install the package, dependencies
	uv sync --frozen --all-extras --all-packages --group lint --group docs

.PHONY: sync
sync: .uv ## Update local packages and uv.lock
	uv sync --all-extras --all-packages --group lint --group docs

.PHONY: format
format: ## Format the code
	uv run ruff format
	uv run ruff check --fix --fix-only

.PHONY: lint
lint: ## Lint the code
	uv run ruff format --check
	uv run ruff check

.PHONY: test
test: ## Run tests and collect coverage data
	uv run coverage run -m pytest tests
	@uv run coverage report

.PHONY: test-all-python
test-all-python: ## Run tests on Python 3.9 to 3.13
	UV_PROJECT_ENVIRONMENT=.venv39 uv run --python 3.9 --all-extras coverage run -p -m pytest
	UV_PROJECT_ENVIRONMENT=.venv310 uv run --python 3.10 --all-extras coverage run -p -m pytest
	UV_PROJECT_ENVIRONMENT=.venv311 uv run --python 3.11 --all-extras coverage run -p -m pytest
	UV_PROJECT_ENVIRONMENT=.venv312 uv run --python 3.12 --all-extras coverage run -p -m pytest
	UV_PROJECT_ENVIRONMENT=.venv313 uv run --python 3.13 --all-extras coverage run -p -m pytest
	@uv run coverage combine
	@uv run coverage report

.PHONY: testcov
testcov: test ## Run tests and generate a coverage report
	@echo "building coverage html"
	@uv run coverage html

.PHONY: eval
eval: ## Evaluate the code
	@echo "Running agents evaluations"
	@uv run python evaluate.py

# `--no-strict` so you can build the docs without insiders packages
.PHONY: docs
docs: ## Build the documentation
	uv run mkdocs build --no-strict

# `--no-strict` so you can build the docs without insiders packages
.PHONY: docs-serve
docs-serve: ## Build and serve the documentation
	uv run mkdocs serve --no-strict

.PHONY: .docs-insiders-install
.docs-insiders-install: ## Install insiders packages for docs if necessary
ifeq ($(shell uv pip show mkdocs-material | grep -q insiders && echo 'installed'), installed)
	@echo 'insiders packages already installed'
else
	@echo 'installing insiders packages...'
	@uv pip install --reinstall --no-deps \
		mkdocs-material mkdocstrings-python
endif

.PHONY: docs-insiders
docs-insiders: .docs-insiders-install ## Build the documentation using insiders packages
	uv run --no-sync mkdocs build -f mkdocs.insiders.yml

.PHONY: docs-serve-insiders
docs-serve-insiders: .docs-insiders-install ## Build and serve the documentation using insiders packages
	uv run --no-sync mkdocs serve -f mkdocs.insiders.yml

.PHONY: cf-pages-build
cf-pages-build: ## Install uv, install dependencies and build the docs, used on CloudFlare Pages
	curl -LsSf https://astral.sh/uv/install.sh | sh
	uv python install 3.12
	uv sync --python 3.12 --frozen --group docs
	uv pip install --reinstall --no-deps \
		mkdocs-material mkdocstrings-python
	uv pip freeze
	uv run --no-sync mkdocs build -f mkdocs.insiders.yml

.PHONY: all
all: format lint typecheck testcov ## Run code formatting, linting, static type checks, and tests with coverage report generation

.PHONY: help
help: ## Show this help (usage: make help)
	@echo "Usage: make [recipe]"
	@echo "Recipes:"
	@awk '/^[a-zA-Z0-9_-]+:.*?##/ { \
		helpMessage = match($$0, /## (.*)/); \
		if (helpMessage) { \
			recipe = $$1; \
			sub(/:/, "", recipe); \
			printf "  \033[36m%-20s\033[0m %s\n", recipe, substr($$0, RSTART + 3, RLENGTH); \
		} \
	}' $(MAKEFILE_LIST)