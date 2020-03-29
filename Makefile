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
	pipenv run pytest -vv -x
	
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
	pipenv run pytest -m focus -x --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb -vv --setup-show --no-cov
# -m focus     | Run only focused tests (@pytest.mark.focus)
# -x           | stop after first failure
# --pdb        | start ipdb on error
# --pdbcls=IPython.terminal.debugger:TerminalPdb | (see line above)
# -vv          | show all of assert comparisons instead of truncating
# --setup-show | show setup of fixtures while executing tests
# --no-cov     | disable coverage report completely

typecheck:
	python -m mypy --config-file setup.cfg --package src

typecheck-test:
	python -m mypy --config-file setup.cfg --package src --package tests

recreate-db:
	dropdb ${POSTGRES_DB}
	createdb ${POSTGRES_DB}
	rm -rf src/plan/migrations/*
	python manage.py makemigrations plan
	python manage.py migrate
	python manage.py create_random_data
