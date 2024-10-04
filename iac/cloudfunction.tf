data "archive_file" "cfzip" {
  type        = "zip"
  output_path = "./modules/data_extractor.zip"
  source_dir  = "../modules/data-extractor"
}

resource "google_cloudfunctions2_function" "function" {
  name        = "data-extractor"
  location    = "europe-west1"
  description = "A new function"
  project     = var.project

  build_config {
    runtime     = "python38"
    entry_point = "main"
    environment_variables = {
      BUILD_CONFIG_TEST = "build_test"
    }
    source {
      storage_source {
        bucket = google_storage_bucket.servier_buckets["tfdeploy"].name
        object = google_storage_bucket_object.object.name
      }
    }
  }

  service_config {
    max_instance_count         = 3
    min_instance_count         = 1
    available_memory           = "256M"
    timeout_seconds            = 540
    environment_variables = {
      SERVICE_CONFIG_TEST = "config_test"
    }
    ingress_settings               = "ALLOW_INTERNAL_ONLY"
    all_traffic_on_latest_revision = true
    service_account_email          = google_service_account.service_account.email
  }

  event_trigger {
    trigger_region = "europe-west1"
    event_type     = "google.cloud.pubsub.topic.v1.messagePublished"
    pubsub_topic   = google_pubsub_topic.succeededjob.id
    retry_policy   = "RETRY_POLICY_RETRY"
  }
}

output "function_uri" {
  value = google_cloudfunctions2_function.function.service_config[0].uri
}
