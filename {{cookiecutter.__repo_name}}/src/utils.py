import argparse
import json

import pandas as pd
import yaml


class Arguments:
    """
    Arguments class parses command line arguments and stores them as attributes.

    Attributes:
    - args (argparse.Namespace): The parsed arguments.
    """
    def __init__(self, *args):
        # Initialize the parser
        self.parser = argparse.ArgumentParser(description="Command Line Arguments")

        # Add arguments to the parser
        for arg in [*args]:
            self.parser.add_argument(f"-{arg[0]}", f"--{arg}", type=str)

        # Parse Arguments
        self.args = self.parser.parse_args()
        for key, value in vars(self.args).items():
            setattr(self, key, value)

class FileReader:
    """
    FileReader class reads a file and returns its content.

    Attributes:
    - file_path (str): The path to the file to be read.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self):
        """Reads a file and returns its content"""
        if self.file_path.endswith(".txt"):
            return self._read_txt()
        elif self.file_path.endswith(".json"):
            return self._read_json()
        elif self.file_path.endswith(".yaml") or self.file_path.endswith(".yml"):
            return self._read_yaml()
        elif self.file_path.endswith(".csv"):
            return self._read_csv()
        elif self.file_path.endswith(".xlsx"):
            return self._read_xlsx()
        else:
            raise ValueError("File format not supported.")
        
    def _read_txt(self) -> str:
        """Read a text file and return its content as a string"""
        with open(self.file_path, "r") as file:
            return file.read()
    
    def _read_json(self) -> dict:
        """Read a JSON file and return its content as a dictionary"""
        with open(self.file_path, "r") as file:
            return json.load(file)
        
    def _read_yaml(self) -> dict:
        """Read a YAML file and return its content as a dictionary"""
        with open(self.file_path, "r") as file:
            return yaml.safe_load(file)
        
    def _read_csv(self) -> pd.DataFrame:
        """Read a CSV file and return its content as a Pandas DataFrame"""
        return pd.read_csv(self.file_path)

    def _read_xlsx(self) -> pd.DataFrame:
        """Read an Excel file and return its content as a Pandas DataFrame """
        return pd.read_excel(self.file_path)