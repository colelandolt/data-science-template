# {{cookiecutter.project_name}}
{{cookiecutter.description}}

## Getting Started
- Copy `.env-template` into `.env` and fill in the values:
```bash
cp .env-template .env
```
- Install dependencies locally with `make setup` or the following commands:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements-dev.txt
pre-commit install
```

## Directory Structure

```
├── config/                     <- Shared configurations
│   └── logger.yml              <- Logging configuration
├── data/                       <- Data artifacts
│   ├── 00_raw                  <- Imutable input data
│   ├── 01_processed            <- The data used for modelling
│   ├── 02_models               <- Trained models
│   ├── 03_output               <- Model output
│   └── 04_reporting            <- Reports and input to frontend
├── notebooks/                  <- Work in progress features in Jupyter notebooks
├── references/                 <- Data dictionaries, manuals, and all other explanatory materials
├── src/                        <- Source code for use in this project
│   ├── __init__.py             <- Makes src a Python module
│   ├── data.py                 <- Module for processing raw data
│   ├── deploy.py               <- Module for deploying a trained model to production
│   ├── evaluate.py             <- Module for evaluatng model performance
│   ├── predict.py              <- Module for making predictions with trained models
│   ├── report.py               <- Module for producing a report of modeling results
│   ├── resources.py            <- Module for connecting to data lakes and data warehouses
│   ├── train.py                <- Module for training machine learning model
│   ├── utils.py                <- Utility functions used across the entire project
│   └── visualize.py            <- Module for visualizing processed data and modeling results
├── tests/                      <- Unit tests for source code
│   ├── test_data.py            <- Tests for processing raw data
│   ├── test_deploy.py          <- Tests for deploying a trained model to production
│   ├── test_evaluate.py        <- Tests for evaluating model performance
│   ├── test_predict.py         <- Tests for making predictions with trained models
│   ├── test_report.py          <- Tests for reporting modeling results
│   ├── test_resources.py       <- Tests for connecting to data lakes and data warehouses
│   ├── test_train.py           <- Tests for training machine learning model
│   ├── test_utils.py           <- Tests for the utility functions used across the entire project
│   └── test_visualize.py       <- Tests for visualizing processed data and modeling results
├── .env-template               <- The template for environment variables
├── .gitignore                  <- The files to exclude from version control
├── .pre-commit-config          <- The configuration for the pre-commit hooks
├── docker-compose.yml          <- The configuration for the Docker container
├── Dockerfile                  <- Dockerfile that contains all commands to assemble the Docker image
├── LICENSE                     <- Open-source license
├── Makefile                    <- Makefile with commands like `make setup` and `make data`
├── README.md                   <- An overview for developers using this project
├── requirements-dev.txt        <- The dependencies file for a local development environment
└── requirements.txt            <- The dependencies file for a production environment
```