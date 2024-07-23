import os

import boto3
import botocore
from dotenv import load_dotenv
import google.api_core
import google.cloud
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

# Load environment variables
load_dotenv()


class AWS:
    """
    AWS resource

    Attributes:
    - access_key_id (str): The AWS access key ID
    - secret_access_key (str): The AWS secret access key
    - region_name (str): The name of the default region
    """
    def __init__(
        self,
        access_key_id: str = os.environ.get("AWS_ACCESS_KEY_ID"),
        secret_access_key: str = os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name: str = os.environ.get("AWS_REGION"),
    ):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name

    def connect(self):
        """
        Initializes an AWS session

        Returns:
        - (boto3.Session): the AWS S3 Resource
        """
        return boto3.Session(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name=self.region_name,
        )


class S3(AWS):
    """
    AWS S3 resource

    Attributes:
    - access_key_id (str): The AWS access key ID
    - secret_access_key (str): The AWS secret access key
    - region_name (str): The name of the default region
    - bucket_name (str): The name of the default AWS S3 bucket
    """
    def __init__(self,bucket_name: str = os.environ.get("AWS_S3_BUCKET")):
        super().__init__()
        self.bucket_name = bucket_name
    
    def connect(self):
        """ Initializes an AWS S3 resource"""
        session = super().connect()
        return session.resource("s3")
    
    def bucket(self):
        """Initializes a connection to an AWS S3 bucket"""
        s3 = self.connect()
        return s3.Bucket(name=self.bucket_name)
    
    def download(self, source_path: str, destination_path: str):
        """
        Downloads a file from an AWS S3 Bucket

        Arguments:
            source_path (str): The path to the file in the S3 Bucekt
            destination_path (str): The path to the location to download the file to
        """
        # Initialize connection to the AWS S3 bucket
        bucket = self.bucket()

        # Download the file from the S3 bucket
        try:
            bucket.download_file(Key=source_path, Filename=destination_path)
        except botocore.exceptions.ClientError:
            raise ValueError(f'File {source_path} not found.')

    def upload(self, source_path: str, destination_path: str):
        """
        Uploads a file to the AWS S3 Bucket.

        Arguments:
            source_path (str): The path to the file in the S3 Bucket
            destination_path (str): The path to the location of the file
        """
        # Initialize connection to the AWS S3 bucket
        bucket = self.bucket()

        # Upload the file to the S3 bucket
        try:
            bucket.upload_file(Filename=destination_path, Key=source_path)
        except FileNotFoundError:
            raise ValueError(f'File {source_path} not found.')


class GCS:
    """
    Google Cloud Storage class to upload and download files to and from a bucket.

    Attributes:
    - project (str): The Google Cloud project ID.
    - bucket_name (str): The name of the bucket to upload and download files from
    """
    def __init__(
        self,
        project: str = os.environ.get("GCP_PROJECT_ID"),
        bucket_name: str = os.environ.get("GCP_BUCKET_NAME")
    ):
        self.project = project
        self.bucket_name = bucket_name

    def connect(self):
        """Initializes a connection to the Google Cloud Storage client."""
        return storage.Client(project=self.project)
    
    def bucket(self):
        """Gets the bucket object from the Google Cloud Storage client."""
        client = self.connect()
        try:
            return client.get_bucket(self.bucket_name)
        except google.cloud.exceptions.Forbidden:
            raise ValueError(
                f"Bucket {self.bucket_name} either does not exist in {self.project} or it is forbidden to access."
            )
         
    def download(self, source_path: str, destination_path: str):
        """
        Downloads a file from the bucket to a local file.
        
        Arguments:
        - source_path (str): The path of the file in the bucket.
        - destination_path (str): The path of the file to save the downloaded file.
        """
        bucket = self.bucket()
        blob = bucket.blob(destination_path)
        try:
            blob.download_to_filename(source_path)
        except google.cloud.exceptions.NotFound:
            raise ValueError(
                f'File {source_path} not found in bucket {self.bucket_name}.'
            )
        
    def upload(self, source_path: str, destination_path: str):
        """
        Uploads a local file to the bucket.

        Arguments:
        - source_path (str): The path of the local file to upload.
        - destination_path (str): The path of the new file in the bucket.
        """
        bucket = self.bucket()
        blob = bucket.blob(destination_path)
        try:
            blob.upload_from_filename(source_path)
        except FileNotFoundError:
            raise ValueError(f'File {source_path} not found.')


