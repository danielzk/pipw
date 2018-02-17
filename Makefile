.PHONY: tests build

ENV_OPT=
ifneq ($(env),)
	ENV_OPT=-e $(env)
endif

tests:
	tox ${ENV_OPT}

wip-tests:
	tox ${ENV_OPT} -- -m wip

review-tests:
	tox ${ENV_OPT} -- --cov-report term-missing --cov=pipw

build:
	rm -rf dist
	python setup.py build
	python setup.py sdist
	python setup.py bdist_wheel --universal

deploy: build
	twine upload dist/*
