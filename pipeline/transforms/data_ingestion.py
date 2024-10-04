"""Data Ingestion"""

import csv

class DataIngestion:
    """
    A class for transforming string data into dictionaries that can be loaded into BigQuery tables.
    """

    def parse_line_method(self, string_input, columns):
        """
        Parses a line of data into a dictionary, mapping column names to values, 
        suitable for loading into BigQuery.

        Args:
            string_input (str): The input string representing a row of data.
            columns (list): A list of column names for the data.

        Returns:
            dict: A dictionary mapping column names to values, or None if the input is invalid.
        """
        # Return None for empty or invalid inputs
        if not string_input.strip():
            return None
        
        # Parse the input string and map values to columns
        values = csv.reader([string_input], skipinitialspace=True)
        return dict(zip(columns, next(values, [])))
