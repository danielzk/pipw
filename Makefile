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

upload-coverage:
	codecov -t $(CODECOV_TOKEN)

build:
	rm -rf dist
	python setup.py build
	python setup.py sdist

release:
	twine upload dist/*
