"""Dataflow pipeline to read GCS files and save data into BigQuery tables."""

import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, WriteToBigQuery
from helpers.constants import BUCKET, END_BUCKET, END_BLOB, PROJECT_ID, DESTINATION_DATASET, DRUGS_TABLE, PUBMED_TABLE, CLINICAL_TRIALS_TABLE, WRITE_TRUNCATE, WRITE_APPEND
from helpers.utils import get_header, upload_file, truncate_bigquery_table
from transforms.date_conversion import ConvertDateFormat
from transforms.data_ingestion import DataIngestion
from transforms.file_reader import ReadFileContent


def parse_json(line):
    """Parse a JSON string into a Python dictionary."""
    return json.loads(line) if line.strip() else None

def run(argv=None):
    # Define pipeline options
    pipeline_options = PipelineOptions(
        runner="DataflowRunner",
        project="eco-watch-430116-g6",
        region="us-east1",
        job_name="servier",
        temp_location=f"gs://{BUCKET}/tmp",
        staging_location=f"gs://{BUCKET}/staging",
        setup_file="./setup.py"
    )


    data_ingestion = DataIngestion()
    headers = {
        "drugs": get_header(f'gs://{BUCKET}/drugs.csv'),
        "pubmed": get_header(f'gs://{BUCKET}/pubmed.csv'),
        "clinical_trials": get_header(f'gs://{BUCKET}/clinical_trials.csv')
    }
    truncate_bigquery_table(PROJECT_ID, DESTINATION_DATASET, PUBMED_TABLE)
    # Create the pipeline
    with beam.Pipeline(options=pipeline_options) as pipeline:
        def create_csv_pipeline(file_name, header, table_name, write_mode):
            return (
                pipeline
                | f'Read {file_name} CSV' >> ReadFromText(f'gs://{BUCKET}/{file_name}.csv', skip_header_lines=1)
                | f'Parse {file_name}' >> beam.Map(lambda s: data_ingestion.parse_line_method(s, header))
                | f'Remove empty {file_name}' >> beam.Filter(lambda x: x is not None)
                | f'Convert {file_name} date format' >> beam.ParDo(ConvertDateFormat())
                | f'Write {file_name} to BigQuery' >> WriteToBigQuery(
                    table=f'{PROJECT_ID}:{DESTINATION_DATASET}.{table_name}',
                    write_disposition=write_mode
                )
            )

        # Process each CSV file for Drugs & Clinical Trials
        drugs_pipeline = create_csv_pipeline('drugs', headers['drugs'], DRUGS_TABLE, WRITE_TRUNCATE)
        clinical_trials_pipeline = create_csv_pipeline('clinical_trials', headers['clinical_trials'], CLINICAL_TRIALS_TABLE, WRITE_TRUNCATE)

        # Process PubMed CSV
        pubmed_csv_pipeline = create_csv_pipeline('pubmed', headers['pubmed'], PUBMED_TABLE,WRITE_APPEND)

        # Process PubMed JSON
        pubmed_json_pipeline = (
            pipeline
            | 'Read Pubmed JSON' >> beam.Create(["pubmed.json"])
            | 'Read each file content' >> beam.ParDo(ReadFileContent())
            | 'Decode Pubmed JSON' >> beam.Map(parse_json)
            | 'Convert Pubmed JSON date format' >> beam.ParDo(ConvertDateFormat())
            | 'Write pubmed JSON to BigQuery' >> WriteToBigQuery(
                f'{PROJECT_ID}:{DESTINATION_DATASET}.{PUBMED_TABLE}',
                write_disposition=WRITE_APPEND
            )
        )

        # Wait for the pipeline to finish
        result = pipeline.run()
        result.wait_until_finish()
        
        # Upload completion file
        upload_file(END_BUCKET, END_BLOB)

if __name__ == '__main__':
    run()