class BigQuery:
    """
    Google BigQuery class to read and write data

    Attributes:
    - project (str): The Google Cloud project ID
    - dataset_id (str): The dataset ID to read and write data from
    """
    def __init__(
        self,
        project: str = os.environ.get("GCP_PROJECT_ID"),
        dataset_id: str = os.environ.get("GCP_DATASET_ID")
    ):
        self.project = project
        self.dataset_id = dataset_id

    def connect(self):
        return bigquery.Client(project=self.project)
    
    def read(self, query: str) -> pd.DataFrame:
        """
        Executes a SQL query and returns the results as a Pandas DataFrame

        Arguments:
        - query (str): The SQL query to execute

        Returns:
        - (pd.DataFrame): The results of the query as a Pandas DataFrame
        """
        # Initialize the BigQuery client
        client = self.connect()
        
        # Execute the SQL query
        try:
            query_job = client.query(query)
            result = query_job.result()
        except google.api_core.exceptions.NotFound:
            table = query.split("FROM")[1].strip().split(" ")[0]
            raise ValueError(f"Table {table} was not found in project {self.project}.")
        except google.api_core.exceptions.BadRequest:
            raise ValueError("Invalid SQL query.")

        # Return the result as a Pandas DataFrame
        return result.to_dataframe()
    
    def write(self, df: pd.DataFrame, table: str):
        """
        Writes a Pandas DataFrame to a BigQuery table.

        Arguments:
        - df (pd.DataFrame): The DataFrame to write to the table.
        - table (str): The fully qualified table reference to write to.
        """
        # Initialize the BigQuery client
        client = self.connect()

        # Write the DataFrame to the table
        try:
            client.load_table_from_dataframe(df, destination=table)
        except google.api_core.exceptions.Forbidden:
            raise ValueError(f"Table {table} does not exist in project {self.project} or it is forbidden to access.")


class Snowflake:
    """
    Snowflake class to read and write data

    Attributes:
    - account (str): The account identifier
    - user (str): The login name of the user
    - password (str): The password for the user
    - warehouse (str): The name of the default warehouse to use
    - database (str): The name of the default database to use
    - schema (str): The name of the default schema to use for the database
    - role (str): The name of the default role to use
    """
    def __init__(
        self,
        account: str = os.environ.get("SNOWFLAKE_ACCOUNT"),
        user: str = os.environ.get("SNOWFLAKE_USER"),
        password: str = os.environ.get("SNOWFLAKE_PASSWORD"),
        warehouse: str = os.environ.get("SNOWFLAKE_WAREHOUSE"),
        database: str = os.environ.get("SNOWFLAKE_DATABASE"),
        schema: str = os.environ.get("SNOWFLAKE_SCHEMA"),
        role: str = os.environ.get("SNOWFLAKE_ROLE"),
    ):
        self.account = account
        self.user = user
        self.password = password
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.role = role

    def connect(self) -> snowflake.connector.SnowflakeConnection:
        """
        Establishes a connection to Snowflake

        Returns:
        - (SnowflakeConnection): the connection to Snowflake
        """
        return snowflake.connector.connect(
            account=self.account,
            user=self.user,
            password=self.password,
            warehouse=self.warehouse,
            database=self.database,
            schema=self.schema,
            role=self.role
        )
    
    def read(self, sql: str) -> pd.DataFrame:
        """
        Reads data from Snowflake using a SQL query

        Arguments:
            sql (str): The SQL query to execute

        Returns:
            df (pd.DataFrame): The dataframe of the query results   
        """
        # Initialize a connection to Snowflake
        conn = self.connect()

        # Initialize a database cursor
        cursor = conn.cursor()

        # Execute the SQL query
        try:
            cursor.execute(command=sql)
        except snowflake.connector.errors.ProgrammingError:
            raise ValueError(f"Invalid SQL query. See error for more details.")

        # Reads the query results into a dataframe
        df = cursor.fetch_pandas_all()

        # Close the Snowflake connection
        conn.close()

        # Return the dataframe
        return df

    def write(self, df: pd.DataFrame, table: str):
        """
        Write the dataframe to Snowflake

        Arguments:
            df (pd.DataFrame): The dataframe to write to Snowflake
            table (str): The name of the table to write to
        """
        # Connect to Snowflake
        conn = self.connect()

        # Write to Snowflake
        try:
            write_pandas(
                conn=conn,
                df=df,
                table_name=table,
                database=self.database,
                schema=self.schema,
                chunk_size=16000,
            )
        except snowflake.connector.errors.ProgrammingError:
            raise ValueError(f"Invalid write operation. See error for more details.")
        
        # Close Snowflake Connection
        conn.close()
        