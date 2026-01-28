# This Makefile is used strictly for repo maintenance. If you are doing the 
# labs, you can safely ignore this whole file.

PYEXEC := python3.10
DOCKERIMAGE := learning-labs

.PHONY: build-docker
build-docker:
	docker build -f Dockerfile -t $(DOCKERIMAGE) .

.PHONY: run-cicd
run-cicd:
	docker run --rm -it  -v ${PWD}:/app --entrypoint bash $(DOCKERIMAGE)

# All the following targets must be run inside the container.
.PHONY: black
black:
	$(PYEXEC) -m black --diff --check -q --color .

.PHONY: black-fix
black-fix:
	$(PYEXEC) -m black -q .

.PHONY: isort-fix
isort-fix: 
	$(PYEXEC) -m isort .

.PHONY: isort
isort: 
	$(PYEXEC) -m isort --check-only .

.PHONY: pylint
pylint: 
	PYTHONPATH="./portfolio_manager:./rabbit_mq:./rabbit_mq/mini_lab" $(PYEXEC) -m pylint portfolio_manager rabbit_mq | tee pylint.out

# Run all the linters in auto-fix mode.
.PHONY: fix-lint
fix-lint: black-fix isort-fix

# Run all the linters in test-only mode without modifying anything.
.PHONY: check-lint
check-lint: black isort pylint

.PHONY: build-lab
build-lab: build-docker

.PHONY: run-lab
run-lab:
	docker run --rm -it -p8888:8888 -v ${PWD}:/app  $(DOCKERIMAGE)

