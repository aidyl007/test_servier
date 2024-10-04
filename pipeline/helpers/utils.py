
import pandas as pd
from google.cloud import storage, bigquery


def get_header(file_path):
    """
    Extracts the header (column names) from a CSV file.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        list: A list of column names (header) from the CSV file.
    """
    # Read the CSV file and return the column names as a list
    return pd.read_csv(file_path).columns.tolist()


def upload_file(bucket_name, file_name):
    """
    Uploads a file with a predefined message to a specified bucket.
    
    Args:
        bucket_name (str): The name of the Google Cloud Storage bucket.
        file_name (str): The name of the file to create in the bucket.
    """
    # Initialize the Cloud Storage client
    storage_client = storage.Client()
    
    # Get the specified bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Create a new blob (file) in the bucket
    blob = bucket.blob(file_name)
    
    # Upload the string 'task completed' to the new file
    blob.upload_from_string('job completed')

def truncate_bigquery_table(project_id, dataset_id, table_id):
    # Initialize  BigQuery client
    client = bigquery.Client(project=project_id)

    # Build table name
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    #  SQL query to truncate a table
    query = f"TRUNCATE TABLE `{table_ref}`"

    # Execute query
    try:
        client.query(query).result()  # Wait query exec 
        print(f"Table {table_ref} has been truncated successfully.")
    except Exception as e:
        print(f"Failed to truncate table {table_ref}: {e}")
