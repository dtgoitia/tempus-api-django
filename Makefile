POSTGRES_DB=tempus

set-up:
	make install
	make install-git-hooks

install-git-hooks:
	pipenv run pre-commit install

install:
	pipenv install --dev

run:
	python manage.py runserver

test: check-migration
	pipenv run pytest --capture=no -vv -x --reuse-db
	# pytest -vv -x --reuse-db --cov=src/ --cov-config .coveragerc
	
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
	rm -rf src/plan/migrations/*
	python manage.py makemigrations plan
	python manage.py migrate
	python manage.py create_random_data
