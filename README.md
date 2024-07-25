# Template Data Science Project Repository
A cookiecutter template for Data Science projects in Python

## Getting Started
1. Install Cookiecutter:
```bash
pip install cookiecutter
```

2. Create a project based on the template:
```bash
cookiecutter git@github.com:colelandolt/data-science-template.git
```

## Description
This template repository alleviates the need for developers to spend time and energy setting up a local development environment and structuring the repository when beginning a new Data Science project. 

The `src/` folder  consists of modules to execute the steps of the Data Science Method. The `tests/` folder consists of tests for these modules. The repository is also configured with a series of pre-commit hooks to format, lint, and check for issues in the code before committing to version control. Lastly, [GNU Make](https://www.gnu.org/software/make/) is used as a task runner, meaning that the shell commands that execute the steps of the Data Science Method are included as recipes in `Makefile`. To use a recipe, execute the following command:
```bash
make <RECIPE_NAME>
```

## Project Organization
Each project using this template is organized into the following layers:

#### Raw
The data we recieve from internal or external sources is the raw data, and this data is **immutable** (see [explanation](https://cookiecutter-data-science.drivendata.org/opinions/#raw-data-is-immutable)).

#### Processed
To perform the modeling and statistical analysis, the raw data needs to be combined, cleaned, and enriched, for example by creating features. 

#### Models
The processed data is used to train predictive models
> In contrast to the previous layers, models are usually stored in `pickle` because they are not in tabular format.

#### Outputs
Model performance metrics, model selection information and predictions are products of modeling and statistical analysis.

#### Reports
Reporting may take place at any point throughout the pipeline. Some example include:
- data quality reports on the inputs
- exploratory data analysis on the processed data
- predictions
- performance evaluation and tracking

If a front-end is constructed, it will access the reports layer to display information to the users and developers.

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

## References
The repository draws inspiration from both the [Cookiecutter Data Science project template](https://github.com/drivendataorg/cookiecutter-data-science), which you can read more about on the [project homepage](https://cookiecutter-data-science.drivendata.org/), as well as Khuyen Tran's [Data Science Cookiecutter template](https://github.com/khuyentran1401/data-science-template), which you can read more about in her [blog post](https://codecut.ai/how-to-structure-a-data-science-project-for-readability-and-transparency-2/).