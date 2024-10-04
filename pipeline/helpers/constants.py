import apache_beam as beam

# Test Project
PROJECT_ID = 'eco-watch-430116-g6'

# Servier test dataset
DESTINATION_DATASET = "servier_test_dataset"

# BigQuery Raw Layer tables
DRUGS_TABLE = "drugs"
PUBMED_TABLE = "pubmed"
CLINICAL_TRIALS_TABLE = "clinicaltrials"

# Storage buckets & blobs
BUCKET = "servierconfigs"
END_BUCKET = "servierdataextract"
END_BLOB = "servier_pipeline"

#WRITE DISPOSITION

WRITE_TRUNCATE=beam.io.BigQueryDisposition.WRITE_TRUNCATE
WRITE_APPEND=beam.io.BigQueryDisposition.WRITE_APPEND