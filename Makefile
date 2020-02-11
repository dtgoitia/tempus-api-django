POSTGRES_DB=tempus

install:
	pipenv install --dev

run:
	python manage.py runserver

test: check-migration
	pytest --ds=tests.settings  -vv -x --reuse-db --cov=src/ --cov-config .coveragerc
	
check-migration:
	python manage.py makemigrations --dry-run --check

format:
	black .

lint: typecheck
	flake8
	make isort

isort:
	isort -rc src/ tests/

shell:
	# python3 manage.py shell_plus
	python manage.py shell

test-dev:
	pytest -f -vv -x tests/

typecheck:
	python -m mypy --config-file setup.cfg --package src

recreate-db:
	dropdb ${POSTGRES_DB}
	createdb ${POSTGRES_DB}
	python manage.py migrate
