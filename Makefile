.PHONY: clean-pyc clean-build docs clean

help:
	@echo "Maintenance:"
	@echo ""
	@echo "    clean - clean up/remove build artefacts"
	@echo "    clean-build - remove build artefacts"
	@echo "    clean-pyc - remove Python file artifacts"
	@echo ""
	@echo "Documentation:"
	@echo ""
	@echo "    docs - generate Sphinx HTML documentation, including API docs"
	@echo "    serve-docs - serve the documentation on \"http://localhost:8080\" during development"
	@echo ""
	@echo "Testing:"
	@echo ""
	@echo "    test - run all of the app's tests and print a coverage report"
	@echo ""
	@echo "Packaging/Distribution:"
	@echo ""
	@echo "    dist - build distribution-ready Python package"
	@echo "    release - upload a built package to pypi"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-docs:
	rm -fr docs/_build/
	rm -f docs/nacelle.*
	rm -f docs/modules.rst

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

dist: clean clean-build
	python setup.py sdist
	ls -lh dist/

docs: clean-docs
	# sphinx-apidoc -o docs/ nacelle
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

release: clean
	twine upload dist/*

serve-docs:
	cd docs/_build/html/; python -m SimpleHTTPServer 8080

test: clean clean-build
	coverage erase
	coverage run --source="nacelle" --omit="google_appengine/*" nacelle/test/runner.py
	coverage report -m
