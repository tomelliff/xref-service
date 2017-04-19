PYTHON_TEST_DISCOVER=python -m unittest discover

.PHONY: all
all: test

.PHONY: test
test: lint unit integration

.PHONY: lint
lint: gitlab-ci-lint flake8

.PHONY: gitlab-ci-lint
gitlab-ci-lint:
	./lint-gitlab-ci.sh

.PHONY: flake8
flake8:
	flake8 --exclude .git,env,test/local

.PHONY: unit
unit:
	$(PYTHON_TEST_DISCOVER) --start-directory test/unit

.PHONY: integration
integration:
	$(PYTHON_TEST_DISCOVER) --start-directory test/integration

.PHONY: contract
contract:
	$(PYTHON_TEST_DISCOVER) --start-directory test/contract

.PHONY: deploy
deploy:
	serverless deploy
