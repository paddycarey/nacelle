.PHONY: docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "test - run tests quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"

clean-docs:
	rm -f docs/nacelle.*
	rm -f docs/modules.rst
	$(MAKE) -C docs clean

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

test:
	./testrunner.sh

docs: clean-docs
	$(MAKE) -C docs html
	xdg-open docs/_build/html/index.html
