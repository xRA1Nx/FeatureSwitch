run-server:
	uvicorn --reload src.apps.main:application

lock: # создание requirements.txt из requirements.in
	pip-compile --generate-hashes --no-annotate --no-header --no-emit-index-url

upgrade: # актуализация версий зависимостей
	pip-compile --upgrade --generate-hashes --no-annotate --no-header --no-emit-index-url

install-dev: # установка зависимостей при локальной разработки
	pip-sync requirements.txt

install-ci: # установка зависимостей с проверкой хешей
	pip install --no-cache-dir --require-hashes -r requirements.tx

install-hooks:
	pre-commit install -t pre-commit -t commit-msg -t pre-push

types: # show only new (not fixed in baseline) annotation errors
	@mypy . | mypy-baseline filter --allow-unsynced || (echo "Mypy check failed"; exit 1)

baseline: # fix the current technical debt
	ruff check --quiet > baseline.txt || true
	mypy . | mypy-baseline sync || true

validate-ci:
	CONFIGURATION=Test make -j$(N_JOBS) types ruff-check

coverage:
	coverage run -m pytest src -q

coverage-report:
	coverage html --skip-covered

test-sharded:
	@echo seed: ${SEED}
	mkdir -p reports/
	chmod 0777 reports/
	pytest -q --randomly-seed=${SEED} --durations=10 --junitxml=reports/junit_report.xml --shard-id=$$(( $(N_SHARD_INDEX) - 1 )) --num-shards=$(N_SHARD_TOTAL)

ruff-fix:
	@ruff format
	@ruff check --fix


ruff-check:
	@echo "Running ruff format check..."
	@ruff format --check
	@echo "Running ruff lint check..."
	@ruff check --exit-non-zero-on-fix
