help:
	@echo "clean - clean up/remove build artefacts"
	@echo "test - run all of the app's tests and print a coverage report"

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

dist: clean clean-build
	python setup.py sdist
	ls -lh dist/

release: clean
	twine upload dist/*

test: clean clean-build
	coverage erase
	coverage run --source="nacelle" --omit="google_appengine/*,nacelle/vendor/*" nacelle/test/runner.py
	coverage report -m
