"""function to extract data from BigQuery."""

import traceback
from google.cloud import bigquery, firestore
from data_extractor.firestore_manager import FirestoreManager
from data_extractor.bigquery_manager import BigqueryManager

COLLECTION = "config"

class ExtractError(Exception):
    """Custom error for extraction operations."""

def extract(document):
    """Extract data from BigQuery based on Firestore configuration."""
    try:
        # Initialize clients and managers
        bq_client = bigquery.Client()
        bq_manager = BigqueryManager(bq_client)
        fs_manager = FirestoreManager(firestore.Client())
        
        # Fetch configuration from Firestore
        config = fs_manager.get_config(COLLECTION, document)   

        # Execute the SQL extraction
        bq_manager.extract(config.get('sql'))
    except Exception as err:
        raise ExtractError(f'Internal error while extracting with config {document}: {err}\n{traceback.format_exc()}')
