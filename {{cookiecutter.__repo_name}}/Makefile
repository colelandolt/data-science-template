.ONESHELL:

.DEFAULT_GOAL := setup

PYTHON = ./.venv/bin/python3
PIP = ./.venv/bin/pip

venv:
	@echo "Initializing virtual environment..."
	python3 -m venv .venv

activate: venv
	@echo "Activating virtual environment..."
	chmod +x ./.venv/bin/activate
	. ./.venv/bin/activate

install: requirements.txt
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

git:
	@echo "Initializing git..."
	git init 

setup: activate install git

pre-commit: 
	pre-commit install
	pre-commit run --all-files

test: 
	pytest

docs: ./src/*
	pdoc --html --output-dir docs src

data: ./src/data.py
	$(PYTHON) ./src/data.py

train: ./src/train.py
	$(PYTHON) ./src/train.py

predict: ./src/predict.py
	$(PYTHON) ./src/predict.py

evaluate: ./src/evaluate.py
	$(PYTHON) ./src/evaluate.py

visualize: ./src/visualize.py
	$(PYTHON) ./src/visualize.py

report: ./src/report.py
	$(PYTHON) ./src/report.py

deploy: .src/deploy.py
	$(PYTHON) ./src/deploy.py

pipeline: data train predict evaluate visualize report deploy

uninstall:
	@echo "Uninstalling all packages..."
	$(PIP) freeze | xargs $(PIP) uninstall -y

clean: 
	@echo "Cleaning Repository..."
	find src -name __pycache__ -print | xargs rm -rf
	find notebooks -name .ipynb_checkpoints -print | xargs rm -rf
	rm -rf .venv

.PHONY: setup pipeline