
import logging
from google.cloud import storage
import apache_beam as beam
from helpers.constants import BUCKET

class ReadFileContent(beam.DoFn):
    """
    A custom Beam DoFn class for reading a file from Google Cloud Storage (GCS).
    """

    def setup(self):
        """Initializes the Google Cloud Storage client."""
        self.storage_client = storage.Client()

    def process(self, file_name):
        """
        Processes the input file name, retrieves the corresponding file from GCS, 
        and yields its content as a string.
        
        Args:
            file_name (str): The name of the file to read from GCS.
        
        Yields:
            str: The content of the file as a string.
        """
        # Get the specified bucket
        bucket = self.storage_client.bucket(BUCKET)
        
        # Retrieve the blob (file) from the bucket
        blob = bucket.blob(file_name)
        
        # Log the name of the blob for debugging purposes
        logging.warning(f"Reading file: {blob.name}")
        
        # Download the file content as a string and yield it
        yield blob.download_as_string()
