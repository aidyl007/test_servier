"""
Transforms date formats to 'YYYY-MM-DD'.
"""
from datetime import datetime
import apache_beam as beam


def convert_date(date_string):
    """
    Converts a date string into the standard format 'YYYY-MM-DD'. 
    Supports multiple date formats: '%Y-%m-%d', '%d/%m/%Y', '%d %B %Y'.
    
    Args:
        date_string (str): The input date string to be converted.
        
    Returns:
        str: The date in 'YYYY-MM-DD' format, or None if the conversion fails.
    """
    if not date_string:
        return None
    
    # Try different date formats until one matches
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d %B %Y'):
        try:
            return datetime.strptime(date_string, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue  # Try the next format if conversion fails
    return None  # Return None if no format matches


class ConvertDateFormat(beam.DoFn):
    """
    A Beam DoFn class for converting date formats in elements of a PCollection.
    Converts the 'date' field in dictionaries or lists of dictionaries.
    """

    def process(self, element):
        """
        Process each element in the PCollection and convert the 'date' field to 'YYYY-MM-DD' format.
        
        Args:
            element (dict or list): An element that contains a 'date' field.

        Yields:
            dict: The element with the converted 'date' field.
        """
        # Check if the element is a dictionary or a list
        if isinstance(element, (dict, list)):
            # If it's a dict, convert the date in that dict
            if isinstance(element, dict):
                if element.get('date') is not None:
                    element['date']  = convert_date(element.get('date')) 
                yield element
            # If it's a list, iterate over the list and convert each date
            else:
                for elem in element:
                    if isinstance(elem, dict):  # Ensure it's a dict before converting
                        if elem.get('date') is not None:
                            elem['date']  = convert_date(elem.get('date')) 
                        yield elem
