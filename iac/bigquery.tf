

resource "google_bigquery_dataset" "servier" {
  provider      = google-beta
  project       = var.project
  dataset_id = "servier_test_dataset"
  description = "Dataset for Servier test"
  location = "EU"

  labels = {
    env = "default"
  }
}

# Define a local variable for common table schema
locals {
  drugs_schema = jsonencode([
    {
      name        = "atccode"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "ATC code"
    },
    {
      name        = "drug"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Drug"
    }
  ])

  pubmed_schema = jsonencode([
    {
      name        = "id"
      type        = "INTEGER"
      mode        = "NULLABLE"
      description = "ID"
    },
    {
      name        = "title"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Title"
    },
    {
      name        = "date"
      type        = "DATE"
      mode        = "NULLABLE"
      description = "Date"
    },
    {
      name        = "journal"
      type        = "STRING"
      mode        = "NULLABLE"
      description = "Journal"
    }
  ])

  clinical_trials_schema = jsonencode([
    {
      name        = "id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "ID"
    },
    {
      name        = "scientific_title"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Scientific title"
    },
    {
      name        = "date"
      type        = "DATE"
      mode        = "REQUIRED"
      description = "Date"
    },
    {
      name        = "journal"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Journal"
    }
  ])

  result_schema = jsonencode([
    {
      name        = "id"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "ID"
    },
    {
      name        = "drug"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Drug"
    },
    {
      name        = "date"
      type        = "DATE"
      mode        = "REQUIRED"
      description = "Date"
    },
    {
      name        = "journal"
      type        = "STRING"
      mode        = "REQUIRED"
      description = "Journal"
    }
  ])
}

# Create tables using the defined schema
resource "google_bigquery_table" "drugs" {
  provider    = google-beta
  project     = var.project
  dataset_id = google_bigquery_dataset.servier.dataset_id
  table_id   = "drugs"
  description = "Drugs table"
  schema = local.drugs_schema
}

resource "google_bigquery_table" "pubmed" {
  provider    = google-beta
  project     = var.project
  dataset_id = google_bigquery_dataset.servier.dataset_id
  table_id   = "pubmed"
  description = "PubMed table"
  schema = local.pubmed_schema
}

resource "google_bigquery_table" "clinicaltrials" {
  provider    = google-beta
  project     = var.project
  dataset_id = google_bigquery_dataset.servier.dataset_id
  table_id   = "clinicaltrials"
  description = "Clinical Trials table"
  schema = local.clinical_trials_schema
}

resource "google_bigquery_table" "result" {
  provider    = google-beta
  project     = var.project
  dataset_id = google_bigquery_dataset.servier.dataset_id
  table_id   = "result"
  description = "Result table"
  schema = local.result_schema
  deletion_protection = false
}
