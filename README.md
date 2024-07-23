# Template Data Science Project Repository
A cookiecutter template for Python Data Science projects

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
This template repository is intended for use in Data Science projects, enabling developers to engage in the Data Science methodology without spending time and energy setting up their development environments and structuring their projects. The repository is adapted from the [Cookiecutter Data Science project template](https://github.com/drivendataorg/cookiecutter-data-science), which you can read more about on the [project homepage](https://cookiecutter-data-science.drivendata.org/). The project structure embodies the [opinions](https://cookiecutter-data-science.drivendata.org/opinions/) set forth by the Cookiecutter Data Science project.

## Contents
The source code in this repository consists of scripts to execute the following steps in the Data Science Method:
- Data Preparation: `src/data.py`
- Data Exploratation: `src/visualize.py`
- Model Training: `src/train.py`
- Model Prediction: `src/predict.py`
- Model Evaluation: `src/evaluate.py`
- Model Deployment: `src.deploy.py`
- Reporting: `src/report.py`

Particularly for data preparation, `src/data.py` comes equipped with a variety of functions to data cleaning and data augmentation, and `src/resources.py` consists of classes to upload and download files from cloud storage, such as AWS S3 and Google Cloud Storage, as well as classes to read and write data from data warehouses, such as Snowflake and BigQuery.

The repository leverages [GNU Make](https://www.gnu.org/software/make/) as a task runner, meaning that the shell commands that execute the above steps of the Data Science Method are included as recipes in `Makefile`. To use a recipe, execute the following command:
```bash
make <RECIPE_NAME>
```

## Project Organization
Each project using this template is organized into the following layers:

#### Raw
The data we recieve from internal or external sources is the raw data, and this data is **immutable** (see [explanation](https://drivendata.github.io/cookiecutter-data-science/#data-is-immutable)).

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
│   │
│   ├── fonts/                  <- NRG brand fonts
│   │
│   ├── palettes.yml            <- NRG brand color palettes
│   │
│   └── logger.yml              <- logging configuration
│
├── data/                       <- Data artifacts
│   │
│   ├── 00_raw                  <- Imutable input data
│   │
│   ├── 01_processed            <- The data used for modelling
│   │
│   ├── 02_models               <- Trained models
│   │
│   ├── 03_output               <- Model output
│   │
│   └── 04_reporting            <- Reports and input to frontend
│
├── notebooks/                  <- Work in progress features in Jupyter notebooks
│
├── references/                 <- Data dictionaries, manuals, and all other explanatory materials
│
├── src/                        <- Source code for use in this project
│   │
│   ├── __init__.py             <- Makes src a Python module
│   │
│   ├── data.py                 <- Script to process raw data
│   │
│   ├── deploy.py               <- Script to deploy the trained model to production
│   │
│   ├── predict.py              <- Script to used trained model to make predictions
│   │
│   ├── train.py                <- Script to train machine learning model
│   │
│   ├── utils.py                <- Utility functions used across the entire project
│   │
│   └── visualize.py            <- Script to visualize processed data and modeling results
│
├── .env-template               <- The template for environment variables
│
├── .pre-commit-config          <- The configuration for the pre-commit hooks
│
├── docker-compose.yml          <- The configuration for the Docker container
│
├── Dockerfile                  <- Dockerfile that contains all commands to assemble the Docker image 
│
├── Makefile                    <- Makefile with commands like `make setup` and `make run`
│
├── README.md                   <- An overview for developers using this project
│
├── requirements-dev.txt        <- The dependencies file for a local development environment
│
└── requirements.txt            <- The dependencies file for a production environment
```
