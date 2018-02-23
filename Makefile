.PHONY: tests build

ENV_OPT=
ifneq ($(env),)
	ENV_OPT=-e $(env)
endif

tests:
ifneq ($(ENV_OPT),)
	tox ${ENV_OPT}
else
	pytest -s -vv
endif

wip-tests:
ifneq ($(ENV_OPT),)
	tox ${ENV_OPT} -- -m wip
else
	pytest -s -vv -m wip
endif

review-tests:
	pylint pipw || exit 0
	tox ${ENV_OPT} -- --cov-report term-missing --cov=pipw

upload-coverage:
	codecov -t $(CODECOV_TOKEN)

build:
	rm -rf dist
	python setup.py build
	python setup.py sdist

release:
	twine upload dist/*
