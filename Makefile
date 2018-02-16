.PHONY: tests build

tests:
	pytest -s -vv

wip-tests:
	pytest -s -vv -m wip

review-tests:
	pytest -s -vv --cov-report term-missing --cov=pipw

build:
	rm -rf dist
	python setup.py build
	python setup.py sdist
	python setup.py bdist_wheel --universal

deploy: build
	twine upload dist/*
