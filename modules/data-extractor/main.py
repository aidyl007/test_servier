""" Data Extraction Module."""

import base64
import json
import logging
from data_extractor.extractor import extract

logger = logging.getLogger('data-extractor')

def main(event, context):
    """Triggered by a Cloud PubSub message.

    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    message = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    print(message["name"])
    if 'output/' not in message["name"]:
        extract(message["name"])
