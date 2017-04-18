.PHONY: all
all: test

.PHONY: test
test: flake8 unit integration

.PHONY: flake8
flake8:
	flake8 --exclude .git,env,test/local

.PHONY: unit
unit:
	python -m unittest discover --start-directory test/unit

.PHONY: integration
integration:
	python -m unittest discover --start-directory test/integration

.PHONY: contract
contract:
	python -m unittest discover --start-directory test/contract
