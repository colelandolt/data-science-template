import logging
import logging.config
import os
from typing import List, Optional

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from utils import Arguments, FileReader


def impute_null(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    """
    Imputes the column mean for missing values in the dataframe

    Arguments:
    - df (pd.DataFrame): The raw dataframe
    - strategy (str): The imputation strategy (mean, median, or most_frequent)

    Returns:
    - (pd.DataFrame): The dataframe with imputed values
    """
    # Store column names and data types
    columns = df.dtypes

    # Initialize Imputer
    imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)

    # Impute null values
    imputer = imputer.fit(df)
    df = imputer.transform(df)
    df = pd.DataFrame(df)

    # Set the names of each column
    df.columns = columns.index

    # Set the data types of each column
    for col, dtype in columns.to_dict().items():
        df[[col]] = df[[col]].astype(dtype)
    
    # Return the non-null dataframe
    return df


def smote(
    df: pd.DataFrame,
    target: str,
    exclude_cols: Optional[List[str]] = [],
    undersampling: Optional[bool] = True
) -> pd.DataFrame:
    """
    Resamples the given dataset using SMOTE and undersampling

    Arguments:
    - df (pd.DataFrame): The dataset to resample
    - target (str): The target variable
    - exclude_cols (Optional[str]): The columns to exclude from resampling
    - undersampling (Optional[bool]): Whether or not to employ undersampling

    Returns:
    - (pd.DataFrame): the oversampled dataset
    """
    # Initialize target variable and independent variables
    drop_cols = [target] + exclude_cols
    X = df.drop(drop_cols, axis=1)
    y = df[[target]]

    # Determine Sampling Strategy
    classes = df[target].unique()
    majority_class = df[target].value_counts().index[0]
    sample_size = len(df[df[target]==majority_class])
    if undersampling: sample_size = int(sample_size/2)
    sampling_strategy = dict(
        zip(classes, np.repeat(sample_size, len(classes)))
    )

    if undersampling:
        over = SMOTE(sampling_strategy=0.5)
        under = RandomUnderSampler(sampling_strategy=sampling_strategy)
        steps = [('over', over), ('under', under)]
    else:
        over = SMOTE(sampling_strategy=sampling_strategy)
        steps = [('over', over)]
    
    # Initialize Resampling Pipeline
    pipeline = Pipeline(steps=steps)

    # Resample the dataset
    X_resampled, y_resampled = pipeline.fit_resample(X, y)

    # Format the resampled dataset
    resampled_df = X_resampled
    resampled_df[target] = y_resampled
    resampled_df = resampled_df.reset_index(drop=True)

    # Return the resampled dataset
    return resampled_df


def resample(
    file_name: str,
    target: str,
    exclude_cols: Optional[List[str]] = None,
    undersampling: Optional[bool] = True
):
    """
    Resamples the dataset and writes the output to data/processed/

    Arguments:
    - file_name (str): The name of the dataset file
    """
    # Read the dataset
    df = pd.read_csv(f"data/raw/{file_name}")
    
    # Impute null values
    if df.isnull().any().any():
        df = impute_null(df)

    # Resample the dataset
    df = smote(
        df=df,
        target=target,
        exclude_cols=exclude_cols,
        undersampling=undersampling    
    )

    # Write the resampled dataset
    df.to_csv(
        f"data/processed/{file_name.split('.')[0]}-resampled.csv", index=False
    )


def main():
    # Configure logger
    log_config = FileReader("conf/logger.yaml").read()
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    
    # Parse command line arguments
    args = Arguments("name", "target")
    name = args.name
    target = args.target


if __name__ == "__main__":
    main()
