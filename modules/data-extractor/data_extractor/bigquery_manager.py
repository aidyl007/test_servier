from google.cloud import bigquery

PROJECT = "eco-watch-430116-g6"
DATASET = 'servier_test_dataset'
RESULT_TABLE = 'result'
EXTRACT_BUCKET = "servierdataextract"

class BigqueryManagerError(Exception):
    """Custom error for BigQuery operations."""

class BigqueryManager:
    """Encapsulates operations for BigQuery."""

    def __init__(self, bigquery_client):
        """Initialize BigQueryManager with a client."""
        self.client = bigquery_client

    def extract(self, sql):
        """Execute a query and export results to Google Cloud Storage.

        Args:
            sql (str): SQL query to execute.

        Returns:
            str: Job ID of the executed query.
        """
        job_config = bigquery.QueryJobConfig(
            destination=self.client.dataset(DATASET).table(RESULT_TABLE),
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        # Run the query
        query_job = self.client.query(sql, job_config=job_config, location='EU')
        query_job.result()  # Wait for the query to finish

        # Extract results to GCS
        destination_uri = f"gs://{EXTRACT_BUCKET}/output/result.json"
        table_ref = bigquery.TableReference.from_string(f"{PROJECT}.{DATASET}.{RESULT_TABLE}")
        extract_job = self.client.extract_table(
            table_ref,
            destination_uri,
            job_config=bigquery.job.ExtractJobConfig(destination_format=bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON),
            location="EU",
        )
        extract_job.result()  # Wait for extraction to complete

        return query_job.job_id  # Return the job ID
