.PHONY: docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "i18n-update - extracts new translations from source code and updates the .po files"
	@echo "i18n-build - compiles .po into .mo files ready to be read by the app"
	@echo "install-devenv - install backend development dependencies from pip"
	@echo "lint - run pep8 checks against the app's code"
	@echo "run - run the local development server for testing/debugging"
	@echo "test - run all of the app's tests and print a coverage report"

clean-docs:
	rm -f docs/nacelle.*
	rm -f docs/modules.rst
	$(MAKE) -C docs clean

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docs: clean-docs
	$(MAKE) -C docs html
	xdg-open docs/_build/html/index.html

i18n-build:
	pybabel compile -f -d ./translations

i18n-init: i18n-extract
	pybabel init -l en_US -d ./translations -i ./translations/messages.pot
	pybabel init -l it_IT -d ./translations -i ./translations/messages.pot

i18n-extract:
	pybabel extract -F ./translations/babel.cfg -o ./translations/messages.pot ./

i18n-update: i18n-extract
	pybabel update -l en_US -d ./translations/ -i ./translations/messages.pot
	pybabel update -l it_IT -d ./translations/ -i ./translations/messages.pot

install-devenv:
	pip install -r nacelle/requirements.txt

lint:
	pep8 --ignore=E501 --exclude=vendor,docs .

run:
	dev_appserver.py .

test:
	coverage erase
	coverage run --source="nacelle" --omit="google_appengine/*,nacelle/vendor/*" nacelle/test/runner.py
	coverage report -m
